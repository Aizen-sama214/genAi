import os
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing import Annotated
from config import Config

os.environ["ANTHROPIC_API_KEY"] = Config().anthropic_api_key

# Define a tool
def multiply(a: float, b: float) -> float:
    return a * b
    

class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Query that is optimized web search.")
    justification: str = Field(
        None, description="Why this query is relevant to the user's request."
    )
    gender: str = Field(None, description="Gender of the candidate.")
    messages: Annotated[list[BaseMessage], add_messages]

class Llm():
    def __init__(self, model_name: str = "claude-3-5-sonnet-latest"):
        self.llm = ChatAnthropic(model=model_name)
        self.llm_with_tools = self.llm.bind_tools([multiply])
        self.structured_llm = self.llm_with_tools.with_structured_output(SearchQuery)


# usage example


if __name__ == "__main__":
    llm = Llm()
    response = llm.structured_llm.invoke(
        "What is the best search query to find jobs in AI?"
    )
    print(response)
    print(response.search_query)
    print(response.justification)
