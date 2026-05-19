# Seven Things That Actually Slow Regulated Product Launches

Most regulated product delays are attributed to "compliance complexity" or "legal review time." Those are symptoms, not causes. The causes are more specific and more addressable than they sound.

The distinction matters because teams that treat "compliance complexity" as a cause will design processes that accept slow timelines as an inherent feature of regulated work. Teams that treat it as a symptom will look for the specific failure underneath and fix it. The seven items below are the specific failures.

---

**1. Legal reviews the product spec instead of the data handling design.**

The feedback arrives on UI decisions and feature scope when the questions that actually matter — what data is collected, how it's stored, who can access it, what the consent mechanism is — are buried in technical documents that no one sent to legal in the first place. Legal reviews what they receive. When they receive a PRD, they produce feedback on the PRD. The PM then spends a week explaining that the UI comments aren't the point, and the data handling question still hasn't been answered. The fix is sending a one-page brief with the data model and consent flow, not the full spec.

**2. Pilot exit criteria defined after the pilot starts.**

Without pre-agreed success criteria, every stakeholder evaluates the pilot through a different lens. Legal is looking for absence of regulatory incidents. Product is looking for completion rate. Business is looking for the numbers that support a go-forward decision. None of them are looking for the same thing. The PM who doesn't define exit criteria before launch will negotiate them under pressure when results are ambiguous — and in a regulated pilot, ambiguous results are the norm, not the exception. The stakeholder with the most conservative read of the results anchors the conversation. Define criteria before launch, get agreement in writing, and refer to the document when the conversation starts.

**3. Compliance and legal give contradictory direction without anyone convening them.**

Legal says the customer consent flow is sufficient. Compliance says it needs additional language. Neither has seen the other's feedback. The PM waits two weeks for a conversation that should take 45 minutes, during which the engineering team has stopped work on the component in question because no one is sure which direction is correct. The resolution is always the same: put both positions in writing, send them to both stakeholders simultaneously, and request a joint decision with a specific date. The delay is in the convening, not in the resolution.

**4. The compliance sign-off lives on a checklist item that no one owns.**

Someone added "compliance approval" to the launch checklist, but no one specified which compliance team, which version of the product, what "approval" means in a documented sense, or who is responsible for obtaining it. The item gets checked when someone thinks it's probably fine. Weeks later, a compliance stakeholder who wasn't part of that judgment asks what sign-off was received and who gave it. There is no good answer. The fix is specificity at the checklist level: named stakeholder, specific product version reviewed, date of review, written record of the outcome.

**5. Engineering waits for full regulatory clarity before writing any code.**

Regulatory guidance is often directional before it's precise. An agency issues a rule; interpretive guidance follows over months. Waiting for complete regulatory clarity before starting any engineering work is a valid risk position, but it is a choice — not an automatic consequence of the regulatory environment. PMs who don't make this choice explicit let teams default to full-stop. The alternative is identifying which components are not subject to regulatory uncertainty and building those now, while holding the uncertain components for later. That requires mapping regulatory risk at the component level, not treating the entire product as a single regulatory unit.

**6. Risk assessments are written for the audit file, not for decision-making.**

A risk assessment that no one reads before a launch decision is not risk management; it's compliance theater. The tell is in how it's written: passive voice, comprehensive coverage of every possible risk, no prioritization, no clear recommendation. It demonstrates that the team thought about risk; it doesn't actually inform a decision. A risk assessment written for decision-making identifies the top three risks by severity and likelihood, states the current mitigation for each, and makes a clear recommendation about whether the residual risk is within the firm's tolerance. That document gets read. The PM who writes it to be used will find that it is.

**7. Go/no-go authority is undefined until someone says no.**

The most expensive version of this: a stakeholder with no clear authority over the launch raises a concern in the final week, and no one knows whether it's blocking or advisory. The launch stalls while everyone figures out the org chart. Then someone who does have authority has to weigh in, which takes time, and now the concern-raiser is part of the conversation at a moment when the PM would rather be closing out the launch checklist. Map authority at kick-off. Document who can block and who cannot. Confirm it with each stakeholder's manager. The conversation is slightly awkward at the start of the project and completely necessary at the end of it.
