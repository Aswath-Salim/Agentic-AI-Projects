import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Task, Crew, LLM

# --------------------------------------------------
# LLM (Gemini)
# --------------------------------------------------
llm = LLM(
    model="gemini-2.5-flash",
    temperature=0.4,
    api_key=os.getenv("GOOGLE_API_KEY")
)

# --------------------------------------------------
# Agents
# --------------------------------------------------

research_agent = Agent(
    role="News Researcher",
    goal="Collect accurate and up-to-date information on a news topic",
    backstory="An investigative journalist skilled at fact-finding and verification.",
    llm=llm,
    verbose=True
)

writer_agent = Agent(
    role="News Writer",
    goal="Write a clear, engaging, neutral news article",
    backstory="A professional newsroom writer with strong storytelling skills.",
    llm=llm,
    verbose=True
)

editor_agent = Agent(
    role="News Editor",
    goal="Review and improve the article for clarity, neutrality, and correctness",
    backstory="A senior editor who ensures journalistic quality and ethics.",
    llm=llm,
    verbose=True
)

# --------------------------------------------------
# Tasks
# --------------------------------------------------

def run_newsroom(topic: str):

    research_task = Task(
        description=f"""
Research the following news topic thoroughly:
"{topic}"

Provide:
- Key facts
- Background
- Recent developments
""",
        agent=research_agent
    )

    writing_task = Task(
        description="""
Using the research provided,
write a complete news article.

Rules:
- Neutral tone
- Professional journalism style
- Clear headline
- 3–5 short paragraphs
""",
        agent=writer_agent
    )

    review_task = Task(
        description="""
Review the news article.

Improve:
- Clarity
- Grammar
- Neutrality
- Factual consistency

Return ONLY the final polished article.
""",
        agent=editor_agent
    )

    crew = Crew(
        agents=[research_agent, writer_agent, editor_agent],
        tasks=[research_task, writing_task, review_task],
        verbose=True
    )

    result = crew.kickoff()
    return result
