# SLA Improvement Teardown

Most SLA improvement initiatives fail not because teams can't fix the root cause, but because they start fixing before they've correctly categorized it. There are four types of SLA degradation, and each requires a different response.

Applying the wrong response wastes engineering time, delays actual recovery, and — most damagingly — produces a status update that says "we're working on it" while the underlying problem continues unchanged. The first job of a platform PM in an SLA degradation situation is to identify the category. Everything else follows from that.

---

## Category 1: Throughput Ceiling

The system works correctly. It cannot keep up with the volume.

You're seeing this when error rates climb or latency degrades in direct proportion to traffic volume, the degradation is consistent across all consumers rather than isolated to specific endpoints, and the system recovers during low-traffic windows without any intervention.

The throughput ceiling is the most intuitive type of SLA degradation and the one teams are fastest to start solving — which is also why it's often misdiagnosed. Before concluding you've hit a ceiling, rule out that you have a single consumer making dramatically more calls than historical baseline (a consumer bug, not a capacity problem) or that recent code changes reduced per-request efficiency.

**First action:** Instrument per-consumer call volume over the last 7 days and compare it to the prior 4-week baseline. If overall volume is up and consumer mix is proportional, you have a capacity problem. If overall volume is flat but one consumer's call rate has doubled, you have a consumer issue. These are different conversations with different owners.

---

## Category 2: Tail Latency Spikes

The p50 is fine. The p99 is not.

You're seeing this when the median response time looks healthy, but a subset of requests — typically 1 to 5% of total volume — are experiencing latencies significantly above the SLA contract. Consumers whose integrations surface the p99 experience are filing tickets. Consumers whose integrations average across all requests may not notice.

Tail latency spikes are frequently misdiagnosed as capacity problems. They are usually not. Common causes include: garbage collection pauses, database lock contention on specific query patterns, resource exhaustion in a thread pool that manifests under specific request conditions, or external dependency calls that succeed but take significantly longer for a subset of requests.

**First action:** Separate p50, p95, and p99 latency charts and look at their behavior independently over a 72-hour window. If p50 is stable and p99 is volatile, you are looking at a tail latency problem, not a capacity problem. The fix is in the tail — which means profiling the slow requests specifically, not adding capacity uniformly.

---

## Category 3: Dependency Failure

Your system is functioning correctly. An upstream or partner dependency is not.

You're seeing this when SLA degradation is isolated to specific functionality that routes through a particular external service — a carrier, a third-party API, a shared internal service owned by another team — and the degradation pattern correlates with that dependency's performance rather than your own traffic patterns.

This category is the most politically complicated because the fix is not yours to implement. You can add circuit breakers, fallback behaviors, and retry logic to reduce the consumer-visible impact. You cannot fix the dependency. The communication and escalation path is different from the other three categories.

**First action:** Isolate whether the degradation is endpoint-specific or platform-wide. If endpoint-specific, trace the call chain for that endpoint and identify the external call. Check whether the dependency has a status page, an incident channel, or an SLA breach report from their team. If the dependency is internal, open a P1 with that team immediately. If external, escalate to whoever owns the vendor relationship.

---

## Category 4: Measurement Error

The SLA appears degraded because the monitoring is wrong.

You're seeing this when consumer-reported behavior does not match what your monitoring shows, when the degradation appeared suddenly without any corresponding traffic change or deployment, or when the degradation pattern doesn't match any plausible technical failure mode.

Measurement error is the most embarrassing category to diagnose and the most important not to skip. I have seen teams spend three weeks optimizing a system for a performance problem that turned out to be a misconfigured alert threshold. The fix for a measurement error is not engineering — it is monitoring calibration.

**First action:** Pull raw response logs from the service itself and compare them against what the monitoring layer is reporting. If they don't match, the monitoring is the problem. Check for: recent changes to monitoring configuration, incorrect percentile calculations, synthetic traffic being included in production metrics, or timezone mismatches in aggregation windows.

---

## Communicating SLA Improvement Progress Without Overpromising

"We're working on it" is the most dangerous status update a platform PM can give. It signals that something is being done without communicating what, when the first evidence of improvement will be visible, or what the consumer should do in the interim. Consumers who receive "we're working on it" have no information they can act on. They will ask again, escalate, or build workarounds — all of which create more noise during the resolution window.

The alternative is a status update structured around what you know, what you're doing, and when the next update will arrive:

- **What you know:** Category of the problem, which consumers are affected, what specifically is degraded
- **What you're doing:** The specific action in progress, who owns it, what it addresses
- **Next update time:** A specific time, not "as soon as we know more"

If you don't yet know the category, say so explicitly and give the time by which you will. "We are diagnosing the root cause. By 3pm today we will have a category determination and a first action. I will send an update at 3pm." That is a status update that gives consumers something to work with.

Overpromising a resolution timeline is worse than the SLA degradation itself. It converts a technical problem into a trust problem, and trust problems take longer to resolve.
