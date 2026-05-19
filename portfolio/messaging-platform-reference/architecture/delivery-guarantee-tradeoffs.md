# Delivery Guarantees: At-Least-Once vs. Exactly-Once in Practice

At-least-once delivery means some messages arrive twice. Exactly-once delivery is theoretically possible and practically expensive. The decision between them is not a technical preference — it's a product commitment to every downstream team and customer who depends on the platform.

Getting this decision wrong doesn't look like a system failure. It looks like a support ticket from a user who received two payment confirmation texts, or a downstream team whose idempotency logic was never designed to handle duplicates because no one told them to build it.

---

## What At-Least-Once Means at Scale

At-least-once delivery is the default for most distributed messaging systems because it's simpler and faster to implement than the alternative. The tradeoff is duplicates: when a network partition or timeout occurs between send and acknowledgment, the system retries. The message may have already been delivered. At small volume, duplicates are rare and low-stakes. At scale, the math changes.

At a 0.05% duplicate rate — typical for a well-tuned platform — one billion messages produces 500,000 duplicates. For a marketing campaign announcing a product sale, those 500,000 duplicates are a UX annoyance and probably not a business failure. For financial transaction confirmations, they're a support escalation queue, a potential compliance review, and in some jurisdictions a regulatory flag. The message type determines whether "well-tuned" is good enough.

This is the first thing I establish when a team onboards: what does a duplicate mean to their use case? The answer determines which delivery guarantee they need, and whether the platform as configured can give it to them.

---

## The Actual Cost of Exactly-Once

Exactly-once delivery requires that each message is processed and delivered precisely one time, even across retries, failures, and restarts. Achieving this demands distributed coordination: idempotency keys paired with read-before-write checks, or distributed transactions across the message store and the delivery layer.

The cost is latency and throughput. Read-before-write on every message adds a storage round-trip — typically 20-100ms per message depending on storage backend and replication topology. That's acceptable for a low-volume transactional flow; it's punishing for a high-throughput notification pipeline. Distributed transactions impose coordination overhead that creates a throughput ceiling. At billions of messages per day, that ceiling is real and expensive to raise.

Engineering owns the implementation. I own the commitment. When I've evaluated exactly-once requirements, the conversation with engineering isn't "can we do this" — it's "what does this cost us in latency budget and throughput headroom, and is the use case worth that cost?" Those are product decisions with technical inputs, not the other way around.

---

## Business-Domain Decision Matrix

The delivery guarantee should follow the business domain, not the engineering team's preference.

**Financial and transactional messages** — 2FA codes, payment confirmations, account balance alerts — require exactly-once delivery or, at minimum, strong idempotency on the consumer side with a deduplication window of 60 seconds or less. A duplicate 2FA code creates user confusion and a potential security surface. A duplicate payment confirmation is a support escalation waiting to happen.

**Operational alerts** — account change notifications, security notices, subscription updates — can tolerate at-least-once delivery with a 24-hour deduplication window. Users understand that they might see two "your password was changed" emails during a system retry; they don't understand being charged twice.

**Marketing and promotional messages** — campaign sends, re-engagement flows, product announcements — are the clear at-least-once case. A duplicate promotional email is a UX annoyance, not a business failure. The cost of building exactly-once infrastructure for marketing sends is not justified by the impact of the failure mode it prevents.

---

## What SLA Language Actually Looks Like

"Best-effort delivery" is not an SLA. It tells downstream teams nothing they can plan around or escalate against.

"At-least-once delivery with a 24-hour deduplication window, targeting less than 0.1% duplicate rate under normal operating conditions" is an SLA. It tells a consumer what guarantee they're getting, what the failure envelope looks like, and what they should build their idempotency logic to handle.

My job is to translate the engineering implementation into language that business stakeholders and downstream engineering teams can act on. That means defining the deduplication window explicitly, stating the target duplicate rate as a measurable number, and being clear about what "normal operating conditions" excludes — planned maintenance windows, declared incidents, force majeure.

---

## The Honest Caveat

At high enough volume, even exactly-once systems develop edge cases. Distributed systems researchers have documented this extensively; anyone who has operated a large-scale messaging platform has experienced it. Coordinator failures, clock skew, and storage partition behavior can produce duplicates in systems designed to prevent them.

The right engineering default is to design consumers to be idempotent regardless of which delivery guarantee the platform commits to. The right product default is to document the guarantee clearly — including its failure conditions — and communicate any changes before they happen, not after. Consumers who know the failure envelope can build for it. Consumers who discover it in production cannot.
