"""
PM Interview Prep Agent — Streamlit UI.
Run: streamlit run app.py
Requires ANTHROPIC_API_KEY in .env or sidebar input.
"""

import os

import anthropic
import streamlit as st
from dotenv import load_dotenv

from agent import (
    compile_prep_guide_stream,
    generate_company_brief,
    generate_interview_themes,
    generate_questions_by_theme,
    save_prep_guide,
)

load_dotenv()

ROLE_LEVELS = [
    "IC4",
    "IC5 / Staff",
    "Senior Staff",
    "Director",
    "Group PM",
]

st.set_page_config(
    page_title="PM Interview Prep",
    page_icon="🎯",
    layout="wide",
)


def _init_session_state() -> None:
    defaults = {
        "prep_complete": False,
        "brief": "",
        "themes": [],
        "questions": {},
        "guide": "",
        "guide_company": "",
        "guide_level": "",
        "error": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _reset_state() -> None:
    st.session_state.prep_complete = False
    st.session_state.brief = ""
    st.session_state.themes = []
    st.session_state.questions = {}
    st.session_state.guide = ""
    st.session_state.guide_company = ""
    st.session_state.guide_level = ""
    st.session_state.error = None


_init_session_state()

# --- SIDEBAR ---
with st.sidebar:
    st.title("PM Interview Prep")
    st.markdown(
        "Generates a tailored prep guide using Claude. "
        "Saves to `portfolio/interview-prep/`."
    )
    st.divider()

    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        help="Get your key at console.anthropic.com",
    )

    st.divider()
    if st.session_state.prep_complete:
        st.success("Guide ready")
    else:
        st.markdown("**Status:** Ready")

# --- MAIN ---
st.title("PM Interview Prep")

col_company, col_level = st.columns([3, 1])

with col_company:
    company_input = st.text_input(
        "Target company",
        placeholder="e.g., Stripe, Notion, Datadog",
    )

with col_level:
    role_level = st.selectbox("Role level", options=ROLE_LEVELS)

can_run = bool(company_input and api_key)
run_button = st.button("Generate Prep Guide", type="primary", disabled=not can_run)

if not api_key:
    st.caption("Enter your Anthropic API key in the sidebar.")
elif not company_input:
    st.caption("Enter a target company above.")

# --- EXECUTION ---
if run_button and can_run:
    _reset_state()
    st.session_state.guide_company = company_input
    st.session_state.guide_level = role_level

    client = anthropic.Anthropic(api_key=api_key)
    progress = st.progress(0, text="Starting...")
    status = st.empty()

    try:
        status.markdown(f"**Step 1 / 4** — Researching {company_input} PM culture...")
        brief = generate_company_brief(client, company_input, role_level)
        st.session_state.brief = brief
        progress.progress(1 / 5, text="Company brief ready")

        status.markdown("**Step 2 / 4** — Identifying interview themes...")
        themes = generate_interview_themes(client, company_input, role_level, brief)
        st.session_state.themes = themes
        progress.progress(2 / 5, text="Themes identified")

        status.markdown("**Step 3 / 4** — Generating questions by theme...")
        questions = generate_questions_by_theme(client, company_input, role_level, themes)
        st.session_state.questions = questions
        progress.progress(3 / 5, text="Questions ready")

        status.markdown("**Step 4 / 4** — Compiling prep guide...")
        guide_area = st.empty()
        full_guide = ""

        with compile_prep_guide_stream(
            client, company_input, role_level, brief, themes, questions
        ) as stream:
            for text in stream.text_stream:
                full_guide += text
                guide_area.markdown(full_guide)

        st.session_state.guide = full_guide
        st.session_state.prep_complete = True
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
    except ValueError as e:
        st.session_state.error = f"Generation error: {e}"
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
if st.session_state.prep_complete and st.session_state.guide:
    st.divider()

    col_save, col_dl, _ = st.columns([1, 1, 4])

    with col_save:
        if st.button("Save to Portfolio", type="secondary"):
            try:
                saved_path = save_prep_guide(
                    st.session_state.guide_company,
                    st.session_state.guide_level,
                    st.session_state.guide,
                )
                st.success(f"Saved: `{saved_path.name}`")
            except OSError as e:
                st.error(f"Save failed: {e}")

    with col_dl:
        slug = st.session_state.guide_company[:30].replace(" ", "-")
        st.download_button(
            label="Download .md",
            data=st.session_state.guide.encode("utf-8"),
            file_name=f"{slug}-prep.md",
            mime="text/markdown",
        )

    st.markdown(st.session_state.guide)
