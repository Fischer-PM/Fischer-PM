# PagerDuty: The Product You Hate That You Can't Remove

PagerDuty built a product that engineers hate to be paged by and can't stop relying on. That tension is the business.

Most enterprise software wins by being pleasant to use. PagerDuty wins by being essential at the worst possible moment. An engineer woken at 3am by a PagerDuty alert is not a happy customer — but they are a deeply embedded one. The product's value is not about experience. It's about presence at the moment when something must not fail.

## What They Actually Built

**Landing on the critical path.** On-call routing for incidents is not a peripheral workflow. When a database goes down, when a payment service starts returning errors, when a customer-facing API degrades — PagerDuty is the system that determines who gets woken up and when. That is not optional once adopted. It is the product that gets blamed when things go wrong and ignored when they go right. Being on the critical path is not the same as being in the critical path — it means removal has consequences that show up immediately and visibly. That's a different kind of switching cost than "we'd have to migrate our data."

**Integrations as moat.** PagerDuty connects to monitoring tools, logging systems, deployment pipelines, and ticketing systems. The typical mid-sized engineering org has a dozen or more integrations configured. Every alert that routes through PagerDuty is a data source pointed at a specific endpoint. Switching to an alternative means re-pointing every integration, re-mapping every routing rule, and re-validating that the replacement handles every edge case the team has spent years configuring around. The integrations aren't features — they're anchors.

**Escalation policies as organizational knowledge.** Over time, PagerDuty accumulates something more valuable than configuration: institutional memory. The escalation policy that says "if the payment service pages and the on-call engineer doesn't acknowledge in 5 minutes, page the payments team lead, then the VP of Engineering" encodes years of organizational decisions about ownership, priority, and accountability. That knowledge doesn't export cleanly. A company migrating off PagerDuty isn't just moving software — they're rebuilding an org chart that exists inside a tool.

**Pricing per user aligned with org growth.** As companies scale, headcount grows, on-call rotations expand, and PagerDuty billing scales with them. This is a favorable dynamic for a vendor: success for the customer means more seats, which means more revenue. The alignment isn't as clean as Stripe's percentage-of-transaction model, but it's still directionally correct — a growing company is a good PagerDuty customer, and PagerDuty has an incentive to help customers grow.

## The Growth Mechanism

One team starts using PagerDuty for on-call routing. Other teams get paged through it when incidents cross service boundaries. Incident response becomes a company-wide process that flows through PagerDuty. Postmortems reference PagerDuty incident timelines. New engineers join and learn PagerDuty as the system of record for how the company handles operational accountability. By the time anyone evaluates alternatives, PagerDuty is not just a tool — it's the language the company uses to talk about incidents. Replacing it requires not just a new tool but a new shared vocabulary.

## What They Sacrifice

The UX is optimized for 3am urgency, not daily usability. PagerDuty's interface reflects a product built around an emergency mode — high-stakes, time-pressured, unambiguous. That design philosophy serves the core use case well and the daily administrative use case poorly. Configuring escalation policies, managing on-call schedules, and reviewing reliability metrics are all operations that happen when the system is working. They don't get the same product investment as the alert flow. This creates real friction in workflows adjacent to the core product — postmortem management, reliability tracking, service ownership — where PagerDuty has expanded but where the product quality is inconsistent.

## Where They're Exposed

Grafana OnCall and open-source alternatives are compelling for engineering-led organizations that are comfortable owning infrastructure. A team running their own Prometheus stack is a team that has already internalized the ops burden — PagerDuty's value proposition of "managed reliability tooling" is less persuasive when they're managing everything else. These orgs can configure an open-source alternative and accept the maintenance cost as a line item that's still cheaper than PagerDuty at scale.

At the top of the market, Microsoft and ServiceNow compete in ITSM buying cycles where PagerDuty's developer-led positioning is a disadvantage. Enterprise IT buyers who start from a ServiceNow relationship don't have to evaluate PagerDuty on engineering-team merit — they can consolidate incident management into an existing vendor they already trust and already have a contract with.

## The PM Lesson

The highest-value PM insight in incident management is not "reduce alert noise" — it's "become the system of record before someone notices you're optional." PagerDuty landed on the critical path early and made switching expensive by accumulating organizational knowledge, not just technical integration. The escalation policy that encodes your org structure is harder to migrate than the webhook that points at your endpoint.

For any platform or API PM: the most durable embedded position is the one where your product holds information that doesn't exist anywhere else. If your product can be replaced by pointing a configuration at a different endpoint, you're a commodity. If replacing your product means reconstructing decisions that were made over years and live nowhere else, you're essential. Build toward the latter — not by locking data, but by being the place where meaningful organizational decisions get recorded.
