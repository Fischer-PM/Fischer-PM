# Architecture Concepts: A PM Reference

These are the terms that come up in engineering conversations that PMs need to understand well enough to make good product decisions — not to write code, but to ask the right questions and spot the wrong assumptions.

---

## Delivery & Reliability

**At-least-once delivery**
A messaging guarantee that ensures every message will be delivered, but doesn't prevent it from being delivered more than once. This is the standard guarantee for most queuing systems, including SQS. The product implication: any system that receives messages must be built to handle duplicates safely — processing the same message twice should produce the same result as processing it once. The common misunderstanding is assuming "reliable" means "exactly once." It doesn't. At-least-once is reliable; it's just not duplicate-free.

**Exactly-once delivery**
A guarantee that each message is delivered and processed precisely one time — no more, no less. This is significantly harder to achieve than at-least-once delivery and usually requires coordination overhead that impacts throughput and latency. The product implication: exactly-once semantics are sometimes necessary (payment processing, inventory decrements) but often over-specified. When a team says they need exactly-once delivery, the right follow-up question is whether idempotency on the consumer side could solve the problem more simply and cheaply.

**Idempotency**
An operation is idempotent if running it multiple times produces the same result as running it once. Submitting a payment that's already been submitted should not charge the customer twice; deleting a record that's already deleted should not throw an error. This is the design principle that makes at-least-once delivery safe. The common misunderstanding is treating idempotency as an optional nice-to-have — in distributed systems it's a correctness requirement, and retrofitting it after a system is in production is expensive.

**Dead letter queue (DLQ)**
A secondary queue that receives messages that couldn't be processed successfully after a defined number of retry attempts. It's a safety valve: instead of losing failed messages or blocking the main queue, they're parked somewhere for investigation and reprocessing. The product implication is operational: a DLQ growing in size is a signal that something in the processing pipeline is broken, and it needs a team that monitors it. PMs often miss that a DLQ is not self-healing — messages sitting there require human intervention or an automated remediation process.

**Retry with exponential backoff**
A strategy where a failed operation is retried, but each retry waits progressively longer before trying again — first 1 second, then 2, then 4, then 8. This prevents a struggling downstream service from being overwhelmed by a flood of retries all arriving at once. The product implication: retry behavior is a product decision dressed as an engineering detail. How long should the system keep trying? What should the user see during retries? Is there a maximum wait time before the operation is considered permanently failed? These questions need PM input, not just engineering judgment.

**Circuit breaker**
A pattern where a service stops sending requests to a failing dependency and instead returns a fallback response immediately, rather than letting every request time out. When the dependency recovers, the circuit breaker gradually allows traffic through again. The product implication: circuit breakers require a decision about what the fallback behavior should be — what does the user see or experience when a dependency is down? That's a product decision. The common misunderstanding is treating the circuit breaker as purely an engineering concern when the fallback experience is a UX question.

**Graceful degradation**
The ability of a system to continue functioning at reduced capability when a component fails, rather than failing entirely. If a recommendation engine goes down, the product shows generic content instead of nothing. If a payment processor is slow, the checkout flow queues the transaction instead of timing out. The common misunderstanding is confusing graceful degradation with acceptable downtime — they're not the same. Degradation means the core flow still works; downtime means it doesn't. Defining what "degraded but functional" looks like is a product responsibility, not an engineering one.

**Failover**
The process of switching from a failed or unhealthy system component to a backup component — automatically or manually. Active failover moves traffic from a broken database to a replica; regional failover routes requests to a different AWS region when one goes down. The product implication: failover takes time, even when automated, and during that window some requests may fail or be delayed. PMs need to understand the failover time objective (how long it takes) as distinct from the recovery time objective (how long before everything is back to normal) — they are often quoted together but represent different phases of an outage.

**Multi-region active-active vs. active-passive**
Two approaches to running a system across multiple geographic regions. In active-active, both regions serve live traffic simultaneously — if one fails, the other absorbs the load with no interruption. In active-passive, one region handles all traffic and the other is a warm standby that takes over only when the primary fails. Active-active is more resilient and better for global latency but dramatically more complex to build and operate — data must stay consistent across regions in real time. Active-passive is simpler but has a failover window. The common misuse: teams claim active-active resilience when they're actually running active-passive, because "active-active" sounds better in a reliability narrative.

