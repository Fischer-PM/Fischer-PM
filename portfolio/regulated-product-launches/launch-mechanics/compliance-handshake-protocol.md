# The PM-to-Legal Handshake Protocol

Involving legal too early generates opinions on things that will change. Involving them too late generates blockers two weeks before go-live. The protocol is about timing the right conversation at the right stage.

This isn't about managing legal — it's about using the engagement productively. Legal's value is precise, not broad. A premature conversation produces a general impression of comfort or discomfort that evaporates when the design changes. A well-timed conversation produces a documented position on a specific implementation that can be relied on.

---

## The Right Moments

Three stages warrant formal legal engagement: when the data handling design is finalized, when the pilot scope is being defined, and when the go-live checklist is being drafted.

**Data handling design finalized.** This is the first moment where legal can give a useful answer. Before the data model is settled, questions about what data is collected, how it's stored, and who can access it are hypothetical. Legal's answer to a hypothetical is a hypothetical. Wait until the design is real enough to review.

**Pilot scope definition.** The pilot is where the product first touches live customers. Legal needs to review the scope — which segment, what volume, what features — before it's set, not after. This is also the moment to document the regulatory framing for the pilot: what standard the pilot is being held to and how compliance will be demonstrated.

**Go-live checklist draft.** The final formal review. At this point, the product design is stable, the pilot results are available, and legal is reviewing the specific implementation against the specific regulatory requirement. This is where documented sign-off is generated.

Do not involve legal at 30% wireframes, during scope discussions that are still in flux, or for general comfort checks. You will get a response, but it won't be actionable, and you will have spent goodwill on a conversation that has to happen again later.

---

## How to Write a Brief for Legal

One page. Four sections. Send it before any meeting — minimum 48 hours in advance.

**What the product does.** Two to three sentences describing the product's function and the customer interaction. No technical jargon. Legal reads this to understand what they're evaluating.

**What data it handles.** Specific: what data types are collected, how they're stored, what the retention policy is, who has access. This is the section legal actually needs. If you send a PRD instead of a brief, legal will spend the meeting extracting this information rather than reviewing it.

**What the regulatory concern is.** Identify the applicable regulation or regulatory domain. If there are multiple, identify the primary one and note the others. Do not assume legal knows which regulation applies to this product — state it.

**What you are asking them to review and by when.** Be explicit about the question. "Does this data handling design satisfy the requirements of [applicable regulation]?" is a reviewable question. "Does this look okay?" is not. Include a response deadline.

---

## What Legal Actually Needs vs. What They Ask For

Legal often asks for the full specification when what they need is the data model. They ask for the complete consent flow when what they need is the specific language the user sees. Give them what they need, not what they ask for — and explain the difference when you send it.

This is not about managing legal; it's about getting a useful answer. A legal team reviewing 80 pages of PRD will produce feedback on UI decisions, feature scope, and implementation details that are not their domain. A legal team reviewing the data model and the consent language will produce feedback on the data model and the consent language, which is the feedback that matters.

When you send the brief, note: "I've attached the data model and consent flow for your review. The full product specification is available if you need it, but I've pulled the sections most relevant to the regulatory question." That framing focuses the review and signals that you've done the work of identifying what matters.

---

## Handling Conflicting Guidance from Different Legal Stakeholders

BSA counsel, product counsel, and privacy counsel sometimes give contradictory direction on the same product. This is more common than it should be and more common than teams plan for.

The protocol: escalate early, document the conflict in writing, and do not proceed without resolution. Moving forward with ambiguous guidance — picking the most permissive interpretation because it's convenient — is worse than the delay required to resolve the conflict. If the product is later questioned, "legal gave us conflicting guidance and we picked the one that worked" is not a defensible position.

The escalation should be a written memo to the relevant legal leads: here is the question, here are the two positions I've received, here is the decision I need to make and by when. Put the conflict in writing so it can be resolved in writing.

---

## When Legal Says "We Need More Time" Two Weeks Before Launch

"We need more time" is not a deliverable. Get specific.

Ask three questions: What specifically do you need time to review? What is the specific question you're trying to answer? When will you have an answer?

If legal can't answer those questions, the issue is usually one of two things: they received the review request too late and are doing real work under time pressure, or they received a review request that wasn't scoped precisely enough to answer. Both are PM failures in process design.

If the review request was properly timed and scoped and legal still cannot produce an answer in time, that is a go/no-go decision for the business — not an automatic delay. Escalate the constraint with the specific question, the specific date needed, and the business impact of the delay. Let the right stakeholder make the call with full information.
