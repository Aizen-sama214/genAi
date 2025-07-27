from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    name : str
    greeting: str

def greeting(state: State):
    """Generate a greeting message based on the user's name."""

    return {"greeting": f"Hello, {state['name']}! How can I assist you today?"}

graph_builder = StateGraph(State)

# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("greeting", greeting)
graph_builder.add_edge(START, "greeting")
graph_builder.add_edge("greeting", END)
graph = graph_builder.compile()


result = graph.invoke({"name": "Alice"})
print(result["greeting"])  # Output: Hello, Alice! How can I assist you today?