---

## Consistency & State

**ACID (Atomicity, Consistency, Isolation, Durability)**
ACID is the set of guarantees that relational databases provide to ensure that transactions are reliable. Atomicity means a transaction either fully completes or fully rolls back — no partial writes. Consistency means the database is always in a valid state. Isolation means concurrent transactions don't interfere with each other. Durability means once a transaction commits, it survives crashes. The product implication: ACID guarantees are what make financial transactions, order management, and inventory tracking trustworthy. The common misunderstanding is assuming all databases provide ACID guarantees — most NoSQL databases sacrifice some of these properties in exchange for scale and speed.

**Eventual consistency**
A model where a system guarantees that all copies of data will eventually agree, but doesn't guarantee they're in sync at any given moment. If you update a record and immediately read it from a different server, you might see the old value for a brief window. The product implication is real: features that read immediately after a write — profile updates, balance displays, status changes — need to account for eventual consistency or users will see stale data. The common misunderstanding is treating eventual consistency as a bug. It's a deliberate trade-off that enables scale; the product team needs to design around it, not just report it as broken.

**Strong consistency**
A guarantee that after a write completes, any subsequent read will return the updated value — everywhere, immediately. Strong consistency is easier to reason about and build products on, but it comes at a cost: it requires coordination between distributed nodes, which adds latency and limits throughput. The product implication: not every feature needs strong consistency. Designing for it everywhere when eventual consistency is acceptable wastes engineering effort and constrains scale unnecessarily. The question to ask is: what's the actual consequence if a user sees a slightly stale value for 500 milliseconds?

**CAP theorem**
The CAP theorem states that a distributed system can only guarantee two of three properties simultaneously: Consistency (every read returns the latest write), Availability (every request gets a response), and Partition tolerance (the system keeps working when network connections between nodes fail). Because network partitions happen in real distributed systems — they're not optional — every system is really choosing between consistency and availability when a partition occurs. The common PM misuse: citing CAP as though it's a design philosophy or a binary choice made once. In practice, most systems make different consistency-availability trade-offs for different operations, and CAP doesn't tell you which trade-off to make — it just tells you that you must make one.

**Optimistic vs. pessimistic locking**
Two strategies for preventing two users or processes from corrupting the same data simultaneously. Pessimistic locking prevents anyone else from reading or modifying a record while one process has it — safe, but creates contention. Optimistic locking allows concurrent access but detects conflicts at write time and rejects the second writer if the data changed while they were working. The product implication: optimistic locking is appropriate when conflicts are rare; pessimistic locking is appropriate when they're common. For features like "edit this shared document" or "claim this inventory item," the locking strategy is a direct product experience decision, not a backend detail.

---

## Scale & Performance

**Horizontal vs. vertical scaling**
Vertical scaling means making a single server bigger — more CPU, more RAM. Horizontal scaling means adding more servers and distributing the load. Vertical scaling is simpler but has a ceiling; you can only make a machine so large, and scaling down requires manual intervention. Horizontal scaling can grow (and shrink) without limit but requires the application to be designed to run as multiple instances simultaneously, which is not always the case. The common misunderstanding: assuming horizontal scaling is always better. For stateful applications or databases, horizontal scaling is significantly harder and sometimes not possible without architectural changes.

**Sharding / partitioning**
Sharding splits a large dataset across multiple databases or storage nodes, each responsible for a subset of the data. Instead of one database holding all user records, three shards might hold one-third each, determined by user ID range or a hash function. This allows the system to scale reads and writes beyond what a single machine can handle. The product constraint: once a sharding strategy is chosen, changing it is extremely difficult and expensive. The common mistake is sharding prematurely — before the data volume justifies it — adding operational complexity with no benefit.

**Caching (and cache invalidation)**
Caching stores the result of an expensive operation — a database query, an API call, a computation — so subsequent requests can retrieve it cheaply from memory instead of recalculating it. It's one of the most effective ways to reduce latency and database load. The hard part is cache invalidation: deciding when a cached value is stale enough to discard and recompute. The product implication is that "show me the latest data" and "respond in under 100ms" are sometimes in direct tension, and the resolution requires a product decision about acceptable staleness — not just an engineering one. The common misuse is treating caching as a performance fix that can be applied anywhere without cost; incorrect cache invalidation is one of the most persistent sources of subtle data bugs.

