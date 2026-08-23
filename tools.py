"""
Agent Tools for Subscription Audit, Staged Cancellation, and Budget Rebalancing.
"""
import json
from strands import tool
from mock_db import SUBSCRIPTIONS, USAGE_TELEMETRY, USER_WISHLIST

@tool
def audit_subscriptions_and_usage() -> str:
    """
    Scans all recurring subscriptions, evaluates 30-day usage telemetry,
    and calculates efficiency metrics (cost per hour, dormancy status, trial expirations).
    """
    audit_report = []
    
    for sub in SUBSCRIPTIONS:
        name = sub["service"]
        cost = sub["cost_monthly"]
        telemetry = USAGE_TELEMETRY.get(name, {"hours_used_last_30_days": 0, "days_since_last_login": 999})
        hours = telemetry["hours_used_last_30_days"]
        days_inactive = telemetry["days_since_last_login"]
        
        # Calculate cost-per-hour efficiency
        if hours > 0:
            cost_per_hour = round(cost / hours, 2)
        else:
            cost_per_hour = "INFINITE (0 hours logged)"
            
        status = "ACTIVE_HEALTHY"
        if sub["is_trial"] and sub["trial_ends_in_days"] <= 3:
            status = f"TRIAL_EXPIRING_IN_{sub['trial_ends_in_days']}_DAYS"
        elif days_inactive >= 30:
            status = "DORMANT_WASTE"
        elif hours < 2.0 and cost > 15.0:
            status = "UNDERUTILIZED"
            
        audit_report.append({
            "service": name,
            "monthly_cost": f"${cost}",
            "hours_last_30d": hours,
            "days_since_last_use": days_inactive,
            "cost_per_hour": f"${cost_per_hour}" if isinstance(cost_per_hour, (int, float)) else cost_per_hour,
            "status_flag": status,
            "is_critical": sub["critical_service"],
            "auto_cancel_allowed": sub["auto_cancel_allowed"]
        })
        
    return json.dumps(audit_report, indent=2)


@tool
def stage_cancellation_action(service_name: str, recommended_action: str, potential_monthly_saving: float) -> str:
    """
    Stages a structured action draft (cancellation, pause, or downgrade) requiring Human-in-the-Loop confirmation.
    """
    staged_payload = {
        "status": "ACTION_STAGED_AWAITING_HUMAN_APPROVAL",
        "target_service": service_name,
        "action_type": recommended_action,
        "monthly_savings": f"${potential_monthly_saving}/mo",
        "annual_projected_savings": f"${round(potential_monthly_saving * 12, 2)}/year",
        "execution_path": f"https://api.portal.example/{service_name.lower().replace(' ', '-')}/manage-subscription",
        "prompt_card": (
            f"⚠️ Decision Required: {service_name} has high waste/inactivity. "
            f"Would you like to execute [{recommended_action}] to save ${potential_monthly_saving}/month?"
        )
    }
    return json.dumps(staged_payload, indent=2)


@tool
def execute_preauthorized_trial_cutoff(service_name: str) -> str:
    """
    Autonomously executes a cancellation for expiring trials where the user granted pre-authorized policy approval.
    """
    target = next((s for s in SUBSCRIPTIONS if s["service"].lower() == service_name.lower()), None)
    if not target:
        return f"Error: Service {service_name} not found."
    
    if target.get("auto_cancel_allowed"):
        return (
            f"SUCCESS: Auto-executed pre-authorized cancellation for '{service_name}'. "
            f"Saved ${target['cost_monthly']}/mo before trial converted to paid renewal."
        )
    return f"POLICY_RESTRICTION: {service_name} does not have pre-authorized cancellation enabled. Stage for human approval instead."


@tool
def rebalance_savings_to_wishlist(monthly_freed_amount: float) -> str:
    """
    Calculates how monthly subscription savings can fund items on the user's personal wishlist.
    """
    annual_freed = monthly_freed_amount * 12
    wishlist_status = []
    
    for item in USER_WISHLIST:
        remaining = max(0.0, item["target_price"] - item["accumulated_savings"])
        months_to_fund = round(remaining / monthly_freed_amount, 1) if monthly_freed_amount > 0 else "N/A"
        wishlist_status.append({
            "item": item["item"],
            "remaining_needed": f"${remaining}",
            "fully_funded_in_months": f"{months_to_fund} months"
        })
        
    return json.dumps({
        "monthly_freed": f"${monthly_freed_amount}",
        "annual_projected": f"${annual_freed}",
        "wishlist_acceleration": wishlist_status
    }, indent=2)
@tool
def execute_confirmed_action(service_name: str, action: str) -> str:
    """
    Executes a user-confirmed action (cancel, pause, downgrade) on an active subscription
    and updates the active subscription registry.
    """
    global SUBSCRIPTIONS
    target = next((s for s in SUBSCRIPTIONS if s["service"].lower() == service_name.lower()), None)
    
    if not target:
        return f"Error: Could not locate active subscription for '{service_name}'."
    
    # Simulate removal/downgrade in our active database
    SUBSCRIPTIONS = [s for s in SUBSCRIPTIONS if s["service"].lower() != service_name.lower()]
    
    return json.dumps({
        "status": "COMPLETED",
        "service": service_name,
        "action_taken": action,
        "monthly_freed": f"${target['cost_monthly']}",
        "message": f"Successfully executed '{action}' for {service_name}. Recurring billing stopped."
    }, indent=2)