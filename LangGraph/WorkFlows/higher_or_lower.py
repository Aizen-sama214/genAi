from typing import TypedDict, List
import random
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    player_name: int
    guesses: List[int]
    attempts: int
    lower_bound: int
    upper_bound: int
    target_number: int
    hint: str
    result: bool
    max_attempts: int

# Nodes
def setup_game(state: State):
    """Initialize the game state with player name and bounds."""
    state["attempts"] = 0
    state["guesses"] = []
    if state.get("lower_bound") is None:
        state["lower_bound"] = 1
    if state.get("upper_bound") is None:
        state["upper_bound"] = 100
    if state.get("target_number") is None:
        state["target_number"] = random.randint(state["lower_bound"], state["upper_bound"])
    if state.get("max_attempts") is None:
        state["max_attempts"] = 3
    print(f"Welcome {state['player_name']}! Guess a number between {state['lower_bound']} and {state['upper_bound']}.")
    return state

def guess(state: State):
    """Make a random integer guess within the bounds."""
    if state.get("hint") is not None:
        if state["hint"] == "higher":
            state["lower_bound"] = state["guesses"][-1] + 1
        elif state["hint"] == "lower":
            state["upper_bound"] = state["guesses"][-1] - 1
    state["guesses"].append(random.randint(state["lower_bound"], state["upper_bound"]))
    state["attempts"] += 1
    print(f"Guessing: {state['guesses'][-1]}")
    return state

def hint(state: State):
    """Provide a hint based on the last guess."""
    if state["guesses"][-1] < state["target_number"]:
        state["hint"] = "higher"
        print("Hint: Try a higher number.")
    elif state["guesses"][-1] > state["target_number"]:
        state["hint"] = "lower"
        print("Hint: Try a lower number.")
    else:
        state["hint"] = "correct"
        print("Hint: You've got it!")   
    return state

# Routers
def validate(state: State):
    """Check if the guess is correct or if the game should continue."""
    if state["target_number"] == state["guesses"][-1]:
        state["result"] = True
        print(f"Congratulations {state['player_name']}! You guessed the number {state['target_number']} in {state['attempts']} attempts.")
        return "end"
    elif state["attempts"] >= state["max_attempts"]:
        state["result"] = False
        print(f"Sorry {state['player_name']}, you didn't guess the number {state['target_number']} in {state['max_attempts']} attempts.")
        return "end"
    else:
        return "hint"
    
# Graph Definition
graph_builder = StateGraph(State)
graph_builder.add_node("setup_game", setup_game)
graph_builder.add_node("guess", guess)
graph_builder.add_node("hint", hint)

graph_builder.add_edge(START, "setup_game")
graph_builder.add_edge("setup_game", "guess")
graph_builder.add_conditional_edges(
    "guess", validate, {"end": END, "hint": "hint"}
)
graph_builder.add_edge("hint", "guess")
graph = graph_builder.compile()

# Example usage
if __name__ == "__main__":
    initial_state = {
        "player_name": "Alice",
        "guesses": [],
        "target_number": 5,
        "lower_bound": 1,
        "upper_bound": 200,
    }
    result = graph.invoke(initial_state)
