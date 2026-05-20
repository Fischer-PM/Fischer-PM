# AWS Services: A PM Reference

This is not a developer guide. It's a reference for PMs who need to understand what a service does, when engineers reach for it, and what product constraints it introduces.

---

## Compute

**EC2 (Elastic Compute Cloud)**
EC2 gives you a virtual server in the cloud — you pick the size, the operating system, and how long it runs. Engineers reach for it when something needs to run continuously: an API server, a background worker, a long-running data job. The key product constraint is that EC2 costs scale with uptime, not with actual usage — a server sitting idle at 3 AM still costs money. If your team is running EC2 instances for workloads that only spike occasionally, you're likely paying for capacity you don't need.

**Lambda**
Lambda runs a piece of code in response to an event — an API call, a file upload, a scheduled trigger — without managing a server. Engineers use it for short, discrete tasks: sending a notification, transforming a file, validating a form submission. The product constraints to know: Lambda functions have a maximum execution time of 15 minutes, which means it's the wrong choice for long-running processes like report generation or large data exports. It also has "cold start" latency — if a function hasn't been invoked recently, the first request is slower, which matters for user-facing features where response time is part of the experience.

**ECS / EKS (Container Orchestration)**
ECS and EKS are the tools teams use to run containerized services at scale — think of them as the system that decides how many copies of a service to run, where to run them, and what to do when one crashes. This is the layer where conversations about microservices, deployment frequency, and service isolation live. The product implication: these tools give teams the ability to deploy individual services independently, which is what enables high deployment velocity. The common mistake is treating ECS and EKS as interchangeable — EKS (Kubernetes) is significantly more complex to operate and usually only warranted for organizations with mature platform engineering teams.

**Fargate**
Fargate runs containers without requiring the team to manage the underlying servers — it handles provisioning, scaling, and patching automatically. Engineers use it to reduce infrastructure overhead when running containerized workloads. The trade-off is cost: Fargate charges more per unit of compute than EC2 because AWS is absorbing the management burden. For variable or unpredictable workloads, the operational savings often justify the premium; for steady, predictable workloads, EC2 is usually cheaper.

---

## Storage

**S3 (Simple Storage Service)**
S3 is object storage — it holds files, images, videos, exports, backups, and static assets at effectively unlimited scale. It's one of the most widely used AWS services because it's cheap, durable, and requires almost no management. The constraint PMs should know: retrieval speed and cost vary significantly by storage class. Standard S3 is fast and accessed frequently; Glacier is designed for archival and can take minutes or hours to retrieve. If a product feature depends on fast retrieval of historical data, the storage class selection matters for the user experience, not just the bill.

**RDS (Relational Database Service)**
RDS is a managed relational database — think PostgreSQL or MySQL, but with AWS handling backups, patching, and failover. It's the right choice when your data has a defined structure and you need strong guarantees that a transaction either fully completes or doesn't happen at all. Scaling RDS vertically (bigger machine) is straightforward; scaling it horizontally (more machines handling reads) requires read replicas and is more complex. For regulated products, Multi-AZ deployment — where a standby copy exists in a second availability zone — is the standard approach to avoiding downtime.

**DynamoDB**
DynamoDB is a managed NoSQL database designed for extremely fast reads and writes at any scale. Engineers use it when they know exactly how data will be queried and need consistent low latency regardless of how large the dataset grows. The critical constraint: DynamoDB requires you to define your data access patterns upfront, when the table is designed. If the product evolves and queries need to work differently than originally anticipated, changing the structure is expensive and often means migrating data. It's a good choice for high-volume, well-understood use cases; it's a risky choice for early-stage products where the data model is still being discovered.

**ElastiCache**
ElastiCache is an in-memory data store — it holds frequently accessed data in RAM so it can be retrieved in microseconds instead of milliseconds. Teams use it to make slow database queries fast: session data, API responses, and computed values that are expensive to regenerate on every request. The product risk is consistency: cached data can be stale. If a user updates their profile and the response still shows old data because it was cached, that's an ElastiCache consistency problem. Features that require always-current data need either short cache TTLs or explicit cache invalidation — both of which add complexity.

---

## Messaging & Eventing

**SQS (Simple Queue Service)**
SQS is a message queue — it holds messages from one service until another service is ready to process them. It decouples producers (the thing generating work) from consumers (the thing doing the work), which means a spike in incoming requests doesn't overwhelm the processing layer. The constraint to know: SQS guarantees at-least-once delivery, which means the same message can occasionally be delivered more than once. Any system built on SQS must be designed to handle duplicate messages without causing problems — this is called idempotency, and it's a real design cost that affects timelines.

**SNS (Simple Notification Service)**
SNS sends a single message to many subscribers simultaneously — one event fans out to multiple destinations. Engineers use it to notify different parts of the system when something happens: a new order triggers an inventory update, a fulfillment notification, and a fraud check all at once. SNS is often paired with SQS: SNS handles the fan-out, and SQS provides durable queuing for each subscriber so no messages are lost if a service is temporarily unavailable.

**EventBridge**
EventBridge is an event bus that routes events between AWS services, between your own internal services, and between your system and external partners. The product advantage is that it includes a schema registry — a catalog of what events exist and what data they contain — which makes event contracts discoverable and reduces integration risk. It's the right choice when building event-driven integrations with third parties or when you want to decouple internal services without building custom routing logic.

**Kinesis Data Streams**
Kinesis Data Streams ingests high-throughput event data in real time — think clickstreams, transaction logs, or sensor data arriving at millions of events per second. Events are ordered within a shard (a unit of capacity), which matters for use cases where sequence is important. The default data retention is 24 hours; extended retention is available up to 7 days or 365 days, but costs more. For product analytics pipelines and real-time fraud detection, the retention window is a design decision with both a product implication (how far back can you replay?) and a cost implication.

