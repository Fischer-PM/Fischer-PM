"""
PM Research Agent — Streamlit UI and orchestration layer.
Imports from agent.py for all Claude API logic.

Run:
    streamlit run app.py

Requires:
    ANTHROPIC_API_KEY set in .env or entered via the sidebar.
"""

import os

import anthropic
import streamlit as st
from dotenv import load_dotenv

from agent import (
    compile_report_stream,
    generate_research_questions,
    research_question,
    save_report,
)

load_dotenv()

RESEARCH_TYPES = [
    "Competitive Analysis",
    "Feature Teardown",
    "Market Sizing",
    "Tech Architecture Review",
    "Strategy Review",
]

st.set_page_config(
    page_title="PM Research Agent",
    page_icon="🔍",
    layout="wide",
)


def _init_session_state() -> None:
    defaults = {
        "research_complete": False,
        "questions": [],
        "findings": [],
        "report": "",
        "report_topic": "",
        "report_type": "",
        "error": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _reset_state() -> None:
    st.session_state.research_complete = False
    st.session_state.questions = []
    st.session_state.findings = []
    st.session_state.report = ""
    st.session_state.report_topic = ""
    st.session_state.report_type = ""
    st.session_state.error = None


_init_session_state()

# --- SIDEBAR ---
with st.sidebar:
    st.title("PM Research Agent")
    st.markdown(
        "Generates PM-style research reports using Claude. "
        "Reports are saved to `portfolio/research-reports/`."
    )
    st.divider()

    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        help="Get your key at console.anthropic.com. Or set ANTHROPIC_API_KEY in .env.",
    )

    st.divider()

    if st.session_state.research_complete:
        st.success("Research complete")
    else:
        st.markdown("**Status:** Ready")

    st.divider()
    st.markdown(
        "**Cost estimate**\n\n"
        "~$0.05–0.10 per run (Sonnet with prompt caching).\n\n"
        "Prompt caching applies across all 6 API calls — "
        "only the first call pays full system-prompt token cost."
    )

# --- MAIN AREA ---
st.title("PM Research Agent")

col_topic, col_type = st.columns([3, 1])

with col_topic:
    topic_input = st.text_input(
        "Research topic",
        placeholder="e.g., Stripe's competitive position in embedded finance",
    )

with col_type:
    research_type = st.selectbox("Research type", options=RESEARCH_TYPES)

can_run = bool(topic_input and api_key)
run_button = st.button("Generate Report", type="primary", disabled=not can_run)

if not api_key:
    st.caption("Enter your Anthropic API key in the sidebar to continue.")
elif not topic_input:
    st.caption("Enter a research topic above.")

# --- RESEARCH EXECUTION ---
if run_button and can_run:
    _reset_state()
    st.session_state.report_topic = topic_input
    st.session_state.report_type = research_type

    client = anthropic.Anthropic(api_key=api_key)
    progress = st.progress(0, text="Starting research...")
    status = st.empty()

    try:
        # Step 1 — Generate questions
        status.markdown("**Step 1 / 6** — Generating research questions...")
        questions = generate_research_questions(client, topic_input, research_type)
        st.session_state.questions = questions
        progress.progress(1 / 7, text="Research questions ready")

        # Steps 2–6 — Research each question
        findings = []
        for i, question in enumerate(questions):
            status.markdown(
                f"**Step {i + 2} / 6** — Researching: _{question}_"
            )
            finding = research_question(
                client, topic_input, research_type, question, i
            )
            findings.append(finding)
            st.session_state.findings = findings
            progress.progress((i + 2) / 7, text=f"Question {i + 1} of 5 complete")

        # Step 7 — Compile and stream final report
        status.markdown("**Step 6 / 6** — Compiling report...")
        report_area = st.empty()
        full_report = ""

        with compile_report_stream(
            client, topic_input, research_type, questions, findings
        ) as stream:
            for text in stream.text_stream:
                full_report += text
                report_area.markdown(full_report)

        st.session_state.report = full_report
        st.session_state.research_complete = True
        progress.progress(1.0, text="Complete")
        status.empty()

    except anthropic.AuthenticationError:
        st.session_state.error = (
            "API key is invalid. Check your key at console.anthropic.com."
        )
        progress.empty()
        status.empty()
    except anthropic.RateLimitError:
        st.session_state.error = "Rate limit reached. Wait a moment and try again."
        progress.empty()
        status.empty()
    except anthropic.APIConnectionError as e:
        st.session_state.error = f"Connection error: {e}"
        progress.empty()
        status.empty()
    except ValueError as e:
        st.session_state.error = f"Research generation error: {e}"
        progress.empty()
        status.empty()
    except Exception as e:  # noqa: BLE001
        st.session_state.error = f"Unexpected error ({type(e).__name__}): {e}"
        progress.empty()
        status.empty()

# --- ERROR DISPLAY ---
if st.session_state.error:
    st.error(st.session_state.error)

# --- REPORT DISPLAY ---
if st.session_state.research_complete and st.session_state.report:
    st.divider()

    col_save, col_dl, _ = st.columns([1, 1, 4])

    with col_save:
        if st.button("Save to Portfolio", type="secondary"):
            try:
                saved_path = save_report(
                    st.session_state.report_topic,
                    st.session_state.report_type,
                    st.session_state.report,
                )
                st.success(f"Saved: `{saved_path.name}`")
            except OSError as e:
                st.error(f"Save failed: {e}")

    with col_dl:
        topic_slug = st.session_state.report_topic[:40].replace(" ", "-")
        st.download_button(
            label="Download .md",
            data=st.session_state.report.encode("utf-8"),
            file_name=f"{topic_slug}.md",
            mime="text/markdown",
        )

    st.markdown(st.session_state.report)
