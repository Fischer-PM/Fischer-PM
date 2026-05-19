# A Taxonomy of Message Loss

Not all message loss is the same. Treating it as a single metric leads to wrong prioritization, unclear ownership, and SLA commitments that don't match the failure modes they're supposed to govern.

A platform reporting a single "message loss rate" is combining at least four distinct failure categories with different causes, different owners, and different remediation paths. When an incident happens and the question is "where did the messages go," the answer depends entirely on which category failed. Without that taxonomy, the investigation is slower, the postmortem is less useful, and the SLA targets are set against the wrong denominator.

---

## 1. Infrastructure Loss

**Definition:** The message was never queued. The platform failed before processing began.

This is the most straightforward category and the one platforms are best at measuring. The message hit the API, the API returned an error or timed out, and the message is gone before any downstream processing occurred.

**Who owns it:** Platform engineering owns the fix; I own the SLA commitment and the communication to downstream teams when it's missed.

**How to detect it:** Queue ingestion success rate is the primary signal — specifically the ratio of API calls resulting in a confirmed-queued message vs. those that returned errors or dropped silently. Dead-letter queue volume is a secondary signal; spikes indicate messages that entered the pipeline but failed at the first processing stage. API response code distribution (4xx vs. 5xx breakdown) helps separate platform failures from caller errors.

**SLA target:** Zero acceptable loss for acknowledged messages — if the platform returned a 200, the message must be queued. Target 99.99% or higher ingestion reliability measured against total attempted sends.

---

## 2. Routing Loss

**Definition:** The message was queued but sent to the wrong destination — bad address, stale routing data, or misconfiguration.

Routing loss is frequently misclassified as delivery loss because it surfaces at the delivery stage. A message sent to an invalid phone number, a deactivated email address, or a stale push token didn't fail because of a delivery problem — it failed because the routing data was wrong before the message left the queue.

**Who owns it:** This is shared territory between the PM and engineering, and the sharing needs to be explicit. The platform is responsible for accurate routing resolution; the data quality of the address list is usually the responsibility of the onboarding team or a shared data service. Surface this as addressability rate — valid destinations divided by total sends — and declining rate is a data quality problem, not a delivery problem.

**How to detect it:** Delivery receipt mismatch between attempted sends and confirmed routes, error code analysis distinguishing invalid-destination codes from delivery-failure codes, and hard vs. soft bounce classification in email (hard bounces are routing failures; soft bounces are delivery failures).

**SLA target:** Tracked as addressability rate, not delivery rate. A platform with 95% addressability and 99% delivery on addressable messages has a different problem than a platform with 100% addressability and 95% delivery.

---

## 3. Delivery Loss

**Definition:** The message was sent to the right place but not received — carrier rejection, email bounce, push token expiry, in-app session absence.

This is the category most teams think of when they say "message loss," and it's the one that gets the most engineering attention. It's also the category most dependent on external partners and therefore the hardest to fully control.

**Who owns it:** The platform negotiates SLA terms with carrier and ESP partners and escalates when partner performance degrades. Engineering monitors delivery receipts and maintains partner integrations. I own the reporting to downstream teams — including being honest when the failure is on a partner's side vs. ours.

**How to detect it:** Delivery receipts from carriers, bounce codes from email service providers, push delivery confirmation from APNS and FCM, in-app event correlation when session presence is a prerequisite.

**SLA target:** Channel-specific. For SMS on a clean number list: 95-99% delivery. For email with proper list hygiene and authenticated sending domains: 98% or higher. Push delivery rates vary significantly based on token freshness and OS-level behavior and should be tracked with that context attached.

---

## 4. Silent Loss

**Definition:** The message was delivered to the device or inbox but the user never saw it — push notification suppressed by Do Not Disturb mode, email landed in spam without a bounce code, in-app notification delivered to a backgrounded session the user never returned to.

**Who owns it:** Almost no one. That's the problem.

Silent loss is the only category where the platform can report successful delivery and the message still failed its purpose. The delivery receipt is truthful; the outcome is not what the sender intended. This category lives in the gap between platform responsibility (delivery) and product responsibility (engagement), and because it falls in a gap, it often has no owner.

**How to detect it:** Impression tracking where available, notification center visibility data on mobile platforms, in-app event correlation — did the user open the app within a reasonable window of delivery? Read rates vs. delivery rates in email, controlling for spam placement.

**SLA target:** Almost no platforms define one. This is a gap worth closing.

---

## Why Silent Loss Matters More Than Most Teams Think

Silent loss is the category most platforms don't measure, and it's the one most correlated with user disengagement from notification channels. A user who receives a push notification that was suppressed by DND three times in a row may disable push entirely. A user whose "important account notices" consistently land in spam eventually stops looking for them. A platform reporting 99.9% delivery with 40% silent loss isn't performing — it's deceiving itself. The downstream consequences of that gap show up in product metrics, not platform metrics, which is exactly why it goes unaddressed for so long.
