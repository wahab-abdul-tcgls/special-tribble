from crewai import Task
from tools import tool
from agents import news_researcher,news_writer

# Research task
research_task = Task(
  description=(
    "Identify the latest news in {topic}."
    "Focus on identifying accurate information from trusted sources"
    "Your final report should clearly articulate the key points,"
  ),
  expected_output='A comprehensive 3 paragraphs long report on the latest news in {topic}.',
  tools=[tool],
  agent=news_researcher,
)

# Writing task with language model configuration
write_task = Task(
  description=(
    "Compose an insightful article on {topic}."
    "Focus on the latest news and trends"
    "This article should be easy to understand, engaging, and positive."
  ),
  expected_output='A 4 paragraph article on {topic} advancements formatted as markdown.',
  tools=[tool],
  agent=news_writer,
  async_execution=False,
  output_file='news.md' 
)