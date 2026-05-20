**Note: This is a simulated postmortem. The company, product, and events are fictional.**

# Postmortem: v1 API Deprecation — Enterprise Consumer Outage on Cutoff Day

**Date:** Q1, first Monday of the quarter  
**Severity:** P1 — three enterprise consumers impacted, production workflows interrupted  
**Status:** Resolved. Policy changes implemented.

---

## What Happened

At 12:01am UTC on the scheduled cutoff date, we disabled Meridian's v1 API. By 11:15am, three enterprise customers had opened support tickets reporting production failures. We reinstated v1 by 2:48pm — approximately four hours and forty-seven minutes after the first ticket.

The timeline of failures:

- **Week -8:** Deprecation announced via email to all 47 API key holders. Migration guides published in the developer portal.
- **Week -4:** Second email sent. 14 of 47 keys had confirmed migration. 33 had not responded.
- **Week -1:** Final reminder sent. No additional confirmations received.
- **Day 0, 12:01am:** v1 API disabled.
- **Day 0, 9:47am:** First ticket. A customer's quarterly financial reconciliation job failed. The job ran on the first Monday of each quarter. This was that Monday.
- **Day 0, 10:23am:** Second ticket. A partner integration — built by a third-party contractor on the customer's behalf — started returning 401s. The customer did not know this integration existed until it broke.
- **Day 0, 11:15am:** Third ticket. A customer's backup sync job, designed to run monthly and last executed six weeks prior, failed on its scheduled run.

We had three customers in production failure for a combined duration of roughly two to five hours each. The financial reconciliation customer had downstream reporting obligations dependent on that job completing by end of business.

## How We Found Out

Support tickets. Not monitoring.

We had no telemetry on v1 API call volume broken down by API key. We had no way to know, before the cutoff, which of the 33 unconfirmed keys were "actively silent" — dormant by design, waiting for a scheduled trigger — versus "passively silent" — abandoned and never coming back. We assumed passive. We were wrong about three of them, and possibly more.

This is the embarrassing part: the email open rates on our deprecation communications were good. Customers received the notices. They read them. And at least two of them didn't connect "v1 is going away" to "this affects the integration my contractor built eighteen months ago that I've never thought about since." We sent communications. We did not verify understanding or coverage.

## Root Cause

**Technical:** We had no per-key activity telemetry on v1. The last-called timestamp was available internally, but only in aggregate. Keys that had not called the API in 30 or more days were treated as inactive by default. There was no mechanism to distinguish seasonal or quarterly-use keys from abandoned ones.

**Process:** The deprecation communication plan was one-directional. We announced. We did not require confirmation. We did not require consumers to tell us what they were using the API for, at what frequency, or what business processes depended on it. Silence was treated as consent to cut.

There is a specific process failure worth naming plainly: we designed the deprecation process to make it easy for us to proceed, not easy for us to be confident we were safe to proceed. Forty-seven emails sent, fourteen confirmations received, and we called that "good enough."

## What We Did Immediately

- Reinstated v1 API within 4 hours of the first ticket
- Issued a 90-day extension with a new cutoff date communicated the same day
- Conducted direct outreach — phone calls, not email — to all 33 unconfirmed key holders within 48 hours
- Discovered two additional dormant-but-active keys during that outreach that had not yet broken because their scheduled runs hadn't triggered yet

## What We Changed Permanently

**On the technical side:**

- Added request-level telemetry to all API versions: call frequency, recency, consumer ID, and endpoint distribution per key
- Created a "last active date" field visible in the developer console for each API key, giving key owners visibility into their own usage without requiring a support request
- Built a quarterly usage digest email for API key holders — an automatic summary of usage in the prior 90 days, sent once per quarter regardless of any active deprecation

**On the policy side:**

- Changed our deprecation policy: any key with recorded activity in the trailing 12 months now requires active confirmation before that key is included in a hard cutoff
- Added a "migration confirmed" gate to the deprecation timeline — a hard cutoff does not proceed until 100% of active keys have either confirmed migration or explicitly acknowledged that their key is inactive
- Defined "active" as any key that has made at least one call in the prior 12 months, with no minimum frequency requirement

## What We'd Do Differently

Run a canary cutoff 72 hours before the real cutoff. Disable v1 for 15 minutes at a verified low-traffic window — 3:00am to 3:15am UTC on a Wednesday — and monitor for any error spikes or unexpected call attempts. Any key that generates errors in the canary window gets flagged for outreach before the real cutoff proceeds.

This would have caught all three affected consumers. Their use cases — quarterly, monthly, contractor-built — would all have triggered errors during a 15-minute outage if that outage hit at the wrong time. We would have known they were active before we cut them permanently.

We did not do this because no one proposed it. It should have been obvious. The lesson is that deprecation runbooks need an explicit "how do we know we're safe to cut" section — not just a communications checklist, but an observational verification step.

## What This Didn't Fix

We still cannot identify API keys that customers have embedded into third-party products the customer does not actively monitor. The contractor-built partner integration that failed on Day 0 was discovered only when it broke. We have added documentation recommending that customers audit third-party integrations before any deprecation window, but we cannot enforce it, and customers who built integrations through third parties often don't have visibility into what those integrations call.

This is a structural problem. We provide API keys. We do not provide complete visibility into how those keys are deployed. Until we can correlate a key to a specific deployment context — not just usage frequency — our "active confirmation" gate still has a blind spot for integrations that customers don't know to confirm.

We've acknowledged it. We haven't solved it.
