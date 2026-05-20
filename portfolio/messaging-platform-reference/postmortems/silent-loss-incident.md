**Note: This is a simulated postmortem. The company, product, and events are fictional.**

# Postmortem: Silent Notification Loss During Market Volatility Event

**Date:** Tuesday, mid-quarter  
**Duration:** 6 hours, 33 minutes (09:14am – 3:47pm, detection at 4:02pm)  
**Severity:** P1 — 94,000 delayed alerts, 6,200 undelivered, zero monitoring alerts fired  
**Status:** Resolved. Monitoring and fallback architecture updated.

---

## What Happened

During a sustained market volatility event, our transaction alert pipeline silently degraded for six hours and thirty-three minutes. Customers did not receive alerts they depended on. Our systems generated no automated alert during that entire window. We found out from customer service.

The timeline:

- **09:14am:** A market volatility event triggered a 340% spike in transaction alert volume. Normal throughput is approximately 80,000 alerts per hour. At peak, we were receiving 272,000 per hour.
- **09:14–09:31am:** Queue depth climbed but did not breach the monitoring threshold. Our alert was configured to fire at a queue depth greater than 500,000 messages. Depth reached 490,000 and temporarily stabilized — just under the line.
- **09:31am:** The downstream push notification service began rate limiting our delivery requests. Queue processing slowed. Depth resumed climbing faster than we were draining it.
- **09:31am–3:47pm:** Over six hours, 94,000 transaction alerts were delivered between 2 and 6 hours late. An additional 6,200 alerts were never delivered — the push tokens associated with those delivery targets had expired during the delay window, and our platform logged the failed delivery and stopped. No retry. No fallback. No alert to anyone.
- **3:47pm:** The customer service team noticed an elevated volume of inbound contacts. Customers calling and writing to ask why they hadn't received expected transaction alerts.
- **4:02pm:** Engineering was pinged. Queue depth identified within minutes. Incident declared.

Six thousand two hundred customers received no transaction alert for activity on their accounts. Our stated SLA for transactional alerts was delivery within 30 seconds. We missed it, for hours, and found out from our customers before we found out from our systems.

## How We Found Out

Customer complaints. Not monitoring.

Our monitoring was configured for queue depth, not queue age. Messages were backing up, but the queue depth stayed near the threshold because we were still processing — just slowly, under rate limiting. Queue age, meaning how long the oldest undelivered message had been waiting, was not monitored at all. We had messages sitting in queue for hours. No alert fired.

This is the part that matters: we had a monitoring configuration that was technically active, technically correct by its own logic, and completely inadequate for detecting the actual failure mode. Queue depth monitoring assumes that a large backlog is the problem. Our problem was a slow drain that kept depth just below the line while messages aged past any reasonable delivery window. The monitoring was watching the wrong thing.

The 3:47pm customer service signal represented customers who had waited long enough to give up and contact us. The actual failure started at 09:31am. We were 6 hours and 16 minutes late to our own incident.

## Root Cause

**Technical:** Monitoring was depth-based, not latency-based. The push notification service downstream had rate limits that were not documented in our integration runbook and were not accounted for in capacity planning. Silent loss on expired push tokens was untracked — the platform logged the delivery failure but took no further action. No retry logic. No fallback channel. No surfacing of the failure to anyone.

**Process:** Our transactional alert SLA — delivery within 30 seconds — was written by product, reviewed and agreed to by engineering, and published on the status page. It was not monitored. There was no automated check that compared actual delivery latency against that commitment in real time or at any interval. The SLA existed as a document and a promise. It did not exist as a measurement.

This is worth being direct about: we committed to customers that they would receive transaction alerts within 30 seconds, and we had no way to know whether we were keeping that commitment on any given day. We had been keeping it, until we weren't, and we found out because customers told us.

## What We Did Immediately

- Manual requeue of all delayed messages where push tokens were still valid; approximately 87% of the 94,000 delayed messages were recoverable
- Direct outreach to 847 customers identified as having received critical transaction alerts more than 2 hours late, prioritized by account activity value
- Posted an incident update on the status page within 2 hours of incident declaration, including acknowledgment that some alerts had not been delivered
- Worked with the downstream push notification provider to document rate limits and received confirmation of their capacity tier

## What We Changed Permanently

**Monitoring:**

- Added queue age monitoring — an alert fires when any message in the transactional alert queue has been waiting longer than 45 seconds, regardless of total queue depth
- Implemented p95 delivery latency tracking for all transactional message types, with a real-time dashboard and an automated alert when p95 exceeds 60 seconds
- Added a daily SLA compliance report that compares actual p95 delivery latency against the published SLA commitment

**Delivery architecture:**

- Expired push tokens now trigger immediate SMS fallback for all messages classified as transactional; informational and marketing message types retain push-only delivery
- Failed delivery — defined as any message not delivered within 90 seconds — now surfaces to a dead-letter queue with active monitoring and a retry policy
- Downstream rate limits for all delivery partners are now documented in integration runbooks and included in quarterly capacity planning reviews

**Process:**

- Added a policy requiring that any SLA commitment published externally must have a corresponding monitoring implementation before the commitment goes live; both artifacts are required to ship together

## What We'd Do Differently

The SLA was defined by product and signed off by engineering without a monitoring implementation attached to it. No one in that conversation asked "how will we know if we're meeting this?" That question should have been mandatory. The failure mode wasn't a surprise in retrospect — a latency-based SLA with no latency monitoring is a known gap. We just didn't see it because no one was looking for gaps.

The right process is that an SLA commitment and its corresponding monitoring specification are a single artifact, written and reviewed together, requiring sign-off from both product and engineering before publication. If we can't monitor it, we don't commit to it. We have now made that explicit in our product development process.

## What This Didn't Fix

Silent loss on in-app notifications remains unmonitored. We track delivery to the notification center — whether the message was accepted by the delivery system — but not whether the notification was actually displayed to an active user. A user with the app open in a degraded state, or a user on a device with notifications suppressed, may not receive a notification that our system marks as delivered. We have no receipt-side signal.

This is an industry-wide constraint. Push delivery receipts are unreliable and, for most platforms, optional. We have acknowledged the gap and have no current plan to close it fully. Our metrics remain delivery-side, which means our SLA compliance numbers reflect what we sent, not what customers received. That distinction matters, and we are not currently measuring it.
