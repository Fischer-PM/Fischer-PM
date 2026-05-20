# Product Management Glossary: Precise Definitions

Most PM glossaries define terms the way textbooks do — correctly but uselessly. This one defines them the way they're misused in practice, because the misuse is usually where the actual problem is.

---

## Metrics & Measurement

**North Star Metric**
The single metric that best captures the value your product delivers to customers — not revenue, not engagement, but the leading indicator of long-term health. A North Star Metric should move when customers are genuinely succeeding with the product, and it should predict retention and revenue rather than follow them. It is not the same as your top-line revenue metric; it's the input that drives revenue over time.

**Common misuse:** Teams pick a metric that's easy to measure rather than one that's meaningful. "Monthly active users" is a North Star for almost no product — it measures presence, not value. A messaging product's North Star might be "messages sent between new connections"; a project management tool's might be "teams that complete their first project within 30 days." If your North Star Metric doesn't tell you whether customers are getting value, it's not a North Star — it's a vanity metric with a prestigious name.

---

**Leading indicator vs. lagging indicator**
A leading indicator predicts future outcomes — it moves before the thing you care about moves. A lagging indicator confirms outcomes that have already occurred. Activation rate is a leading indicator of retention; churn rate is a lagging indicator of product-market fit failure. Both are necessary; the error is relying only on lagging indicators to steer the product.

**Common misuse:** Treating revenue as a leading indicator of product health. Revenue is a lagging indicator of value delivered weeks or months ago. By the time revenue declines, the warning signals were already visible in leading metrics like activation rate, feature engagement, and support ticket volume.

---

**Input metric vs. output metric**
An output metric measures a business result — revenue, retention, NPS. An input metric measures the behavior or action that produces that result — onboarding completion rate, feature adoption, weekly active days. Teams control inputs; outputs follow. Effective product management focuses on identifying which inputs reliably predict outputs and then moving the inputs.

**Common misuse:** Setting team goals on output metrics without establishing which inputs the team controls. "Improve retention by 5%" is an output goal without a strategy. "Increase the percentage of new users who complete three sessions in the first week" is an input goal that, if it predicts retention, gives the team something to actually work toward.

---

**Guardrail metric**
A metric that defines the boundary condition a team must not cross while pursuing its primary goal. A growth team optimizing for signup volume might have a guardrail on support ticket rate — they can't improve signups by lowering the quality bar in ways that overwhelm customer support. Guardrail metrics prevent a team from optimizing one dimension at the expense of another that matters.

**Common misuse:** Treating guardrail metrics as secondary or aspirational. A guardrail metric is a hard constraint, not a soft goal. If you hit your primary metric but breach a guardrail, the experiment failed — full stop.

---

**Vanity metric**
A metric that looks impressive but doesn't reliably connect to business outcomes or customer value. The definition requires context: a metric can be a vanity metric in one situation and a real metric in another. Page views are a vanity metric for a SaaS product where revenue depends on active use — lots of page views with low session depth and high churn means users are browsing without engaging. The same page views metric is a real business metric for a media publisher whose revenue model is advertising impressions. The question is always: does this metric move when the business is actually doing better for customers?

**Common misuse:** Calling any metric you dislike a "vanity metric." The label gets applied to metrics people don't want to be accountable for, not just metrics that lack business relevance. The test is simple: if the metric went up but nothing else improved — not retention, not revenue, not customer outcomes — it's a vanity metric. If it can't be isolated that way, it might be a leading indicator that you haven't validated yet.

---

**DAU / MAU (and the DAU/MAU ratio)**
DAU (Daily Active Users) and MAU (Monthly Active Users) measure how many users engage with a product in a given day or month, respectively. The DAU/MAU ratio — sometimes called the "stickiness ratio" — expresses what fraction of monthly users return on a given day. A ratio of 0.50 means half of monthly users use the product daily. The ratio reveals how frequently valuable the product is: tools used daily (messaging, productivity) should have high DAU/MAU ratios; tools used occasionally (tax software, travel booking) will have low ones by design.

