import os
from crewai import Agent
from crewai_tools import SerperDevTool

os.environ["SERPER_API_KEY"] = "bfd72e656249e0f0ccecb5b6ee41213c7957d23d"
web_search_tool = SerperDevTool()

# Research Agent
researcher = Agent(
    role='AI Research Analyst',
    goal='Discover the latest AI trends and applications',
    backstory=(
        "You are a detail-oriented research analyst. "
        "You specialize in gathering accurate, up-to-date information "
        "from the web and summarizing it for others."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[web_search_tool]   # <-- researcher uses web search
)

#Blog Writer Agent
blog_writer = Agent(
    role='AI Blog Writer',
    goal='Write engaging, insightful blog posts on technology and AI',
    backstory=(
        "You are a creative and articulate blog writer. "
        "You specialize in transforming complex AI topics into "
        "accessible, compelling narratives for a broad audience."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[]  
)