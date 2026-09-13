# Graph 5 - Looping Graph

import random
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    name : str
    numbers : List[int]
    count : int
    final : str

def greeting(state : AgentState) -> AgentState:
    """ This node adds a greeting """
    state["count"] = 0
    state['final'] = f" Hi {state['name']}! "
    return state

def random_node(state : AgentState) -> AgentState:
    """This node will append a random number to the numbers list"""
    number = random.randint(0,10)
    state["numbers"].append(number)
    state["final"] += f"{number} "
    state["count"] += 1
    return state

def decision_node(state : AgentState) -> AgentState:
    if state["count"] < 5 :
        return "loop"
    else:
        return "random"



graph = StateGraph(AgentState)

graph.add_node("greeting_node", greeting)
graph.add_node("random", random_node)

graph.add_edge(START, "greeting_node")
graph.add_edge("greeting_node","random")

graph.add_conditional_edges(
    "random",
    decision_node,
    {
        # EDGE : NODE
        "loop" : "random",
        "random" : END
    }
)

app = graph.compile()

initial_state = {
    "name" : "Xev",
    "numbers" : []
}

result = app.invoke(initial_state)

print(result)