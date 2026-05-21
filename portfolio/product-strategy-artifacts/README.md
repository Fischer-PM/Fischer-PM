Working strategy documents demonstrating senior PM thinking on prioritization, roadmap communication, and the product decisions that don't have clean answers.

These artifacts were developed across platform PM work in infrastructure product environments supporting developer tooling, API platforms, and internal systems at scale.

---

## Table of Contents

**Prioritization**
- [Prioritization Under Constraint](./prioritization/prioritization-under-constraint.md)
- [Technical Debt Is a Product Decision](./prioritization/technical-debt-as-product-decision.md)
- [Saying No Without Losing the Room](./prioritization/saying-no-without-losing-the-room.md)

**Roadmap Communication**
- [Executive Roadmap Memo Template](./roadmap-communication/executive-roadmap-memo-template.md)

**Product Thinking**
- [The Platform-Product Tension Nobody Talks About Honestly](./product-thinking/platform-vs-product-tension.md)
- [Eigenquestions: High-Leverage Strategy Questions Grounded in Rumelt](./product-thinking/eigenquestions.md)

**Product Teardowns**
- [Stripe](./teardowns/stripe.md) — How seven lines of code became a payment moat
- [Twilio](./teardowns/twilio.md) — Why the adoption unit and the buying unit being different was the whole strategy
- [Linear](./teardowns/linear.md) — How refusing to build most of Jira became a competitive position
- [PagerDuty](./teardowns/pagerduty.md) — How to build a product engineers hate to be paged by and can't stop depending on
- [Datadog](./teardowns/datadog.md) — Platform strategy as a sequencing problem, not a vision problem

**Case Studies** *(simulated)*
- [API Deprecation Failure](./case-studies/api-deprecation-failure.md) — When silence from API consumers is treated as confirmation, and what breaks
- [Notification System That Didn't Scale](./case-studies/notification-system-scaling.md) — A throttling fix that inherited a broken classification layer
- [Self-Serve Onboarding Debt](./case-studies/self-serve-onboarding-debt.md) — 68% completion rate masking 6x ticket volume growth
- [AI Feature Shipped Too Early](./case-studies/ai-feature-that-shipped-too-early.md) — 87% accuracy on the wrong dataset, and what it cost
- [Buyer-User Mismatch](./case-studies/internal-tool-buyer-user-mismatch.md) — +42 NPS from users, three enterprise non-renewals from buyers
- [Marketplace Liquidity Collapse](./case-studies/marketplace-liquidity-collapse.md) — Simulated: removing a supply-side subsidy that had silently become a retention mechanism
- [Notification Fatigue Campaign](./case-studies/notification-fatigue-campaign.md) — Simulated: re-engagement that worked for 3 weeks and destroyed the channel
- [The Activation Paradox](./case-studies/activation-paradox.md) — Simulated: shipping the top feature request and watching activation drop 14%

**Feature Analyses** *(real companies, public information)*
- [Netflix Password Sharing Crackdown](./feature-analyses/netflix-password-sharing-crackdown.md) — How a tolerated behavior became a subscriber growth lever, and why timing mattered
- [Duolingo Streak Mechanics](./feature-analyses/duolingo-streak-mechanics.md) — When a retention mechanic becomes the product, and what that costs long-term
- [Shopify's Shop App](./feature-analyses/shopify-shop-app.md) — Why a B2B infrastructure company built a consumer product
- [Spotify Discover Weekly](./feature-analyses/spotify-discover-weekly.md) — Algorithmic discovery as a label relationship problem
- [Twitter/X Community Notes](./feature-analyses/twitter-community-notes.md) — Crowdsourced fact-checking as platform governance strategy

**Architecture Reviews**
- [Slack](./architecture-reviews/slack-architecture.md) — Why the channel model works at 50 people and degrades at 5,000
- [Stripe](./architecture-reviews/stripe-payment-pipeline.md) — Idempotency as a product constraint, not an engineering choice
- [Twilio](./architecture-reviews/twilio-carrier-abstraction.md) — Why "delivered" is a probabilistic signal, not a guarantee
- [Kafka](./architecture-reviews/kafka-event-streaming.md) — Consumer-managed offsets and what that implies for product decisions
- [Notion](./architecture-reviews/notion-block-model.md) — Block-based architecture optimized for expressiveness, not governance

**Glossary**
- [Product Management Glossary](./glossary/product-glossary.md) — 40+ terms defined precisely, each with a "common misuse" callout

---

Product strategy at the senior level is mostly about making good decisions under imperfect information and incomplete authority. The PM who waits for complete information is slow — markets move, windows close, teams sit idle waiting for direction that should have come two weeks ago. The PM who ignores incomplete information is reckless — they commit to the wrong thing with confidence, and the cost is paid by the engineers who build it and the customers who live with it. Everything in this repo lives in that gap: the judgment calls, the forcing questions, the honest tradeoffs, and the communication formats that keep decisions legible to the people who need to act on them.