**Common misuse:** Benchmarking DAU/MAU ratios without accounting for use-case frequency. Comparing a daily communication tool's DAU/MAU to a quarterly reporting tool's is meaningless. The relevant question is whether the DAU/MAU ratio is appropriate for the frequency at which users should need the product, and whether it's trending in the right direction over time.

---

**Retention curve**
A retention curve shows what percentage of users from a given cohort are still active at each subsequent time period — day 1, day 7, day 30, day 90. The shape of the curve matters more than any single data point. A curve that drops sharply and flattens indicates that a segment of users finds lasting value, even if most churn early. A curve that keeps declining without flattening indicates the product hasn't found a retained user base at any segment.

**Common misuse:** Reporting average retention as a single number. "30-day retention is 40%" hides everything important — which users retained, from which acquisition channels, with which behaviors, and whether retention has improved over time. Retention curves without cohort segmentation are nearly useless for product decisions.

---

**Activation metric**
The activation metric is the specific behavior that signals a new user has reached the point where they're likely to stay. It's the moment value is first delivered — not account creation, not first login, but the action that correlates with long-term retention. For a messaging product it might be "sent a message to someone who responded." For a project management tool it might be "created a project and invited a teammate." The activation metric is one of the most valuable things a product team can identify and instrument.

**Common misuse:** Defining activation as a step in the funnel rather than a moment of value. Completing onboarding, confirming an email, and filling out a profile are not activation — they're prerequisites. Activation is the moment the user experiences what they came for. If your activation metric doesn't predict retention at a meaningfully higher rate than the baseline, you've defined the wrong moment.

---

**NPS (Net Promoter Score)**
NPS measures what percentage of customers would recommend a product to others, calculated by subtracting detractors (0-6 ratings) from promoters (9-10 ratings). It's a lagging indicator of customer sentiment that reflects accumulated experience with the product. NPS is useful for tracking directional changes in satisfaction over time and for segmenting customers who are likely to churn or expand. It is not a leading indicator of anything.

**Common misuse:** Using NPS as a primary success metric for product decisions. NPS tells you how customers feel about what they've already experienced — it doesn't tell you which features drove that sentiment, which users are at risk, or what to build next. It's a signal to investigate further, not a conclusion. Teams that optimize for NPS directly often end up improving survey presentation rather than the underlying product experience.

---

**Churn rate**
Churn rate measures the percentage of customers who stop using a product in a given period. It's the most direct lagging indicator of failed retention. The critical distinction is between voluntary churn (customers who actively cancel because the product isn't meeting their needs) and involuntary churn (customers lost due to failed payments, expired cards, or billing system errors). Involuntary churn is often 20-30% of total churn and is recoverable through dunning and payment retry logic — conflating it with voluntary churn leads to misdiagnosis of the retention problem.

**Common misuse:** Reporting a single aggregate churn rate without segmentation. Churn by cohort, acquisition channel, plan type, company size, and geography tells completely different stories. A product with 5% monthly churn in enterprise accounts and 30% in SMB accounts has two different products with two different problems — the aggregate number obscures both.

---

**LTV (Lifetime Value)**
LTV is the total revenue a business expects to receive from a customer over the entire relationship. The standard calculation is average revenue per user divided by churn rate, sometimes multiplied by a gross margin factor. LTV is the numerator in the LTV:CAC ratio, which is the foundational unit economics metric for subscription and recurring-revenue businesses.

**Common misuse:** Most LTV calculations are wrong because they assume static churn and ignore expansion revenue. In SaaS businesses where customers upgrade, add seats, or buy additional products, LTV from expansion can exceed LTV from the original contract. A model that ignores expansion understates LTV significantly. Additionally, using average churn when churn varies by cohort produces a number that describes no actual customer. LTV should be calculated by segment, not as a blended average, or it's directionally misleading.

---

