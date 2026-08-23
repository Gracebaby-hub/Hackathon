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

model = BedrockModel(
    model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    streaming=False
)

# 1. Enyi m (Telemetry & Usage Analyst)
enyi_m = Agent(
    model=model,
    system_prompt="""
    You are 'Enyi m', the Telemetry Specialist.
    Your focus is to query usage data via `audit_subscriptions_and_usage` and assess cost-per-hour efficiency.
    """,
    tools=[audit_subscriptions_and_usage]
)

# 2. Ore mi (Action & Execution Specialist)
ore_mi = Agent(
    model=model,
    system_prompt="""
    You are 'Ore mi', the Execution Specialist.
    Handle trial cutoffs via `execute_preauthorized_trial_cutoff`, stage items waiting for user approval via `stage_cancellation_action`,
    and execute confirmed actions with `execute_confirmed_action`.
    """,
    tools=[
        stage_cancellation_action,
        execute_preauthorized_trial_cutoff,
        execute_confirmed_action
    ]
)

# 3. Aboki na (Wishlist & Rebalancing Specialist)
aboki_na = Agent(
    model=model,
    system_prompt="""
    You are 'Aboki na', the Rebalancing Specialist.
    Use `rebalance_savings_to_wishlist` to show how monthly savings fund personal goals.
    """,
    tools=[rebalance_savings_to_wishlist]
)

# 4. Paddy (Lead Coordinator)
paddy_prompt = """
You are 'Paddy', the user's Everyday Autonomous Subscription Co-Pilot.
Coordinate your squad:
- Consult 'Enyi m' for telemetry analysis.
- Consult 'Ore mi' for pre-authorized actions and staging decisions waiting for user approval.
- Consult 'Aboki na' to calculate wishlist rebalancing.

Label pending user decisions clearly as 'Waiting for your approval'.
"""

paddy = Agent(
    model=model,
    system_prompt=paddy_prompt,
    tools=[
        enyi_m.as_tool(name="enyi_m", description="Analyzes subscription activity, usage hours, and cost-per-hour metrics."),
        ore_mi.as_tool(name="ore_mi", description="Executes pre-authorized trial cutoffs and stages actions waiting for approval."),
        aboki_na.as_tool(name="aboki_na", description="Calculates wishlist goal funding timelines from freed savings.")
    ]
)

if __name__ == "__main__":
    print("\n🛡️ Initializing Paddy & Squad (Enyi m, Ore mi, Aboki na)...\n")
    audit_trigger = (
        "Run the scheduled subscription audit. Have Enyi m evaluate usage, "
        "have Ore mi auto-cancel trials and stage decisions waiting for your approval, "
        "and have Aboki na project wishlist savings rebalancing."
    )
    
    initial_report = paddy(audit_trigger)
    print("\n" + str(initial_report) + "\n")

    print("=" * 65)
    print("Paddy is standing by. Type an instruction (e.g. 'Cancel FitPulse', 'exit'):")
    print("=" * 65)
    
    while True:
        user_input = input("\nYou > ").strip()
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Paddy session closed. Take care!")
            break
        if not user_input:
            continue
            
        response = paddy(user_input)
        print(f"\nPaddy > {str(response)}")