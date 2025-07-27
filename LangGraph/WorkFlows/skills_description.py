from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    name : str
    age: int
    skills: List[str]
    result: str

def greeting(state: State):
    """Generate a greeting message based on the user's name"""

    state["result"] = f'{state["name"]}, welcome to the system!'
    return state

def age_descrition(state: State):
    """Provide a description based on the user's age"""

    if state["age"] < 18:
        state["result"] += " You are a minor."
    elif 18 <= state["age"] < 65:
        state["result"] += " You are an adult."
    else:
        state["result"] += " You are a senior citizen."
    return state

def skills_description(state: State):
    """Provide a description based on the user's skills"""

    if not state["skills"]:
        state["result"] += " You have no skills listed."
    else:
        state["result"] += f" Your skills include: {', '.join(state['skills'])}."
    return state

graph_builder = StateGraph(State)
graph_builder.add_node("greeting", greeting)
graph_builder.add_node("age_description", age_descrition)
graph_builder.add_node("skills_description", skills_description)
graph_builder.add_edge(START, "greeting")
graph_builder.add_edge("greeting", "age_description")
graph_builder.add_edge("age_description", "skills_description")
graph_builder.add_edge("skills_description", END)
graph = graph_builder.compile()

# Example usage
result = graph.invoke({
    "name": "Alice",
    "age": 25,
    "skills": ["Python", "Data Analysis"]
})
print(result["result"])  # Output: Alice, welcome to the system! You are an

# adult. Your skills include: Python, Data Analysis.
# Output: Alice, welcome to the system! You are an adult. Your skills include: Python, Data Analysis.
# You can modify the input to test different scenarios.
# Output: Alice, welcome to the system! You are an adult. Your skills include: Python, Data Analysis.

result = graph.invoke({
    "name": "Bob",
    "age": 70,
    "skills": []
})  
print(result["result"])  # Output: Bob, welcome to the system! You are a senior citizen. You have no skills listed.
