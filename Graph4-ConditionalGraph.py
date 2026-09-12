# Graph 4 - Conditional Graph


from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    number1 : int
    operation : str
    number2 : int
    result : int

def adder(state : AgentState) -> AgentState:
    """ Add the two numbers """
    state['result'] = state["number1"] + state["number2"]
    return state

def subtractor(state : AgentState) -> AgentState:
    """ Subtract the two numbers """
    state['result'] = state["number1"] - state["number2"]
    return state

def decision_node(state : AgentState) -> AgentState:
    if(state["operation"] == "+"):
        return "addition_operation"
    if(state["operation"] == "-"):
        return "subtraction_operation"


graph = StateGraph(AgentState)

graph.add_node("addition_node", adder)
graph.add_node("subtraction_node", subtractor)
graph.add_node("router_node", lambda state : state)

graph.add_edge(START, "router_node")

graph.add_conditional_edges(
    "router_node",
    decision_node,
    {
        # EDGE : NODE
        "addition_operation" : "addition_node",
        "subtraction_operation" : "subtraction_node"
    }
)
graph.add_edge("addition_node", END)
graph.add_edge("subtraction_node", END)

app = graph.compile()

result = app.invoke({ "number1":20, "number2":30, "operation":"+"})
result2 = app.invoke({ "number1":20, "number2":30, "operation":"-"})
print(result)
print(result2)