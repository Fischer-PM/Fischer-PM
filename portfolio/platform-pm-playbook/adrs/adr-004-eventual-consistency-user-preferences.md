# ADR-004: Accepting Eventual Consistency for User Preference Propagation

*Simulated decision record — fictional company (Prism), representative of real patterns in distributed preference management.*

---

## Status

Accepted. The consistency model was correct for most scenarios. One incident exposed the gap where it wasn't.

---

## Context

Prism's platform stored user notification preferences — channel opt-ins, frequency caps, category subscriptions — in a central preference service. Twelve downstream systems consumed these preferences to decide whether to send a notification.

The question was consistency: when a user updated a preference, how quickly was that change visible to all twelve consumers?

**Option A — Strong consistency:** Preference updates are synchronously propagated to all consumers before the write is acknowledged. The user's change takes effect immediately everywhere.

**Option B — Eventual consistency:** Preference updates are written to the preference service and propagated asynchronously. Consumers cache preferences locally and refresh on a TTL or event-driven basis. The user's change takes effect everywhere within a bounded window.

---

## Decision

**Chose Option B: Eventual consistency with a target propagation window of 60 seconds.**

The case for eventual consistency:
- **Performance:** Synchronous propagation to twelve systems on every preference write would have made preference updates slow (12 round trips or a broadcast with coordination). The user experience of a preference update is binary — did it work or not — and a 60-second propagation window is invisible to users in normal interaction patterns.
- **Availability:** Strong consistency would create availability coupling between the preference service and all twelve consumers. If any consumer was slow or unavailable, preference writes would fail. Eventual consistency means a consumer outage doesn't block preference updates.
- **Operational simplicity:** Caching preferences locally with TTL-based refresh is a well-understood pattern. Synchronous broadcast is not.

The 60-second window was based on: how quickly could a user re-encounter a notification after updating a preference? For most notification types, re-encounter within 60 seconds was unlikely. For time-sensitive alerts, the preference service was bypassed — security and regulatory notifications didn't check opt-out state.

---

## Consequences

### What worked

Preference writes were fast and available. Consumer cache hit rates were high, reducing load on the preference service. Twelve teams integrated against a simple, predictable interface.

### The incident: "eventually" was 47 minutes

Four months post-launch, a bug in the preference propagation service caused preference updates to stop propagating to three of the twelve consumers. The bug didn't cause errors — the propagation service continued to run and report healthy. It was simply not publishing update events. Consumer caches continued serving stale preferences from their last successful refresh.

The detection vector was a user complaint: a user had opted out of marketing emails three hours earlier and was still receiving them. Support pulled the logs, found the opt-out was correctly recorded in the preference service, and escalated.

Root cause: a silent failure in the event publish path. The propagation service was dequeuing update events and attempting to publish them; a downstream connection issue was causing silent drops with no retry and no dead-letter capture.

**The 47-minute gap in the incident title:** That was the time between when the user opted out and when the preference propagated after the incident was resolved. Three consumers had caches that were 47 minutes stale before the fix was deployed.

What made this worse from a product and compliance perspective: one of the three affected consumers was the marketing email system. Users who opted out during the failure window continued to receive marketing email until the cache refreshed. That's a compliance event, not just an operational incident.

### The hidden assumption

The eventual consistency model was designed with a failure mode in mind: a consumer might use a slightly stale preference. It was not designed for the failure mode where propagation stops entirely and caches age indefinitely.

The operational assumption was that consumers would detect stale caches through normal operation. That assumption was wrong — a consumer with a 47-minute-old cache looks identical to a consumer with a 60-second-old cache from the consumer's perspective.

**What this means:** Eventual consistency requires explicit staleness monitoring that is independent of the propagation path. The right metric is cache age at each consumer — not "is the propagation service healthy" but "how old is the oldest preference entry in each consumer's cache?" That metric should alert before it becomes a compliance event.

### What the model gets right

For the 99.7% case, eventual consistency with a 60-second window is correct. The alternative — synchronous propagation to twelve consumers — would have made the availability and performance profile significantly worse for a problem that materializes rarely.

The lesson isn't that eventual consistency was wrong. It's that "eventual" needs a defined upper bound, that upper bound needs to be monitored per-consumer, and a propagation failure should be detectable within minutes, not hours.

The postmortem added: per-consumer cache age monitoring with a 5-minute staleness alert threshold, DLQ capture for failed event publishes, and a monthly chaos test that validates propagation recovery behavior. None of those were in the original design.
