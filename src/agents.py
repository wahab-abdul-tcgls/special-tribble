from crewai import Agent
import os
from dotenv import load_dotenv
load_dotenv()
from tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")

llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                           verbose=True,
                           temperature=0.8,
                           google_api_key=os.getenv("GOOGLE_API_KEY"))

### researcher agent
news_researcher=Agent(
    role="Researcher",
    goal='Uncover latest news and trending stories in {topic}',
    verbose=True,
    memory=True,
    backstory=(
        "Driven by curiosity, you're at the forefront of"
        "innovation, eager to explore and share knowledge that could change"

    ),
    tools=[tool],
    llm=llm,
    allow_delegation=True

)

news_writer = Agent(
  role='Writer',
  goal='Narrate compelling latest news stories about {topic}',
  verbose=True,
  memory=True,
  backstory=(
    "With a flair for simplifying complex topics, you craft"
    "engaging narratives that captivate and educate, bringing new"
    "discoveries to light in an accessible manner."
  ),
  tools=[tool],
  llm=llm,
  allow_delegation=False
)