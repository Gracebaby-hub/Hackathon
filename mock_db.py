"""
Mock Database for Subscription & Usage Monitor.
Simulates banking/subscription billing records and device/service usage logs.
"""

# Active subscriptions tracked by the system
SUBSCRIPTIONS = [
    {
        "id": "sub_01",
        "service": "StreamFlix Premium",
        "cost_monthly": 19.99,
        "category": "Entertainment",
        "billing_cycle": "monthly",
        "is_trial": False,
        "trial_ends_in_days": None,
        "critical_service": False,
        "auto_cancel_allowed": False
    },
    {
        "id": "sub_02",
        "service": "FitPulse Gym & Fitness App",
        "cost_monthly": 29.99,
        "category": "Health & Fitness",
        "billing_cycle": "monthly",
        "is_trial": False,
        "trial_ends_in_days": None,
        "critical_service": False,
        "auto_cancel_allowed": False
    },
    {
        "id": "sub_03",
        "service": "DesignPro Vector Suite",
        "cost_monthly": 34.00,
        "category": "Productivity",
        "billing_cycle": "monthly",
        "is_trial": True,
        "trial_ends_in_days": 2,  # Free trial expiring in 48 hours!
        "critical_service": False,
        "auto_cancel_allowed": True  # User set rule: auto-cancel trials before charge
    },
    {
        "id": "sub_04",
        "service": "CloudWorkspace Cloud Storage",
        "cost_monthly": 9.99,
        "category": "Storage",
        "billing_cycle": "monthly",
        "is_trial": False,
        "trial_ends_in_days": None,
        "critical_service": True,  # Protected: Agent cannot terminate without explicit human approval
        "auto_cancel_allowed": False
    }
]

# 30-day activity telemetry
USAGE_TELEMETRY = {
    "StreamFlix Premium": {
        "hours_used_last_30_days": 1.5,
        "days_since_last_login": 22,
        "sessions_count": 2
    },
    "FitPulse Gym & Fitness App": {
        "hours_used_last_30_days": 0.0,
        "days_since_last_login": 45,
        "sessions_count": 0
    },
    "DesignPro Vector Suite": {
        "hours_used_last_30_days": 0.5,
        "days_since_last_login": 12,
        "sessions_count": 1
    },
    "CloudWorkspace Cloud Storage": {
        "hours_used_last_30_days": 48.0,
        "days_since_last_login": 1,
        "sessions_count": 85
    }
}

# User's target savings wishlist
USER_WISHLIST = [
    {"item": "ANC Noise-Cancelling Headphones", "target_price": 180.00, "accumulated_savings": 45.00},
    {"item": "Annual Cloud Certification Exam", "target_price": 150.00, "accumulated_savings": 60.00}
]