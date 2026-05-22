"""
PM Digest Generator — Streamlit UI.
Run: streamlit run app.py
Requires ANTHROPIC_API_KEY in .env or sidebar input.
"""

import os

import anthropic
import streamlit as st
from dotenv import load_dotenv

from agent import (
    compile_digest_stream,
    parse_topics,
    research_topic,
    save_digest,
)

load_dotenv()

TIME_HORIZONS = ["This week", "This month", "Last quarter"]

st.set_page_config(
    page_title="PM Digest",
    page_icon="📰",
    layout="wide",
)


def _init_session_state() -> None:
    defaults = {
        "digest_complete": False,
        "topics": [],
        "findings": [],
        "digest": "",
        "error": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _reset_state() -> None:
    st.session_state.digest_complete = False
    st.session_state.topics = []
    st.session_state.findings = []
    st.session_state.digest = ""
    st.session_state.error = None


_init_session_state()

# --- SIDEBAR ---
with st.sidebar:
    st.title("PM Digest")
    st.markdown(
        "Generates a PM briefing across multiple topics using Claude. "
        "Saves to `portfolio/digests/`."
    )
    st.divider()

    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        help="Get your key at console.anthropic.com",
    )

    st.divider()
    if st.session_state.digest_complete:
        st.success("Digest ready")
    else:
        st.markdown("**Status:** Ready")

    st.divider()
    st.caption(
        "Based on Claude's training knowledge. "
        "Verify specifics before acting on them."
    )

# --- MAIN ---
st.title("PM Digest Generator")

col_topics, col_horizon = st.columns([3, 1])

with col_topics:
    topics_input = st.text_area(
        "Topics to cover",
        placeholder="One per line, or comma-separated.\ne.g.\nStripe vs. Adyen competitive positioning\nOpenAI API pricing changes\nKafka vs Pulsar adoption trends",
        height=130,
    )

with col_horizon:
    time_horizon = st.selectbox("Time horizon", options=TIME_HORIZONS)
    st.caption("Up to 6 topics.")

topics_parsed = parse_topics(topics_input) if topics_input else []
can_run = bool(topics_parsed and api_key)
run_button = st.button("Generate Digest", type="primary", disabled=not can_run)

if topics_parsed:
    st.caption(f"Topics detected: {', '.join(topics_parsed)}")

if not api_key:
    st.caption("Enter your Anthropic API key in the sidebar.")

# --- EXECUTION ---
if run_button and can_run:
    _reset_state()

    client = anthropic.Anthropic(api_key=api_key)
    total_steps = len(topics_parsed) + 1  # +1 for compile
    progress = st.progress(0, text="Starting...")
    status = st.empty()

    try:
        findings = []
        for i, topic in enumerate(topics_parsed):
            status.markdown(f"**Step {i + 1} / {total_steps}** — Researching: _{topic}_")
            finding = research_topic(client, topic, time_horizon)
            findings.append(finding)
            st.session_state.findings = findings
            progress.progress((i + 1) / (total_steps + 1), text=f"Topic {i + 1} of {len(topics_parsed)} done")

        status.markdown(f"**Step {total_steps} / {total_steps}** — Compiling digest...")
        digest_area = st.empty()
        full_digest = ""

        with compile_digest_stream(client, topics_parsed, findings, time_horizon) as stream:
            for text in stream.text_stream:
                full_digest += text
                digest_area.markdown(full_digest)

        st.session_state.topics = topics_parsed
        st.session_state.digest = full_digest
        st.session_state.digest_complete = True
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
if st.session_state.digest_complete and st.session_state.digest:
    st.divider()

    col_save, col_dl, _ = st.columns([1, 1, 4])

    with col_save:
        if st.button("Save to Portfolio", type="secondary"):
            try:
                saved_path = save_digest(
                    st.session_state.topics,
                    st.session_state.digest,
                )
                st.success(f"Saved: `{saved_path.name}`")
            except OSError as e:
                st.error(f"Save failed: {e}")

    with col_dl:
        st.download_button(
            label="Download .md",
            data=st.session_state.digest.encode("utf-8"),
            file_name=f"pm-digest-{__import__('datetime').date.today().isoformat()}.md",
            mime="text/markdown",
        )

    st.markdown(st.session_state.digest)
