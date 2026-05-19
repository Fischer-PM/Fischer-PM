Reference frameworks and decision artifacts for platform PMs managing omnichannel messaging infrastructure at scale.

Drawn from managing messaging platforms processing billions of messages across SMS, email, push, and in-app channels.

---

## Table of Contents

**Architecture**
- [Delivery Guarantees: At-Least-Once vs. Exactly-Once in Practice](architecture/delivery-guarantee-tradeoffs.md)
- [When to Unify Channels vs. Keep Them Separate](architecture/channel-strategy-decisions.md)

**Operations**
- [A Taxonomy of Message Loss](operations/message-loss-taxonomy.md)
- [Defining SLAs That Are Actually Measurable](operations/sla-definition-playbook.md)

**Strategy**
- [Run-the-Engine Overhead: The Hidden Cost of Scale](strategy/run-the-engine-overhead.md)

---

## Guiding Perspective

Messaging platforms at scale are not primarily a technical problem — they're a contract management problem. The platform makes implicit and explicit delivery contracts with every downstream team and end-user dependent on it. Those contracts exist whether you write them down or not: if a team onboards to your platform expecting 99.9% delivery and you're actually running at 97%, you've made a promise you didn't know you made and broken it before anyone noticed. The PM's job is to define those contracts clearly, measure against them honestly, and renegotiate them openly when something changes. That means writing SLAs in terms consumers can verify themselves, classifying failure modes precisely enough that ownership is unambiguous, and treating a degraded guarantee as a product decision — not just an engineering incident.
