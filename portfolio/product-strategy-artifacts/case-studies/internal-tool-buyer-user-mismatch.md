**Note: This is a simulated case study. The company, product, and events are fictional.**

# The Buyer-User Mismatch: When Rep Adoption Is the Wrong Success Metric

**Company: Orion** (enterprise sales operations platform)

---

## Situation

Orion's new pipeline forecasting feature launched to strong early numbers. Within 60 days, 78% of sales reps had adopted it. NPS from reps was +42. Qualitative feedback was consistently positive — reps said it was faster, easier to use, and less disruptive to their workflow than the previous process.

At 90-day contract renewal, three of the four enterprise customers that had adopted the feature did not renew. In each case, the renewal conversation went badly in the same way: RevOps had a problem with the forecasting data quality and attributed it to the feature.

I had shipped what I thought was a successful feature. The customers who mattered most had decided it was not.

---

## Constraint

The PM had treated rep adoption as the primary success metric. The research process had reflected that: five rep interviews during discovery, rep usability testing during design, rep feedback sessions after beta. Buyer input — VP of Sales and RevOps — had been collected in one discovery session and not revisited after design began.

The constraint wasn't resources. It was scope of perspective. The research had been thorough on one stakeholder group and thin on the other. By the time renewal conversations surfaced the problem, the design was shipped and 78% of reps were using it daily.

Redesigning a feature with that adoption level, on a short renewal timeline, was not a real option.

---

## Decision

The feature had been designed to reduce the time reps spent entering forecast data. The previous process required reps to fill out a structured form with 12 fields per opportunity, updated weekly. The new feature reduced that to 4 fields with smart defaults, and updated on deal activity rather than on a fixed schedule.

Reps loved it because it reduced their weekly forecast burden from 45 minutes to 10 minutes. That was a real gain and a real improvement.

What I hadn't understood during design: the data that buyers — VPs of Sales, RevOps — used for board-level forecasting wasn't the summary data. It was the granular rep-entered data. The three fields we had eliminated included deal confidence rating, next step specificity, and competitive displacement flag. Buyers used those fields to build the models they presented to their boards.

When reps entered data faster, they entered less data. The fields that felt optional to reps were not optional to buyers. Buyer signal quality dropped 60% within 90 days.

---

## What Broke

RevOps discovered the degradation when preparing a board deck for Q3 business review. The forecasting model they'd been running for two years suddenly had incomplete inputs. When they traced it back, the change in data quality correlated exactly with the feature launch.

Three of four enterprise buyers in the next renewal cycle saw Orion as having broken their forecasting capability. The language in one renewal call was direct: "You optimized for the wrong person."

The fourth customer renewed because their RevOps team had noticed the data quality issue early and had trained their reps to fill in the missing fields manually, outside the product. They had worked around the feature to preserve the outcome they needed. Their renewal was not evidence that the feature was working — it was evidence that they had compensated for it.

---

## What Changed

Feature redesign: faster entry was preserved, but structured required fields were restored for the three data points buyers relied on. The implementation was progressive disclosure — reps saw a fast four-field form, and the system prompted for additional fields only when the opportunity met specific criteria: deal size above threshold, stage at or past demo, close date within 60 days. High-signal opportunities required more input. Low-signal opportunities didn't.

The redesign also added a data quality dashboard for RevOps — a view that showed field completion rates by rep, by region, and over time. Buyers could now monitor signal quality without having to run it through a separate analysis.

Both changes were shipped eight weeks after the renewal failures surfaced. Two of the three churned customers were reengaged at the next renewal cycle. One did not return.

---

## What I'd Do Differently

Map the buyer-user conflict before designing anything.

In an enterprise B2B product, the person who performs an action and the person who benefits from that action are often different people. Reps enter data. RevOps and VPs use that data. These are not the same job, and they often want different things from the same interaction: the rep wants to enter data quickly, the buyer wants the data to be complete and structured.

When the person performing the action and the person benefiting from the action are different, you have a design tension that needs to be made explicit before you start designing. "What does the rep need from this interaction" and "what does RevOps need from this interaction" are two separate questions with two separate answers that may be in direct conflict.

I had asked both questions. I had not held them in the same room and worked out the conflict. I had answered the rep question thoroughly and the buyer question lightly, and the design reflected that imbalance.

The 78% adoption rate and the +42 NPS were real. They measured the rep experience accurately. They said nothing about whether the feature was working for the business. Measuring success from only one stakeholder's perspective, in an enterprise product with multiple stakeholders, isn't a measurement problem — it's a framing problem. I had framed the feature as a rep tool and measured it as a rep tool. It was actually a data collection mechanism, and the people who depended on that data were not in my measurement model.
