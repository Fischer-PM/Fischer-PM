# Compressing a Week-Long Process to Under 20 Minutes: A KYC/CDD Teardown

*This is a thought exercise based on structural patterns common across KYC/CDD information collection processes. The math is real; the specifics are generalized.*

The typical KYC/CDD information collection process takes five to seven business days — not because the regulation requires it, but because the product was built around the process the compliance team already had, not around what the regulation actually required.

That distinction is doing a lot of work. Most KYC/CDD timelines are inherited from paper-era workflows that were digitized without being redesigned. The form got an online version. The review steps stayed sequential. The back-and-forth clarification cycle moved to email. Nothing structurally changed, so the timeline didn't change either. The regulation was not the binding constraint. The product design was.

---

## Why Week-Long Timelines Persist

These are structural causes, not organizational laziness.

**Open-form data collection with no inline validation.** When a user submits a form with no guidance on what constitutes a sufficient response, the reviewer has to interpret what they received, determine whether it meets the standard, and send a clarification request if it doesn't. That cycle — submission, review, clarification, resubmission — takes days by itself, and it repeats for every field that doesn't meet the standard. The user isn't slow; the form is uninstructive.

**Sequential review steps that could run in parallel.** Identity verification, beneficial ownership collection, and risk tier assignment are frequently run in sequence because that's how the paper process worked. In a digital product, they don't have to be. Some of these steps have no dependency on each other. Running them sequentially is a process artifact, not a regulatory requirement.

**Collecting information the regulation doesn't require.** Compliance teams building the original process often added fields "to be safe" — ownership thresholds lower than required, additional beneficial owners outside the regulatory definition, supplemental documentation that no rule specifies. Over time, no one audited the original scope against the actual regulation. The form grew. The timeline grew with it.

**No guidance for the user on what counts as sufficient documentation.** If the user doesn't know whether a screenshot of a state ID meets the standard, they'll submit one and wait. If the submission doesn't meet the standard, they'll receive a rejection and submit again. Real-time guidance — "this document type is accepted," "this image resolution is insufficient" — eliminates the ambiguity that drives most resubmission cycles.

---

## Three Decisions That Enable Compression to Under 20 Minutes

**Decision 1: Scope reduction.**

Audit which data fields the regulation actually requires versus which were added "to be safe." In most KYC/CDD processes, 20–40% of collected information is not required by the applicable regulation. It was added by a compliance team that was being cautious, and it has never been revisited.

Removing non-required fields eliminates collection time directly. It also eliminates clarification cycles that occur when users don't understand why they're being asked for something — because they're often right to be confused.

The tradeoff is real: this requires legal sign-off on what's truly required versus what's policy preference. Some teams find that conversation harder than building the form. It surfaces disagreements between legal and compliance about where the regulatory floor actually sits. But that conversation is worth having explicitly, not avoiding by keeping the over-scoped form.

**Decision 2: Guided UX over open-form collection.**

Replace open text fields with structured inputs, inline validation, and real-time feedback on whether the submission is sufficient before the user clicks submit. This is not a UX nicety — it's the mechanism that eliminates the clarification cycle. If the user knows in real time that their document is acceptable, there is no resubmission loop.

The tradeoff is front-loaded cost: more design and engineering investment before launch. The downstream math is consistent across implementations — structured, validated input reduces support volume by 60–70% relative to open-form collection. The unit economics favor the investment, but the investment has to happen before anyone sees the return.

**Decision 3: Staged validation.**

Identity verification — confirming the person is who they say they are — can typically be completed in minutes with the right tooling. Risk decisioning — what tier this customer falls into, what enhanced due diligence applies — often requires information that can be collected and reviewed asynchronously. Don't block the user on a decision that doesn't need to happen in real time.

The tradeoff requires compliance and engineering to reach agreement on which steps can be async, what the user's state is during the async period, and what triggers a hold. Some compliance teams resist async decisioning because it feels like reducing scrutiny. It isn't — it's sequencing scrutiny correctly. The regulatory standard for what gets reviewed doesn't change. The user's wait time does.

---

## The Regulatory Constraint That Actually Can't Move

Identity verification standards. The regulation specifies what constitutes sufficient documentation — what document types are accepted, what information they must contain, what the collection and storage requirements are. That floor doesn't move, and it shouldn't. The goal of the product work above is not to reduce what gets verified. It's to reach the same verified outcome through a product experience that doesn't require five days of back-and-forth to get there.

---

## What "Done" Looks Like

From a product standpoint: the user completes the process without leaving and returning. From a legal standpoint: the submission satisfies the documentation standard and creates an audit trail. These are different definitions. The PM's job is to satisfy both without pretending they're the same. A clean user experience that doesn't generate a defensible audit trail isn't done. A comprehensive audit trail built on a process that users abandon at 40% completion isn't done either. Both have to be true simultaneously — and the product design has to be built with both criteria visible from the start.
