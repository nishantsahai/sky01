from crewai import Task
from agents import researcher, blog_writer

# Research Task
research_task = Task(
    description='Research the top 3 AI applications transforming businesses in 2025',
    expected_output='A bullet-point summary of findings with references.',
    agent=researcher
)

# Writing Task
blog_task = Task(
    description='Write a blog post about the top 3 AI applications transforming businesses in 2025',
    expected_output='A well-structured blog article with introduction, body, and conclusion.',
    agent=blog_writer
)