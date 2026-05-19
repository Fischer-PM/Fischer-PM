# Human-in-the-Loop Design: Load-Bearing vs. Theatrical

Most AI products have human review in the wrong places. It's not because teams don't value human judgment — it's because they add review to make stakeholders comfortable, not to actually change outcomes.

The distinction matters because theatrical review carries real costs: it slows the product, creates compliance overhead, and — most dangerously — gives everyone involved a false sense that a failure was caught. When the review was never capable of catching the failure, the sense of safety is the problem, not a solution to it.

## The Defining Question

Human review is load-bearing when it can meaningfully alter the output or catch a failure that the model can't catch itself. It's theatrical when the reviewer doesn't have enough context, authority, or time to do anything different from what the model said.

That test sounds simple. In practice, it requires being honest about what reviewers are actually able to do — which means asking hard questions about domain expertise, available time, and authority to change the output. A reviewer who rubber-stamps 95% of outputs in a five-second queue is not providing load-bearing review. They're providing the appearance of oversight while the product ships at model-quality regardless.

## Four Points in an AI Workflow Where the Question Matters Most

**Before generation — human input shaping the prompt or context.** This is almost always load-bearing. The human who provides the input that shapes the AI's context — the brief, the parameters, the constraints — is making decisions that meaningfully change the output space. A well-constructed input is the highest-leverage point of human involvement in most AI workflows. Teams that add review after generation but not before it have the emphasis backwards.

**During generation — real-time interruption.** Rarely practical, and usually theatrical when it exists. The latency and UX cost of a human checkpoint mid-generation is high, and the reviewer's ability to intervene meaningfully is low without seeing the full output. The exception is streaming output with an early-exit mechanism — but that's a UX pattern, not a review mechanism. In most workflows, interrupting generation produces friction without proportional quality improvement.

**After generation, before delivery — human approval of output.** This is where most teams put their review steps, and it's load-bearing only under two conditions: the reviewer has domain expertise to evaluate the output, and the reviewer has authority and time to change it. A legal team reviewing AI-generated contract language before it goes to a client — load-bearing, assuming they read it. A customer success manager approving fifty AI-generated outreach emails in a fifteen-minute window — theatrical, because they can't actually evaluate whether each email is accurate and appropriate in the time they have.

**After delivery — human correction of errors.** Load-bearing for the model's training loop and for future output quality; theatrical for the user who already received the wrong answer. This is an important distinction. Post-delivery correction mechanisms are valuable product features — they improve the system over time. But they should not be described as "human oversight of AI outputs" in the same breath as pre-delivery review, because they don't protect the user who encountered the failure. They prevent the failure from recurring. Those are different promises.

## What Theatrical Review Reveals

When I find theatrical review in a product, it usually means one of two things: the team hasn't built evals robust enough to catch the failure modes they're worried about, or stakeholders required a human checkpoint as a condition of launch and the team added one without asking whether it would actually work.

Both are fixable. Better evals are a PM and engineering problem. Stakeholder conversations about what review actually accomplishes are a PM problem. Keeping theatrical review because it's easier than fixing the underlying issue is how products ship with the appearance of safety rather than the reality of it.

The test for load-bearing review is simple: if removing it wouldn't change the output distribution, it's theatrical. Run the thought experiment on every review step in your workflow. The ones that survive are load-bearing. The ones that don't are candidates for removal — which forces you to do the harder work of building better evals and better models rather than relying on human review to catch what the model misses.

---

Removing theatrical review speeds up the product and — more importantly — forces you to be honest about where the model's failure modes actually live. A team that can't remove a review step without losing confidence in the product hasn't built sufficient confidence in the model. That's a real problem. Adding a reviewer who can't actually evaluate the output is not a solution to it.
