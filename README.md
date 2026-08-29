# 🛡️ Autonomous Subscription & Usage Monitor Agent ("Everyday Agent")

An autonomous multi-agent system built using the **Strands Agents SDK** and powered by **Amazon Bedrock** (Claude 3.5/4.5 Haiku) to eliminate subscription waste, monitor telemetry, and safeguard personal budgets.

---

## 💡 The Problem
The average consumer and knowledge worker spends over **$1,000 annually** on forgotten trials, dormant apps, and unoptimized tier plans. Manual audits are tedious, leading to chronic subscription fatigue.

## 🚀 The Solution
Our Everyday Agent acts as an intelligent financial co-pilot with a multi-agent orchestration architecture:
* **Background Telemetry Analysis:** Evaluates cost-per-hour, idle days, and usage engagement.
* **Pre-authorized Micro-actions:** Autonomously executes trial cutoffs 48 hours prior to renewal without requiring human micro-management.
* **Human-in-the-Loop (HITL) Safety:** Stages high-impact cancellation/downgrade decisions for single-click interactive human review.
* **Goal-Oriented Rebalancing:** Calculates freed capital and directly maps it toward user wishlist milestones.

---

## 🏗️ Architecture
+---------------------------------------+
                     |    User Interface (Streamlit / CLI)   |
                     +---------------------------------------+
                                         ▲
                                         │ Natural Language Dialogue
                                         ▼
                     +---------------------------------------+
                     |                 PADDY                 |
                     |       (Lead Orchestrator Agent)       |
                     |         Amazon Bedrock Claude         |
                     +---------------------------------------+
                                         │
        +--------------------------------+--------------------------------+
        │                                │                                │
        ▼                                ▼                                ▼
+--------------------+        +--------------------+          +--------------------+
|      ENYI M        |        |       ORE MI       |          |      ABOKI NA      |
| (Telemetry Expert) |        | (Execution Guard)  |          | (Goal Rebalancer)  |
+--------------------+        +--------------------+          +--------------------+
| • Reads usage logs |        | • Auto-cuts trials |          | • Models savings   |
| • Cost-per-hour    |        | • Stages approvals |          | • Rebalances cash  |
| • Flags dormancy   |        | • Executes changes |          | • Wishlist timeline|
+--------------------+        +--------------------+          +--------------------+
        │                                │                                │
        +--------------------------------+--------------------------------+
                                         │
                                         ▼
                     +---------------------------------------+
                     | Deterministic Tool & DB Access Layer  |
                     |       (Mock DB / Banking Feeds)       |
                     +---------------------------------------+

## 🛠️ Tech Stack & Prerequisites
* **Runtime:** Python 3.10+
* **Framework:** Strands Agents SDK (`strands-agents`, `strands-agents-tools`)
* **LLM Engine:** Amazon Bedrock (Anthropic Claude via System-Defined Inference Profiles)
* **Configuration:** `python-dotenv`, `boto3`

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
   cd your-repo-name
2. Set up the virtual environment:

   Bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
3. Install dependencies:

   Bash
   pip install python-dotenv strands-agents strands-agents-tools boto3
   Configure AWS Bedrock credentials:
4. Create a .env file in the root folder:

   Code snippet
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_DEFAULT_REGION=us-east-1
5. Run the Multi-Agent System:

   Bash
   python app.py
   
🔒 Safety & Guardrails
No Unilateral Destructive Deletions: High-value subscriptions are never cancelled without explicit conversational confirmation.

Deterministic Tool Operations: Sensitive status changes are managed through verified tool APIs rather than raw LLM generation.

Auditable Logs: Every executed and staged event outputs an itemized receipt.
