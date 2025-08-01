from pydantic import BaseModel, Field
from typing import Optional, List, Annotated, Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command
from graph.models import llm_model
from graph.state import State
from graph.constants import NODE

def format_docs(docs: List[str]) -> str:
    """
    Format the list of documents into a single string.
    """
    return "\n".join(docs)

def format_hallucination_grader_prompt(state: State) -> str:
    """
    Format the prompt for the hallucination grader.
    """
    return f"""
    FACTS: {format_docs(state.context)}
    STUDENT ANSWER: {state.answer}
    """

class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in generation answer."""

    grounded: bool = Field(description="Answer is grounded in the facts, true or false")
    explanation: str = Field(description="Explain the reasoning for the score")

def router_hallucination(state: State):
    """
    Decide whether to route query to perform websearch or retrieve local documents.
    """
    prompt_instructions = SystemMessage(
        content  = """You are a teacher grading a quiz. 
                    You will be given FACTS and a STUDENT ANSWER. 
                    Here is the grade criteria to follow:
                    (1) Ensure the STUDENT ANSWER is grounded in the FACTS. 
                    (2) Ensure the STUDENT ANSWER does not contain "hallucinated" information outside the scope of the FACTS.
                    Score:
                    A score of 1 means that the student's answer meets all of the criteria. This is the highest (best) score. 
                    A score of 0 means that the student's answer does not meet all of the criteria. This is the lowest possible score you can give.
                    Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. 
                    Avoid simply stating the correct answer at the outset."""
    )
    edge_llm = llm_model.with_structured_output(GradeHallucinations)
    result = edge_llm.invoke([prompt_instructions] + HumanMessage(content= format_hallucination_grader_prompt(state)))
    if result.grounded:
        return Command(goto=NODE.USER_VALIDATION)
    elif state.max_retries > 0:
        return Command(
            goto=NODE.ANSWER_GENERATION,
            update={"max_retries": state.max_retries - 1}
        )
    else:
        return Command(goto=NODE.USER_VALIDATION)