**Rate limiting vs. throttling**
These terms are often used interchangeably but describe different mechanisms. Rate limiting caps how many requests a client can make in a time window — exceed the limit and requests are rejected outright. Throttling slows down request processing when the system is under load — requests are queued or delayed rather than immediately rejected. The product implication: rate limiting is about protecting the system from abuse or overuse; throttling is about managing load gracefully. A good API has both. The common mistake is treating the rate limit as a product feature ("our API allows 1,000 requests per minute") without thinking through the actual user experience when that limit is hit — what does the client do? Retry? Fail? Queue?

**Backpressure**
Backpressure is a mechanism where a downstream system signals to an upstream system that it's overwhelmed and needs to slow down. Instead of buffering an unlimited number of incoming requests until it crashes, a system applies backpressure to prevent being flooded. The product implication: backpressure is what separates a system that degrades gracefully under load from one that falls over. When engineering describes a system as "backpressure-aware," it means the system has built-in load shedding — which is a reliability feature worth calling out in product specifications.

**Cold start**
A cold start is the additional latency incurred when a computing resource — a Lambda function, a containerized service, a database connection pool — needs to be initialized from scratch because it hasn't been used recently. For Lambda, this can add hundreds of milliseconds or more to the first request after a period of inactivity. The product implication: cold starts matter most for user-facing, latency-sensitive endpoints that have irregular traffic patterns. The common misunderstanding is dismissing cold start as a minor infrastructure concern — for a login flow or a checkout endpoint that receives burst traffic after idle periods, it's a direct user experience problem.

**p50 / p95 / p99 latency (and why averages lie)**
Latency percentiles describe how fast a system responds for different segments of requests. p50 is the median — half of requests are faster, half are slower. p95 means 95% of requests complete within that time. p99 means 99% complete within that time. The remaining 1% — the tail — is where the slowest requests live. The product implication: average latency hides tail behavior. A system with an average response time of 200ms might have a p99 of 4 seconds — meaning 1 in 100 users waits 20 times longer than the median. For products with high transaction volume, 1% of requests is a large number of real people. The common mistake is reporting and monitoring average latency as a proxy for user experience; it's not.

---

## Architecture Patterns

**Monolith vs. microservices**
A monolith is a single deployable unit — one codebase, one deployment, all features in one place. Microservices breaks a system into many small, independently deployable services that communicate over a network. Monoliths are simpler to build, test, and operate — they're usually the right choice for early-stage products where iteration speed matters more than scale. Microservices enable independent deployment, team autonomy, and targeted scaling, but introduce network complexity, distributed system problems, and significant operational overhead. The common mistake is migrating to microservices as a default maturity milestone rather than as a response to a specific problem that microservices actually solve.

**Event-driven architecture**
An architecture where services communicate by producing and consuming events — things that happened — rather than by calling each other directly. A service publishes an "order placed" event; inventory, fulfillment, and fraud services each respond to it independently. This decouples services so that each can evolve without needing the others to change simultaneously. The product implication: event-driven systems are harder to test end-to-end and harder to debug when something goes wrong, because cause and effect are separated in time and space. The common misunderstanding is equating "event-driven" with "resilient" — an event-driven system with no error handling or dead letter queues can silently lose events.

**Event sourcing**
An approach where the state of a system is not stored directly, but derived by replaying a log of all events that have ever occurred. Instead of storing "current balance: $500," you store every transaction that led to that balance. State is computed by replaying the event log. The product advantage is a complete, immutable audit trail — you can reconstruct the state at any point in time. The common misunderstanding is that event sourcing and event-driven architecture are the same thing — they're not. Event sourcing is a persistence strategy; event-driven architecture is a communication pattern. They're often used together but serve different purposes.

**CQRS (Command Query Responsibility Segregation)**
CQRS separates the parts of a system that write data (commands) from the parts that read data (queries), allowing each to be optimized independently. The write side might use a normalized relational database for correctness; the read side might use a denormalized cache or search index for speed. The product implication: CQRS can dramatically improve read performance for complex queries, but it introduces the possibility of read-write lag — a write might not be immediately visible in the read model. The common misuse is applying CQRS to systems that don't have meaningfully different read and write requirements, adding complexity with no benefit.

