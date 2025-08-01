from pydantic import BaseModel, Field
from typing import Annotated, Optional, List


class State(BaseModel):
    """
    Represents the state of the graph.
    """
    question: str = Field(description="The question being asked.")
    answer: str = Field(description="The answer to the question by llm.")
    web_search: bool = Field(description="Whether web search is used.")
    context: List[str] = Field(description="The context used to answer the question.")
    max_retries: int = Field(default=3, description="Maximum number of retries for the llm to generate an answer to the question.")



