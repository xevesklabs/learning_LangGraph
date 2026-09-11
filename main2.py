# Exercise Graph 1 - create a Personalized Compliment Agent 



from os import name
from typing import Dict, TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    name : str

def compliment_node(state : AgentState) -> AgentState :
    """ this node appends a compliment at the end"""

    state['name'] = state['name'] + ", you're doing great"
    return state

graph = StateGraph(AgentState)

graph.add_node("complimenter", compliment_node)
graph.add_edge(START, "complimenter")
graph.add_edge("complimenter", END)

app = graph.compile()
result = app.invoke({"name" : "Xev"})
print(result)


# output -----

# {'name': "Xev, you're doing great"}