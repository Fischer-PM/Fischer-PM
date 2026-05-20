# Notification System Scaling: The Triage That Made Things Worse

**Note: This is a simulated case study. The company, product, and events are fictional.**

**Company: Arcline** (fintech payments platform)

---

## Situation

The notification system at Arcline was designed for 10,000 daily active users. It was a reasonable scope at the time — the platform had launched as a mid-market payments tool and the original infrastructure reflected that.

By month 18, Arcline had 500,000 daily active users. Nobody had made a deliberate decision to stop scaling the notification service; it had just been deprioritized quarter after quarter in favor of feature work. The delivery rate degradation happened slowly: 99.2% in month one, 97.8% by month eight, 94.1% by month seventeen. That's a 5.1 percentage point drop over a year and a half, which sounds manageable until you do the math — at 500,000 DAUs, a 5.1% failure rate is 25,500 missed notifications per day.

No one caught it because delivery rate wasn't on anyone's weekly dashboard. It surfaced when a market volatility event triggered a spike in transaction volume. The notification queue fell behind, alerts delayed by two to four hours, and customers found out about their transactions from their bank's app before Arcline notified them. Support volume tripled overnight.

---

## Constraint

The notification service wasn't owned by one team. It was a shared dependency across four product teams: payments, fraud, account management, and marketing. Any architectural change — queue redesign, service split, infrastructure scaling — required coordinating across all four teams, aligning on a design, and running a migration that touched every caller.

Engineering gave me an honest estimate: full rebuild was 14 weeks. That included design, implementation, cross-team coordination, and staged rollout. The business wanted a production fix in three weeks. A market event had just exposed the problem publicly. Three weeks was not a negotiating position — it was a constraint.

I had three weeks to meaningfully improve notification reliability without touching the architecture.

---

## Decision

The approach was to buy headroom without rebuilding. If the queue was overwhelmed, the answer was to make it do less — specifically, to stop treating all notifications as equal priority.

I proposed throttling non-critical notifications: marketing messages, weekly account summaries, promotional alerts. These would enter a secondary queue with a lower throughput ceiling, freeing capacity in the primary queue for transactional alerts — payment confirmations, fraud flags, account access notifications. The classification already existed in the message schema in a rough form. We'd enforce it at the queue level.

What I was sacrificing: marketing team's ability to deliver time-sensitive campaigns reliably. That was a known trade. I flagged it to marketing leadership before the change went live. They understood the priority.

The plan was to ship the triage in three weeks, then pursue the architectural rebuild on a slower timeline as a technical debt item.

---

## What Broke

The throttling logic worked. The classification logic didn't.

The existing message classification system was rule-based — it used a combination of message type strings and sender ID patterns to assign priority. No one had audited it in over a year. When we implemented queue-level throttling based on that classification, we inherited every error in the underlying system.

Fraud alerts were being miscategorized as "informational" because of a rule that had been written when fraud alerts came from a different sender ID. At some point, the fraud team had migrated their notification sender without updating the classification rules. The fraud alert message type string hadn't changed, but the sender ID pattern check was failing silently, and the fallback was "informational."

Four customers received fraud alerts four hours late. One of them had already disputed the transaction through their bank before the Arcline alert arrived. That dispute created a chargeback, which created a compliance record, which elevated the incident from a customer experience issue to a regulatory one.

---

## What Changed

We pulled fraud alerts out of the classification system entirely and hardcoded them as high-priority at the message schema level. Then we did what I should have done before launch: audited every active message type against its classification and confirmed the mapping was accurate.

The audit took two days. It found six additional miscategorizations — none as severe as fraud alerts, but two of them involved account access notifications that deserved higher priority than they were getting.

We also changed how priority was assigned going forward. Instead of the system inferring priority from message type and sender patterns, each caller was required to declare priority explicitly as a field on the message schema. The default if you didn't declare was low. High-priority required justification in the internal documentation. The rule-based inference system was deprecated.

The architectural rebuild was accelerated from a technical debt item to a compliance risk. Engineering got it scoped at eight weeks by reducing scope on two other initiatives. It shipped at week nine.

---

## What I'd Do Differently

The throttling decision was the right call under the constraints. Three weeks, no architecture changes, buy headroom — that logic was sound.

The mistake was implementing it on top of a classification system I had never audited. I knew the classification layer existed. I read the code. I didn't verify that the code matched reality.

Before shipping any triage that depends on a classification system, audit the classification. Pull a sample of recent messages across every type. Check whether the assigned priority matches what you'd assign if you read the message manually. Assume the system is wrong until you've confirmed it's right, because rule-based classification systems accumulate drift every time a caller changes something upstream and doesn't update the rules.

I shipped a triage on an assumption. The assumption was wrong. The cost of being wrong was a compliance record. That's a bad trade for skipping two days of audit work.
