# When Your LLM Provider Changes the Model Without Telling You

*Simulated failure analysis — fictional product (Fulcrum), representative of real patterns in LLM-dependent production systems.*

---

The contract said "GPT-4." The API still said "GPT-4." The model behavior changed materially anyway.

---

## What Happened

Fulcrum was an AI writing assistant for B2B sales teams. It drafted follow-up emails, summarized call notes, and generated proposal language from bullet points provided by the rep. The product had been in production for seven months with stable quality metrics: user editing rate (how often a user substantially rewrote Fulcrum's output), adoption rate, and CS ticket volume for quality complaints.

In month eight, without any deployment on Fulcrum's end, three things changed within a two-week window:

**Output verbosity increased.** Fulcrum's email drafts got longer. The average draft had been 3-4 short paragraphs; it became 5-6. Users were editing more to shorten outputs.

**Refusal rate increased.** Fulcrum had a feature for generating aggressive competitive positioning ("our product does X, competitor does not"). The model began occasionally declining to generate comparative claims, citing potential inaccuracy. Users expected the feature to work; support tickets flagged it as broken.

**Tone shifted.** The outputs became more formal. Sales reps writing to SMB customers described the change as "sounds like a lawyer wrote it."

None of this was caused by any change in Fulcrum's codebase. The prompts hadn't changed. The API version hadn't changed. The provider had silently updated the model behind the same API endpoint.

---

## What the Provider Contract Actually Said

"GPT-4" is a model family identifier, not a version pin. The provider's documentation, if you read it carefully, described ongoing improvements to the model and noted that behavior could change as improvements were made. "Improvements" is doing significant work in that sentence — from the provider's perspective, a higher refusal rate on potentially inaccurate claims is an improvement. From Fulcrum's perspective, it broke a customer-facing feature.

The option to pin to a specific model version existed. It wasn't used. The assumption was that "GPT-4" was stable and that changes would be backward-compatible. It wasn't an unreasonable assumption. It was wrong.

---

## What the PM Team Missed

**No behavioral baseline was tracked.** Fulcrum had quality metrics (editing rate, CSAT, CS volume). It did not have behavioral metrics: average output length, refusal rate per prompt type, tone distribution across outputs. When behavior changed, the first signal was user editing rate ticking up — a lagging outcome metric. A behavioral baseline would have surfaced the change within days of the model update.

**No eval suite captured the specific behaviors that mattered.** The team had a manual QA process: review a sample of outputs weekly and rate them. This caught obvious regressions but was too slow to detect subtle behavioral drift and too subjective to catch tone shifts. A structured eval suite — test prompts with expected output characteristics — would have run continuously and flagged the verbosity and tone changes automatically.

**Provider dependency was treated as infrastructure, not product risk.** The assumption was that the LLM provider relationship was like an AWS service: it does what it says it does, the API is the contract, and changes are managed through versioning. That assumption doesn't hold for LLM providers. Model behavior is not specified in a schema; it emerges from training, and training changes. The provider is not managing backward compatibility the way an infrastructure provider manages API versioning.

---

## What Recovery Required

The immediate fix was pinning to a specific model version. This required identifying which model version had been active before the behavior change (the provider's status page had the deployment history) and configuring the API call to specify that version. This stabilized behavior within 24 hours of identifying the root cause.

The harder work was rebuilding the monitoring infrastructure so this couldn't happen silently again.

**Behavioral evals.** The team built a set of 200 test prompts covering each major use case: email drafts, call summaries, proposal language, competitive positioning. Each test prompt had expected output characteristics: length range, tone classification (formal vs. casual), required content (must include a CTA), prohibited content (must not include a refusal for competitive positioning prompts). The eval ran nightly against the production model configuration. Any test that began failing was treated as a potential model change.

**Version monitoring.** The team added a canary request: a fixed prompt sent once per hour to the API, with the response logged and characterized. When the canary response changed in detectable ways (length, tone, content), it triggered a review. This was not a perfect detector but it was a faster signal than user editing rate.

**Provider change management.** The team established a relationship with the provider's enterprise account team and requested advance notice of planned model updates. This improved the situation but didn't fully solve it — not all model updates were planned or communicated.

---

## The Structural Problem

The underlying tension is that LLM providers' incentives are to improve model quality on aggregate benchmarks, not to preserve the specific behavioral characteristics of any individual application. A model update that scores higher on safety benchmarks and instruction-following evals is, from the provider's perspective, a better model. From a B2B SaaS application's perspective, it might be a breaking change.

This is not a solvable problem through monitoring alone. It requires treating model selection and version pinning as a deliberate product decision — one with a maintenance cost (you eventually have to upgrade when the pinned version is deprecated) and a risk profile that needs to be owned explicitly.

The PM who assumes the LLM provider is managing behavioral stability is offloading a product risk they don't know they're taking.
