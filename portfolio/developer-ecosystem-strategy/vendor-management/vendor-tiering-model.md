# Vendor Tiering at Scale

At 200 vendor integrations, "we treat everyone equally" means "we prioritize no one." Tiering is not a value judgment about vendors — it's a capacity allocation decision. Without it, support and integration resources flow toward whoever asks loudest, whoever has the most organizational advocates, or whoever happens to land in the queue at the right time. None of those are good criteria.

## The Four Tiering Criteria

Tiering works when you apply criteria in combination, not in isolation. A vendor that scores high on one criterion and low on the others may not belong in the top tier. The four criteria:

**API call volume (trailing 90 days).** Volume is a proxy for platform dependency. A vendor making 5M API calls per quarter has built something real on top of the platform; a deprecation without notice is a significant operational event for them. Volume alone doesn't determine tier — a high-volume vendor with a commodity relationship is not the same as a high-volume strategic partner — but it anchors the conversation in reality rather than aspiration.

**Revenue impact (direct or attributed).** This includes direct revenue where the vendor relationship has a commercial component, and attributed revenue where the integration supports a customer journey that generates revenue upstream. Both matter. Attributed revenue is harder to measure and worth the effort — it makes visible the integrations that look small and have outsized business impact.

**Integration complexity (ongoing support load, not just onboarding).** Some integrations have high ongoing complexity: they hit edge cases regularly, they span multiple APIs that interact in non-obvious ways, or they're built on older API versions that require maintenance attention. Onboarding complexity is a one-time cost. Ongoing complexity is a recurring cost that compounds at scale. Weight the latter more heavily.

**Business relationship type (strategic partner vs. standard vendor).** Strategic partners — first-of-kind integrations, anchor relationships in a new market segment, vendors with joint roadmap commitments — warrant different treatment than standard vendors. This criterion should be applied carefully: it's easy to inflate to justify preferred treatment for a relationship someone on the team likes. Apply it to relationships that have formal strategic designation, not informal affinity.

## What Each Tier Receives

**Tier 1:** Dedicated integration support with named contacts, proactive deprecation notice with a minimum one-quarter lead time, SLA commitment with active monitoring. These vendors get a quarterly review of their integration health, advance notice of platform changes that affect their use cases, and a direct escalation path for production issues.

**Tier 2:** Responsive support with defined SLAs (not best-effort), advance deprecation notice with a minimum 30-day lead time, documentation updated on API changes. Tier 2 vendors are not monitored proactively, but they have clear response time commitments and are not left to discover breaking changes after the fact.

**Tier 3:** Self-serve documentation, best-effort support, standard deprecation terms. This is not "no support" — it's support that scales through documentation quality rather than headcount. The investment for tier-3 vendors is in making self-serve actually work, not in providing coverage that can't be sustained.

## How Tiering Changes Over Time

A vendor that grows from 50K to 5M API calls per quarter has changed. Their dependency on the platform has changed. Their blast radius in the event of a failure has changed. The tier that was correct at onboarding may not be correct 18 months later.

Build a quarterly review process. Review trailing 90-day volume against current tier assignments. Flag vendors whose volume, revenue impact, or relationship type has changed materially. The review doesn't need to be comprehensive — a spreadsheet against the four criteria takes a few hours. What it produces is a tier assignment that reflects current reality, not initial estimates.

Static classification is a slow drift toward misalignment. The Tier 1 vendor who doesn't deserve the designation anymore is consuming resources that belong elsewhere.

## The Mistake of Tiering by Relationship

The vendor your team has a warm relationship with is not always the vendor most dependent on the platform. Relationship-based tiering looks like fairness and creates misalignment. It directs resources toward accessibility rather than impact.

I've seen this pattern produce tier-1 treatment for a vendor making 20K calls per quarter because their partnership manager had a strong relationship with the team, and tier-2 treatment for a vendor making 2M calls per quarter because they were quiet and self-sufficient. The quiet, self-sufficient vendor is the one who actually needs the proactive deprecation notice — because when something breaks for them, the impact is real.

## Communicating Tier Changes

Tier changes should be communicated with specifics: what tier the vendor is moving to, what criteria drove the decision, and what changes in their experience. "You've moved to Tier 1, which means you'll have a named integration contact, receive a minimum one-quarter notice before deprecations that affect your integration, and be included in our quarterly platform roadmap briefings" is a message vendors can act on.

"We're increasing your support level" is not. It doesn't set expectations, and it doesn't tell the vendor what they've gained or what's expected of them in return.

Give advance notice of tier changes when possible, especially downgrades. A vendor moving from Tier 2 to Tier 3 should have time to prepare for self-serve documentation before the change takes effect, not discover it when their support ticket response time changes.
