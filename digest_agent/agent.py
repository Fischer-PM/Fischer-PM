"""
PM Digest Generator — Claude API orchestration layer.
No Streamlit dependencies. All functions independently testable.
"""

import re
from datetime import date
from pathlib import Path

import anthropic

DIGESTS_DIR = Path(__file__).parent.parent / "portfolio" / "digests"
MODEL = "claude-sonnet-4-6"
MAX_TOKENS_TOPIC = 600
MAX_TOKENS_COMPILE = 3000

SYSTEM_PROMPT = """You are a senior PM analyst writing a weekly briefing for a practitioner audience. \
The reader is a platform PM focused on developer ecosystems, messaging infrastructure, and AI products.

Writing principles:
- "What moved" means a concrete signal, not a category update — name the specific thing
- Strategic implication is PM-centric: what does this mean for how you build, price, or position?
- Open questions are specific and answerable — not "further research needed"
- Acknowledge knowledge cutoff honestly when relevant: Claude's training has a cutoff date, \
so treat recent signals as directional, not confirmed
- No filler: no "it is worth noting," "this highlights," or "in conclusion"
- Tone is collegial and direct — written for someone who reads this at 7am with coffee"""


def _cached_system() -> list[dict]:
    return [
        {
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }
    ]


def research_topic(
    client: anthropic.Anthropic,
    topic: str,
    time_horizon: str,
) -> str:
    """
    One call per topic. Returns structured prose covering what moved,
    why it matters, and the open question. max_tokens=600.
    """
    prompt = (
        f"Topic: {topic}\n"
        f"Time horizon: {time_horizon}\n\n"
        "Write a briefing entry for this topic covering:\n"
        "1. **What moved** — the most significant concrete signal or development "
        f"in this space {time_horizon.lower()}. If your training knowledge doesn't "
        "cover this period, note that and give the most recent directional signal you have.\n"
        "2. **Why it matters for PMs** — the strategic implication, specifically for "
        "someone building platform products, developer tools, or API infrastructure\n"
        "3. **Open question** — one specific, tractable question this surfaces\n\n"
        "Use those three headers. 2–3 sentences per section. No preamble."
    )
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS_TOPIC,
        system=_cached_system(),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


def compile_digest_stream(
    client: anthropic.Anthropic,
    topics: list[str],
    findings: list[str],
    time_horizon: str,
):
    """
    Final call (streamed). Assembles the full digest with cross-cutting themes.
    Returns a streaming context manager — iterate over .text_stream.
    """
    digest_date = date.today().isoformat()
    topics_list = ", ".join(topics)

    findings_block = "\n\n---\n\n".join(
        f"## {topic}\n\n{finding}"
        for topic, finding in zip(topics, findings)
    )

    prompt = (
        f"Compile a PM digest from the following topic briefings.\n\n"
        f"Date: {digest_date}\n"
        f"Topics: {topics_list}\n"
        f"Horizon: {time_horizon}\n\n"
        "Use this structure exactly:\n\n"
        f"# PM Digest — {digest_date}\n"
        f"*Topics: {topics_list} | Horizon: {time_horizon}*\n"
        "*Note: Based on Claude's training knowledge — verify specifics before acting on them.*\n\n"
        "## Cross-Cutting Themes\n"
        "[1–2 paragraphs on what connects this week's topics. "
        "What common dynamic is playing out across them?]\n\n"
        "[Then one section per topic, using the briefings below as raw material. "
        "Keep the three-header structure (What moved / Why it matters / Open question) "
        "but synthesize and sharpen the prose.]\n\n"
        "## What to Watch\n"
        "[2–3 specific forward-looking signals across all topics — "
        "the things worth monitoring over the next 30–60 days]\n\n"
        "---\n\n"
        f"RAW BRIEFINGS:\n\n{findings_block}"
    )

    return client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS_COMPILE,
        system=_cached_system(),
        messages=[{"role": "user", "content": prompt}],
    )


def save_digest(topics: list[str], content: str) -> Path:
    """Saves to portfolio/digests/digest-<date>.md"""
    DIGESTS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"digest-{date.today().isoformat()}.md"
    path = DIGESTS_DIR / filename
    path.write_text(content, encoding="utf-8")
    return path


def parse_topics(raw: str) -> list[str]:
    """Parses comma-separated or newline-separated topic list. Returns up to 6 topics."""
    if "," in raw:
        topics = [t.strip() for t in raw.split(",")]
    else:
        topics = [t.strip() for t in raw.splitlines()]
    return [t for t in topics if t][:6]
