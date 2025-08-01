from pydantic import BaseModel, Field
from typing import Optional, List, Annotated, Literal
from graph.models import llm_model
from graph.state import State
from langchain_core.messages import HumanMessage, SystemMessage
from graph.constants import NODE



class RouterQuery(BaseModel):
    """
    Route the query to the appropriate node type.
    """
    datasource: Literal["web", "knowledge_base"] = Field(description="Given a user question choose to route it to web search or a vectorstore.")


def router_query(state: State):
    """
    Decide whether to route query to perform websearch or retrieve local documents.
    """
    prompt_instructions = SystemMessage(
        content = """You are an expert at routing a user question to a vectorstore or web search.

                    The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
                                                        
                    Use the vectorstore for questions on these topics. For all else, use web-search."""
    )
    edge_llm = llm_model.with_structured_output(RouterQuery)
    result = edge_llm.invoke([prompt_instructions] + HumanMessage(content= state["question"]))
    if result.datasource == "knowledge_base":
        return NODE.RETRIEVE
    else :
        return NODE.WEBSEARCH
    