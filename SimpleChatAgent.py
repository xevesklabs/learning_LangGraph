# Simple chat agent/Bot (Doesn't have Memory)

from email import message
from typing import TypedDict
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    message : str

llm = ChatOllama(
    model="ornith-1.5:9b",
    base_url="http://localhost:11434"
)

def agent(state : AgentState) -> AgentState:
    response = llm.invoke(state["message"])
    print(f" \n AI : {response.content}")
    return state


graph = StateGraph(AgentState)

graph.add_node("agent_node", agent)
graph.add_edge(START, "agent_node")
graph.add_edge("agent_node", END)

app = graph.compile()

while(1):
    print(" \n --------------------- \n")
    message = input("enter text ::  ")
    if (message == "exit"):
        break
    initial_state = { "message" : message}
    app.invoke(initial_state)