**CAC (Customer Acquisition Cost)**
CAC is the total cost to acquire one new customer, calculated by dividing total sales and marketing spend by the number of new customers acquired in the same period. The LTV:CAC ratio should exceed 3:1 for most SaaS businesses to be economically sound; below that, the business is spending more to acquire customers than it will recoup.

**Common misuse:** Excluding sales costs from CAC for products with a sales-assisted motion. Some teams calculate CAC using only marketing spend, which dramatically understates the true cost of acquisition. CAC should include fully-loaded sales and marketing costs: salaries, commissions, tools, advertising, events, and content production. The version of CAC that excludes sales costs is a marketing efficiency metric — useful, but not the same thing as true acquisition economics.

---

## Discovery & Research

**Jobs to Be Done (JTBD)**
Jobs to Be Done is a framework for understanding the progress a customer is trying to make in a specific circumstance — not a task they want to complete or a feature they want to use, but the underlying goal that hired the product to help them achieve it. The "job" is the unit of analysis, and it persists even when technology changes: the job of "feel confident I won't miss an important message" exists whether the solution is email, Slack, or something that hasn't been invented yet.

**Common misuse:** Treating JTBD as a synonym for user story or use case. "As a user, I want to filter search results" is not a job — it's a feature request. The job behind it might be "quickly find the specific thing I know exists without wading through irrelevant results." JTBD surfaces the why; features address the how. Confusing them means building features that satisfy the stated request without solving the actual problem.

---

**Desirability / Feasibility / Viability / Usability**
These are the four risk types in product development. Desirability: do customers want this? Feasibility: can engineering build it? Viability: does it work as a business? Usability: can customers figure out how to use it? Balanced discovery addresses all four before committing to build.

**Common misuse:** PMs most often skip viability (can we actually make money from this, and does it fit the business model?) and usability (will users understand this without explanation?). Feasibility gets checked because engineers are in the room. Desirability gets checked because customer research is visible. Viability gets assumed. Usability gets deferred to UX review — which happens after the design is fixed. The result is products that are technically sound and customer-requested but economically unsustainable or operationally confusing.

---

**Assumption vs. hypothesis vs. insight**
An assumption is something believed to be true without evidence — "our users prefer mobile over desktop." A hypothesis is a testable version of an assumption — "if we build a mobile-first experience, we'll see a 20% increase in daily active users among users acquired through paid mobile channels." An insight is a validated learning from evidence — "users who onboard on mobile churn 40% faster than desktop users, indicating the mobile experience has a retention problem." Moving from assumption to hypothesis to insight is the structure of disciplined discovery.

**Common misuse:** Calling assumptions insights. A customer interview where one person says they want a feature is not an insight — it's an assumption with weak supporting evidence. An insight requires a pattern across evidence sources, with some confidence that it generalizes. Teams that call assumptions insights skip the validation step and build on unstable ground.

---

**Attitudinal vs. behavioral research**
Attitudinal research captures what people say — surveys, interviews, focus groups, NPS verbatims. Behavioral research captures what people do — clickstream data, session recordings, A/B test results, funnel analytics. People reliably say things they don't do and do things they don't say. Both types of research are necessary because they answer different questions: attitudinal research explains why; behavioral research establishes what actually happens.

**Common misuse:** Treating either type as sufficient alone. A team that builds only from behavioral data may optimize the existing flow without ever discovering that users are trying to accomplish something the product doesn't currently support. A team that builds only from interviews may build products based on what users claim they want rather than what they demonstrably need. The strongest product decisions triangulate across both.

---

**Continuous discovery vs. episodic discovery**
Continuous discovery is a practice of running ongoing customer research — weekly or bi-weekly interviews, regular usability tests, persistent feedback loops — so that customer insights inform product decisions in near-real time. Episodic discovery is research conducted in discrete projects: a month-long user research initiative before a major feature, a satisfaction survey after a launch. Continuous discovery keeps a team calibrated to customers constantly; episodic discovery creates periodic checkpoints that go stale between cycles.

