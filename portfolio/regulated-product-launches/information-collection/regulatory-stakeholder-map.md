# Mapping Regulatory Stakeholder Authority

Not everyone in a compliance review process has the same authority, and treating them as if they do is one of the most common reasons regulated product launches slow down at the wrong moments.

A stakeholder who raises a concern in week eight of a twelve-week project can stop the launch if they have blocking authority. The same concern raised by someone with advisory authority is a different conversation — important to address, but not a veto. PMs who haven't mapped authority before the project starts find out the difference at the worst possible time.

---

## Blocking vs. Advisory Authority

**Blocking authority** means a stakeholder can stop the launch. Their unresolved objection is sufficient to prevent go-live. This is typically legal (for regulatory interpretation), the primary compliance function overseeing the product domain, and in some firms, a designated regulatory sign-off role at the leadership level.

**Advisory authority** means a stakeholder can raise concerns and those concerns must be documented and considered — but they cannot unilaterally block the launch. This often includes business-side compliance, product risk, and line-of-business compliance officers who implement policy rather than set it.

The practical implication: identify both lists at the start of the project, write them down, and confirm them with each stakeholder's manager if there's any ambiguity. You want to find out that someone has blocking authority at kick-off, not when they send a hold request in the final week.

---

## The Functional Difference Between Legal and Compliance

PMs conflate legal and compliance constantly, and it sends them into the wrong conversation at the wrong time.

**Legal** interprets what the regulation requires. They read the statute, the rule, the guidance, and any relevant enforcement actions, and they tell you what the regulatory standard is. Their question is: does this product design satisfy the regulatory requirement?

**Compliance** operationalizes how the firm meets the regulatory standard. They translate legal's interpretation into policies, procedures, and controls that the firm runs. Their question is: does this product design satisfy our firm's compliance policy?

These can have different answers. A product design might satisfy the regulation as written but fall short of the firm's more conservative internal policy. It might satisfy the firm's policy in a way that legal hasn't reviewed for the specific implementation. Asking legal a compliance question and asking compliance a legal question are both ways of getting answers that don't resolve the actual problem.

Before any review meeting, know which question you're asking and who is actually positioned to answer it.

---

## When to Involve Legal (and When You're Wasting the Relationship)

Legal bandwidth is finite and goodwill is a real asset. Using it on premature reviews is expensive.

**Bring legal in when:** the product touches a new regulatory domain they haven't reviewed before; the data handling design is finalized and ready for substantive review; the pilot scope is being defined and needs regulatory framing; you're finalizing the go-live checklist and need documented sign-off on a specific implementation.

**Do not bring legal in when:** the wireframes are at 30% and the scope is still moving; you want a general comfort check before committing to a design direction (you won't get a useful one, and you'll spend the relationship on a conversation that has to happen again); the question you're bringing them is really a compliance policy question that compliance should answer first.

The discipline here is about respecting the difference between a conversation that generates a reviewable artifact and one that generates a verbal impression. Verbal impressions from legal are not sign-off. They are not defensible if the product is later questioned. Save the formal engagement for when you have something specific enough to get a specific answer.

---

## What "Regulatory Sign-Off" Actually Means

It is not a checkbox. It is a documented record that the relevant stakeholder reviewed the specific version of the product — the data model, the consent flow, the audit trail mechanism — and did not object, with that review recorded in writing.

The version matters. "Legal approved the concept six weeks ago" is not the same as "legal reviewed the final implementation and signed off on it." Concepts change. Implementations include decisions that weren't part of the concept. Any regulatory defense of the product will be based on what was actually reviewed, not what someone thought was being built.

The PM's job is to generate real sign-off, not the appearance of it. That means sending a written brief, receiving a written response, and keeping both in the project record. Verbal approval in a meeting that isn't documented is not a risk position you want to be in.

---

## Structuring the PM-Legal Working Relationship

Schedule a standing touchpoint at project milestones, not continuously. Continuous access to legal invites premature questions and generates opinions on things that will change. Milestone-based touchpoints — at scope finalization, at pilot definition, at go-live readiness — create natural moments for substantive review when there's something real to review.

Before any meeting, send a brief. One page. Four sections: what the product does, what data it handles, what the regulatory concern is, what you are asking them to review and by when. Do not send the PRD. The PRD is written for engineers and contains a hundred decisions legal doesn't need to weigh in on. Sending it invites feedback on all of it. A focused brief invites feedback on the actual question.

The working relationship with legal functions best when they understand that you will use their time precisely. That reputation is built by showing up with specific questions and acting on the answers.