**Kinesis Firehose**
Kinesis Firehose takes streaming data and delivers it to a destination — S3, Redshift, or OpenSearch — without requiring you to write consumer code. It handles batching, compression, and delivery automatically. The constraint: Firehose introduces a delivery delay of 60 to 900 seconds, which means it's not appropriate for anything that needs true real-time processing. For analytics pipelines where near-real-time is sufficient, it's a low-effort and cost-effective choice.

---

## API & Networking

**API Gateway**
API Gateway is a managed layer that sits in front of your backend services and handles rate limiting, authentication, request validation, and logging. It lets teams expose APIs to external developers or internal consumers without exposing backend infrastructure directly. The product constraint: API Gateway adds latency to every request, and throttling limits are set at the account level by default, not per API or per customer. At scale, hitting those default limits causes unexpected failures that are difficult to diagnose without understanding the underlying service configuration.

**CloudFront**
CloudFront is AWS's content delivery network — it caches content at edge locations around the world so users get responses from a server close to them rather than one in a single region. For global products, this meaningfully improves load times. The constraint: cache invalidation is not instant. After a deploy, updated content can take time to propagate across all edge locations, which means users in different regions may see different versions of the product temporarily. For time-sensitive content changes, this is a coordination problem that PMs should be aware of.

**Route 53**
Route 53 is AWS's DNS service — it translates domain names into the IP addresses of your servers and controls where traffic goes. For product decisions, the most relevant capability is failover routing: Route 53 can detect when a region is unhealthy and automatically redirect traffic to a backup region. The constraint: DNS changes take time to propagate because of TTL (time to live) settings, which control how long DNS resolvers cache the old answer. Low TTLs enable faster failover but increase DNS query volume and cost; high TTLs are cheaper but slow down recovery.

**VPC (Virtual Private Cloud)**
A VPC is a private, isolated network within AWS that controls which services can communicate with each other and what can reach the public internet. Most production environments run inside a VPC to limit exposure. The product relevance: VPC misconfigurations are one of the most common causes of connectivity failures between internal services, and they're often invisible until something breaks in production. When an engineering team says a service "can't reach" another service, VPC security group rules are frequently the root cause.

---

## Observability & Operations

**CloudWatch**
CloudWatch is AWS's default monitoring and logging service — it's where metrics are recorded, logs are stored, and alarms are triggered when thresholds are crossed. When something breaks in a production AWS environment, CloudWatch is usually the first place engineers look. The cost constraint: storing logs in CloudWatch isn't free, and log retention beyond the default period adds up at high volume. PMs working on cost optimization should know that log retention policies are a meaningful lever.

**X-Ray**
X-Ray is a distributed tracing service that shows how a single request travels through multiple services — from the API layer through each microservice to the database and back. It's the tool engineers use to answer "why is this request slow?" in a microservice architecture, where latency can be introduced at any one of many service boundaries. Without X-Ray or equivalent tracing, diagnosing latency regressions in complex systems is largely guesswork.

**CloudTrail**
CloudTrail records every action taken against AWS resources — who made an API call, when, from where, and what changed. It's the audit log for the infrastructure layer. For products in regulated industries — financial services, healthcare, legal — CloudTrail is typically required for compliance, not optional. PMs should know it exists and that it's the authoritative record when a compliance team asks "who made that change and when."

---

## Auth & Identity

**Cognito**
Cognito is AWS's managed identity service — it handles user sign-up, sign-in, password management, and token issuance. It supports OAuth, SAML, and social login providers like Google and Apple, which makes it a reasonable default for products that don't want to build authentication from scratch. The product caveat: Cognito has documented quirks around user migration (moving users from another identity provider is non-trivial) and token refresh behavior (expired tokens can cause silent failures that look like session bugs). Plan for these before choosing Cognito for a product with a large existing user base.

**IAM (Identity and Access Management)**
IAM controls what each person, application, and AWS service is allowed to do — it's the permission system for the entire AWS environment. When a Lambda function needs to read from S3, an IAM role grants that permission. When an engineer needs to deploy to production, an IAM policy defines what they're allowed to touch. The product relevance: overly permissive IAM roles are a leading cause of security incidents in cloud environments. In regulated products, IAM configuration is often a direct audit concern, and understanding the principle of least privilege is essential for having credible conversations with security and compliance teams.

---

## Workflow & Orchestration

**Step Functions**
Step Functions orchestrates multi-step workflows — sequences of tasks with conditional branching, retry logic, and error handling built in. Engineers use it to replace fragile cron jobs, ad hoc scripts, and manual hand-offs between systems. The product advantage is visibility: the state of any workflow execution is recorded and auditable, which means when a process fails partway through, you can see exactly where it stopped and why. For operations-heavy products where process reliability is a product quality concern, Step Functions is a meaningful improvement over custom orchestration code.

**SageMaker**
SageMaker is AWS's managed platform for training and deploying machine learning models. It handles the infrastructure work — provisioning compute, managing experiments, serving models at scale — so data scientists can focus on the models themselves. For PMs, the relevant distinction is between model training (compute-intensive, runs periodically, expensive) and model serving (runs continuously, cost depends on traffic volume and latency requirements). These have different cost profiles and different operational considerations, and conflating them is a common source of AI feature timeline misestimates.

---

## A Note on AWS and Risk

The most important thing a PM can know about AWS is not what each service does but what it costs when something goes wrong. Understand the failure mode, the recovery time, and the cost of the wrong choice before a service is selected — not after it's in production.
