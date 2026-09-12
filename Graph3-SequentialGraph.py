# Graph 3 - Sequential Graph


from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    name : str
    age : int
    final : str

def first_node(state : AgentState) -> AgentState:
    """ This is the first node of the sequence"""
    state['final'] = f" Hi {state['name']}!"
    return state

def second_node(state : AgentState) -> AgentState:
    """This ois the second node of the sequence"""
    state["final"] = state["final"] + f", Your age is {state['age']}."
    return state

graph = StateGraph(AgentState)

graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)

graph.add_edge(START, "first_node")
graph.add_edge("first_node","second_node")
graph.add_edge("second_node", END)

app = graph.compile()

result = app.invoke({ "name" : "Xev", "age" : 21})

print(result)