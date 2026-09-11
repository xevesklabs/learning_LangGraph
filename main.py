# handle single input 


from typing import Dict, TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display


class AgentState(TypedDict):  # state schema
    message : str

def greeting_node(state: AgentState) -> AgentState:
    """ simple node that adds a greeting messagre to the state """

    state['message'] = "Hey " + state["message"] + ", How are you ?"
    return state


graph = StateGraph(AgentState)
graph.add_node("greeter", greeting_node)
graph.add_edge(START, "greeter")
graph.add_edge("greeter", END)
app = graph.compile()

result = app.invoke({"message" : "xev"})
print (result)


png = app.get_graph().draw_mermaid_png()

with open("graph.png", "wb") as f:
    f.write(png)

print("Graph saved as graph.png")

