# Platform PM Playbook

Opinionated decision frameworks and working artifacts from platform PM work at billions-of-messages scale and 4B+ annual API calls.

My background spans platform product management across large-scale financial services and real estate technology environments, where platform teams served both internal engineering consumers and external partners under production SLA commitments.

---

## Table of Contents

### Deprecation
- [Deprecation Decision Framework](deprecation/deprecation-decision-framework.md) — Four forcing questions before you commit to a sunset
- [Migration Communication Template](deprecation/migration-communication-template.md) — How to announce the same change to engineers, product leads, and executives

### API Governance
- [API Contract Ownership](api-governance/api-contract-ownership.md) — Who owns the schema, what constitutes a breaking change, and what happens when something breaks anyway
- [Platform Health Metrics That Actually Matter](api-governance/metrics-that-matter.md) — Which numbers to track, which to distrust, and one metric almost no one has on their dashboard

### Scalability
- [Protecting the Critical Path](scalability/critical-path-protection.md) — The three moments the critical path is most at risk and how to defend it before the meeting starts
- [SLA Improvement Teardown](scalability/sla-improvement-teardown.md) — Four categories of SLA degradation and why misidentifying the type is the most common failure mode

### Architecture Decision Records *(simulated)*
- [ADR-001: Async Queues Over Synchronous APIs](adrs/adr-001-async-queues-over-sync-apis.md) — How replacing a synchronous service chain with SQS queues stopped cascade failures (and what the team got wrong about monitoring)
- [ADR-002: Kafka for Fanout, SQS for Delivery](adrs/adr-002-kafka-vs-sqs-notification-fanout.md) — When and why to split notification infrastructure across two queue systems, with architecture diagrams
- [ADR-003: Centralizing Notifications Across 7 Products](adrs/adr-003-centralized-notification-service.md) — The compliance win, the blast radius problem, and why edge cases are where the requirements actually live
- [ADR-004: Eventual Consistency for User Preferences](adrs/adr-004-eventual-consistency-user-preferences.md) — Why "eventual" needs a defined upper bound, and what happens when propagation stops silently

### Postmortems
- [API Migration Postmortem](postmortems/api-migration-postmortem.md) — Simulated: a v1 deprecation that broke three enterprise consumers on cutoff day, and what the process failed to catch

### Glossary
- [AWS Services: A PM Reference](glossary/aws-glossary.md) — What each service does, the product problem it solves, and one constraint a PM should know before it's in production
- [Architecture Concepts: A PM Reference](glossary/architecture-glossary.md) — 35+ distributed systems terms defined in product language, with common misunderstandings called out

---

## Guiding Perspective

Platform PMs live at the intersection of two conflicting imperatives: move fast for the business, maintain contracts for the consumers. These two goals are not naturally compatible, and anyone who tells you otherwise is probably optimizing for only one of them. The business wants new capabilities shipped quickly, experiments run cheaply, and infrastructure costs minimized. Consumers — the engineering teams, product teams, and external partners building on your platform — want stability, predictability, and the assurance that what works today will still work next quarter. The platform PM's job is not to pick a side. It is to make the tension visible, price it honestly, and ensure that every shortcut taken in the name of speed has a named owner and a known due date. These artifacts reflect that operating principle. They are not templates for consensus — they are tools for making hard calls faster and defending those calls with evidence.
