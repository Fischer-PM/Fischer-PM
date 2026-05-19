# Executive Roadmap Memo Template

An executive doesn't need context; they need the decision, the tradeoff, and what they have to do (if anything). Everything else is noise.

This template is built around that constraint. It strips out background, process narrative, and hedge language — the things PMs tend to include because they feel like responsible communication but actually make the memo longer to read and harder to act on. The format below is what remains when you remove everything an executive doesn't need to see.

---

## The Template

```
TO: [name, title]
FROM: [PM name]
DATE: [date]
RE: [one-line subject — the decision or commitment being communicated]

WHAT'S HAPPENING
[One sentence. The decision made or the change in direction.]

WHY
[Two to three sentences. What drove this decision. Not background — the specific reason.]

WHAT WE'RE DOING
[The choice made and the key tradeoff accepted. What we're investing in and what we're deferring.]

WHAT WE'RE NOT DOING
[Equally important. Names the scope that was considered and excluded. This prevents future surprises.]

HOW WE'LL KNOW IT'S WORKING
[The metric and the timeline. Specific and measurable.]

WHAT WE NEED FROM YOU
[One ask, or "no action needed." If there's no ask, say so explicitly.]
```

---

## Field-by-Field Notes

**RE line:** Write it as a decision or a change, not a topic. "Q3 Roadmap Update" is a topic. "Deferring the vendor API migration to Q4 and reallocating capacity to authentication stability" is a decision. Executives skim RE lines first. The one that communicates the actual content gets read; the other one gets opened later.

**WHAT'S HAPPENING:** One sentence. If you need two, the decision isn't clear yet. Write this field last — it will be cleaner once you've written the others.

**WHY:** This is not the history of how you got here. It's the specific reason this decision is right now. "Customer-facing error rates on the authentication service increased 40% over the past three weeks and are projected to worsen under Q3 load" is a reason. "We've been discussing this for a while and the team reached consensus" is not.

**WHAT WE'RE DOING / WHAT WE'RE NOT DOING:** These fields belong together. The doing field without the not-doing field creates a false picture of scope. If you chose to invest in X, you chose to not invest in something else. Name it. Executives who see a decision without its tradeoff will ask about it in the next meeting, which means you'll be explaining it reactively instead of proactively.

**HOW WE'LL KNOW IT'S WORKING:** A specific metric and a specific timeline. "Improved reliability" is not measurable. "Authentication error rates below 0.5% by end of Q3" is. If you can't write this field specifically, that's information — it means the decision lacks a success condition, and that's worth knowing before you commit.

**WHAT WE NEED FROM YOU:** Be direct. If you need a decision, say so and give a deadline. If you need air cover with another team, say so specifically. If you're informing and nothing is needed, write "No action needed." That last phrase is underused and valuable — it tells the executive they can stop reading and not worry about a follow-up.

---

## What Not to Put in an Executive Memo

**Background history.** If you shipped something last quarter that's relevant, say so in one clause — "following the Q2 integration work" — not in a paragraph. They don't need the story of how you got here. They need to know where you are.

**Process description.** How you made the decision is not the memo's subject. "After three rounds of stakeholder sessions and a team workshop" tells them nothing actionable. Remove it.

**Team shout-outs.** Save recognition for the all-hands or the team Slack. A shout-out in an executive memo reads as filler. It dilutes the content and signals that the PM isn't sure how to fill the space.

**Hedge language.** "We believe," "we think," "we feel," "we hope" — replace every one of these with what you know or what you're committing to. "We believe this will improve reliability" is a hedge. "This will reduce authentication errors by an estimated 60%; we'll validate against that target by September 30th" is a commitment. Executives make decisions based on commitments, not beliefs.

---

This format is designed to be read in 90 seconds. If it takes longer than that, it's too long. Cut until it fits.
