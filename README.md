# 🧠 FinAssist – Autonomous Financial Auditor with Multi-Agent Architecture

**FinAssist** is a multi-agent AI system that functions as an autonomous financial auditor for individuals and small businesses. It leverages the Agent Development Kit (ADK) to orchestrate collaboration between specialized agents that extract, classify, analyze, and simulate financial data. The system not only tracks expenses—it detects patterns, simulates future financial scenarios, and delivers personalized, ethical recommendations.

---

## 🚀 What It Does

FinAssist helps users make better financial decisions through the cooperation of autonomous agents. It can:

- Understand natural language inputs like “I paid Netflix yesterday.”
- Classify and organize financial transactions into categories.
- Analyze financial patterns, detect anomalies, and surface insights.
- Simulate what-if financial scenarios to guide decisions.
- Generate clear, personalized reports with visualizations.
- Ensure all recommendations are ethical and user-centered.

---

## 🧩 Key Features

| Feature                  | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| 🗣️ **Natural Language Input** | Accepts user inputs via chat or form and parses them into structured data.      |
| 📊 **Transaction Classification** | Categorizes expenses and incomes intelligently using semantic embeddings.     |
| 🔎 **Insight Detection** | Detects unusual spending, duplicate subscriptions, or lifestyle inflation. |
| 🔄 **Scenario Simulation** | Models hypothetical financial changes and their long-term effects.         |
| 🧭 **Ethical Reasoning** | Filters out harmful or unrealistic suggestions (e.g., skipping meals to save). |
| 📑 **Report Generation** | Generates summaries and dashboards via Google Sheets or Looker Studio.     |

---

## 🛠️ How It Works (Agent Architecture)

FinAssist is built using the **Agent Development Kit (ADK)** and Google Cloud technologies to enable modular collaboration between agents.

### 🧠 Agents Overview

| Agent Name         | Responsibilities                                                                 |
|---------------------|----------------------------------------------------------------------------------|
| **InputAgent**      | Parses text or uploaded files (CSV, PDF, emails) and normalizes transaction data. |
| **CategorizerAgent**| Classifies transactions into financial categories using ML and rule-based logic. |
| **InsightAgent**    | Identifies trends, risky behaviors, or cost-saving opportunities.                |
| **SimulationAgent** | Enables "what-if" simulations (e.g., "What if I cancel Uber?").                  |
| **EthicsAgent**     | Evaluates suggestions to ensure they are constructive and non-harmful.           |
| **ReportAgent**     | Generates summaries, explanations, and dashboards.                              |

---

## 🧰 Tech Stack

| Technology        | Purpose                                      |
|-------------------|----------------------------------------------|
| **Agent Development Kit (ADK)** | Core multi-agent framework                         |
| **Google Cloud Functions & Pub/Sub** | Orchestration and event handling               |
| **BigQuery**      | Scalable financial data storage and querying |
| **Vertex AI (Gemini/PaLM)** | Natural language understanding and generation  |
| **Google Sheets API / Looker Studio** | Reporting and dashboard generation            |
| **Optional: Firebase Auth** | Multi-user authentication                        |

---

## 📽️ Example Use Case

1. User types: `Yesterday I paid $13.99 for Spotify and $50 for gas.`
2. **InputAgent** processes the input and extracts transactions.
3. **CategorizerAgent** tags Spotify as "Entertainment" and gas as "Transportation."
4. **InsightAgent** notices that gas spending has increased 20% from last month.
5. **SimulationAgent** offers: “Switching to public transport could save $40/month.”
6. **EthicsAgent** checks if the suggestion is practical and healthy.
7. **ReportAgent** sends a visual summary to the user’s Google Sheet.

---

## 🎯 Why It Matters

Most personal finance tools only track and visualize data. FinAssist **thinks**, **simulates**, and **recommends**—like a financial co-pilot that respects your values and context. The use of multiple intelligent agents enables transparency, modularity, and collaborative reasoning not found in traditional monolithic apps.

---

## 📌 How to Run (Coming Soon)

- Setup instructions
- Environment variables
- Deployment to GCP
- Demo walkthrough

---

## 📎 License

MIT License – for non-commercial, hackathon use.

---

## 🤝 Team

Built by EigenCore for the **Agent Development Kit Hackathon with Google Cloud**.
