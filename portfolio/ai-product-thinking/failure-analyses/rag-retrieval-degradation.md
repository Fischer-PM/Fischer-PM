# How RAG Retrieval Quality Degraded at Scale

*Simulated failure analysis — fictional product (Helix), representative of real patterns in production RAG deployments.*

---

The system worked well at launch. Twelve months later it was giving worse answers than a keyword search. The retrieval architecture hadn't changed. The knowledge base had grown.

---

## What Happened

Helix was a customer support AI built on retrieval-augmented generation. Customers asked questions; Helix retrieved relevant content from a knowledge base of ~4,000 articles and generated a response. At launch, answer quality — measured by resolution rate and customer satisfaction on AI-handled tickets — was strong enough to justify automated handling of 45% of inbound volume.

Twelve months post-launch: the knowledge base had grown to 11,000 articles. Resolution rate on AI-handled tickets had dropped from 74% to 61%. Customer satisfaction on AI-handled tickets had declined. The ops team was routing an increasing share of previously auto-handled tickets back to human agents.

The model hadn't changed. The retrieval system hadn't changed. The chunk size and embedding model were unchanged. The knowledge base had grown.

---

## Root Cause: Retrieval Precision Degrades as the Corpus Grows

RAG retrieval is a similarity search: given a query, retrieve the top-k most similar chunks from the corpus. When the corpus is small, the top-k chunks are likely to be genuinely relevant. When the corpus is large, the top-k chunks include more near-matches — documents that are semantically adjacent to the query but don't contain the answer.

The generator (LLM) receives the retrieved chunks as context. When the retrieved context contains the answer, the generator produces a correct response. When the retrieved context contains near-matches but not the answer, the generator synthesizes a plausible response from adjacent information — which is often wrong in ways that aren't obviously wrong. The output reads as confident and well-structured. It's just not correct.

Three compounding factors made this worse at Helix:

**Duplicate content.** As the knowledge base grew, articles were added that substantially overlapped with existing articles. The same troubleshooting steps appeared in four different articles across different product lines. Retrieval would pull two or three of these and fill the context window with redundant information, leaving less room for genuinely relevant content.

**Article age and freshness.** The knowledge base contained articles written at product launch alongside articles written eighteen months later. When a product feature had changed, both the old article and the new article appeared in the corpus. Retrieval had no freshness signal — a two-year-old article describing deprecated behavior was equally likely to be retrieved as the current documentation.

**Query distribution shift.** Customer questions changed as the product matured. Early customer questions were basic ("how do I connect X"). Later customer questions were more complex and specific ("why does X fail when Y is configured"). The knowledge base had been built and evaluated against the early question distribution. Complex, specific questions retrieved less relevant content because the knowledge base didn't have high-density coverage of edge cases.

---

## What the PM Should Have Caught

**Retrieval quality wasn't measured separately from answer quality.** The operational dashboard tracked resolution rate and CSAT — outcomes. It didn't track retrieval precision: given this query, did the top-k retrieved chunks contain the answer? Those are different things. A drop in retrieval precision is a leading indicator for a drop in answer quality, and it would have shown the degradation trend months earlier.

**The knowledge base had no quality control process.** Articles were added without a review for overlap with existing content, freshness of existing articles, or coverage of the query types being handled. The assumption was that more content was better. In a RAG system, more content is only better if the retrieval mechanism can distinguish the relevant content from the noise. Without quality control, content growth degrades retrieval precision.

**The eval set hadn't been updated.** The system was being evaluated against a fixed set of test questions written at launch. Those questions were representative of early user queries. They weren't representative of the complex, specific queries that were actually coming in at month 12. The eval showed stable accuracy on questions the system had always handled well, while degrading on questions the eval didn't include.

---

## What Recovery Required

The team ran a retrieval audit: for a sample of 500 real customer queries, they manually reviewed what was retrieved and assessed whether the retrieved chunks contained the answer. Retrieval precision on complex queries was 41% — less than half of complex queries were being answered from actually relevant retrieved content.

The remediation had three components:

**Content deduplication and freshness tagging.** Duplicate and substantially overlapping articles were merged or removed. Articles were tagged with a last-validated date; articles older than 12 months without a review were flagged for content team review. This reduced the corpus from 11,000 to 7,200 articles and improved retrieval precision on complex queries to 67%.

**Query-type routing.** Complex, specific queries were detected and either routed to human agents or handled with a different retrieval configuration (larger k, re-ranking). Rather than trying to make the RAG system handle everything equally well, the team acknowledged that it performed better on some query types than others and routed accordingly.

**Eval set refresh.** The evaluation set was rebuilt quarterly using real queries from the previous 90 days, stratified by complexity and category. Accuracy targets were set per query type, not in aggregate.

---

## The Durable Lesson

A RAG system's performance is a function of corpus quality as much as model capability. Growing the corpus without managing retrieval quality is how you build a system that gets worse as it scales.

The monitoring requirement: retrieval precision per query type, tracked continuously, with separate thresholds by complexity. That metric tells you whether the retrieval layer is working before the answer quality metrics tell you it isn't.
