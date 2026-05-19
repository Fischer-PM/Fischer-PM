# Designing a Reusable Notifications API: Three Decisions That Defined the Architecture

This is a design retrospective framed as a thought exercise on the product-level decisions in building a reusable notifications API. The decisions are real patterns; the specifics are generalized.

The goal was a notifications API that multiple products could consume without rebuilding notification logic each time. Three decisions shaped the architecture. One of them created more downstream friction than anticipated.

## Decision 1: What Goes in the API Contract vs. What's the Caller's Responsibility

The fundamental question was where to draw the line between what the API owns and what the caller owns.

**Option A:** The API handles channel selection and payload construction. Callers pass in a notification type and a set of parameters; the API assembles the message and chooses the channel.

**Option B:** The caller specifies channel and payload; the API handles delivery. The API is essentially a delivery mechanism with no opinions about content or routing.

**Option C:** The API handles delivery routing; the caller specifies intent and content. The caller describes what the notification is for and what it should say; the API determines where to send it based on user preferences and context.

We chose Option C — intent-based routing. The caller describes the notification purpose and the content; the API determines channel based on user preferences and context. This is the most opinionated of the three options and, in retrospect, the most correct for the use case.

The tradeoff: intent-based routing required maintaining user channel preferences within the notifications service, which created a dependency that didn't exist before. Two consuming teams had to migrate their preference logic out of their own systems and into the notifications service before they could use the API. That migration took longer than the API build itself. The decision was right; the plan for managing the dependency wasn't.

## Decision 2: Delivery Guarantees

The choice was between two delivery models with meaningfully different complexity profiles.

**At-least-once delivery:** Simple to implement. Creates a duplicate handling burden on consumers — if a notification is delivered twice, the consumer needs to handle that gracefully or the user gets two messages.

**Idempotent delivery with deduplication key:** More complex to implement. The API accepts a caller-provided key and deduplicates on that key within a defined window. Consumers don't need to handle duplicates because the API does.

We chose at-least-once with a documented deduplication window of 24 hours. The rationale was that most notifications in the expected use cases were not sensitive to duplicates, and requiring every consumer to implement a deduplication key would add friction to the API contract.

The tradeoff: most consumers didn't implement idempotency handling on their side either, and some use cases turned out to be more sensitive to duplicates than initially assessed. The documentation was explicit about the guarantee and the consumer responsibility. But explicit documentation that most consumers don't read before their first production incident is documentation that's doing less work than it looks like. That was a documentation failure in terms of placement and emphasis, not a documentation failure in terms of accuracy — but it had the same effect.

## Decision 3: Multi-Channel Routing

The third decision was how the API should handle consumers who want to reach users across multiple channels.

**Option A:** Consumers specify the channel. The API delivers to that channel. Simple, but puts routing logic back in the caller.

**Option B:** The API routes based on user preference. The API knows the user's preferred channel and delivers there. Callers don't need to think about routing.

**Option C:** The API tries the preferred channel and falls back to a secondary channel if the primary fails. Consumer code doesn't change; the API handles failure silently.

We chose Option B as the primary model with Option C as the fallback behavior — user preference is primary, and if the preferred channel fails, the API falls back to a secondary channel without requiring consumer code changes.

The tradeoff: debugging delivery failures became significantly harder because the consumer couldn't see which channel was attempted, which failed, and why the fallback was triggered. From the consumer's perspective, the notification either arrived or it didn't, with no visibility into the delivery path. We added a delivery trace endpoint in v1.1 that exposed per-notification channel attempt history. It resolved the observability gap, but it should have been in v1.0.

## What I'd Do Differently

The dependency on preference migration (Decision 1) needed a concrete migration plan and timeline before the API launched, not after. Announcing that two teams needed to migrate preference logic as part of adoption is a different conversation than showing up with a migration path, tooling, and a timeline.

The documentation for delivery guarantees (Decision 2) should have been surfaced in the onboarding flow, not buried in the reference documentation. The teams who needed it most were the ones who integrated quickly and didn't read the reference docs first.

The delivery trace endpoint (Decision 3) should have shipped with v1.0. Observability gaps in a notifications API create support volume that's hard to resolve without that data — and the support volume arrives immediately after launch, not later.

The documentation release should have included working examples for every consuming team's primary use case before the API went live. Letting teams discover edge cases in production costs more than writing one more example.
