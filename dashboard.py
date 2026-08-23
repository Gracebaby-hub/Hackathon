import os
import streamlit as st
from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel
from tools import (
    audit_subscriptions_and_usage,
    stage_cancellation_action,
    execute_preauthorized_trial_cutoff,
    rebalance_savings_to_wishlist,
    execute_confirmed_action
)

load_dotenv()

st.set_page_config(
    page_title="Paddy — Autonomous Subscription Monitor",
    page_icon="🛡️",
    layout="wide"
)

# Initialize Multi-Agent Squad
@st.cache_resource
def get_paddy_squad():
    model = BedrockModel(
        model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        streaming=False
    )

    # 1. Enyi m (Telemetry Analyst)
    enyi_m = Agent(
        model=model,
        system_prompt="""
        You are 'Enyi m', the Telemetry & Usage Specialist.
        Your job is to examine subscription telemetry via `audit_subscriptions_and_usage`,
        evaluating hours spent, cost-per-hour ROI, and identifying dormant vs. active subscriptions.
        """,
        tools=[audit_subscriptions_and_usage]
    )

    # 2. Ore mi (Action Execution Specialist)
    ore_mi = Agent(
        model=model,
        system_prompt="""
        You are 'Ore mi', the Action & Execution Specialist.
        Your responsibilities:
        1. Auto-terminate expiring trials via `execute_preauthorized_trial_cutoff`.
        2. Stage decisions that are waiting for your approval using `stage_cancellation_action`.
        3. Execute user-confirmed actions via `execute_confirmed_action`.
        """,
        tools=[
            stage_cancellation_action,
            execute_preauthorized_trial_cutoff,
            execute_confirmed_action
        ]
    )

    # 3. Aboki na (Rebalance & Wishlist Specialist)
    aboki_na = Agent(
        model=model,
        system_prompt="""
        You are 'Aboki na', the Financial Rebalancing Specialist.
        Calculate how freed-up funds accelerate the user's wishlist goals using `rebalance_savings_to_wishlist`.
        """,
        tools=[rebalance_savings_to_wishlist]
    )

    # 4. Paddy (Lead Coordinator)
    paddy = Agent(
        model=model,
        system_prompt="""
        You are 'Paddy', the user's intelligent Everyday Financial Co-Pilot.
        You coordinate your trusted squad:
        - Enyi m (analyzes usage & waste)
        - Ore mi (takes safe execution steps and stages items waiting for your approval)
        - Aboki na (calculates wishlist goal acceleration)

        Always refer to decisions needing user action as 'Waiting for your approval'.
        Maintain a supportive, clear, and proactive tone.
        """,
        tools=[
            enyi_m.as_tool(
                name="enyi_m",
                description="Consult Enyi m for telemetry analysis, usage hours, and cost efficiency."
            ),
            ore_mi.as_tool(
                name="ore_mi",
                description="Consult Ore mi to auto-cancel trials, stage approval cards, or execute confirmed actions."
            ),
            aboki_na.as_tool(
                name="aboki_na",
                description="Consult Aboki na to map monthly savings toward wishlist goals."
            )
        ]
    )
    return paddy

paddy = get_paddy_squad()

# Main Header
st.title("🛡️ Paddy — Your Smart Subscription Co-Pilot")
st.caption("Powered by Amazon Bedrock & Multi-Agent Squad: Enyi m 🔍 | Ore mi ⚡ | Aboki na 💰")

# Sidebar
with st.sidebar:
    st.header("⚡ Paddy Control Hub")
    st.info("Paddy monitors your subscriptions in the background so you never leak cash.")
    
    if st.button("🚀 Run Scheduled Audit", use_container_width=True, type="primary"):
        with st.spinner("Paddy is coordinating with Enyi m, Ore mi, and Aboki na..."):
            prompt = (
                "Run the scheduled monthly subscription audit. Ask Enyi m to analyze usage, "
                "have Ore mi auto-cancel trials and stage items waiting for your approval, "
                "and have Aboki na calculate wishlist acceleration."
            )
            response = paddy(prompt)
            if "messages" not in st.session_state:
                st.session_state.messages = []
            st.session_state.messages.append({"role": "assistant", "content": str(response)})

    st.divider()
    st.subheader("👥 Your Agent Squad")
    st.markdown("""
    - 🔍 **Enyi m**: Usage & Telemetry Analyst
    - ⚡ **Ore mi**: Execution & Action Guard
    - 💰 **Aboki na**: Wishlist & Savings Rebalancer
    """)

# Main Content Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Portfolio & Savings Overview")
    m1, m2, m3 = st.columns(3)
    m1.metric("Active Plans", "4", "-2 Optimized")
    m2.metric("Monthly Waste", "$83.98", "Reallocatable")
    m3.metric("Annual Savings", "$1,007.76", "+100% Impact")

    st.markdown("---")
    st.subheader("⏳ Waiting for Your Approval")

    c1, c2 = st.columns(2)
    with c1:
        st.error("🔴 **FitPulse Gym App**\n\n*45 days dormant ($29.99/mo)*")
        if st.button("Approve Cancel (FitPulse)", key="btn_fitpulse", use_container_width=True):
            with st.spinner("Ore mi is processing the cancellation..."):
                res = paddy("Please execute immediate cancellation for FitPulse Gym & Fitness App.")
                st.session_state.messages.append({"role": "assistant", "content": str(res)})
                st.rerun()

    with c2:
        st.warning("🟡 **StreamFlix Premium**\n\n*1.5 hrs used ($19.99/mo)*")
        if st.button("Approve Downgrade (StreamFlix)", key="btn_streamflix", use_container_width=True):
            with st.spinner("Ore mi is processing the tier downgrade..."):
                res = paddy("Please execute downgrade for StreamFlix Premium to Basic tier.")
                st.session_state.messages.append({"role": "assistant", "content": str(res)})
                st.rerun()

with col2:
    st.subheader("💬 Chat with Paddy & Squad")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am **Paddy**, your financial co-pilot. Click **'Run Scheduled Audit'** or type a message below to review subscriptions with **Enyi m**, **Ore mi**, and **Aboki na**."}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask Paddy (e.g., 'Cancel FitPulse', 'Check wishlist impact')..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Paddy is on it..."):
                response = paddy(prompt)
                st.markdown(str(response))
                st.session_state.messages.append({"role": "assistant", "content": str(response)})