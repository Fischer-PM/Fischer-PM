# When to Unify Channels vs. Keep Them Separate

The appeal of a unified omnichannel platform is real — one API, one preference model, one delivery contract. The cost is equally real. Most teams that build unified platforms underestimate how different SMS, email, push, and in-app are at the infrastructure level, and overestimate how much unification benefits end users.

I've seen this go wrong in both directions: teams that built rigid unified abstractions and couldn't add a new channel without six weeks of schema migration, and teams that kept every channel as an isolated silo and had no way to enforce cross-channel consent or suppression. The answer is not "unify everything" or "keep everything separate" — it's knowing which layer to unify and which to leave alone.

---

## The Forcing Questions

Before committing to a unified abstraction, I ask three questions. The answers usually tell you whether unification is helping you or creating complexity you'll spend years working around.

**Can you express all channels in a shared message model?**

SMS has a 160-character body limit for GSM-7 encoded messages and stricter limits for Unicode. Email supports HTML, attachments, multi-part MIME bodies, and has no practical length ceiling. Push notifications have OS-imposed payload size limits — Apple Push Notification service enforces 4KB; FCM has its own constraints — and the payload structure differs between iOS and Android. In-app notifications require an active user session to display; they don't deliver to idle users the way SMS and push do.

A shared message model that handles all of these honestly ends up with so many optional, channel-specific fields that it's no longer a model — it's a schema with a lot of nullable columns. That's not unification; it's a leaky abstraction with extra steps.

**Do channels share delivery contracts?**

SMS delivery status comes from carrier delivery reports, which are asynchronous, carrier-specific, and sometimes missing entirely. Email delivery is tracked through open events, bounce codes (hard and soft), and complaint events from ISPs — none of which have standardized timing. Push delivery depends on device token validity, OS-level delivery confirmation, and whether the device was online when the message was sent. In-app delivery is conditioned entirely on session presence: if the user isn't in the app, there's no delivery event at all.

These failure modes don't overlap. A retry strategy that works for SMS (resend if no carrier delivery receipt within 5 minutes) is wrong for in-app (there's nothing to retry if the session ended). Encoding these into a single delivery contract requires so many carve-outs that the contract stops being meaningful.

**Do channels share failure modes?**

They don't. Carrier rejection, email domain blacklisting, push token expiry, and in-app session timeout are four distinct failure categories with different detection methods, different remediation paths, and different ownership. Routing them through a unified failure handling layer usually means the unified layer handles none of them well.

---

## Where a Unified Abstraction Helps

The places where channel-agnostic logic genuinely belongs in a shared layer:

- **User preference management**: whether a user prefers push over SMS is a routing decision, not a channel-specific decision
- **Consent and opt-out handling**: a suppression list should span channels; a user who opts out of marketing messages shouldn't receive them via SMS or email or push
- **Rate limiting across channels**: if a user's message frequency cap applies across all channels, that logic has to live somewhere shared
- **Cross-channel deduplication**: suppressing a message a user already received via email from also being sent via push is a shared concern

These are the right things to unify. They don't care what channel delivers the message, so they don't inherit any channel's constraints.

---

## When Unification Becomes Leaky

The abstraction starts leaking when channel-specific failure handling needs to change the shared layer's behavior. When SMS retry logic needs a different backoff curve than email bounce handling. When a new channel's SLA commitment doesn't fit the single latency target the unified contract expresses. When adding WhatsApp or RCS as a new channel requires a schema migration that touches existing consumers' API contracts.

At that point, the unified abstraction is no longer reducing complexity — it's distributing complexity to every team that depends on it.

---

## How to Add a New Channel Safely

Treat a new channel as a new service that implements the same interface contract, not as an extension of an existing channel's code. The shared API surface should be stable; the channel-specific implementation behind it should be isolated.

Before a new channel launches, I define its SLA separately: delivery rate targets, latency windows, failure mode classification, and monitoring ownership. Not after launch, when the defaults are already set and changing them is a negotiation. The channel-specific SLA goes into documentation before the first consumer onboards.

---

## The Product Test for Channel Expansion

"We should support X channel" is a valid product input that needs a delivery contract attached to it. It's true when there is demonstrated user need — not assumed need — and when you can make and keep a delivery commitment for that channel. It is not true when a stakeholder wants to use a trending channel because a competitor announced it, or because it tests well in a survey.

I've held this line more than once. The channels that get added because of genuine user need and a defensible SLA get maintained and improved. The channels added because of stakeholder enthusiasm and no delivery contract become the ones that generate the most support load and the most complaints when they underperform.
