# Kafka Architecture Review
**Product: Apache Kafka / Confluent**
**Architectural focus: Append-only log with consumer-managed offsets**

## The Core Architectural Bet

The message broker does not track what each consumer has processed. Consumers track their own position (offset) in the log. The log retains messages for a configurable period, regardless of whether they've been consumed. This inverts the traditional queue model — where the broker owns delivery state — and gives consumers full control over their position in the stream. The bet is that durability, replay, and consumer independence are more valuable than guaranteed-once delivery managed by the broker. This is an architectural statement about who should own reliability: Kafka says the consumer owns it.

## What This Makes Possible

**Replay.** Consumers can re-read historical messages — useful for backfills when a new downstream system is introduced, debugging production issues by replaying real event traffic, and recovering from processing errors without data loss. In a traditional queue, once a message is consumed and acknowledged, it's gone. In Kafka, it's in the log until the retention window expires.

**Consumer independence.** Multiple consumers can read the same stream at their own pace without affecting each other. A real-time fraud detection system and a daily analytics batch job can both consume the same payment events stream — the fraud system processes in milliseconds, the batch job runs at 2 AM, and neither knows the other exists. This decoupling enables independent team development at scale.

**High throughput.** The append-only write model is extremely fast. Kafka is designed for millions of events per second across horizontally scaled partitions. The architecture achieves this throughput because it does not need to maintain per-consumer delivery state — the broker is stateless with respect to consumers.

**Decoupling producers from consumers.** Producers don't need to know who is consuming their events. A payments team can publish a payment-completed event without knowing whether fraud detection, analytics, notifications, and ledger systems are all consuming it. Adding a new consumer doesn't require a producer change. This is the core architectural enabler for microservices at scale.

## What This Makes Hard

**Exactly-once delivery.** The consumer-managed offset model means a consumer that crashes before committing its offset will re-read and re-process messages on restart. Designing for idempotency is required, not optional. Kafka introduced exactly-once semantics in later versions, but implementing them correctly requires careful configuration that most teams don't get right on first attempt.

**Schema evolution.** There is no native schema enforcement in Kafka. Producers can change their event structure at any time, and consumers must handle messages in formats they didn't expect. Schema registries (like Confluent's) address this, but they are an add-on, not a core property. Teams that skip schema governance ship systems that fail silently when a producer adds or renames a field.

**Operational complexity.** Kafka requires significant infrastructure — historically ZooKeeper for cluster coordination, now KRaft — plus partition management, replication configuration, and consumer group management. Managed services like Confluent address the operational overhead but add meaningful cost. A team that picks Kafka for its technical properties and underestimates the operational requirements will spend the first six months managing the platform rather than building product.

**Debugging.** The distributed nature of Kafka makes tracing a specific message through a pipeline non-trivial. When a downstream system has incorrect data, determining whether the error is in the event payload, the consumer logic, or the offset commit sequence requires observability tooling that doesn't come with Kafka out of the box. Consumer lag monitoring, dead letter queue management, and distributed tracing all need to be added separately.

## Failure Modes

**Consumer lag accumulation.** If a consumer processes events slower than they arrive, lag grows. At scale, a consumer that falls several hours behind can take days to catch up — because catching up requires processing historical events while also keeping up with new ones. During this period, downstream systems are operating on stale data. The architecture has no built-in backpressure mechanism to prevent this.

**Partition imbalance.** Kafka distributes load across partitions, but if the partition key is poorly chosen, one partition receives disproportionate volume — a hotspot. That partition's consumer becomes the bottleneck. The problem is non-obvious to debug because aggregate throughput looks healthy while one consumer is overwhelmed. Fixing it typically requires repartitioning, which is a disruptive operation.

**Retention cliff.** When a consumer falls so far behind that messages it needs have exceeded the retention window, those events are gone. There is no built-in recovery. The system is in a state where the consumer has missed data it can never retrieve, and the downstream implications — missed transactions, incomplete analytics, unprocessed events — depend entirely on what the consumer was doing. This failure mode is silent until its consequences surface elsewhere.

## PM Implications

Kafka is the right architecture when you need replay, high throughput, and consumer independence. It is not the right architecture when you need guaranteed once-and-only-once processing without careful engineering investment, when operational overhead is a constraint, or when producers and consumers need to negotiate schemas. The PM building on Kafka needs to own the answer to a specific question: what happens when a consumer is down for 24 hours? If the answer isn't "it catches up and nothing is lost," the system isn't designed correctly for Kafka yet.

The second implication is about organizational fit. Kafka rewards teams that invest in platform engineering — observability, schema governance, consumer group management. Teams that want Kafka's throughput benefits without the platform investment will get neither. The architecture's properties are real, but they require a level of operational maturity that many product teams underestimate when they pick Kafka because it's the industry standard. Confluent's managed offering reduces the operational overhead significantly, but it shifts the cost from engineering time to dollar spend, which is a product and financial planning question, not just a technical one.
