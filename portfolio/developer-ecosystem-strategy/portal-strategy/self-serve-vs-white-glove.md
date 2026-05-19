# Self-Serve vs. White-Glove: A Decision Framework

The instinct to give every vendor white-glove support sounds like excellent service. At 200 vendors, it's a capacity crisis in slow motion. The team becomes the bottleneck for every onboarding, every question, every edge case — and because the cost is diffuse and the pain is gradual, it's easy to miss until the queue is unmanageable.

The right question isn't "do we have capacity to support this vendor?" It's "what level of support is actually warranted, and what's the cost of providing more than that?"

## The Four Decision Variables

### 1. Integration Complexity

How many custom configurations does this integration require? How likely is the vendor to encounter unexpected edge cases in your API's behavior?

Some integrations are genuinely complex — non-standard authentication patterns, high payload volume with specific rate limit considerations, dependencies on multiple APIs that interact in ways the documentation doesn't fully capture. These warrant white-glove. The vendor will have questions that aren't answerable from documentation alone, and a support ticket back-and-forth is more expensive than a few hours of proactive guidance.

Low-complexity integrations — standard auth, well-documented endpoints, no unusual edge cases — are good self-serve candidates. The documentation should be enough. If it isn't, the right fix is the documentation, not adding white-glove to compensate for gaps.

### 2. Vendor Tier

What's the business value of this relationship? High-revenue vendors, strategic partners, and first-of-kind integrations warrant more investment, both because the stakes are higher and because the learnings from those integrations often improve the platform for everyone who follows.

Tier 3 commoditized vendors at low volume do not warrant the same investment. That's not a judgment about the vendor — it's a capacity allocation decision. White-glove support for a tier-3 vendor at low volume is a subsidy the platform cannot afford at scale, and providing it inconsistently is worse than having a clear policy.

### 3. Error Blast Radius

If this integration fails in production, what's the customer impact? This variable overrides tier in some cases.

A tier-3 vendor with high blast radius — payment processing, identity verification, anything that sits in a critical customer path — needs more support than the tier designation suggests. The failure mode isn't "this vendor has a bad experience." It's "customers can't complete transactions." That's a different problem.

High blast radius integrations should get additional pre-production review regardless of tier, and clear escalation paths in case of production failure.

### 4. Support Cost at Scale

At 200 vendors, the marginal cost of white-glove is significant. Track support hours per vendor per quarter. When the ongoing support time for a self-serve vendor exceeds what a structured white-glove onboarding would have cost, the economics have flipped.

This happens more than it should. A vendor that generates eight support tickets over three months has consumed more support capacity than a two-hour guided onboarding would have. The pattern is often invisible because the cost is distributed across individual tickets, not aggregated per vendor.

## The Opinionated Call

At low complexity + tier 3 + low blast radius: self-serve with documentation is the right call. White-glove for this tier is a subsidy the platform can't afford at scale. Providing it anyway creates an expectation that's unsustainable and crowds out support capacity for vendors who need it more.

This is a policy that requires defense, because individual requests for more support always feel reasonable. The framework gives you the basis for that defense: here are the criteria, here is where this vendor scores, here is what that means for support level.

## Behavioral Signals to Upgrade

Some self-serve vendors reveal themselves as needing more support through their behavior:

- Opens 5 or more support tickets in the first 30 days. This is a signal that documentation is insufficient for this vendor's use case, the integration is more complex than initially assessed, or both.
- Has a failed production deployment. A production failure in the first quarter is a prompt to reassess whether self-serve was the right call and what additional support would prevent recurrence.
- Is a strategic partnership that wasn't initially tier-classified correctly. Tier classification at onboarding is an estimate based on available information. It should be revisited when the relationship changes.

When these signals appear, the response isn't to add support reactively. It's to re-run the framework, determine the right support tier, and reset proactively. Reactive support for a vendor who needed white-glove all along costs more than getting the classification right at the start.
