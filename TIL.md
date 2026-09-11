# Today I Learned — LangGraph Basics

**Date:** September 11, 2026
**Topic:** LangGraph — Graphs, Nodes, State, and Inputs

---

## 1. What is LangGraph?

LangGraph is a framework for building applications using **graphs and nodes**.

A LangGraph application can be thought of as:

```text
Input → Node → Node → Node → Output
```

Each node performs some operation on the current state.

The **state** contains the information that flows through the graph.

---

# 2. Creating a State

We can define the state using `TypedDict`.

```python
from typing import TypedDict


class AgentState(TypedDict):
    message: str
```

Here:

```python
class AgentState(TypedDict):
```

defines the structure of our state.

The state contains:

```text
message → str
```

So an example state could be:

```python
{
    "message": "Soura"
}
```

---

# 3. Creating a Node

A **node** is a Python function that performs some operation on the state.

Example:

```python
def greeting_node(state: AgentState) -> AgentState:
    state["message"] = "Hey " + state["message"] + ", How are you?"
    return state
```

The node:

1. Receives the state.
2. Processes the state.
3. Modifies the state.
4. Returns the state.

For example:

```text
Input:
{
    "message": "Soura"
}

        ↓

greeting_node

        ↓

Output:
{
    "message": "Hey Soura, How are you?"
}
```

---

# 4. Creating a Graph

To create a LangGraph graph:

```python
from langgraph.graph import StateGraph, START, END
```

Then:

```python
graph = StateGraph(AgentState)
```

Here we are telling LangGraph that our graph will use `AgentState`.

---

# 5. Adding a Node to the Graph

We add a node using:

```python
graph.add_node("greeter", greeting_node)
```

The first argument:

```python
"greeter"
```

is the name of the node.

The second argument:

```python
greeting_node
```

is the function that will execute.

So:

```text
greeter
   ↓
greeting_node()
```

---

# 6. Connecting Nodes

LangGraph uses edges to determine the flow of execution.

We can connect the starting point to our node:

```python
graph.add_edge(START, "greeter")
```

And connect the node to the end:

```python
graph.add_edge("greeter", END)
```

The resulting graph is:

```text
START
  ↓
greeter
  ↓
 END
```

---

# 7. Compiling the Graph

Before running the graph, we compile it:

```python
app = graph.compile()
```

Now `app` is the executable version of our graph.

---

# 8. Running the Graph

We can execute the graph using:

```python
result = app.invoke({
    "message": "Soura"
})
```

Then:

```python
print(result)
```

Output:

```text
{
    'message': 'Hey Soura, How are you?'
}
```

---

# 9. Handling a Single Input

A simple example with one input:

```python
from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    message: str


def greeting_node(state: AgentState) -> AgentState:
    state["message"] = "Hey " + state["message"] + ", How are you?"
    return state


graph = StateGraph(AgentState)

graph.add_node("greeter", greeting_node)

graph.add_edge(START, "greeter")
graph.add_edge("greeter", END)

app = graph.compile()

result = app.invoke({
    "message": "Soura"
})

print(result)
```

The important idea:

```text
Input
  ↓
{
    "message": "Soura"
}
  ↓
greeting_node
  ↓
{
    "message": "Hey Soura, How are you?"
}
```

---

# 10. Handling Multiple Inputs

A state can contain multiple pieces of information.

For example:

```python
class AgentState(TypedDict):
    values: list[int]
    name: str
    result: str
```

Now our state contains three fields:

```text
values → list of integers
name   → string
result → string
```

Example input:

```python
{
    "values": [10, 34, 20],
    "name": "Xev"
}
```

---

# 11. Processing Multiple Inputs

We can create a node that uses multiple values from the state:

```python
def process_values(state: AgentState) -> AgentState:
    state["result"] = (
        f"Hi there {state['name']}! "
        f"Your sum = {sum(state['values'])}"
    )
    return state
```

The node uses:

```python
state["name"]
```

and:

```python
state["values"]
```

to create:

```python
state["result"]
```

---

# 12. Complete Multiple-Input Example

```python
from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    values: list[int]
    name: str
    result: str


def process_values(state: AgentState) -> AgentState:
    """Process multiple different values."""

    state["result"] = (
        f"Hi there {state['name']}! "
        f"Your sum = {sum(state['values'])}"
    )

    return state


graph = StateGraph(AgentState)

graph.add_node("result", process_values)

graph.add_edge(START, "result")
graph.add_edge("result", END)

app = graph.compile()

result = app.invoke({
    "values": [10, 34, 20],
    "name": "Xev"
})

print(result)
```

Output:

```text
{
    'values': [10, 34, 20],
    'name': 'Xev',
    'result': 'Hi there Xev! Your sum = 64'
}
```

---

# 13. Important Lesson About `invoke()`

When passing multiple inputs, they should be inside **one dictionary**.

### Correct:

```python
app.invoke({
    "values": [10, 34, 20],
    "name": "Xev"
})
```

### Incorrect:

```python
app.invoke(
    {"name": "Xev"},
    {"values": [10, 34, 20]}
)
```

The second argument is not treated as another state dictionary.

This caused:

```text
KeyError: 'values'
```

because the node received a state containing only:

```python
{
    "name": "Xev"
}
```

and therefore:

```python
state["values"]
```

did not exist.

---

# 14. Overall LangGraph Flow

The main concept learned today is:

```text
                  STATE
                    │
                    ▼
              ┌───────────┐
              │   START   │
              └─────┬─────┘
                    │
                    ▼
              ┌───────────┐
              │   NODE    │
              │           │
              │ Process   │
              │  State    │
              └─────┬─────┘
                    │
                    ▼
              ┌───────────┐
              │    END    │
              └───────────┘
```

In Python:

```python
graph = StateGraph(AgentState)

graph.add_node("node_name", node_function)

graph.add_edge(START, "node_name")
graph.add_edge("node_name", END)

app = graph.compile()

result = app.invoke(input_state)
```

---

# 15. Key Things I Learned Today

* LangGraph represents workflows as **graphs**.
* A **node** is usually a Python function.
* Nodes receive and return **state**.
* `TypedDict` can be used to define the state schema.
* `StateGraph()` creates a graph using a state schema.
* `add_node()` adds a node.
* `add_edge()` defines the flow between nodes.
* `START` represents the beginning of the graph.
* `END` represents the end of the graph.
* `compile()` turns the graph into an executable application.
* `invoke()` runs the graph.
* Multiple inputs can be stored in the same state dictionary.
* All required initial state values should be passed together in the `invoke()` dictionary.

---

# 16. Mental Model

The easiest way to remember LangGraph:

```text
State
  ↓
Graph
  ↓
Node
  ↓
Process State
  ↓
Updated State
  ↓
Next Node
  ↓
Final State
```

Or simply:

```text
INPUT → GRAPH → NODE(S) → OUTPUT
```

The **state is the information that travels through the graph**.
