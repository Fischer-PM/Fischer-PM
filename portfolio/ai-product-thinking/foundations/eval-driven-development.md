# Eval-Driven Development for Product Managers

If you don't define how to evaluate an AI feature before you build it, you won't be able to tell whether it works after you ship it. That's not an engineering problem. That's a PM problem.

This is the piece of AI product development that most PM frameworks skip because it sounds like an ML concern. It isn't. Evals are the mechanism by which you hold the product accountable to what you said it would do. Delegating them to engineering is the same as delegating acceptance criteria to engineering — technically possible, but a sign that the PM hasn't done their job.

## What an Eval Is (for a Non-ML Audience)

An eval is a test that determines whether an AI system is doing what you said it would do. Three distinctions matter for PMs who haven't worked with ML teams before.

Unlike a unit test, an eval measures quality, not correctness. A unit test has a binary pass/fail based on whether code does an exact thing. An eval asks whether a model output is good — which requires defining what "good" means before you run the test. That definition is a PM responsibility.

Unlike an A/B test, an eval doesn't require users. You can run evals on a model before anyone touches the product, using a curated set of inputs designed to cover the scenarios that matter. This means you can catch failure modes before launch rather than discovering them through user complaints.

Unlike a benchmark, an eval is specific to your product. Generic model benchmarks tell you how a model performs on standardized tasks. They tell you nothing about whether the model works for your use case, your users, and your acceptable failure rate.

## Why the PM Owns Eval Criteria (Even When Engineering Owns the Model)

Engineering can determine whether the model outputs a response. Only the PM can determine whether the response was useful. Those are different questions, and conflating them produces evals that are technically correct but measure the wrong thing.

A model that always returns an output passes an engineering eval. If the outputs are confident and wrong half the time, users stop trusting the product within two weeks. The PM who delegated eval design to engineering gets a system that passes all its tests and fails in production. I've seen this happen. It's not because the engineering team was careless — it's because no one told them what "useful" meant in terms specific enough to measure.

The PM also owns the failure mode prioritization. Engineering will write evals that cover the common case because that's what's easiest to test. The PM needs to push on the uncommon cases that matter most — the edge cases where a wrong answer does real damage, the inputs that the model hasn't been tuned for, the scenarios where confident-sounding output is more dangerous than no output at all.

## How to Define Evals Before You Build

Five questions to answer before your first line of code:

**1. What does "correct" look like for this feature?** Not vague — specific. "Summarizes the document accurately" is not an eval criterion. "Returns the three most important action items from a meeting transcript, each under 20 words, without hallucinating details not in the transcript" is a criterion you can test against.

**2. What are the top three failure modes you're worried about?** Name them explicitly. Hallucination? Overconfidence in low-signal inputs? Responses that are technically accurate but unhelpful given the user's actual question? Each failure mode you can name is one you can test for. Each one you can't name will find you in production.

**3. How will you measure user satisfaction — separately from model quality?** User satisfaction is not a proxy for model quality. A user who doesn't know the answer was wrong will rate the experience highly. A user who gets a correct answer delivered in an unusable format will rate it poorly. These are different problems with different solutions, and you need metrics that distinguish them.

**4. What's your latency budget, and is it in the eval?** A model that passes all quality evals but takes eight seconds per response has not passed its evals. Latency is a product requirement. It belongs in the eval suite alongside accuracy and recall — not as an afterthought after the model is already selected.

**5. What's the minimum acceptable score before launch?** This is the question most teams avoid because it forces a conversation about what "good enough" means. Have that conversation before you build. A team that hasn't defined their launch threshold will ship when they're tired of testing, not when the product is ready.

## Four Common Eval Failures

**Precision/recall confusion.** These are two different things and optimizing for one usually hurts the other. Precision measures whether the answers the model gives are correct. Recall measures whether the model gives answers for all the inputs it should. In products where a wrong answer is costly (medical, legal, financial), you want high precision even if that means the model declines to answer sometimes. In products where missing an answer is costly, you optimize for recall. Most teams don't make this choice explicitly, which means they make it implicitly and badly.

**Unmeasured edge cases.** The eval tests the 80% case. The product breaks on the 20% case that matters most — the unusual input, the adversarial user, the context the model wasn't tuned for. An eval suite that only covers common scenarios is an eval suite that will produce a false sense of confidence before launch.

**User satisfaction as a proxy for model quality.** "Users are happy" is not an eval. It's a signal that tells you something is working but doesn't tell you what to fix when something isn't. User satisfaction surveys after AI feature launches often reveal nothing about which model behaviors are responsible for the satisfaction score, which makes them useless as diagnostic tools.

**Latency not in the eval.** I have seen teams select a model based on quality evals, build the product around it, and then discover in load testing that the latency is unacceptable for a synchronous user-facing interaction. The latency budget wasn't in the eval. The model swap two weeks before launch cost three engineering-weeks of rework.

---

You don't need ML expertise to define good evals. You need clarity about what the feature is supposed to do and the discipline to write it down before you start. The PM who hands engineering a launch checklist that doesn't include eval criteria hasn't finished the job. The eval is where the product's promise becomes testable — and testable promises are the only kind worth making.
