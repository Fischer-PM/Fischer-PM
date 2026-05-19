# Platform Health Metrics That Actually Matter

API call volume is the metric every platform team tracks and the one most likely to mislead them. High call volume can mean a thriving ecosystem or an inefficient consumer making redundant calls. The number alone doesn't tell you which.

I've worked on platforms processing billions of messages annually and managing 4B+ API calls per year. In those environments, the gap between the metrics that feel important and the metrics that are actually predictive of platform health becomes expensive very quickly. What follows is the framework I use to build a platform dashboard that tells the truth.

---

## 1. Leading vs. Lagging Indicators

Most platform dashboards are weighted toward lagging indicators — numbers that confirm something has already gone wrong. Leading indicators are harder to collect and easier to ignore, which is exactly why they matter more.

**Leading indicators to track:**

- **Error rate trending** — not the error rate at a point in time, but whether it is moving. An error rate of 0.8% that was 0.4% three weeks ago is a different situation than an error rate of 0.8% that has been stable for two quarters. Trend is the signal; the number is the context.
- **p99 latency trend** — same logic. A p99 latency of 450ms that has climbed from 280ms over six weeks is an early warning. A stable 450ms is a different problem — it may be a design constraint rather than a degradation.
- **Consumer adoption rate** — how many new consumers are successfully completing their first integration per quarter? A platform with 4B annual API calls but zero new consumer onboardings in two quarters is in quiet decline regardless of what the volume number says.

**Lagging indicators worth tracking (but not confusing with health signals):**

- **SLA breach frequency** — tracks that something went wrong, not that something is about to
- **Consumer team churn** — when engineering teams migrate away from your platform, that decision was made weeks or months before it appears in any metric

---

## 2. Anti-Metrics

These are numbers that appear on platform dashboards constantly and routinely mislead the teams reading them.

**Call volume alone.** High volume can mean healthy adoption or a consumer calling your API in a retry loop because you haven't designed good error guidance. Volume without error rate context and consumer count context is nearly meaningless.

**Uptime percentage in isolation.** 99.9% uptime sounds like success. It represents 8.7 hours of downtime per year. Whether that's acceptable depends entirely on when those hours occurred, which consumers were affected, and whether the SLA contract allows for it. Uptime as a single number strips out all of that context.

**Number of APIs.** A platform with 47 endpoints is not inherently healthier or more capable than one with 12. API count tends to grow as a function of team age and organizational negotiation, not as a function of consumer need. Tracking it as a health metric incentivizes proliferation over consolidation.

---

## 3. Guardrail Metrics

Guardrail metrics are numbers that should never move outside a defined range. They are not targets to optimize toward — they are floors and ceilings that, if crossed, require immediate escalation regardless of what everything else looks like.

For a messaging platform: p99 latency above 600ms triggers a guardrail review. Error rate above 1.2% on any endpoint triggers a guardrail review. SLA breach in any calendar month triggers a guardrail review.

The value of a guardrail metric is that it removes negotiation from the response. If the guardrail is crossed, the conversation is not "let's see how this trends next week." The conversation is "what broke and when are we fixing it."

---

## 4. The Wrong Default: Incident Count Per Month

When platform health feels uncertain, teams default to counting incidents. It's the most available number and feels like a proxy for reliability.

It is the wrong question. Incident count tells you nothing about severity, duration, consumer impact, or cost. A platform with 3 incidents per month that each affected 1 consumer for 4 minutes is healthier than a platform with 1 incident per month that took down 12 consumers for 6 hours.

The right question is incident cost — measured in consumer-hours of impact, not incident reports filed. Incident cost = (number of affected consumers) × (duration of impact) × (criticality weight of the affected consumers). That number is harder to calculate and much more honest about what actually happened.

---

## 5. The Missing Metric: Time-to-First-Successful-API-Call

This metric should be on every platform dashboard. Almost none have it.

Time-to-first-successful-API-call (TTFSAC) measures how long it takes a new consumer — from the moment they receive access credentials — to complete their first successful API call in a development or staging environment. It is a direct measure of developer experience, documentation quality, and onboarding infrastructure.

In my experience, platforms that think their onboarding is smooth typically have TTFSAC somewhere between 2 and 5 days when you actually measure it. Platforms with genuinely good onboarding have TTFSAC under 4 hours. The gap between what teams believe and what this metric reveals is almost always instructive.

TTFSAC is also a leading indicator for consumer adoption rate. If new consumers are struggling to complete a first call, they will not become productive integrators — and they will not refer your platform to other teams. Measuring it is the first step to improving it.
