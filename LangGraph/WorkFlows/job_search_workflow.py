from config import Config
# from Tools.job_data_tools import load_job_data, filter_jobs_by_location
from basic_block import Llm
from typing import TypedDict, Annotated, Sequence, Optional
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages



# job_data = load_job_data()


#graph state
class CandidateProfileState(BaseModel):
    name: Optional[str] = Field(None, description="Name of the candidate.")
    age: Optional[int] = Field(None, description="Age of the candidate.")
    is_active: Optional[bool] = Field(None, description="Is the candidate actively looking for a job?")
    messages: Annotated[Sequence[BaseMessage], add_messages]
    success: Optional[bool] = Field(None, description="Indicates if the candidate profile extraction was successful.")

# Initialize LLM
llm = Llm(model_name="claude-3-5-sonnet-latest").llm.with_structured_output(CandidateProfileState)

# Nodes
def extract_candidate_profile(state:  CandidateProfileState) -> CandidateProfileState:
    system_prompt = SystemMessage(content="You are a job assistant. Please extract the candidate's profile information. Ask them " \
    "for their name, age, and whether they are actively looking for a job.")

    print("Extracting candidate profile from messages...")
    response = llm.invoke([system_prompt] + state.messages)
    return {
        "name": response.name,
        "age": response.age,
        "is_active": response.is_active,
        "messages": response.messages,
        "success": response.success
    }

def endpoint(state: CandidateProfileState) -> str:
    if state.name and isinstance(state.age, int) and state.is_active is not None:
        return {
            "name": state.name,
            "age": state.age,
            "is_active": state.is_active,
            "messages": state.messages,
            "success": True
        }
    return {
        "name": None,
        "age": None,
        "is_active": None,
        "messages": state.messages,
        "success": False
    }


# Router
def validate_candidate_profile(state: CandidateProfileState) -> str:
    """Validate candidate profile data"""

    print("Validating candidate profile...")
    if state.name and isinstance(state.age, int) and state.is_active is not None:
        return "Pass"
    return "Fail"

job_extractor_graph = StateGraph(CandidateProfileState)

job_extractor_graph.add_node("extract_candidate_profile", extract_candidate_profile)
job_extractor_graph.add_node("endpoint", endpoint)

job_extractor_graph.add_edge(START, "extract_candidate_profile")
# job_extractor_graph.add_conditional_edges(
#     "extract_candidate_profile", validate_candidate_profile, {"Fail": "extract_candidate_profile", "Pass": }
# )
job_extractor_graph.add_edge("extract_candidate_profile", "endpoint")
job_extractor_graph.add_edge("endpoint", END)

# Compile
job_extractor = job_extractor_graph.compile()

# Invoke
messages = [
    HumanMessage(content = "Hi, I am looking for a job"),
    HumanMessage(content = "My name is John Doe"),
    HumanMessage(content = "I am 30 years old"),
    HumanMessage(content = "I am actively looking for a job")
]
result = job_extractor.invoke({"messages": [messages[0]]})
print("Candidate Profile Extracted:")
print(result)