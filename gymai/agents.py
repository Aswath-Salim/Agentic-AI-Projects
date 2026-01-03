from crewai import Agent, Task, Crew, LLM

llm = LLM(model="gemini/gemini-2.5-flash")

intake_agent = Agent(
    role="Fitness Intake Assistant",
    goal="Ask fitness-related questions and collect user data",
    backstory="""
    Ask ONE question at a time.
    Collect:
    Age, Height, Weight, Goal, Diet, Activity, Sleep.
    When done reply ONLY:
    PROFILE_COMPLETE
    """,
    llm=llm
)

workout_agent = Agent(
    role="Workout Coach",
    goal="Create workout plan",
    backstory="Certified gym trainer",
    llm=llm
)

diet_agent = Agent(
    role="Diet Planner",
    goal="Create diet plan",
    backstory="Nutrition expert",
    llm=llm
)

lifestyle_agent = Agent(
    role="Lifestyle Coach",
    goal="Create lifestyle plan",
    backstory="Wellness expert",
    llm=llm
)

def intake_response(chat, profile):
    task = Task(
        description=f"""
        Chat history:
        {chat}

        Known profile:
        {profile}

        Ask the next best question.
        If complete, reply ONLY:
        PROFILE_COMPLETE
        """,
        agent=intake_agent,
        expected_output="A single question or PROFILE_COMPLETE"
    )

    crew = Crew(
        agents=[intake_agent],
        tasks=[task],
        verbose=False
    )

    result = crew.kickoff()

    return str(result)   # ✅ IMPORTANT



def generate_plans(chat):
    tasks = [
        Task(
            description=f"Create workout plan from chat:\n{chat}",
            agent=workout_agent,
            expected_output="A structured workout plan"
        ),
        Task(
            description=f"Create diet plan from chat:\n{chat}",
            agent=diet_agent,
            expected_output="A structured diet plan"
        ),
        Task(
            description=f"Create lifestyle plan from chat:\n{chat}",
            agent=lifestyle_agent,
            expected_output="A structured lifestyle plan"
        )
    ]

    crew = Crew(
        agents=[workout_agent, diet_agent, lifestyle_agent],
        tasks=tasks,
        verbose=False
    )

    result = crew.kickoff()
    return str(result)   # ✅ IMPORTANT
