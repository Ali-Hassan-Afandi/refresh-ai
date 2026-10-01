import sys
from pathlib import Path

import streamlit as st

# Make existing backend Python modules importable.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

import os

for key in (
    "GROQ_API_KEY",
    "GROQ_MODEL",
    "SUPABASE_URL",
    "SUPABASE_SERVICE_ROLE_KEY",
    "DEMO_FALLBACK",
):
    if key in st.secrets:
        os.environ[key] = str(st.secrets[key])

from app.models.schemas import StartNegotiationRequest
from app.services.negotiation import start, run_all, approve

st.set_page_config(
    page_title="ReFresh AI",
    page_icon="🌱",
    layout="wide",
)

st.title("🌱 ReFresh AI")
st.caption("Autonomous B2B Perishable Exchange")

st.subheader("At-risk inventory")

col1, col2, col3 = st.columns(3)
col1.metric("Product", "Strawberries")
col2.metric("Available inventory", "50 kg")
col3.metric("Remaining commercial window", "48 hours")

st.divider()

if st.button("Run autonomous negotiation", type="primary"):
    with st.spinner("AI agents are negotiating..."):
        request = StartNegotiationRequest()
        state = start(request)
        state = run_all(state)
        st.session_state["negotiation"] = state

state = st.session_state.get("negotiation")

if state:
    st.subheader("Negotiation Room")

    for offer in state.offers:
        with st.container(border=True):
            st.write(
                f"**{offer.actor.upper()} AGENT** — "
                f"Rs. {offer.price_per_kg:,.0f}/kg"
            )
            st.caption(offer.rationale)

    st.info(f"Transaction status: {state.status}")

    if state.status == "AWAITING_APPROVAL":
        if st.button("Approve transaction"):
            state = approve(state)
            st.session_state["negotiation"] = state
            st.rerun()

    if state.status == "COMPLETED":
        st.success(
            f"Transaction completed: "
            f"{state.agreed_quantity} kg at "
            f"Rs. {state.agreed_price}/kg"
        )