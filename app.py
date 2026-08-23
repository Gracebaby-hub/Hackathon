import os
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

# Shared Bedrock Model instance
model = BedrockModel(
    model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    streaming=False
)

# 1. SPECIALIST: Telemetry & Usage Analyst Agent
analyst_agent = Agent(
    model=model,
    system_prompt="""
    You are the Telemetry & Usage Specialist Agent.
    Your sole focus is to query usage data with `audit_subscriptions_and_usage`,
    analyze cost-per-hour efficiency, and categorize subscriptions by health status
    (Healthy, Dormant Waste, Underutilized, Expiring Trial).
    """,
    tools=[audit_subscriptions_and_usage]
)

# 2. SPECIALIST: Action & Execution Agent
execution_agent = Agent(
    model=model,
    system_prompt="""
    You are the Action & Execution Specialist Agent.
    Your responsibilities:
    1. Cut off expiring trials if auto-cancellation is allowed using `execute_preauthorized_trial_cutoff`.
    2. Stage human approval cards for dormant/underutilized services using `stage_cancellation_action`.
    3. Finalize cancellations/downgrades upon human confirmation using `execute_confirmed_action`.
    """,
    tools=[
        stage_cancellation_action,
        execute_preauthorized_trial_cutoff,
        execute_confirmed_action
    ]
)

# 3. COORDINATOR: Lead Orchestration Agent
coordinator_prompt = """
You are the Lead Subscription Coordinator Agent.
You manage the multi-agent workflow to eliminate recurring subscription waste and safeguard user finances.

Your Workflow:
1. When starting an audit, delegate data analysis to the Telemetry Analyst and action staging to the Execution Agent.
2. Call `rebalance_savings_to_wishlist` to project financial reallocation toward user goals.
3. Present an executive summary detailing auto-executed actions, staged human approval decisions, and budget impact.
4. When the user approves/rejects an action, delegate execution to the Execution Agent and present the final updated savings.
"""

coordinator_agent = Agent(
    model=model,
    system_prompt=coordinator_prompt,
    tools=[
        analyst_agent.as_tool(
            name="telemetry_analyst",
            description="Analyzes subscription activity, logins, usage hours, and cost efficiency metrics."
        ),
        execution_agent.as_tool(
            name="action_executor",
            description="Executes pre-authorized trial cutoffs, stages human-in-the-loop approvals, and applies confirmed cancellations."
        ),
        rebalance_savings_to_wishlist
    ]
)

if __name__ == "__main__":
    print("\n🔍 Initializing Multi-Agent Subscription & Usage Audit System...\n")
    audit_trigger = (
        "Run the scheduled subscription audit. Have the telemetry analyst evaluate usage, "
        "have the action executor handle pre-authorized trials and stage approvals, "
        "and project wishlist savings rebalancing."
    )
    
    initial_report = coordinator_agent(audit_trigger)
    print("\n" + str(initial_report) + "\n")

    print("=" * 65)
    print("Multi-Agent System Ready. Enter approval (e.g. 'Cancel FitPulse', 'exit'):")
    print("=" * 65)
    
    while True:
        user_input = input("\nYou > ").strip()
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Multi-Agent session terminated. Have a productive day!")
            break
        if not user_input:
            continue
            
        response = coordinator_agent(user_input)
        print(f"\nLead Coordinator > {str(response)}")