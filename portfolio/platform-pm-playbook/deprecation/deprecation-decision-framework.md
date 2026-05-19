# Deprecation Decision Framework

The instinct to deprecate before you're ready costs almost as much as the instinct to maintain past the point of usefulness. Most teams get it wrong in both directions.

Deprecating too early traps downstream consumers mid-build. Deprecating too late creates a maintenance burden that quietly taxes every engineer on the platform team — not in dramatic incidents, but in the slow drag of keeping two surfaces alive simultaneously. The goal of a deprecation framework isn't to find the "right" moment in the abstract. It's to make the decision deliberately, with the information that actually matters, before the decision gets made for you by a budget cycle or an executive offsite.

These are the four questions I work through before committing to a deprecation.

---

## 1. Is downstream dependency count growing or shrinking?

This sounds obvious. It rarely gets asked explicitly.

A service with 12 downstream consumers that had 18 six months ago is in decline. Consumers are already leaving on their own. Your job is to manage the tail cleanly, not to force a migration that may already be happening organically. A service with 12 downstream consumers that had 8 six months ago is being adopted. Deprecating it now means interrupting teams mid-integration and burning the trust that got them there.

The number of consumers matters less than the direction of that number. Pull your dependency graph, check it against the last two quarters, and know which way you're moving before you make any announcement. A service in decline and a service in growth require fundamentally different timelines, different communication strategies, and different migration support investments.

---

## 2. What is the blast radius of a hard cutoff?

There is a meaningful difference between a soft sunset and a hard cutoff. Conflating them is one of the most common mistakes I see in deprecation planning.

A **soft sunset** means the service continues to function but receives no new investment — no feature work, no SLA improvements, and eventually no support escalations. Consumers can remain on it as long as they accept those terms, but they are on notice that migration is their responsibility. This is appropriate when the replacement is available, the migration path is documented, and consuming teams have capacity to move on their own timeline.

A **hard cutoff** means the service goes dark on a specific date. Traffic that hasn't migrated stops working. This is appropriate only when you have a security or compliance reason that makes continued operation genuinely untenable — or when the cost of maintaining two surfaces has crossed a threshold you can quantify and defend to leadership in writing.

Blast radius analysis for a hard cutoff requires knowing: which consumers have active production traffic, which are legacy integrations with minimal or no traffic, and what fails for end users if those consumers haven't migrated in time. I want that answer documented before I agree to any cutoff date.

---

## 3. Does the replacement meet the existing SLA contract?

Not: is it better? Not: does it have more features? The question is whether it meets the contract the consumers currently depend on.

If the current service has a 99.9% uptime SLA and the replacement has demonstrated 99.7% in staging, that's a problem, not a migration announcement. Consumers built their systems around the contract you made. Asking them to accept a degraded contract in the name of modernization is a breach of the relationship, even if the replacement is architecturally superior in every other dimension.

I check four things: uptime SLA parity, p99 latency parity, error rate profile, and rate limit structure. If all four match or exceed the existing contract, the migration conversation is operational. If any fall short, the replacement isn't ready — regardless of what the roadmap says or what engineering leadership believes about its trajectory.

---

## 4. Who bears the migration cost — platform or consumer?

This question determines the timeline more than any technical factor.

If the platform team is doing the migration work — writing the adapters, running the tests, handling the cutover in coordination with consumers — you can move faster. If you're asking 12 engineering teams to each allocate sprint capacity to migrate their integrations, you're now negotiating with 12 different roadmaps. Some of those teams will move in weeks. Some will take two quarters. Some will request the soft sunset option and stay on the legacy surface indefinitely.

Knowing who bears the cost changes how you communicate the deprecation, how you set the timeline, and how much support infrastructure you need to build alongside the migration path. A migration where consumers bear the cost requires dedicated support channels, thorough documentation, and a runway measured in quarters, not sprints.

---

## Worked Example: Fictional Messaging Service

Suppose I'm evaluating deprecation of a messaging service with 12 downstream consumers. Four are active — they have ongoing production traffic and depend on the service for core functionality. Eight are passive — they integrated at some point, have minimal or no current traffic, and may not have a team that actively owns the integration anymore.

Working through the four questions:

**Dependency direction**: The active consumer count has held flat for three quarters. No new consumers have onboarded. The service is not in growth.

**Blast radius**: A hard cutoff affects 4 active consumers with real production exposure. The 8 passive consumers represent cleanup work, not production risk. I would treat this as a soft sunset with a defined end-of-support date, not a hard cutoff — unless a compliance reason surfaces that I haven't accounted for.

**SLA parity**: I check the replacement against current contract terms across all four dimensions. If parity is met, migration conversations begin. If parity is not met, migration conversations begin after parity is achieved — not before.

**Migration cost**: With 4 active consumers, I'd offer platform-supported migration — meaning the platform team writes the migration guide, provides a dedicated integration environment, and staffs a support channel for the duration. The 8 passive consumers receive a notification and a longer timeline. We do not spend engineering time chasing inactive integrations.

Decision: soft sunset announced in the current quarter, hard cutoff communicated 2 quarters out, platform-supported migration for the 4 active consumers, passive consumers handled via notification only.

---

## The Caveat This Framework Doesn't Resolve

This framework works when the deprecation decision is genuinely technical and operational. It does not help when the pressure to deprecate is primarily budgetary — when someone in finance or senior leadership has decided that the cost of running two systems is too high and the timeline is driven by a cost target, not a readiness assessment.

That is a separate conversation requiring different tools. The blast radius analysis and SLA parity check are useful evidence in that conversation, but they won't resolve the tension between operational readiness and financial pressure on their own. Knowing which type of pressure is actually driving the deprecation discussion is the first thing to establish — before opening the planning doc.
