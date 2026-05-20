**Note: This is a simulated case study. The company, product, and events are fictional.**

# The AI Feature That Shipped Too Early

**Company: Vela** (enterprise operations platform)

---

## Situation

Vela's product team shipped an AI-generated incident summary feature after eight weeks of development. The feature was designed to automatically generate a narrative summary of an incident — timeline, contributing factors, affected systems, responsible teams — from the structured data already logged in Vela's incident management module.

Internal testing showed summaries were accurate 87% of the time on the test set. The model performed well on the incidents engineering had used to develop and tune it. Product leadership pushed to ship — the market window for AI differentiation felt narrow, competitors were announcing similar features, and eight weeks of work had produced something that looked genuinely useful.

I flagged the eval set concern in the pre-launch review. The concern was noted and the ship decision held.

---

## Constraint

The eval set was built entirely from internal incidents — Vela's own engineering incidents, which the team had access to and had used throughout development. Internal incidents had predictable structures: short timelines, two or three participants, a single system failure with a clear resolution sequence.

Customer incidents were different in ways I knew abstractly but hadn't quantified: longer timelines, more participants, cross-system dependencies, organizational complexity that internal incidents didn't have. The model had never been evaluated against customer data before launch. Doing that evaluation properly would have taken time we felt we didn't have.

The constraint was real: a rigorous eval on customer data required anonymizing a representative sample, running the model against it, and having subject-matter reviewers assess the outputs. That was a week of coordinated work at minimum.

---

## Decision

Shipped to 15% of accounts behind a feature flag. Monitored for qualitative feedback via support tickets. No automated eval running against production outputs — we'd watch the tickets and respond to what surfaced.

The implicit logic: if something is badly wrong, customers will tell us. If the ticket volume is low, the feature is probably fine.

What I sacrificed: the ability to detect systematic failure modes before customers encountered them. A support ticket monitor only catches failures that customers notice, can articulate, and choose to report. It misses everything else.

---

## What Broke

Two weeks after launch, a customer escalated. Their incident summary had attributed the outage to the wrong team.

The model had identified a pattern match — the incident data contained structural similarities to a past incident Vela had seen from this customer. It generated a plausible-sounding summary that named a specific team as the root cause. The summary was wrong. The actual cause was a configuration issue in a different system, handled by a different team.

The customer had forwarded the summary to their executive team before reviewing it. By the time they caught the error, the summary had already been used in an internal postmortem meeting. The customer had to send a correction. They were not pleased.

The failure mode was exactly what I'd been worried about before launch: the model's pattern-matching behavior, which worked well on predictable internal incidents, was generating confident-sounding output on complex customer incidents where the patterns didn't hold.

---

## What Changed

Feature flag rolled back to 5% of accounts — the smallest cohort, limited to customers who had opted in explicitly.

Automated evals were added using anonymized customer incident data. We pulled 200 real incidents with known outcomes, ran the model against them, and had two reviewers assess accuracy. The eval results confirmed the pattern: accuracy on simple incidents was 89%, close to what internal testing had shown. Accuracy on multi-team incidents with complex timelines was 61%. The model was producing confident wrong answers on exactly the cases where wrong answers caused the most damage.

Human review was added as a required step for any summary touching a multi-team incident before it was surfaced to the customer.

The relaunch six weeks later included a confidence score in the UI — "high confidence" or "review recommended" — calculated from incident complexity signals. Customers could see when the model was uncertain before acting on the output.

---

## What I'd Do Differently

The 87% accuracy number was real. It was measured on the wrong data.

Before launch, I needed one week of evaluation against production-like data. Not a full test set — 50 real customer incidents reviewed by two people would have been enough to surface the multi-team failure mode. That's a calibration exercise, not a research project. It would have changed the ship decision or changed the feature design before the ship decision was made.

The pressure to ship was genuine. Competitors were moving. The market window felt narrow and the argument was credible. But the cost of shipping the feature wrong wasn't a delayed launch — it was an enterprise customer sending a correction email to their executive team and a feature rollback. That's a worse outcome than shipping two weeks later with a confidence score and a scoped rollout.

I knew the eval set was wrong before we shipped. I raised it. I didn't push hard enough on what it would take to fix it, and I didn't make the cost of being wrong concrete enough to change the decision. "Our eval set may not represent customer data" is easy to wave away. "Here's what happens if the model generates a confident wrong answer in a multi-team incident" is harder to wave away. I led with the first and should have led with the second.
