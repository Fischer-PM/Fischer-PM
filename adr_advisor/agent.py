"""
ADR Advisor — Claude API orchestration layer.
Generates Architecture Decision Records in the style of the existing
portfolio ADRs (retrospective voice, Mermaid diagrams, honest consequences).
No Streamlit dependencies.
"""

import re
from datetime import date, timedelta
from pathlib import Path
from random import choice

import anthropic

GENERATED_ADRS_DIR = Path(__file__).parent.parent / "portfolio" / "generated-adrs"
MODEL = "claude-sonnet-4-6"

# Fictional company names matching the portfolio's style
FICTIONAL_COMPANIES = [
    "Vantara", "Nexar", "Cordia", "Prism", "Halcyon",
    "Meridian", "Stratum", "Celeris", "Orion", "Luminal",
]

SYSTEM_PROMPT = """You are a senior platform PM writing Architecture Decision Records for a portfolio. \
Your ADRs follow a specific style based on these characteristics of the existing ADR library:

Voice and structure:
- Written in retrospective voice — the decision was made 6–12 months ago and you are documenting \
what happened, including what went wrong
- Status section names a real operational outcome, not just "Accepted"
- Architecture section includes a Mermaid flowchart diagram (before/after or topology)
- Context section presents exactly 3 lettered options (Option A, Option B, Option C) with trade-offs
- Decision section names the chosen option and argues against the alternatives explicitly
- Consequences section has three subsections: "What worked", "What we got wrong", and "What persists"
- "What we got wrong" includes a named incident with specifics: timeline, detection vector, \
number of users affected, or other concrete detail
- "What persists" is honest about the lasting constraint the decision introduced

Tone:
- PM-practitioner voice, not academic
- Numbers and specifics wherever plausible (even if illustrative)
- Honest about organizational friction, timeline overruns, and unintended consequences
- No hedging language — assertions about what happened, not speculation about what might"""


def _cached_system() -> list[dict]:
    return [
        {
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }
    ]


def suggest_company_name() -> str:
    return choice(FICTIONAL_COMPANIES)


def analyze_decision(
    client: anthropic.Anthropic,
    decision_text: str,
    domain: str,
) -> str:
    """
    Call 1. Extracts the core problem, identifies 3 natural options,
    and surfaces the primary forcing function behind the decision.
    Returns structured analysis text used as context for the ADR generation.
    """
    prompt = (
        f"Domain: {domain}\n"
        f"Decision to document: {decision_text}\n\n"
        "Analyze this architectural decision. Return:\n\n"
        "PROBLEM: [One sentence — what operational or product pressure forced this decision]\n\n"
        "OPTION A: [Name] — [2-sentence description of this approach and its primary trade-off]\n"
        "OPTION B: [Name] — [2-sentence description]\n"
        "OPTION C: [Name] — [2-sentence description]\n\n"
        "RECOMMENDED: [A, B, or C] — [One sentence on why this is the strongest choice]\n\n"
        "FORCING FUNCTION: [What made the status quo untenable — the specific trigger]\n\n"
        "Be specific to the domain. Name real technologies, patterns, or constraints where relevant."
    )
    response = client.messages.create(
        model=MODEL,
        max_tokens=700,
        system=_cached_system(),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


def generate_adr_stream(
    client: anthropic.Anthropic,
    decision_text: str,
    company_name: str,
    domain: str,
    analysis: str,
):
    """
    Call 2 (streamed). Generates the full ADR document.
    Returns a streaming context manager — iterate over .text_stream.

    The ADR is written in retrospective voice as if accepted ~9 months ago.
    Includes a Mermaid architecture diagram and a named incident in Consequences.
    """
    # Set a plausible retrospective acceptance date
    acceptance_date = date.today() - timedelta(days=270)
    acceptance_str = acceptance_date.strftime("%B %Y")

    prompt = (
        f"Write a complete Architecture Decision Record for {company_name}.\n\n"
        f"Decision: {decision_text}\n"
        f"Domain: {domain}\n"
        f"Acceptance date (retrospective): {acceptance_str}\n\n"
        f"Analysis:\n{analysis}\n\n"
        "Generate the full ADR using this exact structure:\n\n"
        "---\n\n"
        f"# ADR: [Concise decision title]\n"
        f"*{company_name} — internal architecture decision record*\n\n"
        "## Status\n"
        f"Accepted — {acceptance_str}. [One sentence on the operational outcome 9 months later — "
        "include one honest note about something that didn't go as expected.]\n\n"
        "## Architecture: Before and After\n\n"
        "```mermaid\n"
        "[flowchart LR or TD diagram showing before-state on the left/top "
        "and after-state on the right/bottom. Use real service/component names "
        "relevant to the domain. 6–10 nodes.]\n"
        "```\n\n"
        "*[One sentence caption explaining what the diagram shows and what changed.]*\n\n"
        "## Context\n\n"
        "[3–4 paragraph narrative: the problem, what made the status quo untenable, "
        "and the constraints that shaped the options. Then present the three options:]\n\n"
        "**Option A — [Name]:** [Description + trade-offs]\n\n"
        "**Option B — [Name]:** [Description + trade-offs]\n\n"
        "**Option C — [Name]:** [Description + trade-offs]\n\n"
        "## Decision\n\n"
        "[Chosen option stated clearly in the first sentence. Then 2–3 paragraphs arguing "
        "against the alternatives — why they were rejected, not just what they were.]\n\n"
        "## Consequences\n\n"
        "### What worked\n\n"
        "[2–3 specific operational improvements with concrete signals: latency numbers, "
        "incident reduction, team velocity, etc.]\n\n"
        "### What we got wrong\n\n"
        "[A named incident or failure mode that emerged. Include: what happened, "
        "when it was detected, what the impact was (users affected, duration, data), "
        "and what the root cause turned out to be.]\n\n"
        "### What persists\n\n"
        "[The lasting constraint or complexity this decision introduced — the thing "
        "the team still navigates today. Be honest that this is a real trade-off, "
        "not a temporary limitation that will be resolved.]\n"
    )

    return client.messages.stream(
        model=MODEL,
        max_tokens=3000,
        system=_cached_system(),
        messages=[{"role": "user", "content": prompt}],
    )


def save_adr(company_name: str, decision_text: str, content: str) -> Path:
    """Saves to portfolio/generated-adrs/<company-slug>-<decision-slug>-<date>.md"""
    GENERATED_ADRS_DIR.mkdir(parents=True, exist_ok=True)
    company_slug = re.sub(r"[^a-z0-9]+", "-", company_name.lower()).strip("-")
    decision_slug = re.sub(r"[^a-z0-9]+", "-", decision_text.lower()).strip("-")[:40]
    filename = f"{company_slug}-{decision_slug}-{date.today().isoformat()}.md"
    path = GENERATED_ADRS_DIR / filename
    path.write_text(content, encoding="utf-8")
    return path
