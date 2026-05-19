# API Contract Ownership

An API without clear ownership is a liability. When two teams think they own the contract, no one does — and the consumer pays the price.

I've seen this failure mode in both directions. The first is the platform team that treats schema changes as implementation details, ships them without consumer notification, and then spends three weeks on incident bridges when integrations break. The second is a governance structure so rigid that a simple field addition requires six weeks of committee review. Both extremes are wrong. The version of this that works is a written agreement that establishes accountability without creating bureaucracy — and that distinguishes clearly between changes that need a runway and changes that don't.

This is that agreement.

---

## Merge Authority on Schema Changes

A single team holds merge authority on the API contract. That team is accountable for schema changes, and "accountable" means they are the first call when a change breaks a consumer, regardless of who requested the change.

Merge authority does not mean sole authorship. Consumers and partner teams can propose schema changes. Merge authority means one team reviews, approves, and ships — and absorbs the accountability that goes with it.

**Breaking vs. non-breaking changes — the distinction that matters:**

A **non-breaking change** adds to the contract without removing or altering existing behavior. Examples:
- Adding an optional request field with a documented default
- Adding a new response field that consumers can choose to ignore
- Adding a new endpoint alongside existing endpoints
- Expanding an enum with a new valid value (only if consumers handle unknown enum values gracefully — this requires verification)

A **breaking change** removes, renames, or alters existing behavior in a way that requires consumer code changes to continue functioning. Examples:
- Removing a field from a request or response schema
- Renaming a field (`recipient_id` → `recipient_ref`)
- Changing a field's data type
- Tightening validation rules that previously accepted certain inputs
- Changing rate limit structure downward
- Changing error codes or error shapes that consumers parse

When there is ambiguity about whether a change is breaking, the default is to treat it as breaking. The cost of an unnecessary runway is lower than the cost of an undisclosed breaking change.

---

## Notification SLA

**Non-breaking changes:** Minimum 2 full sprint cycles of advance notice before the change ships to production. This gives consuming teams time to update their integration tests, documentation, and any code that pattern-matches on response shapes. Two sprint cycles is not a courtesy — it is the minimum required for a team with a full sprint backlog to absorb the information and act on it without dropping other commitments.

**Breaking changes:** Minimum 1 full quarter of advance notice, with active migration support for the duration. A quarter gives consuming teams time to plan the migration into their roadmap, staff it appropriately, and execute without emergency-mode pressure. Migration support means a dedicated support channel, documented migration guide, and at least two scheduled office hours sessions during the migration window.

---

## Emergency Fixes

Emergency fixes are the exception that proves the rule. When a security patch requires an immediate breaking change — a compromised authentication scheme, an injection vulnerability, an exposed data field — the notification SLA does not apply. The change ships.

The protocol in that case:

1. The fix ships to production with a simultaneous notification to all downstream consumers. Not before — simultaneous.
2. The notification includes: what changed, what the consumer must do, and a contact for urgent help.
3. The platform team staffs a dedicated incident channel for 72 hours post-deployment.
4. A post-incident review is scheduled within 5 business days. That review covers both the security issue and whether the change could have been designed to be less disruptive.

Emergency changes are not a precedent for skipping the SLA on non-emergency changes. If the emergency process is invoked more than once per quarter, that is a signal that something is broken upstream — in the design review process, in the security review process, or in the team's definition of "emergency."

---

## Escalation Path for Undisclosed Changes

When a consumer reports a behavior change they were not notified about, the path is:

1. The consuming team files a report in [intake channel] with the observed behavior, the expected behavior based on the documented contract, and the date the discrepancy was first noticed.
2. The platform team acknowledges within 4 business hours and determines whether the change was intentional (missed notification) or unintentional (regression).
3. If intentional and undisclosed: the platform team owns the remediation — either reverting the change or issuing an emergency migration support engagement at no cost to the consumer's sprint capacity.
4. If unintentional (regression): the platform team treats it as a P1 incident and follows standard incident protocol.
5. In both cases, the incident is logged against the platform team's governance record and reviewed in the next quarterly contract ownership review.

---

This agreement doesn't prevent bad API decisions. It creates accountability for them. That's different, and it matters. A team that knows it will be the first call when a change breaks a consumer makes different decisions than a team that ships and hopes. Accountability changes behavior before the incident, not just after it.
