#  Graph 3 - Sequential Graph Exercise

# Your task :
    # 1. Accepts a user's name,  age, and a list of their skills.
    # 2.Pass the state via three nodes that : 
        # - First node : Presonalizes the name field with greeting.
        # - Second Node : Describe the user's age.
        # - Third node : Lists the user's skills in a formatted string.
    # 3. The final output in the result field should be a combined message in this format.

# Output : "Linda, welcome to the system! You are 31 years old! You have skills in : Python, Machine Learning, langGraph"

from asyncio import graph
from typing import TypedDict, List, final
from unittest import result
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    name : str
    age : int
    skills : List[str]
    final : str

def first_node(state : AgentState) -> AgentState:
    """ This node personalizes the Namw ith a greeting """
    state['final'] = f"{state['name']}, welcome to the system! "
    return state

def second_node(state : AgentState) -> AgentState:
    """ Describes the user's age """
    state['final'] += f"You are {state['age']} years old! "
    return state

def third_node(state : AgentState) -> AgentState:
    """ Lists the user's skills in a formatted string """
    state['final'] += f"{", ".join(state['skills'])}"
    return state 

graph = StateGraph(AgentState)

graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)
graph.add_node("third_node", third_node)

graph.add_edge(START, "first_node")
graph.add_edge("first_node", "second_node")
graph.add_edge("second_node" ,"third_node")
graph.add_edge("third_node", END)

app = graph.compile()

result = app.invoke({"name" : "Xev", "age" : 21, "skills" : ["python", "LangGraph"]})
print(result)