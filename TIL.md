# Today I Learned — LangGraph Basics

**Date:** September 11, 2026
**Topic:** LangGraph — Graphs, Nodes, State, and Inputs

---

## 1. What is LangGraph?

LangGraph is a framework for building applications using **graphs and nodes**.

```text
Input → Node → Node → Output
```

The **state** contains the information that flows through the graph.

---

## 2. Creating State

State can be defined using `TypedDict`.

```python
from typing import TypedDict

class AgentState(TypedDict):
    message: str
```

---

## 3. Creating a Node

A node is a Python function that processes the state.

```python
def greeting_node(state: AgentState) -> AgentState:
    state["message"] = "Hey " + state["message"] + ", How are you?"
    return state
```

A node:

1. Receives state.
2. Processes it.
3. Modifies it.
4. Returns it.

---

## 4. Creating a Graph

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(AgentState)
```

Add a node:

```python
graph.add_node("greeter", greeting_node)
```

Connect it:

```python
graph.add_edge(START, "greeter")
graph.add_edge("greeter", END)
```

Flow:

```text
START → greeter → END
```

---

## 5. Compile and Run

```python
app = graph.compile()

result = app.invoke({
    "message": "Soura"
})
```

---

## 6. Multiple Inputs

State can contain multiple fields:

```python
class AgentState(TypedDict):
    values: list[int]
    name: str
    result: str
```

Example:

```python
{
    "values": [10, 34, 20],
    "name": "Xev"
}
```

A node can use multiple fields:

```python
def process_values(state: AgentState) -> AgentState:
    state["result"] = (
        f"Hi there {state['name']}! "
        f"Your sum = {sum(state['values'])}"
    )
    return state
```

---

## 7. Important `invoke()` Lesson

Multiple inputs go inside **one dictionary**.

```python
app.invoke({
    "values": [10, 34, 20],
    "name": "Xev"
})
```

Not:

```python
app.invoke(
    {"name": "Xev"},
    {"values": [10, 34, 20]}
)
```

---

## 8. Overall Flow

```text
State
  ↓
Graph
  ↓
Node
  ↓
Updated State
  ↓
Next Node
  ↓
Final State
```

### Key Things I Learned

* **Graph** → workflow
* **Node** → processes state
* **State** → information flowing through the graph
* `TypedDict` → defines state structure
* `add_node()` → adds a node
* `add_edge()` → connects nodes
* `START` → beginning
* `END` → ending
* `compile()` → prepares the graph
* `invoke()` → runs the graph
* Multiple inputs go in one state dictionary



# Today I Learned - Sequential Graph
**Date:** September 12, 2026

* Learned how to create a **3-node sequential graph**.
* Learned how to pass `name`, `age`, and `skills` through the state.
* Learned how each node can **modify the same `final` field**.
* Learned how to connect nodes in sequence using `add_edge()`.
* Learned how to use `join()` to convert a list of skills into a formatted string.
* Learned how to combine the output from multiple nodes into one final message.



# Today I Learned — LangGraph Basics

**Date:** September 13, 2026
**Topic:** LangGraph — Conditional Graphs

* Learned how to create a **conditional graph**.
* Learned how to use `add_conditional_edges()`.
* Learned how a **router node** decides which node to execute.
* Learned how to create different paths based on `operation1` and `operation2`.
* Learned how to perform two separate operations using conditional routing.
* Learned how to use multiple routers in the same graph.
* Learned how `result1` and `result2` store the results of each operation.

```text
START
  ↓
Router 1
  ↓
 + / -
  ↓
Operation 1
  ↓
Router 2
  ↓
 + / -
  ↓
Operation 2
  ↓
END
```
