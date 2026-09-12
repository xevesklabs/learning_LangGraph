# Graph 4 - Conditional Graph Exercise 


from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    number1 : int
    number2 : int
    number3 : int
    number4 : int
    operation1 : str
    operation2 : str
    result1 : int
    result2 : int
    

def adder1(state : AgentState) -> AgentState:
    """ Add the two numbers """
    state['result1'] = state["number1"] + state["number2"]
    return state

def subtractor1(state : AgentState) -> AgentState:
    """ Subtract the two numbers """
    state['result1'] = state["number1"] - state["number2"]
    return state

def decision_node1(state : AgentState) -> AgentState:
    if(state["operation1"] == "+"):
        return "addition_operation1"
    if(state["operation1"] == "-"):
        return "subtraction_operation1"


def adder2(state : AgentState) -> AgentState:
    """ Add the two numbers """
    state['result2'] = state["number3"] + state["number4"]
    return state

def subtractor2(state : AgentState) -> AgentState:
    """ Subtract the two numbers """
    state['result2'] = state["number3"] - state["number4"]
    return state

def decision_node2(state : AgentState) -> AgentState:
    if(state["operation2"] == "+"):
        return "addition_operation2"
    if(state["operation2"] == "-"):
        return "subtraction_operation2"


graph = StateGraph(AgentState)

graph.add_node("addition_node1", adder1)
graph.add_node("subtraction_node1", subtractor1)
graph.add_node("router_node1", lambda state : state)

graph.add_edge(START, "router_node1")

graph.add_conditional_edges(
    "router_node1",
    decision_node1,
    {
        # EDGE : NODE
        "addition_operation1" : "addition_node1",
        "subtraction_operation1" : "subtraction_node1"
    }
)

graph.add_node("addition_node2", adder2)
graph.add_node("subtraction_node2", subtractor2)
graph.add_node("router_node2", lambda state : state)

graph.add_edge("addition_node1", "router_node2")
graph.add_edge("subtraction_node1", "router_node2")


graph.add_conditional_edges(
    "router_node2",
    decision_node2,
    {
        # EDGE : NODE
        "addition_operation2" : "addition_node2",
        "subtraction_operation2" : "subtraction_node2"
    }
)
graph.add_edge("addition_node2", END)
graph.add_edge("subtraction_node2", END)

app = graph.compile()

initial_state = {
    "number1": 10,
    "number2": 5,
    "number3": 7,
    "number4": 2,
    "operation1": "-",
    "operation2": "+",
    "result1": 0,
    "result2": 0
}

result = app.invoke(initial_state)

print(result)
