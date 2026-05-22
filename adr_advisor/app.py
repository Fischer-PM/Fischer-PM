"""
ADR Advisor — Streamlit UI.
Generates Architecture Decision Records in the style of the existing portfolio ADRs.
Run: streamlit run app.py
Requires ANTHROPIC_API_KEY in .env or sidebar input.
"""

import os

import anthropic
import streamlit as st
from dotenv import load_dotenv

from agent import (
    analyze_decision,
    generate_adr_stream,
    save_adr,
    suggest_company_name,
)

load_dotenv()

DOMAINS = [
    "Messaging / Async",
    "API Design",
    "Data Storage",
    "Auth / Identity",
    "Infrastructure / Compute",
    "Observability",
    "Other",
]

st.set_page_config(
    page_title="ADR Advisor",
    page_icon="📐",
    layout="wide",
)


def _init_session_state() -> None:
    defaults = {
        "adr_complete": False,
        "analysis": "",
        "adr": "",
        "adr_company": "",
        "adr_decision": "",
        "error": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _reset_state() -> None:
    st.session_state.adr_complete = False
    st.session_state.analysis = ""
    st.session_state.adr = ""
    st.session_state.adr_company = ""
    st.session_state.adr_decision = ""
    st.session_state.error = None


_init_session_state()

# --- SIDEBAR ---
with st.sidebar:
    st.title("ADR Advisor")
    st.markdown(
        "Generates Architecture Decision Records in retrospective style — "
        "complete with Mermaid diagrams and honest consequences. "
        "Saves to `portfolio/generated-adrs/`."
    )
    st.divider()

    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        help="Get your key at console.anthropic.com",
    )

    st.divider()
    if st.session_state.adr_complete:
        st.success("ADR ready")
    else:
        st.markdown("**Status:** Ready")

    st.divider()
    st.markdown(
        "**Style reference:** Matches the four existing ADRs in "
        "`portfolio/platform-pm-playbook/adrs/`"
    )

# --- MAIN ---
st.title("ADR Advisor")

decision_input = st.text_area(
    "Describe the architectural decision",
    placeholder=(
        "e.g., We need to decide between synchronous REST calls vs. async queues "
        "for inter-service communication in our notification pipeline. "
        "Currently services call each other directly via HTTP and we're seeing "
        "cascading failures under load."
    ),
    height=120,
)

col_company, col_domain = st.columns([2, 2])

with col_company:
    company_input = st.text_input(
        "Fictional company name",
        placeholder=f"e.g., {suggest_company_name()} (leave blank to auto-assign)",
    )

with col_domain:
    domain = st.selectbox("Domain", options=DOMAINS)

can_run = bool(decision_input and api_key)
run_button = st.button("Generate ADR", type="primary", disabled=not can_run)

if not api_key:
    st.caption("Enter your Anthropic API key in the sidebar.")
elif not decision_input:
    st.caption("Describe the decision above.")

# --- EXECUTION ---
if run_button and can_run:
    _reset_state()

    # Use provided company name or auto-assign one
    company_name = company_input.strip() if company_input.strip() else suggest_company_name()
    st.session_state.adr_company = company_name
    st.session_state.adr_decision = decision_input

    client = anthropic.Anthropic(api_key=api_key)
    progress = st.progress(0, text="Starting...")
    status = st.empty()

    try:
        status.markdown(f"**Step 1 / 2** — Analyzing decision for *{company_name}*...")
        analysis = analyze_decision(client, decision_input, domain)
        st.session_state.analysis = analysis
        progress.progress(1 / 3, text="Analysis complete")

        status.markdown("**Step 2 / 2** — Drafting ADR...")
        adr_area = st.empty()
        full_adr = ""

        with generate_adr_stream(
            client, decision_input, company_name, domain, analysis
        ) as stream:
            for text in stream.text_stream:
                full_adr += text
                adr_area.markdown(full_adr)

        st.session_state.adr = full_adr
        st.session_state.adr_complete = True
        progress.progress(1.0, text="Complete")
        status.empty()

    except anthropic.AuthenticationError:
        st.session_state.error = "API key is invalid."
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
    except Exception as e:  # noqa: BLE001
        st.session_state.error = f"Unexpected error ({type(e).__name__}): {e}"
        progress.empty()
        status.empty()

# --- ERROR ---
if st.session_state.error:
    st.error(st.session_state.error)

# --- OUTPUT ---
if st.session_state.adr_complete and st.session_state.adr:
    st.divider()

    col_save, col_dl, col_analysis, _ = st.columns([1, 1, 1, 3])

    with col_save:
        if st.button("Save to Portfolio", type="secondary"):
            try:
                saved_path = save_adr(
                    st.session_state.adr_company,
                    st.session_state.adr_decision,
                    st.session_state.adr,
                )
                st.success(f"Saved: `{saved_path.name}`")
            except OSError as e:
                st.error(f"Save failed: {e}")

    with col_dl:
        company_slug = st.session_state.adr_company.replace(" ", "-").lower()
        st.download_button(
            label="Download .md",
            data=st.session_state.adr.encode("utf-8"),
            file_name=f"adr-{company_slug}.md",
            mime="text/markdown",
        )

    with col_analysis:
        if st.button("Show Analysis", type="secondary"):
            st.session_state.show_analysis = not st.session_state.get("show_analysis", False)

    if st.session_state.get("show_analysis") and st.session_state.analysis:
        with st.expander("Decision Analysis (Step 1 output)", expanded=True):
            st.markdown(f"```\n{st.session_state.analysis}\n```")

    st.markdown(st.session_state.adr)
