# Exercise for Graph 2 - how to handle multiple values 
# task : Create a graph where you pass in a single list of integers along with a name and an operation.
# if the operation is a '+', you add the elemants and if it is a "*",
# you multiply all the elements, all within the same node

import math
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    name : str
    values : List[int]
    operation : str 
    result : str

def processor_node(state : AgentState) -> AgentState :
    if(state['operation'] == '+'):
        state['result'] = f"Hi {state['name']} ', your answer is {sum(state['values'])}"
    if(state['operation'] == "*"):
        state['result'] = f"Hi {state['name']} ', your answer is {math.prod(state['values'])}"

    return state 

graph = StateGraph(AgentState)

graph.add_node("process", processor_node)
graph.add_edge(START, "process")
graph.add_edge("process", END)

app = graph.compile()

result = app.invoke({
    "name" : "Xev",
    "values" : [10, 20, 30],
    "operation" : "+"
})

result2 = app.invoke({
    "name" : "James",
    "values" : [10, 20, 30],
    "operation" : "*"
})

print(result)
print(result2)


# output ----

# {'name': 'Xev', 'values': [10, 20, 30], 'operation': '+', 'result': "Hi Xev ', your answer is 60"}
# {'name': 'James', 'values': [10, 20, 30], 'operation': '*', 'result': "Hi James ', your answer is 6000"}