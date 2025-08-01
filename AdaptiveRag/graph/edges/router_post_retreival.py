from pydantic import BaseModel, Field
from typing import Optional, List, Annotated, Literal
from graph.models import llm_model
from graph.state import State
from langchain_core.messages import HumanMessage, SystemMessage
from graph.constants import NODE


def router_query(state: State):
    """
    Check whether the documents retrieved are relevant to the question or not.
    """
    web_search = state.web_search
    if web_search:
        return NODE.ANSWER_GENERATION
    return NODE.WEB_SEARCH
    