# Defining SLAs That Are Actually Measurable

Most SLAs are aspirational targets written by engineering to describe what the system does when things go well. A real SLA is a commitment with consequences when it's missed. Most teams have the former and call it the latter.

This distinction matters more than it sounds. A target that's never enforced teaches downstream teams that the numbers aren't real, which means they stop planning around them. Once that trust is gone, the SLA document becomes a formality that nobody reads before an incident and nobody references during one. The goal of this playbook is to define SLAs that are specific enough to be enforceable, observable enough to be verifiable by the consumer, and honest enough to reflect what the platform can actually sustain.

---

## The SLA vs. Target Distinction

A target is internal — engineering cares whether it's met, and the consequence of missing it is an internal conversation about what went wrong. An SLA is a contract — a downstream team or customer can act on a miss, whether that means escalating, requesting a postmortem, or triggering a negotiated remedy.

The difference is who bears the cost when it's violated. If the answer is "only the platform team feels the pain," it's a target. If a downstream team's product reliability or a customer's business outcome degrades when the number is missed, it's an SLA. Both are legitimate and necessary; conflating them is what produces documents that look like SLAs but function like aspirational targets.

---

## Observable Outcome Framing

SLAs should be written in terms the consumer can measure themselves, not in terms of internal telemetry only the platform team can access.

"Messages processed within 5 seconds of API acknowledgment, measured as the time between the platform's 200 response and queue confirmation" is observable — the consumer can correlate their API call timestamp with their delivery event timestamp.

"Processing time under 5 seconds" with no definition of when the clock starts is not observable. The consumer has no way to verify it, which means they can't escalate confidently when they think it's being violated, and the platform team can't defend against an incorrect escalation.

Every SLA I write specifies: the start event, the end event, the measurement window, and whether the metric is an average, a p95, or a p99. The number means nothing without those anchors.

---

## Three Questions Before Committing to a Number

Before I commit to a specific SLA target, I ask three questions — not to slow the process down, but to avoid committing to a number the platform can't actually keep.

**What's the p99 performance, not just the average?** Average performance is almost always better than p99. If the SLA is written against the average and the consumer experiences the p99, there's a credibility problem even if the SLA technically isn't violated. I write SLAs against p99 by default and make the choice explicit when I don't.

**What's the failure mode when we miss it — is recovery automatic or manual?** An SLA on a system that self-heals within seconds of degradation is a different commitment than an SLA on a system that requires on-call intervention. The consequence of a miss is part of what the consumer needs to know.

**Does our monitoring actually measure this metric or a proxy?** I've seen platforms commit to delivery latency SLAs measured by a dashboard that tracks queue processing time — not end-to-end delivery time including partner delivery confirmation. The SLA says one thing; the alert fires on something else. Before committing to any SLA, I verify that the metric we're committing to is the metric we're monitoring.

---

## Processing SLA vs. Delivery SLA

These are separate commitments and need to be written separately, because they're governed by different failure modes and have different owners.

**Processing SLA:** The platform accepted the message via API and queued it for delivery within the committed window. This is entirely within platform control. A processing SLA of "99.9% of messages queued within 1 second of API acknowledgment" is enforceable and measurable by the platform alone.

**Delivery SLA:** The message reached the end recipient. This depends on external partners — carriers, email service providers, device operating systems — whose performance the platform can influence but not fully control. A delivery SLA of "95% of SMS messages delivered within 60 seconds of processing" is reasonable but requires the caveat that carrier-declared outages affecting delivery are outside the platform's control envelope.

Conflating these two in a single SLA creates a commitment the platform can't keep when a carrier degrades. Separating them lets the consumer know which layer failed when something goes wrong.

---

## How to Renegotiate an SLA

Renegotiate proactively, not after a miss.

When platform capacity, architecture, or operating conditions change in a way that makes a committed SLA unsustainable, the right move is to bring data to the affected teams before the number starts being missed consistently. Show what the platform can actually sustain. Propose a new number with a date when the new commitment takes effect. Give enough advance notice that downstream teams can adjust their own planning.

The PM who renegotiates transparently — even when the new number is worse — retains credibility with downstream teams because they've demonstrated that the numbers mean something. The PM who misses silently and explains it away after the fact has taught every downstream team that the SLA document is decorative. Recovering from that lesson takes longer than any renegotiation.