**Common misuse:** Treating a quarterly user research project as sufficient discovery. The problem isn't that episodic research is invalid — it's that the product world changes faster than the research cadence. A team doing episodic discovery is always making decisions based on insights that are months old. Continuous discovery is the practice that closes that gap.

---

**Problem interview vs. solution interview**
A problem interview explores the customer's current situation, struggles, and behaviors without presenting a product or feature as a solution. A solution interview presents a specific product or concept and seeks feedback on it. Problem interviews surface whether a problem is real, how severe it is, and how customers currently cope. Solution interviews validate whether a proposed solution addresses that problem effectively. The critical rule: problem interviews must happen before solution interviews, or you'll get feedback on your proposed solution without ever confirming the problem is worth solving.

**Common misuse:** Running solution interviews as if they were problem interviews. "What do you think of this feature?" is not a problem interview. Neither is a demo with feedback questions. Solution interviews bias respondents toward the framing you've already committed to and rarely surface the insight that your solution is addressing the wrong problem.

---

## Prioritization

**RICE**
RICE is a prioritization framework that scores opportunities by Reach (how many users affected per period), Impact (estimated effect on the goal, usually a rough multiplier), Confidence (how sure you are of the Reach and Impact estimates, expressed as a percentage), and Effort (person-weeks to build). Score = (Reach × Impact × Confidence) / Effort. The framework is useful for making prioritization logic explicit and comparable across a backlog.

**Common misuse:** Confidence is the hardest input to measure honestly and the one most often inflated. Teams assign 80% or 90% confidence to almost everything because admitting uncertainty feels like weakness. A 90% confidence score on an unvalidated assumption is not confidence — it's wishful thinking dressed up as rigor. RICE scores are only as honest as the confidence inputs, and confident-sounding numbers with unvalidated assumptions produce a numerically precise ranking of guesses.

---

