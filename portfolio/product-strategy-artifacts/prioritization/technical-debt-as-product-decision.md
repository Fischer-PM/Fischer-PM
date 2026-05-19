# Technical Debt Is a Product Decision

Technical debt is not an engineering problem that gets escalated to PM when it becomes a roadmap conversation. It is a product decision expressed as an engineering constraint. The PM who treats it as someone else's problem will find it owns them.

This is not a philosophical point. It has practical consequences. When a PM defers to engineering on what debt to carry and when, the result is that debt decisions get made without someone whose job is to weigh velocity, customer impact, and business risk simultaneously. Debt accumulates by default, not by choice. That's a worse outcome than making a deliberate decision to carry it.

---

## How to Evaluate Tech Debt as a Product Risk

The right questions are not engineering questions. They're product questions.

What's the probability this debt slows feature delivery in the next two quarters? Not whether it might — it might. What's the actual likelihood, given what's on the roadmap? If the next three features all touch the same subsystem where the debt lives, the probability is high. If they don't, it may be low enough to carry.

What's the timeline? Debt that will matter in six months needs to be addressed differently than debt that will matter in two years. A two-year horizon is speculative; act on it in planning but don't sacrifice current delivery. A six-month horizon is a roadmap input; it belongs in the next cycle's conversation.

What's the blast radius if it fails? Some debt creates a slow drag on velocity. Some creates a single point of failure that will take down a customer-facing service on a Friday at 5 PM. These are not the same category of risk. The blast radius determines the urgency.

---

## When to Pay It Down, Work Around It, or Escalate

**Pay it down** when the debt is on the critical path for what you need to ship and it's compounding — meaning each sprint you don't address it makes the next sprint harder. The compounding test is important. Non-compounding debt can be deferred. Compounding debt on the critical path is borrowing at a high interest rate.

**Work around it** when the debt is isolated and containable — when you can ship what you need to ship without touching it and the workaround doesn't create new debt in the process. The second condition matters. Workarounds that generate new debt are paying off one loan with another.

**Escalate** when the debt is blocking multiple teams or creating customer-facing risk. At that point it's not a local engineering concern — it's a platform risk with broad impact. Escalation in this context means bringing it to the roadmap conversation as a first-class item with a business case, not as an engineering complaint.

---

## How to Communicate Tech Debt Tradeoffs to Stakeholders Who Don't Want to Hear It

Frame it as a capacity question, not a code quality question. "The codebase needs refactoring" is not a business statement. No one who controls budget has a line item called "refactoring."

"This debt will cost us approximately six weeks of engineering velocity over the next two quarters, which means two features on the roadmap will slip or we'll need to choose which ones" is a business statement. It has a cost, a timeline, and a decision that someone needs to make. That's a conversation a stakeholder can engage with.

The specific number matters less than having one. "Significant velocity drag" is easy to dismiss. A number forces a response.

---

## Three Signs a Tech Debt Situation Has Become a Product Emergency

First: new feature development requires touching the debt to ship. When the path to building something new runs directly through something broken, you can no longer defer. The choice isn't between addressing debt and not addressing debt — it's between addressing it now or not shipping the feature.

Second: the debt is causing customer-facing degradation. Latency creep, increasing error rates, support ticket patterns that trace to the same subsystem — when customers are experiencing the debt, it's no longer a technical concern. It's a product problem.

Third: engineers are routing around the debt in ways that create new debt. When the team starts building scaffolding to avoid touching the problem area, the debt is spreading. The original problem plus the workarounds will cost more to address than the original problem alone would have.

---

## What to Ask Engineering During Planning

"What debt are we creating with this decision, and when will it need to be addressed?"

This question changes the conversation before the sprint starts, not after. It makes debt creation a conscious choice rather than a side effect, and it forces the team to commit to a timeline for addressing it. A decision made with eyes open — "we're taking on debt here and we'll address it in Q3" — is categorically different from debt that accumulates without anyone choosing it.

Ask it every cycle. The answers will vary. The habit of asking is what matters.
