from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_experimental.tools import PythonREPLTool
#from langchain.tools import WikipediaQueryRun


# 1) A simple web sreach tool
ddg_search = DuckDuckGoSearchRun(name="duckduckgo_search")

# 2) Wikipedia tool
wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(), name="wikipedia")

# 3) Python REPL (useful for precise math / quick snippets)
python_repl = PythonREPLTool(name="python_repl")

# 4) A simple custom calculator tool 
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers together."""
    return a * b

# 5) A simple custom calculator tool 
@tool("calculator", return_direct=False)
def calculator(expr: str) -> str:
    """Evaluate a basic arithmetic expression safely (e.g., '15*12', '180+20')."""
    import re
    if not re.fullmatch(r"[0-9\+\-\*\/\(\)\s\.]+", expr):
        return "Invalid expression."
    try:
        result = eval(expr, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


tools = [ddg_search, WikipediaQueryRun, PythonREPLTool, multiply, calculator]

model = ChatOpenAI(model="gpt-4o")
memory = InMemorySaver()
agent_executor = create_agent(
    model,
    tools=tools,
    checkpointer=memory
)

config = {"configurable": {"thread_id": "user_session_1"}}

# Interaction 1
response = agent_executor.invoke(
    {"messages": [{"role": "user", "content": "What is 15 times 12?"}]},
    config
)

print(response["messages"][-1].content) 

# Interaction 2 (Agent remembers the previous result)
response = agent_executor.invoke(
    {"messages": [{"role": "user", "content": "Now add 20 to that."}]},
    config
)   
print(response["messages"][-1].content) 

# Interaction 3 
response = agent_executor.invoke(
    {"messages": [{"role": "user", "content": "Today's temperature in New York"}]},
    config
)   
print(response["messages"][-1].content)