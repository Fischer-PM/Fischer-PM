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

---

## Guiding Perspective

Platform PMs live at the intersection of two conflicting imperatives: move fast for the business, maintain contracts for the consumers. These two goals are not naturally compatible, and anyone who tells you otherwise is probably optimizing for only one of them. The business wants new capabilities shipped quickly, experiments run cheaply, and infrastructure costs minimized. Consumers — the engineering teams, product teams, and external partners building on your platform — want stability, predictability, and the assurance that what works today will still work next quarter. The platform PM's job is not to pick a side. It is to make the tension visible, price it honestly, and ensure that every shortcut taken in the name of speed has a named owner and a known due date. These artifacts reflect that operating principle. They are not templates for consensus — they are tools for making hard calls faster and defending those calls with evidence.
