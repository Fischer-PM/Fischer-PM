# Managing APIs as Products

The moment a second team builds on top of your API, it's no longer a technical asset — it's a product. That distinction matters, because products have users, and users have expectations you can't ignore when you push code. An internal team that depended on an undocumented behavior and wakes up to a broken integration on Monday morning doesn't care that the change was technically correct. They care that something stopped working.

## Who Your Users Are and What They Want

API consumers split into two categories with meaningful differences.

Internal consumers want speed, stability, and predictability. They'll tolerate rough documentation if the API is reliable and doesn't change without notice. What they won't tolerate is surprise — an API change that breaks their integration without warning, a version deprecation announced two weeks before end-of-life, a behavior change that isn't in the changelog. Internal consumers are often less vocal than external ones because they're in the same organization and have informal escalation paths, but they're also capable of building significant workarounds that make future platform changes harder to implement.

External consumers want documentation, versioning, and support. They can't call the engineering team directly. They depend on written information being correct, on version stability, and on a support path when things break. The bar for documentation quality is higher because there's no fallback. A good rule of thumb: if an external consumer can't successfully integrate using only the published documentation and examples, the documentation isn't good enough.

The overlap is that both groups value reliability and predictability above most other things. The divergence is in their fallback options when things break. Internal teams have more; external teams have fewer.

## API Versioning Is a Product Decision

The engineering question is "can we implement a new version?" That's almost always yes. The product question is "how long will we support the old one and at what cost?" That's a business call with implications for engineering roadmap, support capacity, and consumer trust.

A version deprecation that gives 90 days notice costs less in consumer trust than one that gives 30 days. A version that's actively supported — bug fixes applied, security patches backported — costs more in engineering time than one that's officially stable with no new changes. These are tradeoffs, and they should be made explicitly rather than discovered after the deprecation announcement.

The decision framework: what's the migration burden on consumers? What's the ongoing cost of supporting the old version? What's the risk of keeping a deprecated version active longer than planned? Name those numbers before setting a deprecation date.

## What an API Roadmap Actually Contains

An API product roadmap is not a list of new features. It has three input streams:

Consumer feedback: what's missing, what's broken, what's undocumented but relied upon. This comes from support tickets, integration reviews, and direct conversations with consumer teams. The most useful signal is the thing consumers have built workarounds for — those workarounds are telling you where the API failed them.

Platform priorities: what needs to deprecate because it's a security risk or a scaling liability, what needs to expand because the platform is moving in a new direction, what performance envelope the API needs to operate within. These are constraints that shape the roadmap from the platform side.

Reliability commitments: what cannot change without major versioning, what SLAs the API is committed to, what behavior is formally guaranteed. This is the stable layer that consumer teams depend on to build confidently. If reliability commitments aren't explicit, consumers will infer them from behavior — and then you'll break them accidentally.

A roadmap that only shows new capabilities is a roadmap that makes existing consumers nervous.

## Measuring API Product Success Beyond Call Volume

Call volume tells you the API is running. These metrics tell you whether it's working:

**Time-to-first-successful-call for new consumers.** The baseline measure of whether a new consumer can actually use the API without help. If this number is high, the documentation and examples are failing.

**Error rate by consumer, not aggregate.** An aggregate error rate of 2% looks fine. An error rate of 40% for one consumer and 0.1% for everyone else looks fine in aggregate and is a crisis for that one consumer. Consumer-level error rates surface problems that aggregate metrics hide.

**Feature adoption rate.** Are consumers using new API capabilities, or are they pinned to v1 behaviors? Low adoption of newer features is a signal that migration burden is too high, the new capabilities aren't well-documented, or consumers don't see value in moving. All of those are product problems.

**Support ticket volume per consumer.** A consumer generating significant support volume is either hitting documentation gaps, encountering unexpected behavior, or in a use case the API wasn't designed for. All three are worth understanding.

## The Inflection Point

An API becomes a product when a consumer has built something that depends on your behavior — including undocumented behavior. That's when you have to start acting like you have users, because you do. The consumer doesn't know which behaviors are documented and which aren't. They know what their integration does and doesn't work. Your responsibility as a PM is to understand that distinction and decide, explicitly, which behaviors you're committing to maintain and which you're not — before a change makes the answer obvious.
