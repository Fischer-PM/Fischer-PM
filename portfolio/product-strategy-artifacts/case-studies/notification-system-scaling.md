**Note: This is a simulated case study. The company, product, and events are fictional.**

# Notification System Scaling: The Triage That Made Things Worse

**Company: Arcline** (fintech payments platform)

---

## Situation

Arcline's notification system was built for 10,000 daily active users. By month 18, the platform had 500,000. Notification delivery rate dropped from 99.2% to 94.1% over six months. No one noticed until a batch of transaction alerts failed during a market volatility event — and customers found out about their transactions from their bank instead of from Arcline.

The drop hadn't happened overnight. It was slow and unmonitored — 99.2% down to 97.8% down to 94.1%, quarter by quarter, with no alert threshold set on delivery rate. By the time it surfaced, the number of daily missed notifications was over 25,000. The market event just made the failure visible.

Support volume tripled in 48 hours. The business wanted a fix immediately.

---

## Constraint

The notification service was a shared dependency for four product teams: payments, fraud, account management, and marketing. Any architectural change — queue redesign, service split, infrastructure scaling — required cross-team coordination, design alignment, and a migration that touched every caller.

Engineering gave me an honest estimate: full rebuild was 14 weeks. The business wanted a production fix in three. A market event had just exposed the problem publicly, and three weeks was not a negotiating position — it was a constraint.

I had three weeks to meaningfully improve notification reliability without touching the architecture.

---

## Decision

The approach was to buy headroom without rebuilding. If the queue was overwhelmed, the answer was to make it do less — specifically, to stop treating all notifications as equal priority.

I proposed throttling non-critical notifications: marketing messages, weekly account summaries, promotional alerts. These would enter a secondary queue with a lower throughput ceiling, freeing capacity in the primary queue for transactional alerts — payment confirmations, fraud flags, account access notifications. A rough classification already existed in the message schema. We'd enforce it at the queue level.

What I was sacrificing: the marketing team's ability to deliver time-sensitive campaigns reliably. That was a known trade. I flagged it to marketing leadership before the change went live. They accepted it.

The plan was to ship the triage in three weeks, then pursue the architectural rebuild on a slower timeline.

---

## What Broke

The throttling logic worked. The classification logic didn't.

The existing message classification system was rule-based — it used a combination of message type strings and sender ID patterns to assign priority. No one had audited it in over a year. When we implemented queue-level throttling based on that classification, we inherited every error in the underlying system.

Fraud alerts were being miscategorized as "informational" because of a rule that had been written when fraud alerts came from a different sender ID. At some point, the fraud team had migrated their notification sender without updating the classification rules. The fraud alert message type string hadn't changed, but the sender ID pattern check was failing silently, and the fallback was "informational."

Four customers received fraud alerts four hours late. One had already disputed the transaction through their bank before the Arcline alert arrived. That dispute created a chargeback, which created a compliance record, which elevated the incident from a customer experience issue to a regulatory one.

---

## What Changed

Fraud alerts were pulled out of the classification system entirely and hardcoded as high-priority at the message schema level. Then came the audit I should have done before launch: every active message type checked against its assigned classification, confirmed by a person.

The audit took two days. It found six additional miscategorizations — none as severe as fraud alerts, but two involved account access notifications that were getting lower priority than they deserved.

We also changed how priority was assigned going forward. Instead of the system inferring priority from message type and sender patterns, each caller was required to declare priority explicitly as a field on the message schema. The default if you didn't declare was low. High-priority required documentation. The rule-based inference system was deprecated.

The architectural rebuild was reclassified from technical debt to a compliance risk. Engineering scoped it at eight weeks by reducing scope on two other initiatives. It shipped at week nine.

---

## What I'd Do Differently

The throttling decision was right. The implementation was wrong because it inherited a classification system I hadn't audited.

Before shipping any triage that depends on a classification layer, audit the classification. Pull a sample of recent messages across every type. Check whether the assigned priority matches what you'd assign if you read the message manually. Assume the system is wrong until you've confirmed it's right — rule-based classification systems accumulate drift every time a caller changes something upstream and doesn't update the rules.

I read the classification code. I did not verify that the code matched reality. Those are different things. The code made sense given its original assumptions. The original assumptions had been invalidated months earlier by a sender migration nobody documented.

I shipped a triage on an assumption. The assumption was wrong. The cost of being wrong was a compliance record. That's a bad trade for skipping two days of audit work.
