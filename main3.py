# handle multiple inputs 

from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    values : List[int]
    name : str
    result : str

def process_values( state : AgentState) -> AgentState :
    """ this function process multiple different values """
    state['result'] = f"Hi there {state['name']}! Your sum = {sum(state['values'])}"
    return state

graph = StateGraph(AgentState)
graph.add_node("result", process_values)
graph.add_edge(START, "result")
graph.add_edge("result", END)

app = graph.compile()

result = app.invoke({
    "values" : [10,34,20],
    "name" : "Xev"
})
print(result)