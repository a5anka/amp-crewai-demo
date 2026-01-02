# my_first_crew.py

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool  # Web search tool

# Initialize tools
search_tool = SerperDevTool()  # Requires SERPER_API_KEY or use built-in tools

# Agent 1: Researcher
researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in {topic}',
    backstory="""You're a seasoned researcher with a knack for
    uncovering the latest trends and data. You're known for your
    thorough analysis and attention to detail.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool]
)

# Agent 2: Writer
writer = Agent(
    role='Tech Content Writer',
    goal='Craft compelling content about {topic}',
    backstory="""You're a skilled writer who can transform complex
    technical information into engaging, easy-to-understand content.
    You have a talent for storytelling.""",
    verbose=True,
    allow_delegation=False
)

# Task 1: Research
research_task = Task(
    description="""Research the latest developments in {topic}.
    Focus on:
    - Key innovations in the last 6 months
    - Major players and their contributions
    - Emerging trends

    Provide a detailed bullet-point summary.""",
    expected_output='A comprehensive research report with bullet points',
    agent=researcher
)

# Task 2: Write Summary
writing_task = Task(
    description="""Using the research provided, write a 3-paragraph
    article about {topic} that:
    - Starts with an engaging hook
    - Explains key developments clearly
    - Ends with future implications

    Target audience: Technical professionals.""",
    expected_output='A 3-paragraph article',
    agent=writer
)

critic = Agent(
    role='Content Critic',
    goal='Review and improve written content',
    backstory='You have an eye for quality and accuracy',
    verbose=True
)

critique_task = Task(
    description='Review the article and suggest 3 improvements',
    expected_output='A list of 3 specific suggestions',
    agent=critic
)

# Add to crew
crew = Crew(
    agents=[researcher, writer, critic],
    tasks=[research_task, writing_task, critique_task],
    process=Process.sequential,
    verbose=True
)

# Run the crew
if __name__ == "__main__":
    result = crew.kickoff(inputs={'topic': 'AI agent frameworks'})
    print("\n\n########################")
    print("## FINAL RESULT:")
    print("########################\n")
    print(result)
