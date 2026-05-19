# Protecting the Critical Path

The three moments when the critical path is most at risk are also the three moments when everyone is most confident it isn't: after a successful launch, during a roadmap planning cycle, and when a new stakeholder joins the conversation.

I've watched critical path failures get set up in each of these windows — never maliciously, always with good intentions, and always by people who believed they understood the system well enough to know the change was safe. That confidence is the hazard. What follows is how I identify the risk early in each situation and how I communicate the constraint without being dismissed as obstructionist.

---

## 1. After a Successful Launch

A successful launch generates two things simultaneously: real evidence that the system works under load, and a strong organizational pull toward replicating or extending what just shipped.

The risk in this window is that shortcuts taken during the launch — workarounds, hardcoded assumptions, capacity decisions made for "launch week" conditions — get treated as permanent architecture because they worked. The team is in celebration mode. Questioning any of it feels like refusing to acknowledge the win. So the shortcuts stay, and the next project is scoped on top of them.

I look for two signals in this window. First, any configuration or limit that was set as a temporary measure but was never formally scheduled for review — rate limits dialed down "until we understand the load," caches warmed manually "just for launch," circuit breakers with wider thresholds "until traffic stabilizes." Every one of these has a critical path implication if the next project assumes them as permanent. Second, I look for scope additions that get proposed in the post-launch glow before the operational review is complete. New features proposed before the post-launch incident review is written are features proposed without complete information.

When I communicate this to leadership, I don't frame it as risk aversion. I frame it as sequencing: the post-launch operational review closes the loop on what conditions the next project is actually building on. Two weeks. Then scope the next thing.

---

## 2. During Roadmap Planning

Roadmap planning cycles are where the critical path gets compromised most consistently and most invisibly. New scope enters the plan through a process that is fundamentally optimized for saying yes — initiatives get prioritized, teams get excited, commitments get made. The dependency analysis comes later, if at all.

The specific failure mode: a new initiative is added to the roadmap with a launch date that assumes a platform capability that is itself on the roadmap, two quarters out, with its own dependencies. The connection is not surfaced because the people planning the initiative and the people planning the platform capability are in different planning cycles, using different tools, with no shared artifact that makes the dependency visible.

I maintain a living critical path map that is updated before and after every roadmap planning cycle. Not a dependency spreadsheet — a map with named services, named teams, and explicit sequencing requirements. Before each planning cycle, I share the current version with whoever is facilitating the session and flag the three to five constraints that are most likely to be load-bearing for incoming scope. This isn't a veto. It's information surfaced before the commitment is made, when it can still change the planning decision, rather than after, when it can only create conflict.

When I communicate this to leadership during planning, I use a specific frame: "Here are the three things that have to happen before X is launchable. Two are on track. One is not. Here's the decision you need to make." Options, not obstacles.

---

## 3. When a New Stakeholder Joins

New stakeholders — a new VP, a new engineering lead, a new business partner with platform access — arrive with external perspective, genuine curiosity, and a strong organizational incentive to demonstrate value quickly. That incentive produces "quick win" proposals within the first 30 to 60 days. The quick wins are often real in isolation. They are frequently critical path risks in context.

The signal is a proposed change that looks straightforward from a product or business perspective but touches a shared service, a contract, or a dependency that has downstream implications the new stakeholder hasn't had time to map. The proposal is made in a meeting, gets positive energy from the room, and starts moving before anyone has checked whether it conflicts with an existing commitment.

I address this by scheduling a 30-minute critical path orientation with any new stakeholder who will be making or influencing scope decisions. Not a document — a conversation. I walk through the current critical path, the three to five constraints that are actively governing our roadmap, and the team or process for flagging proposed changes that might intersect with them. The goal is not to slow them down. It's to give them the context that makes their proposals stronger, because proposals that account for dependencies get implemented faster than proposals that discover them mid-execution.

---

## The Honest Caveat

You cannot protect the critical path alone. A platform PM who identifies every risk accurately but communicates it poorly — or at the wrong time to the wrong person — will not change the outcome. The most important skill is knowing which allies to brief before the meeting, not which arguments to make during it.

The engineering lead who will be the first to notice the dependency conflict. The product partner whose roadmap intersects with the constraint. The finance stakeholder who owns the cost model that makes the timeline make sense. Brief them first. Not to build coalition for its own sake — to ensure that when the conversation happens in the room, the people with relevant context are already in the conversation and not hearing it for the first time.

Critical path protection is fundamentally a coordination problem dressed up as a technical one. Treat it accordingly.
