"""
NYC Taxi Analysis Crew — Streamlit App
Multi-agent CrewAI pipeline for analyzing NYC yellow taxi trip data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data.loader import load_nyc_taxi_data, get_summary_stats
from crew.runner import run_crew

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NYC Taxi Crew AI",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

  html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

  .stApp { background: #0d0f14; color: #e8eaf0; }

  /* Sidebar */
  [data-testid="stSidebar"] { background: #13151c !important; border-right: 1px solid #1f2330; }

  /* Metric cards */
  [data-testid="stMetric"] {
    background: #13151c;
    border: 1px solid #1f2330;
    border-radius: 12px;
    padding: 16px 20px;
  }
  [data-testid="stMetricValue"] { color: #f7c948 !important; font-size: 1.6rem !important; font-weight: 700 !important; }
  [data-testid="stMetricLabel"] { color: #8892a4 !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.05em; }

  /* Section headers */
  .section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #f7c948;
    letter-spacing: 0.04em;
    margin: 24px 0 12px;
    text-transform: uppercase;
    border-bottom: 1px solid #1f2330;
    padding-bottom: 8px;
  }

  /* Agent output cards */
  .agent-card {
    background: #13151c;
    border: 1px solid #1f2330;
    border-left: 3px solid #f7c948;
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.7;
    color: #c8d0df;
    white-space: pre-wrap;
  }

  .agent-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #f7c948;
    margin-bottom: 10px;
  }

  /* Hero banner */
  .hero {
    background: linear-gradient(135deg, #13151c 0%, #1a1d26 50%, #0f1118 100%);
    border: 1px solid #1f2330;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
  }
  .hero h1 { font-size: 2.2rem; font-weight: 700; color: #f7c948; margin: 0 0 6px; }
  .hero p  { color: #8892a4; font-size: 0.95rem; margin: 0; }

  /* Tab styling */
  .stTabs [data-baseweb="tab"] { color: #8892a4; font-weight: 600; }
  .stTabs [aria-selected="true"] { color: #f7c948 !important; border-bottom: 2px solid #f7c948 !important; }

  /* Spinner */
  .stSpinner > div { border-top-color: #f7c948 !important; }

  /* Buttons */
  .stButton > button {
    background: #f7c948;
    color: #0d0f14;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 10px 28px;
    font-size: 0.9rem;
    letter-spacing: 0.03em;
  }
  .stButton > button:hover { background: #ffd966; }

  /* Divider */
  hr { border-color: #1f2330; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🚕 NYC Taxi Crew")
    st.markdown("---")

    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get a free key at console.groq.com",
    )

    st.markdown("---")
    n_rows = st.slider("Sample size (rows)", min_value=1000, max_value=10000, value=5000, step=500)
    st.markdown("---")

    st.markdown("**Agents in this crew:**")
    st.markdown("🔍 **Data Analyst** — finds patterns")
    st.markdown("📰 **Insight Reporter** — tells the story")
    st.markdown("🎯 **Strategy Advisor** — drives action")
    st.markdown("---")

    st.markdown(
        "<small style='color:#8892a4'>Built with CrewAI · Groq · Streamlit<br>"
        "Data: NYC TLC Yellow Taxi</small>",
        unsafe_allow_html=True,
    )


# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def get_data(n: int):
    return load_nyc_taxi_data(n)


with st.spinner("Loading NYC taxi data..."):
    df = get_data(n_rows)

stats = get_summary_stats(df)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <h1>🚕 NYC Taxi Crew AI</h1>
  <p>Multi-agent CrewAI pipeline • {stats['total_trips']:,} trips analysed •
  ${ stats['total_revenue']:,.0f} total revenue</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Avg Fare", f"${stats['avg_fare']}")
c2.metric("Avg Distance", f"{stats['avg_distance']} mi")
c3.metric("Avg Duration", f"{stats['avg_duration_min']} min")
c4.metric("Avg Tip", f"{stats['avg_tip_pct']}%")
c5.metric("Peak Hour", f"{stats['peak_hour']}:00")
c6.metric("Busiest Day", stats['busiest_day'])

st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🤖 AI Crew Analysis", "🗂️ Raw Data"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    PLOTLY_LAYOUT = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c8d0df", family="Space Grotesk"),
        margin=dict(t=36, b=36, l=36, r=36),
        xaxis=dict(gridcolor="#1f2330", linecolor="#1f2330"),
        yaxis=dict(gridcolor="#1f2330", linecolor="#1f2330"),
    )
    YELLOW = "#f7c948"
    TEAL   = "#4ec9b0"
    PINK   = "#f48fb1"

    row1_left, row1_right = st.columns(2)

    # Chart 1: Trips by Hour
    with row1_left:
        st.markdown('<div class="section-title">Trips by Hour of Day</div>', unsafe_allow_html=True)
        hourly = df.groupby("hour").size().reset_index(name="trips")
        fig = px.bar(
            hourly, x="hour", y="trips",
            color="trips", color_continuous_scale=[[0, "#1f2330"], [1, YELLOW]],
        )
        fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, coloraxis_showscale=False)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    # Chart 2: Trips by Day
    with row1_right:
        st.markdown('<div class="section-title">Trips by Day of Week</div>', unsafe_allow_html=True)
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        daily = df.groupby("day_of_week").size().reindex(day_order).reset_index(name="trips")
        fig = px.bar(
            daily, x="day_of_week", y="trips",
            color="trips", color_continuous_scale=[[0, "#1f2330"], [1, TEAL]],
        )
        fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, coloraxis_showscale=False)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    row2_left, row2_right = st.columns(2)

    # Chart 3: Fare Distribution
    with row2_left:
        st.markdown('<div class="section-title">Fare Amount Distribution</div>', unsafe_allow_html=True)
        capped = df[df["fare_amount"] <= 60]
        fig = px.histogram(capped, x="fare_amount", nbins=50, color_discrete_sequence=[YELLOW])
        fig.update_layout(**PLOTLY_LAYOUT, showlegend=False)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    # Chart 4: Tip % vs Distance scatter
    with row2_right:
        st.markdown('<div class="section-title">Tip % vs Trip Distance</div>', unsafe_allow_html=True)
        sample = df[df["tip_pct"] > 0].sample(n=min(1500, len(df)), random_state=1)
        fig = px.scatter(
            sample, x="trip_distance", y="tip_pct",
            opacity=0.4, color_discrete_sequence=[TEAL],
        )
        fig.update_layout(**PLOTLY_LAYOUT, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    row3_left, row3_right = st.columns(2)

    # Chart 5: Avg Fare by Hour
    with row3_left:
        st.markdown('<div class="section-title">Avg Fare by Hour</div>', unsafe_allow_html=True)
        hourly_fare = df.groupby("hour")["fare_amount"].mean().reset_index()
        fig = px.line(
            hourly_fare, x="hour", y="fare_amount",
            markers=True, color_discrete_sequence=[YELLOW],
        )
        fig.update_layout(**PLOTLY_LAYOUT, showlegend=False)
        fig.update_traces(line_width=2.5, marker_size=6)
        st.plotly_chart(fig, use_container_width=True)

    # Chart 6: Payment type donut
    with row3_right:
        st.markdown('<div class="section-title">Payment Type Split</div>', unsafe_allow_html=True)
        payment_map = {1: "Credit Card", 2: "Cash", 3: "No Charge / Dispute"}
        pay_df = df["payment_type"].map(payment_map).value_counts().reset_index()
        pay_df.columns = ["payment", "count"]
        fig = px.pie(
            pay_df, names="payment", values="count",
            hole=0.55,
            color_discrete_sequence=[YELLOW, TEAL, PINK],
        )
        fig.update_layout(**PLOTLY_LAYOUT, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: AI CREW ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown(
        "Ask your AI crew a question about this dataset, or run a full analysis.",
        unsafe_allow_html=True,
    )

    user_question = st.text_input(
        "Your question (optional)",
        placeholder="e.g. Why are late-night fares higher? How can drivers earn more on weekdays?",
    )

    run_btn = st.button("🚀 Run Crew Analysis")

    if not groq_api_key and run_btn:
        st.warning("⚠️ Please enter your Groq API Key in the sidebar first.")

    elif run_btn and groq_api_key:
        with st.spinner("🤖 Agents are collaborating... this takes ~60 seconds"):
            try:
                outputs = run_crew(stats, groq_api_key, user_question)

                st.markdown('<div class="section-title">🔍 Data Analyst Output</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="agent-card"><div class="agent-label">Agent: Senior NYC Taxi Data Analyst</div>'
                    f'{outputs.get("data_analysis", "No output")}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown('<div class="section-title">📰 Insight Reporter Output</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="agent-card"><div class="agent-label">Agent: Urban Mobility Insight Reporter</div>'
                    f'{outputs.get("insight_report", "No output")}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown('<div class="section-title">🎯 Strategy Advisor Output</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="agent-card"><div class="agent-label">Agent: NYC Taxi Fleet Strategy Advisor</div>'
                    f'{outputs.get("strategy_plan", "No output")}</div>',
                    unsafe_allow_html=True,
                )

            except Exception as e:
                st.error(f"Crew run failed: {e}")
                st.info(
                    "Make sure your Groq API key is valid and you have internet access. "
                    "Check that all requirements are installed: `pip install -r requirements.txt`"
                )

    else:
        st.markdown("""
<div style='background:#13151c;border:1px dashed #1f2330;border-radius:12px;padding:28px;text-align:center;color:#8892a4;'>
  <div style='font-size:2.5rem;margin-bottom:12px'>🤖</div>
  <div style='font-size:1rem;font-weight:600;color:#c8d0df;margin-bottom:6px'>Your crew is ready.</div>
  <div style='font-size:0.85rem'>Enter your Groq API key in the sidebar and click <b>Run Crew Analysis</b>.</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: RAW DATA
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown(f"**{len(df):,} rows** · showing first 500", unsafe_allow_html=True)
    st.dataframe(
        df.head(500).style.format({
            "fare_amount": "${:.2f}",
            "tip_amount": "${:.2f}",
            "total_amount": "${:.2f}",
            "trip_distance": "{:.2f} mi",
            "trip_duration_min": "{:.1f} min",
            "tip_pct": "{:.1f}%",
            "speed_mph": "{:.1f} mph",
        }),
        use_container_width=True,
        height=520,
    )

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download full CSV", csv, "nyc_taxi_sample.csv", "text/csv")