**Pub/sub**
Pub/sub (publish/subscribe) is a messaging pattern where a publisher sends messages to a topic without knowing who will receive them, and subscribers receive only the messages for topics they've opted into. This decouples publishers from subscribers — either can be added, removed, or changed without affecting the other. The product implication: pub/sub is what enables fan-out — one event triggering many independent reactions simultaneously. The constraint: pub/sub typically doesn't guarantee ordering or exactly-once delivery, which must be handled by subscribers if those properties matter.

**Request-response vs. async messaging**
Request-response is synchronous: a caller sends a request and waits for an answer before proceeding. Async messaging is asynchronous: the caller sends a message and continues without waiting, receiving the result later (if at all). Request-response is simpler to reason about and the right model for user-facing interactions that need an immediate answer. Async messaging is better for work that takes a long time, work that can be deferred, or work that should be retried on failure. The common mistake is defaulting to request-response because it's familiar, then building polling or timeout hacks when the underlying operation takes longer than expected — a sign that async was the right model from the start.

**Saga pattern**
A saga is a pattern for managing a multi-step business transaction across multiple services without using a distributed transaction — something that's technically complex and often impractical at scale. Instead, each step publishes an event on success, and if a later step fails, compensating events are triggered to undo the earlier steps. The product implication: sagas make it possible to implement complex workflows (order processing, provisioning, multi-party approvals) across service boundaries. The constraint: compensating transactions must be explicitly designed. The common misunderstanding is treating saga failure handling as an engineering edge case — what happens when a step fails midway is a product question about the user experience and data state.

**API gateway pattern**
The API gateway pattern places a single entry point in front of all backend services. Clients call one gateway; the gateway routes to the appropriate service, handles auth, rate limiting, and logging, and aggregates responses when needed. The product benefit is a consistent surface area for external developers and a single place to enforce cross-cutting concerns. The risk: the API gateway becomes a bottleneck or a single point of failure if not designed carefully. The common mistake is treating the API gateway as only an infrastructure concern — the routing rules, rate limits, and authentication mechanisms it enforces are directly product decisions about who can do what and how.

**Sidecar pattern**
A sidecar is a secondary process that runs alongside a main service in the same deployment unit, handling cross-cutting concerns like logging, metrics, service discovery, or security — without modifying the main service's code. It's a way to add capabilities to any service without changing that service. The product implication: when a platform team offers a "sidecar" for observability or security, product teams can adopt it without code changes, which lowers the cost of adoption. The common misunderstanding is treating sidecars as a magic performance-free abstraction — they consume resources, and in containerized environments they add operational complexity that the platform team must own and maintain.

---

## Data

**Schema evolution**
Schema evolution is the process of changing the structure of stored data — adding a column, renaming a field, removing an attribute — without breaking existing systems that depend on the old structure. In fast-moving products, schemas change frequently. The product constraint: schema changes in production systems require coordination across every system that reads or writes that data, and some changes (renaming a field, changing a data type) are backward-incompatible, meaning they can break systems that aren't updated simultaneously. PMs need to understand that "can we just add a field?" is rarely as simple as it sounds when the data is shared across services or exposed via an API.

**Data normalization vs. denormalization**
Normalization organizes data to eliminate redundancy — each piece of information is stored once and referenced everywhere else. Denormalization intentionally duplicates data to make queries faster, accepting redundancy in exchange for read performance. Normalization is appropriate for transactional systems where data changes frequently and correctness matters most. Denormalization is appropriate for analytical and read-heavy systems where query speed matters more than storage efficiency. The common misunderstanding is treating normalization as universally correct and denormalization as a hack — in the right context, denormalization is the right choice, not a compromise.

**OLTP vs. OLAP**
OLTP (Online Transaction Processing) describes systems designed for high-volume, low-latency reads and writes of individual records — the operational database that runs the product. OLAP (Online Analytical Processing) describes systems designed for complex queries across large datasets — the data warehouse that answers business intelligence questions. The critical product implication: running analytical queries directly against an OLTP database is a common source of production incidents. Analytics workloads compete with operational workloads for the same resources, which is why they belong in separate systems. PMs who route ad hoc reporting queries to the production database are creating a reliability risk they may not recognize as such.

