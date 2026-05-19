# Migration Communication Template

The same deprecation announcement lands differently depending on who's reading it. Engineers want dates and endpoints. Product leads want impact and alternatives. Leadership wants risk and cost.

Sending the same message to all three audiences is one of the most reliable ways to make a migration more painful than it needs to be. Engineers who receive an executive-summary-level announcement don't know what to do. Executives who receive a technical rundown don't know why it was sent to them. The communication isn't just a formality — it's the first signal to each audience about whether the platform team understands their actual concerns.

What follows is a template for communicating a single deprecation to three distinct audiences, written from the perspective of a messaging API migration at a platform operating at scale.

---

## To Engineering Partners

**Subject: [ACTION REQUIRED] Messaging API v2 deprecation — migration path and timeline**

The Messaging API v2 endpoint (`/v2/messages/send`) will reach end-of-support on [DATE — 16 weeks from this notice]. After that date, the endpoint will return `410 Gone` for all requests.

**What's changing:** All traffic must migrate to the v3 endpoint (`/v3/messages/dispatch`). The request schema is documented at [internal link]. Key differences: the `recipient_id` field is now `recipient_ref`, and batch requests support up to 500 messages per call instead of 250.

**Migration path:** A migration guide with before/after examples is at [internal link]. A dedicated integration environment is available at [environment URL] through [DATE]. If you need help with edge cases — rate limiting behavior, error handling for carrier failures, retry logic — reach out to [Slack channel] or file a ticket in [queue].

**What breaks if you don't migrate:** Starting [DATE], any service still calling `/v2/messages/send` will receive `410` errors. Depending on your error handling, this may surface as silent failures, user-facing errors, or downstream queue backlog. We have mapped your current traffic volume and can share projected impact on request.

**Questions:** [Slack channel] is monitored through the end of the migration window. Platform team is available for a 30-minute technical review session if your integration has non-standard requirements — book via [link].

---

## To Product Leadership

**Subject: Messaging API migration — what it means for your product area**

We are migrating the internal messaging infrastructure from API v2 to v3 over the next 16 weeks. This is a planned upgrade, not an incident response.

**Capability affected:** Outbound messaging — notifications, confirmations, and transactional messages sent to end users. The underlying messaging capability is not changing. The technical contract that engineering teams use to invoke it is being updated.

**User impact:** None expected. The migration is designed to be transparent to end users. If a team in your product area delays their migration past [DATE], they may experience message delivery failures until they complete the migration. We have identified the engineering teams in your area that need to act and have sent them technical instructions directly.

**What I need from you:** Nothing, unless one of your engineering teams flags a conflict with an upcoming launch that falls inside the migration window. If that happens, contact me directly and we will work out the sequencing. The migration window was set with 16 weeks of runway to accommodate most sprint cycles.

**Timeline:** Migration window opens now. End-of-support for v2: [DATE]. Migration window closes [DATE + 2 weeks] to allow for any final cleanup.

---

## To Executive Leadership

The platform team is retiring the v2 messaging API and migrating to v3 over the next 16 weeks. The v2 endpoint processes approximately 340M messages per month and serves 4 active internal consumers. The v3 replacement has been in production validation for 8 weeks and meets or exceeds all existing SLA commitments. If consuming teams do not migrate by [DATE], they will experience delivery failures until migration is complete. The platform team has identified all affected consumers, provided migration documentation, and staffed a support channel for the duration. No action is needed from this group unless a team escalates a timeline conflict.

---

## What Not to Put in a Deprecation Announcement

**Background history.** No one needs to know that v2 was originally built as a stopgap in 2019 or that v1 was deprecated three years ago. History is noise in a migration announcement. It signals uncertainty rather than confidence.

**Blame.** If v2 accumulated technical debt because of decisions made under pressure, that context belongs in an internal retrospective, not in a communication to the teams who now have to migrate. Migration announcements that include context about why the old system was flawed put consumers in the position of relitigating decisions they had no part in making.

**Apologies.** An apology in a deprecation announcement suggests the decision is negotiable or that the timeline is flexible because someone feels bad about it. Neither is helpful. If the timeline is flexible, say so with specifics. If it isn't, don't signal that it might be by hedging with regret.

A migration announcement should communicate exactly what is changing, when, and what the consumer needs to do. Everything else is distraction.
