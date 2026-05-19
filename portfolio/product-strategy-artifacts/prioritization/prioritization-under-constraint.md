# Prioritization Under Constraint

Most prioritization frameworks assume you have time to run them. At the platform layer, the constraint is usually a deadline you didn't set and a dependency you don't fully control. The framework doesn't matter if you're solving the wrong problem.

When the quarter is half over, two teams are blocked on your roadmap, and an executive wants to know what's shipping in six weeks, a scoring spreadsheet is not the answer. The answer is a set of forcing questions that cut through the noise fast enough to be useful.

---

## The Four Forcing Questions

**1. What breaks if this doesn't ship by X date — specifically?**

Not "what would be nice to have done" but what actually fails, who is affected, and whether that's recoverable. Most teams answer this vaguely. The answer needs to be specific.

"Our partner integration goes live Q3" is vague. "If the authentication endpoint isn't ready by July 15th, the partner's engineering team misses their contractual launch window, and we absorb the penalty clause" is specific. Those two statements lead to completely different prioritization decisions.

The follow-on question matters as much as the answer: is the impact recoverable? A delayed internal tool is recoverable. A missed contractual commitment in a regulated environment might not be. Knowing which you're dealing with changes how much runway you can afford to use on anything else.

**2. Who has blocking authority over this decision, and what's their actual concern?**

Stakeholders state preferences. The PM's job is to find the constraint underneath the preference.

"I want feature X by date Y" is a stated preference. It usually means one of three things: they've made a commitment to someone else that depends on X, they're worried that without X, some outcome becomes likely that they're trying to prevent, or they're operating on an assumption about what X will accomplish that may not be accurate. Solve for the underlying concern, not the stated request.

This matters for prioritization because it tells you how much flexibility actually exists. If the real concern is a commitment they've made externally, there's no flexibility — the date is hard. If the real concern is a risk they're trying to mitigate, there may be other ways to mitigate it that don't require the full feature by the stated date. You won't find that out by taking the request at face value.

**3. What's the blast radius of being wrong?**

Some wrong prioritization decisions cost a sprint. Some cost a quarter. Some create technical debt that compounds for two years and slows every team that touches that codebase.

The stakes determine the appropriate investment in getting the decision right. A low-blast-radius decision should be made fast, with available information, and revisited if it turns out to be wrong — the cost of being wrong is low enough that speed matters more than accuracy. A high-blast-radius decision warrants spending a day or two getting better information before committing. Applying the same level of rigor to both is a misallocation.

Name the blast radius explicitly. "If we're wrong about this, what does that look like in six months?" is a question worth five minutes of your next team meeting.

**4. What can be shipped incrementally versus what requires the full scope?**

This is the single most useful question in most scope debates, and it's almost never asked directly.

Most disagreements about what's in scope are actually disagreements about what constitutes a shippable unit. One party thinks you need the full feature to deliver any value. Another thinks a subset delivers enough value to count. Both parties are often talking past each other because they haven't made that definition explicit.

When you surface this question, one of three things becomes clear: the feature genuinely requires full scope to deliver any value (rare), there's a useful subset that delivers most of the value and can ship first (common), or there's a version of the feature that unblocks the dependency without solving the long-tail cases (very common in platform work). Knowing which you're in before the sprint starts saves significant time.

---

## The Honest Limitation

This approach works when you have enough information to answer the four forcing questions. When you don't — when the deadline is real but vague, when you don't know who actually has authority, when blast radius is hard to estimate — the right call is to spend a day getting that information before prioritizing, not to run a scoring model on incomplete inputs.

A scoring model applied to incomplete information produces confident-looking wrong answers. A day spent getting clarity produces better inputs. The PM who knows the difference, and acts on it, makes fewer decisions that have to be walked back.
