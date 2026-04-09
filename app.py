"""
pm-decision-copilot — Streamlit UI entry point.

Usage:
    streamlit run app.py
"""

import streamlit as st
from core.orchestrator import Orchestrator

st.set_page_config(
    page_title="PM Decision Copilot",
    page_icon="🧭",
    layout="wide",
)

st.title("PM Decision Copilot")
st.caption("Multi-agent framework: Discovery → Analysis → Critique")

with st.sidebar:
    st.header("How it works")
    st.markdown(
        """
        1. **Discovery** — surfaces context & assumptions
        2. **Analysis** — evaluates options with PM frameworks
        3. **Critique** — stress-tests the recommendation
           _(loops back if confidence score is low)_
        """
    )

problem = st.text_area(
    "Describe the PM decision or problem you need help with:",
    height=150,
    placeholder="e.g. We're debating whether to build a native mobile app or double down on our PWA...",
)

if st.button("Run Copilot", type="primary", disabled=not problem.strip()):
    with st.spinner("Running agents..."):
        orchestrator = Orchestrator()
        result = orchestrator.run(problem.strip())

    st.subheader("Discovery")
    st.json(result.get("problem_brief", {}))

    st.subheader("Analysis")
    st.json(result.get("analysis", {}))

    st.subheader("Critique")
    critique = result.get("critique", {})
    score = critique.get("score", "—")
    passes = critique.get("passes", False)
    st.metric("Confidence Score", f"{score} / 10", delta="Pass" if passes else "Retry")
    st.json(critique)

    iterations = result.get("iterations", 1)
    if iterations > 1:
        st.info(f"Pipeline ran {iterations} iteration(s) to reach this recommendation.")