**Opportunity scoring**
Opportunity scoring (from Anthony Ulwick's Outcome-Driven Innovation framework) is a method for identifying the highest-priority customer outcomes to target. It surveys customers on two dimensions for each outcome: importance (how important is this outcome to you?) and satisfaction (how satisfied are you with current solutions?). The opportunity score surfaces outcomes that are highly important but poorly satisfied — where the market gap is largest. It's a structured way to find where to focus product investment based on revealed customer priorities rather than stated feature preferences.

**Common misuse:** Treating opportunity scoring as a one-time activity rather than an ongoing input. Customer priorities shift as markets evolve and competitors improve. An opportunity score from 18 months ago may point to problems that have since been solved by a competitor or that the customer no longer considers urgent. The output needs to be refreshed to remain directionally useful.

---

**Opportunity cost**
In roadmap decisions, opportunity cost is the value of the best alternative you're giving up when you choose to build something. Choosing to spend three months building Feature A means not building Features B, C, and D in that same period. The opportunity cost is the value of whichever of those alternatives would have been most valuable. Every roadmap decision carries opportunity cost even when it's never named, and ignoring it produces roadmaps that optimize for the value of what's chosen without accounting for the value of what's foregone.

**Common misuse:** Applying opportunity cost analysis only to rejected ideas. Opportunity cost is equally relevant to work already committed — if market conditions change or a higher-priority opportunity emerges mid-quarter, continuing to build an in-flight feature has a real opportunity cost that should be made explicit, not assumed away because the work has already started.

---

**Technical debt as prioritization input**
Technical debt is the accumulated cost of design decisions made under time or resource pressure that now make future changes slower, riskier, or more expensive. In a prioritization context, technical debt competes with feature work for engineering capacity, and the return on debt reduction is expressed in future velocity — paying down debt now means faster, cheaper feature development later. It's not visible on a roadmap unless made explicit, which means it tends to be underinvested.

**Common misuse:** Treating technical debt as a binary ("we have debt / we don't") rather than a prioritization input with tradeoffs. Not all debt is equally expensive to carry. High-interest debt — in code paths touched frequently, in systems with reliability requirements, in components that block new feature development — should be prioritized like a high-impact initiative. Low-interest debt can be deferred without consequence. PMs who outsource the entire judgment call to engineering get roadmaps where debt investment is either systematically neglected or justified without reference to product impact.

---

**HiPPO effect**
HiPPO stands for Highest Paid Person's Opinion. It describes the tendency for meetings and decisions to default to the view of the most senior person in the room, regardless of whether that person has the most relevant information or the strongest evidence. The HiPPO effect is a decision-making bias, not a process — it can happen in any meeting where authority and evidence are conflated.

**Common misuse:** Treating HiPPO as only a leadership problem. The HiPPO effect is also perpetuated by teams that don't bring evidence to decision conversations, making it easy for opinion to fill the vacuum. The antidote is not pushing back on seniority — it's structuring decisions around data, user research, and explicit frameworks that make the basis for a decision visible and debatable regardless of who's in the room.

---

## Strategy

**Product-market fit**
Product-market fit is the state in which a product satisfies a strong market demand — not just that customers use it, but that they would be genuinely disappointed if it went away. The Sean Ellis test operationalizes this: survey active users and ask how they'd feel if they could no longer use the product. If more than 40% say "very disappointed," you have meaningful evidence of product-market fit. Below that threshold, something fundamental needs to change about the product or the market being targeted.

**Common misuse:** Declaring product-market fit based on revenue or growth rate alone. A product can grow through aggressive marketing without having product-market fit — customers acquire, churn quickly, and the growth rate is a function of acquisition spend, not retained value. The "very disappointed" threshold is a useful forcing function because it measures the depth of value, not the volume of acquisition.

---

**Moat**
A moat is a durable competitive advantage — a structural reason why a product is hard to displace even when a competitor offers a similar feature set. There are four primary moat types: network effects (the product becomes more valuable as more people use it), switching costs (it is painful or expensive for customers to leave), economies of scale (unit costs fall as volume grows, creating a cost advantage incumbents can sustain), and intangible assets (brand, patents, regulatory approvals, or exclusive data that competitors cannot easily replicate). Moats are what make market position defensible over time; without one, competitive advantage is temporary.

**Common misuse:** Describing product quality or a technology lead as a moat. Both are temporary advantages — quality can be matched, and technology leads compress rapidly in most markets. A true moat is structural: it makes the product harder to displace even for a competitor that matches the features. Assess moats by asking: "If a well-funded competitor launched a product with equivalent features tomorrow, how quickly would we lose?" A feature-quality advantage erodes in months; a network-effect moat takes years to overcome.

---

**Platform vs. product**
A product delivers value directly to end users. A platform creates the infrastructure, APIs, and capabilities that enable other products — built internally or by third parties — to deliver value. The distinction matters because the customer, the success metrics, and the investment model are different. A product succeeds when end users accomplish their goals; a platform succeeds when the products built on it succeed. Platform investment tends to be longer-horizon and harder to attribute to near-term revenue.

**Common misuse:** Calling internal tooling a "platform" when it serves no external or cross-team building surface. A shared component library is not a platform. An internal deployment tool is not a platform. Platform implies that others can build on top of it, that there is an API or extension surface, and that the platform owner is accountable for the success of what others build. Anything short of that is infrastructure or shared services — legitimate, but different from a platform in strategy and investment terms.

---

**Land and expand**
Land and expand is a go-to-market strategy where initial adoption is deliberately scoped — to a single team, a single department, a single use case — with the expectation that demonstrated value will drive broader adoption within the same account. The "land" phase prioritizes low friction to first value; the "expand" phase relies on internal champions, usage data, and organizational word-of-mouth to grow the contract. It's the dominant model for bottom-up enterprise SaaS.

**Common misuse:** Treating land and expand as a sales strategy rather than a product strategy. Expansion happens because the product creates visible value that spreads — not because the sales team follows up six months later. If the product doesn't create natural sharing, collaboration, or cross-team utility, there's nothing for the expand motion to leverage. The product architecture, collaboration features, and admin visibility are all expansion infrastructure that must be built deliberately.

---

**Bottom-up vs. top-down go-to-market**
In a bottom-up GTM, the product is adopted by individual users or teams who discover it independently, and the relationship with the organization scales from use up to procurement. In a top-down GTM, the sale starts with executive sponsorship and procurement, and the product is then deployed to users from the top down. Bottom-up tends to produce faster time-to-value and lower CAC but requires a product experience that stands alone without a salesperson. Top-down produces larger initial contracts but longer sales cycles and higher CAC. Most mature B2B products use both motions simultaneously for different market segments.

**Common misuse:** Assuming bottom-up works automatically because the product is good. Bottom-up GTM requires deliberate product design — frictionless onboarding, self-serve value, viral or collaborative mechanics, and a free or trial tier. A technically excellent product without these elements may still require a sales motion to reach enterprise buyers, regardless of how strong the user experience is.

---

**Product-led growth (PLG)**
PLG is a go-to-market strategy where the product itself is the primary driver of acquisition, conversion, and expansion — rather than sales or marketing. Users discover the product, adopt it without a salesperson, reach a paid threshold through use, and expand their usage or license within the organization based on the value they've experienced. PLG requires a product that delivers value quickly enough to generate genuine pull.

**Common misuse:** Treating PLG as a cost-reduction strategy rather than a distribution strategy. The most common failure mode is removing the sales and marketing budget while expecting the product to compensate, without investing in the product experience, onboarding, freemium architecture, or upgrade mechanics that make PLG actually work. PLG shifts investment from sales and marketing to product — it doesn't eliminate the investment. A product designed for sales-led motion cannot become PLG without significant product redesign.

---

**Flywheel vs. funnel**
A funnel is a linear model: users enter at the top, convert through stages, and exit as customers. Acquisition, activation, retention, revenue, referral. Each stage leaks. A flywheel is a circular model: growth generates more growth because the product gets better, the network gets stronger, or costs fall as scale increases. The distinction matters for investment decisions: funnel thinking prioritizes fixing leaks at each stage; flywheel thinking prioritizes the drivers that accelerate the loop. Not every product has a flywheel — claiming one without identifying the specific reinforcing mechanism is usually a rationalization, not a strategy.

**Common misuse:** Drawing a loop and calling it a flywheel. A flywheel requires a genuine reinforcing mechanism — network effects, data accumulation that improves the product, economies of scale that enable lower pricing, or brand reputation that reduces CAC over time. The test is: does more usage cause the product to get better for existing and future users in a way that drives more usage? If the loop only holds when everything goes right, it's not a flywheel — it's an aspiration.

---

## Execution

**PRD vs. spec vs. brief**
A PRD (Product Requirements Document) defines the problem, the target user, the goals, the success metrics, and the high-level requirements for a feature or product area. It answers why and what. A spec (specification) defines the detailed behavior of a specific implementation — edge cases, error states, exact logic. It answers how in technical detail. A brief is a short, directional document used to align stakeholders on goals and approach before detailed work begins — typically one to two pages, used to get to a shared understanding quickly without premature detail. Use a PRD when alignment on scope and goals is the risk; use a spec when engineering precision is the risk; use a brief when speed and alignment are both needed and over-documentation is the risk.

**Common misuse:** Writing a PRD when a brief would do, then calling the brief a PRD when rigor is actually needed. The format should match the risk and the audience. For well-understood problems with a clear direction, a brief is faster and creates less maintenance overhead. For novel problems, regulated features, or high-stakes launches, a PRD ensures shared understanding before significant investment. Using the same format for everything — either always light or always heavy — is a sign the team hasn't matched documentation to decision risk.

---

**Definition of Done vs. Definition of Ready**
Definition of Done describes the conditions that must be true for work to be considered complete — not just coded, but tested, documented, instrumented, reviewed, and deployed. Definition of Ready describes the conditions that must be true before work enters a sprint — the story is estimated, acceptance criteria are written, dependencies are resolved, and designs are finalized. Both exist to prevent work that isn't actually ready from being started and work that isn't actually done from being called complete.

**Common misuse:** Treating "shipped to production" as the definition of done. A feature that's deployed but not instrumented, not documented, and not monitored is not done — it's in an unknown state. If the team can't measure whether the feature is working, answer a customer support question about it, or understand what happens when it fails, the feature isn't done. PMs who accept "shipped" as done create instrumentation and documentation debt that compounds with every subsequent launch.

---

**Kill criteria**
Kill criteria are the pre-agreed conditions under which a project, experiment, or feature will be stopped or abandoned — defined before work begins, not after the team is emotionally invested in the outcome. They might be a time threshold ("if we haven't reached 10% adoption in 60 days"), a metric threshold ("if satisfaction drops below baseline"), or a technical threshold ("if the error rate exceeds 2%"). Most teams don't write kill criteria because writing them requires admitting in advance that the work might fail.

**Common misuse:** Treating kill criteria as a procedural formality rather than a commitment device. Kill criteria only work if they're honored. A team that sets criteria and then negotiates away from them when the deadline arrives has achieved nothing except the appearance of rigor. The value of kill criteria is that they move the hard conversation about failure from the moment of failure (when sunk cost bias is at its peak) to the moment of commitment (when the decision can be made dispassionately).

---

**Launch vs. release**
A release is the act of deploying code to production — making a feature technically available. A launch is the coordinated go-to-market moment: the communication plan, the customer announcement, the sales enablement, the support readiness, the measurement plan. These are separate events and can — and often should — happen at different times. Features can be released behind a flag long before they're launched; some features are launched without ceremony because they're small iterations. Conflating them creates launches that aren't ready and releases that are treated as launches.

**Common misuse:** Using "ship it" as the end of the product process. The feature going to production is the beginning of the product phase — measurement, iteration, and learning start at release, not end there. Teams that treat launch as the finish line create products that ship but never mature.

---

**Instrumentation**
Instrumentation is the practice of adding tracking, logging, and analytics to a feature so that its behavior in production can be measured and understood. It's what makes it possible to know whether a feature is working, who's using it, how, and with what outcome. The principle: instrumentation should be designed and implemented before launch, not after. Post-launch instrumentation misses the baseline data needed to understand change, requires a second deployment cycle, and often gets deprioritized because the team has already moved on.

**Common misuse:** Treating instrumentation as optional or post-launch work. A feature without instrumentation is a hypothesis that can never be tested. The most common rationalization is "we'll add tracking in the next sprint" — this reliably doesn't happen. Every launch without instrumentation is an investment in a feature whose impact will never be known.

---

**Rollback plan**
A rollback plan is a pre-defined procedure for reverting a production change if it causes problems — typically returning to the previous version of code, configuration, or data. For feature flags, rollback is often a configuration change; for data migrations, it may require reverting transformations or restoring from backup. The plan should specify who has authority to initiate a rollback, what the trigger conditions are, how long the rollback window is, and what happens to data created between deployment and rollback.

**Common misuse:** Confusing "we can roll back the code" with "we have a rollback plan." Code rollback is the easy part. Data rollback — undoing side effects, database changes, and state mutations caused by the deployed code — is where most rollback plans fail. Any feature that writes new data, changes existing records, or triggers downstream processes needs an explicit data rollback strategy, not just a deployment revert.

---

## Org & Process

**DRI (Directly Responsible Individual)**
The DRI is the single person accountable for the outcome of a decision or deliverable — not the whole team, not the committee, not the manager. There may be many contributors, many reviewers, and many stakeholders, but there is exactly one DRI who is responsible for making sure the thing actually happens and who owns the outcome. The DRI model exists to prevent diffused accountability, where everyone feels partially responsible and no one feels fully responsible.

**Common misuse:** Assigning a DRI without giving them decision authority. A DRI who must get approval from three stakeholders before making any significant call isn't a DRI — they're a coordinator with accountability but not authority. The DRI model only works when the DRI has the authority to make the decisions within their scope. Otherwise, it's accountability theater that creates frustration without improving outcomes.

---

**RACI**
RACI is an accountability framework that defines four roles for any decision or deliverable: Responsible (the person doing the work), Accountable (the person who owns the outcome — only one per item), Consulted (people whose input is sought before decisions are made), and Informed (people who need to know the outcome after decisions are made). It's designed to make decision rights explicit and prevent both confusion about ownership and unnecessary involvement of people who don't need to weigh in.

**Common misuse:** Using RACI to document accountability rather than to clarify it before problems occur. RACI charts are most often created after a project has already experienced confusion about ownership — they're retroactive documentation of what should have been established upfront. More critically, RACI tends to fail when too many people are listed as Accountable (violating the one-owner rule) or when everyone ends up in Consulted for everything, which reproduces the decision-by-committee problem the framework was meant to solve.

---

**Two-pizza team**
The two-pizza rule, associated with Amazon, holds that a team should be small enough to be fed by two pizzas — roughly six to ten people. The principle is that small teams move faster, communicate more directly, have lower coordination overhead, and maintain clearer ownership. It's a heuristic for organizational design, not a precise formula.

**Common misuse:** Using the two-pizza rule as a justification for team fragmentation without considering team dependencies. Small teams that are tightly coupled — where one team cannot ship without coordination with three others — are not actually autonomous, regardless of their headcount. The principle behind the two-pizza rule is autonomy, not just size. A team of eight that must get sign-off from five stakeholders before deploying is larger than a team of eight with full ownership of their surface area, in every way that matters.

---

**Conway's Law**
Conway's Law, articulated by Melvin Conway in 1967, states that organizations design systems that mirror their own communication structure. A company with three engineering teams building a product will produce a product with three distinct components, whether or not that's the right architecture for the product. The law operates whether or not it's recognized — org structure shapes product architecture whether teams intend it to or not.

**Common misuse:** Treating Conway's Law as a caution rather than as an actionable design principle. The Inverse Conway Maneuver — deliberately designing your organization to match the architecture you want to produce — is a legitimate approach to organizational and product design. If you want loosely coupled microservices, you need loosely coupled teams with clear ownership boundaries. If teams are tightly coupled in their communication patterns, their systems will be too, regardless of architectural intent.

---

**Team Topologies types**
Team Topologies (Matthew Skelton and Manuel Pais) defines four fundamental team types for modern software organizations. Stream-aligned teams are organized around a flow of work — a product, a user journey, or a business domain — and are the primary value-delivery teams in the organization. Platform teams build and operate internal platforms that stream-aligned teams use; they enable other teams rather than delivering end-user value directly. Enabling teams are temporary or ongoing teams that help stream-aligned teams adopt new capabilities, practices, or technologies — they transfer capability and then step back. Complicated-subsystem teams own highly specialized components that require deep expertise to build and maintain, and they exist to reduce the cognitive load of stream-aligned teams that would otherwise need to become specialists themselves.

**Common misuse:** Labeling existing teams with Team Topologies terminology without changing how they operate. Calling an infrastructure team a "platform team" while it continues to operate as an internal service team with no product mindset, no external interface, and no accountability to developer experience changes nothing about how work flows. Team Topologies is a structural and cultural model — the value comes from the operating model, not the label.

---

## A Note on Precision in PM Language

Precision in PM language matters not because vocabulary is important, but because imprecise terms lead to imprecise decisions. When a team argues about whether a metric is a "North Star," they're usually arguing about what the product is actually for. When a team debates whether something is a "platform," they're really debating the investment model, the customer, and the success criteria. Clarify the definition; clarify the strategy. The terminology is just the shortcut to the real question underneath.