**Data pipeline**
A data pipeline is a system that moves data from one place to another, transforming it along the way — extracting from a source, applying business logic, and loading it into a destination. Pipelines are how operational data gets into analytics systems, how events from multiple services get joined into a unified view, and how machine learning models get training data. The product implication: data pipelines are infrastructure, and like all infrastructure they need ownership, monitoring, and maintenance. A broken pipeline means stale or missing data in dashboards, models, and reports — which affects product decisions. The common misunderstanding is treating a data pipeline as a one-time setup rather than an ongoing operational concern.

**Batch vs. streaming**
Batch processing collects data over a period of time and processes it all at once — nightly ETL jobs, weekly reports, monthly billing runs. Streaming processes data as it arrives, continuously, with latency measured in seconds or milliseconds rather than hours. The product implication: batch is simpler, cheaper, and sufficient for most analytics use cases. Streaming is necessary when the product requires near-real-time data — fraud detection, live dashboards, personalization that reacts to what a user just did. The common mistake is building streaming infrastructure when batch would meet the actual product requirement, adding operational complexity and cost for latency requirements no one actually specified.

---

## Observability

**Structured logging**
Structured logging means writing log entries as machine-parseable data — typically JSON with defined fields — rather than free-form text strings. Instead of logging "User 12345 failed login at 14:03," a structured log writes a JSON object with fields for user_id, event_type, timestamp, and result. The product implication: structured logs can be queried, aggregated, and alerted on programmatically, which makes observability tooling dramatically more effective. The common misunderstanding is treating structured logging as a developer preference — it's an operational requirement for any system where you need to search or analyze logs at scale.

**Metrics vs. logs vs. traces**
Metrics are numeric measurements aggregated over time — request count, error rate, CPU usage. They're efficient to store and query, and they're what dashboards and alerts are built on. Logs are discrete records of events — individual requests, errors, and state changes. They're useful for investigation but expensive to store at high volume. Traces are records of how a single request flows through multiple services — they connect the dots between metrics ("latency is high") and logs ("here's what happened in each service for this specific request"). The product implication: a team without all three is operating blind in different ways. Metrics tell you something is wrong; logs and traces tell you why.

**SLI / SLO / SLA**
An SLI (Service Level Indicator) is a specific measurement of system behavior — request success rate, API response time, data processing latency. An SLO (Service Level Objective) is the internal target for that measurement — "99.9% of requests complete in under 200ms." An SLA (Service Level Agreement) is the contractual commitment made to customers, typically with financial consequences if violated. The critical distinction: SLOs are internal engineering targets; SLAs are external commitments with consequences. An SLA should always be achievable with meaningful headroom — if the SLO is 99.9%, the SLA might commit to 99.5%. PMs are often involved in setting SLAs without understanding that the SLA must be grounded in actual SLO performance, not aspiration.

**Error budget**
An error budget is the amount of unreliability a service is allowed to have while still meeting its SLO. If a service has a 99.9% availability SLO, the error budget is 0.1% of total time — roughly 43 minutes per month. When the error budget is consumed, new feature work pauses and reliability work takes priority. The product implication: the error budget is a mechanism for balancing reliability and velocity as a shared responsibility between engineering and product. The common misuse is treating the error budget as an engineering metric that PMs don't need to understand — it's actually a direct constraint on the product roadmap.

**Distributed tracing**
Distributed tracing tracks a single request as it travels through multiple services, capturing timing and metadata at each step. Each service adds a record to the trace, creating a complete picture of where time was spent and where errors occurred. The product implication: in a microservice architecture, a slow user experience can be caused by any one of many services, and without tracing, identifying which service is responsible requires guesswork. Distributed tracing is what makes "the checkout flow is slow" actionable instead of just observable. The common misunderstanding is treating distributed tracing as an optional observability enhancement — in microservice architectures it's a baseline operational requirement.

---

## A Note on Why PMs Need to Understand Architecture

Understanding architecture is not about designing systems. It's about understanding what your product decisions actually commit the engineering team to. Every feature request carries an architectural cost — sometimes in complexity, sometimes in reliability risk, sometimes in future flexibility. A PM who doesn't understand those costs will underestimate timelines, overpromise reliability, and create technical debt they can't see. The questions in this glossary are not engineering questions. They're the questions that determine whether a product is actually possible to build, maintain, and trust — and that makes them product questions too.
