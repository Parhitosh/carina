from crewai import Task


def get_tasks(agents: dict, stats: dict, user_question: str = "") -> list:
    """
    Returns three sequential tasks that mirror the
    Write → Review → Test pattern from the original crew.
    Here: Analyze → Report → Strategize.
    """

    stats_str = "\n".join(f"  - {k}: {v}" for k, v in stats.items())
    focus = f"\nUser question to focus on: {user_question}" if user_question else ""

    # ── Task 1: Data Analysis ────────────────────────────────────────────────
    analysis_task = Task(
        description=(
            f"You have been given the following summary statistics from a sample "
            f"of NYC yellow taxi trips:\n\n{stats_str}\n"
            f"{focus}\n\n"
            "Your job:\n"
            "1. Identify the top 5 most statistically interesting patterns.\n"
            "2. Highlight anomalies or surprising numbers.\n"
            "3. Compare key metrics (fare, distance, tip) across peak vs. off-peak hours.\n"
            "4. Note what the payment-type split suggests about rider demographics.\n"
            "5. Produce a structured analysis in bullet-point form."
        ),
        expected_output=(
            "A structured bullet-point analysis with at least 5 data findings, "
            "each citing specific numbers from the stats provided."
        ),
        agent=agents["data_analyst"],
    )

    # ── Task 2: Insight Reporting ────────────────────────────────────────────
    insight_task = Task(
        description=(
            "Using the data analyst's findings, write a clear executive-level "
            "insight report.\n\n"
            "Requirements:\n"
            "- Open with a one-sentence headline insight.\n"
            "- Cover 3 themes: Revenue Patterns, Rider Behavior, Operational Efficiency.\n"
            "- Use simple language — no jargon.\n"
            "- Each theme should have 2-3 key takeaways.\n"
            "- End with a 'Watch Out' section flagging 1-2 risks or concerns in the data."
        ),
        expected_output=(
            "A polished insight report with a headline, three themed sections "
            "(Revenue, Rider Behavior, Efficiency), and a Watch Out section."
        ),
        agent=agents["insight_reporter"],
        context=[analysis_task],
    )

    # ── Task 3: Strategy Recommendations ────────────────────────────────────
    strategy_task = Task(
        description=(
            "Based on the analysis and the insight report, generate a prioritized "
            "set of recommendations for NYC taxi fleet operators.\n\n"
            "Structure your output as:\n"
            "**Quick Wins (implement in < 1 month)**\n"
            "  - 2-3 immediate actions with expected impact\n\n"
            "**Medium-Term Plays (1-6 months)**\n"
            "  - 2-3 strategic initiatives\n\n"
            "**Long-Term Vision (6+ months)**\n"
            "  - 1-2 transformative ideas\n\n"
            "Every recommendation must reference a specific data point to justify it."
        ),
        expected_output=(
            "A prioritized three-tier recommendation plan (Quick Wins, "
            "Medium-Term, Long-Term) with data-backed justifications."
        ),
        agent=agents["strategy_advisor"],
        context=[analysis_task, insight_task],
    )

    return [analysis_task, insight_task, strategy_task]
