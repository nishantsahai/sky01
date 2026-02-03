from typing import TypedDict, List, Any, Literal

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from langchain_openai import ChatOpenAI
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_experimental.tools.python.tool import PythonREPLTool

from langchain_core.messages import HumanMessage, AIMessage


# -------------------------------
# 1. Shared State
# -------------------------------
class AgentState(TypedDict, total=False):
    messages: List[Any]
    next: Literal["research_agent", "math_agent", "finish"]


# -------------------------------
# 2. Worker Agents
# -------------------------------
model = ChatOpenAI(model="gpt-4o")

search_tool = DuckDuckGoSearchRun(name="search")
python_tool = PythonREPLTool(name="python_repl")

research_agent = create_react_agent(model=model, tools=[search_tool])
math_agent = create_react_agent(model=model, tools=[python_tool])


# -------------------------------
# 3. Supervisor Node 
# -------------------------------
supervisor_prompt = """
You are a supervisor agent.
Choose who should handle the next step:
- 'research_agent'
- 'math_agent'
- 'finish'

Rules:
- If user needs external info or real‑world facts → choose research_agent
- If user asks math, calculation, or computation → choose math_agent
- If the task appears done → choose finish

Return ONLY one word.
"""

def supervisor_node(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o")

    messages = [
        {"role": "system", "content": supervisor_prompt},
        *state["messages"],
    ]

    result = llm.invoke(messages)
    text = result.content.lower().strip()

    if "research" in text:
        return {"next": "research_agent"}
    if "math" in text or "compute" in text:
        return {"next": "math_agent"}
    if "finish" in text:
        return {"next": "finish"}

    # fallback: inspect last user message
    last_user_msg = None
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            last_user_msg = msg.content.lower()
            break

    if last_user_msg and any(
        w in last_user_msg for w in ["calculate", "sum", "divide", "multiply"]
    ):
        return {"next": "math_agent"}

    return {"next": "research_agent"}


# -------------------------------
# 4. Worker Nodes
# -------------------------------
def research_node(state: AgentState):
    response = research_agent.invoke({"messages": state["messages"]})
    return {"messages": response["messages"]}

def math_node(state: AgentState):
    response = math_agent.invoke({"messages": state["messages"]})
    return {"messages": response["messages"]}


# -------------------------------
# 5. Graph Build
# -------------------------------
workflow = StateGraph(AgentState)

workflow.add_node("supervisor", supervisor_node)
workflow.add_node("research_agent", research_node)
workflow.add_node("math_agent", math_node)

workflow.add_edge(START, "supervisor")

workflow.add_conditional_edges(
    "supervisor",
    lambda s: s["next"],
    {
        "research_agent": "research_agent",
        "math_agent": "math_agent",
        "finish": END
    },
)

workflow.add_edge("research_agent", "supervisor")
workflow.add_edge("math_agent", "supervisor")

memory = InMemorySaver()
graph = workflow.compile(checkpointer=memory)