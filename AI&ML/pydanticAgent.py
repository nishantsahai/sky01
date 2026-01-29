"""
Simple AI Agent using pydantic-ai
This agent can answer questions, perform calculations, and search for information
"""

import os
from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext


# Define the dependencies that the agent can use
@dataclass
class AgentDeps:
    """Dependencies available to the agent"""
    user_name: str
    context: dict[str, str] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}


# Define structured output models
class CalculationResult(BaseModel):
    """Result of a calculation"""
    expression: str = Field(description="The mathematical expression")
    result: float = Field(description="The calculated result")
    explanation: str = Field(description="Human-readable explanation")


class SearchResult(BaseModel):
    """Result of a search query"""
    query: str = Field(description="The search query")
    summary: str = Field(description="Summary of findings")
    sources: list[str] = Field(description="Relevant sources or information")


# Create the agent with system prompt
agent = Agent(
    'openai:gpt-4o-mini',  # You can change this to other models
    deps_type=AgentDeps,
    system_prompt=(
        "You are a helpful AI assistant named AITonic. "
        "You can help users with questions, perform calculations, and provide information. "
        "Always be friendly, clear, and concise in your responses. "
        "When greeting users, use their name if available."
    )
)


# Define tools for the agent
@agent.tool
def calculate(ctx: RunContext[AgentDeps], expression: str) -> CalculationResult:
    """
    Perform mathematical calculations.
    
    Args:
        ctx: The context containing dependencies
        expression: A mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")
    
    Returns:
        CalculationResult with the result and explanation
    """
    try:
        # Use eval safely with limited scope
        result = eval(expression, {"__builtins__": {}}, {})
        return CalculationResult(
            expression=expression,
            result=float(result),
            explanation=f"The result of {expression} is {result}"
        )
    except Exception as e:
        return CalculationResult(
            expression=expression,
            result=0.0,
            explanation=f"Error calculating {expression}: {str(e)}"
        )


@agent.tool
def search_knowledge(ctx: RunContext[AgentDeps], topic: str) -> SearchResult:
    """
    Search for information about a topic.
    
    Args:
        ctx: The context containing dependencies
        topic: The topic to search for
    
    Returns:
        SearchResult with summary and sources
    """
    # Simple knowledge base (in a real application, this would query a database or API)
    knowledge_base = {
        "python": {
            "summary": "Python is a high-level programming language known for its simplicity and readability.",
            "sources": ["python.org", "Python documentation"]
        },
        "ai": {
            "summary": "Artificial Intelligence involves creating systems that can perform tasks requiring human intelligence.",
            "sources": ["AI research papers", "Machine learning textbooks"]
        },
        "pydantic": {
            "summary": "Pydantic is a data validation library using Python type hints.",
            "sources": ["pydantic-docs.helpmanual.io"]
        }
    }
    
    topic_lower = topic.lower()
    for key, value in knowledge_base.items():
        if key in topic_lower:
            return SearchResult(
                query=topic,
                summary=value["summary"],
                sources=value["sources"]
            )
    
    return SearchResult(
        query=topic,
        summary=f"I don't have specific information about {topic} in my knowledge base.",
        sources=["General knowledge"]
    )


@agent.tool
def save_user_preference(ctx: RunContext[AgentDeps], key: str, value: str) -> str:
    """
    Save a user preference for later reference.
    
    Args:
        ctx: The context containing dependencies
        key: The preference key (e.g., "favorite_color")
        value: The preference value (e.g., "blue")
    
    Returns:
        Confirmation message
    """
    ctx.deps.context[key] = value
    return f"Saved preference: {key} = {value}"


@agent.tool
def get_user_preference(ctx: RunContext[AgentDeps], key: str) -> str:
    """
    Retrieve a saved user preference.
    
    Args:
        ctx: The context containing dependencies
        key: The preference key to retrieve
    
    Returns:
        The preference value or a message if not found
    """
    value = ctx.deps.context.get(key)
    if value:
        return f"Your {key} is: {value}"
    return f"No preference found for {key}"


# Main interaction function
async def run_agent(user_message: str, user_name: str = "User") -> str:
    """
    Run the agent with a user message.
    
    Args:
        user_message: The message from the user
        user_name: The name of the user
    
    Returns:
        The agent's response
    """
    deps = AgentDeps(user_name=user_name)
    result = await agent.run(user_message, deps=deps)
    return result


# Example usage
async def main():
    """Main function demonstrating the agent"""
    print("=" * 60)
    print("AI Agent Demo")
    print("=" * 60)
    print()
    
    # Example 1: Simple greeting
    print("Example 1: Greeting")
    response = await run_agent("Hello! My name is Peter.", user_name="Peter")
    print(f"User: Hello! My name is Peter.")
    print(f"Agent: {response}")
    print()
    
    # Example 2: Calculation
    print("Example 2: Calculation")
    response = await run_agent("Can you calculate 15 * 23 + 100?", user_name="Peter")
    print(f"User: Can you calculate 15 * 23 + 100?")
    print(f"Agent: {response}")
    print()
    
    # Example 3: Information search
    print("Example 3: Knowledge Search")
    response = await run_agent("Tell me about Black Holes", user_name="Peter")
    print(f"User: Tell me about Black holes")
    print(f"Agent: {response}")
    print()
    
    # Example 4: Save preference
    print("Example 4: Saving Preferences")
    response = await run_agent("Save my favorite color as blue", user_name="Peter")
    print(f"User: Save my favorite color as blue")
    print(f"Agent: {response}")
    print()
    
    # Example 5: General question
    print("Example 5: General Question")
    response = await run_agent("What's the weather like?", user_name="Peter")
    print(f"User: What's the weather like?")
    print(f"Agent: {response}")
    print()


if __name__ == "__main__":
    import asyncio
    
    # Set your OpenAI API key
    # os.environ["OPENAI_API_KEY"] = "your-api-key-here"
    
    # Check if API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  Please set your OPENAI_API_KEY environment variable")
        print("   export OPENAI_API_KEY='your-key-here'")
    else:
        asyncio.run(main())