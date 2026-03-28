# 🚕 NYC Taxi Crew AI

A **CrewAI multi-agent pipeline** for analyzing NYC yellow taxi trip data, deployed as a **Streamlit web app**.

Inspired by the `ai-code-collaboration-crew` architecture — three specialized agents working sequentially, each building on the previous one's output.

---

## 🤖 The Crew

| Agent | Role | Equivalent in original repo |
|---|---|---|
| **Data Analyst** | Finds patterns & anomalies in trip stats | Coder Agent |
| **Insight Reporter** | Translates numbers into business stories | Reviewer Agent |
| **Strategy Advisor** | Recommends concrete actions | Tester/QA Agent |

---

## 📊 Features

- **Live Dashboard** — 6 interactive Plotly charts (trips by hour, day, fare distribution, tip patterns, payment split)
- **AI Crew Analysis** — Run all 3 agents sequentially with a single click
- **Custom Questions** — Ask agents anything about the dataset
- **Data Export** — Download the full sample as CSV
- **Auto data loading** — Downloads real NYC TLC parquet data; falls back to realistic synthetic data if offline

---

## 🚀 Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/nyc-taxi-crew.git
cd nyc-taxi-crew

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Then open http://localhost:8501, enter your **Groq API key** in the sidebar, and click **Run Crew Analysis**.

---

## 🔑 API Key

This app uses [Groq](https://console.groq.com) (free tier available) with `llama3-70b-8192`.

You can enter the key in the Streamlit sidebar, or set it in `.env`:

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

---

## ☁️ Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → select `app.py`
4. In **Secrets**, add:
   ```toml
   GROQ_API_KEY = "gsk_your_key_here"
   ```
5. Deploy ✅

To use Secrets instead of the sidebar input, update `app.py` line:
```python
groq_api_key = st.secrets.get("GROQ_API_KEY", "")
```

---

## 📁 Project Structure

```
nyc-taxi-crew/
├── app.py                    # Streamlit UI (Dashboard + AI tab + Raw data)
├── crew/
│   ├── __init__.py
│   ├── agents.py             # 3 CrewAI agents with roles & backstories
│   ├── tasks.py              # Sequential tasks (Analyze → Report → Strategize)
│   └── runner.py             # Crew instantiation & kickoff
├── data/
│   ├── __init__.py
│   └── loader.py             # NYC TLC data loader + synthetic fallback
├── .streamlit/
│   └── config.toml           # Dark theme config
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🛠️ Tech Stack

- [CrewAI](https://github.com/crewAIInc/crewAI) — multi-agent orchestration
- [Groq](https://console.groq.com) — LLM inference (llama3-70b)
- [Streamlit](https://streamlit.io) — web UI
- [Plotly](https://plotly.com) — interactive charts
- [NYC TLC Open Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) — yellow taxi trips

---

## 📸 Demo Content

For your Instagram / YouTube demo, this app covers:
- **Reel hook**: "3 AI agents just analyzed 5,000 NYC taxi trips in 60 seconds 🚕"
- Show the dashboard first (instant visual impact)
- Then run the crew live and scroll through agent outputs
- Highlight the Strategy Advisor's "Quick Wins" as the money shot
