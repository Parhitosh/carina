from crewai import Agent


def get_agents(llm) -> dict:
    """
    Returns the three specialized agents for NYC taxi data analysis.
    Mirrors the Coder / Reviewer / Tester pattern but adapted for data work:
      - Data Analyst    → digs into raw numbers
      - Insight Reporter → surfaces business meaning
      - Strategy Advisor → recommends actions
    """

    data_analyst = Agent(
        role="Senior NYC Taxi Data Analyst",
        goal=(
            "Analyze NYC taxi trip data to uncover patterns in fares, distances, "
            "trip durations, peak hours, and passenger behavior. "
            "Produce precise, quantitative findings."
        ),
        backstory=(
            "You are a veteran data analyst who has worked with NYC TLC datasets "
            "for over a decade. You have an obsession with statistical accuracy "
            "and always back every claim with numbers from the data."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    insight_reporter = Agent(
        role="Urban Mobility Insight Reporter",
        goal=(
            "Transform raw taxi statistics into clear, compelling business insights. "
            "Identify trends that matter to fleet operators, city planners, and riders."
        ),
        backstory=(
            "You are a former Bloomberg data journalist turned urban-mobility consultant. "
            "You excel at translating complex datasets into stories that non-technical "
            "stakeholders immediately understand and act on."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    strategy_advisor = Agent(
        role="NYC Taxi Fleet Strategy Advisor",
        goal=(
            "Based on data analysis and insights, recommend concrete, actionable "
            "strategies to maximize revenue, improve driver efficiency, and "
            "enhance passenger experience."
        ),
        backstory=(
            "You are a management consultant who has advised major ride-hail and "
            "taxi companies across global cities. You focus on ROI-driven "
            "recommendations backed by data, not guesswork."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    return {
        "data_analyst": data_analyst,
        "insight_reporter": insight_reporter,
        "strategy_advisor": strategy_advisor,
    }
