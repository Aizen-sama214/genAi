import config
import os

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY

from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

def get_weather(city: str) -> str:  
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:  
    user_name = config["configurable"].get("name")
    system_msg = f"You are a helpful assistant. Address the user as {user_name}."
    return [{"role": "system", "content": system_msg}] + state["messages"]

checkpointer = InMemorySaver()

class WeatherResponse(BaseModel):
    conditions: str
    temperature: float

agent = create_react_agent(
    model="gpt-4o-mini",
    tools=[get_weather],
    prompt=prompt,
    checkpointer=checkpointer,
    response_format=("Provide the temperature in Celsius.", WeatherResponse)
)

config={
   "configurable": {
      "name": "Anirudh",
      "thread_id": "1"
   }
}

# Run the agent
response1 = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
    config=config
)

response2 = agent.invoke(
    {"messages": [{"role": "user", "content": "Is that better than in nyc?"}]},
    config=config
)


print(response1)  # Print the last message from the assistant

print(response2)  # Print the last message from the assistant

{
   'messages': [
      HumanMessage(
         content='what is the weather in sf', 
         additional_kwargs={}, 
         response_metadata={}, 
         id='aac73311-c573-4d25-88f3-3d3c472cacb5'
        ), 
      AIMessage(
         content=[
            {
               'text': "Hello Anirudh,\n\nI'd be happy to check the weather in San Francisco for you. Let me get that information right away.", 
               'type': 'text'
            }, 
            {
               'id': 'toolu_01N9qbfn1GWNDnkoH6kcnyaA', 
               'input': 
                {
                   'city': 'San Francisco'
                }, 
                'name': 'get_weather', 
                'type': 'tool_use'
            }
        ], 
        additional_kwargs={}, 
        response_metadata={'id': 'msg_015vX18KUy3xdzR1ZDWechiL', 'model': 'claude-3-7-sonnet-20250219', 'stop_reason': 'tool_use', 'stop_sequence': None, 'usage': {'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0, 'input_tokens': 397, 'output_tokens': 85, 'server_tool_use': None, 'service_tier': 'standard'}, 'model_name': 'claude-3-7-sonnet-20250219'}, id='run--3ac26a1d-c6a9-4c3f-af9d-e12790472067-0', tool_calls=[{'name': 'get_weather', 'args': {'city': 'San Francisco'}, 'id': 'toolu_01N9qbfn1GWNDnkoH6kcnyaA', 'type': 'tool_call'}], 
        usage_metadata={'input_tokens': 397, 'output_tokens': 85, 'total_tokens': 482, 'input_token_details': {'cache_read': 0, 'cache_creation': 0}}), 
    ToolMessage(
       content="It's always sunny in San Francisco!", 
       name='get_weather', 
       id='e2401109-2773-4df8-9ce5-71fd56690a35', 
       tool_call_id='toolu_01N9qbfn1GWNDnkoH6kcnyaA'
    ), 
    AIMessage(
       content="Good news, Anirudh! It's always sunny in San Francisco right now. Perfect weather to enjoy the city's attractions. Is there anything else about San Francisco or any other location you'd like to know about?", 
       additional_kwargs={}, 
       response_metadata={'id': 'msg_01Fc53PsC6BWZomRZjFiinNu', 'model': 'claude-3-7-sonnet-20250219', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0, 'input_tokens': 500, 'output_tokens': 50, 'server_tool_use': None, 'service_tier': 'standard'}, 'model_name': 'claude-3-7-sonnet-20250219'}, 
       id='run--5b5bc908-4691-42be-9956-de63716f185e-0', 
       usage_metadata={'input_tokens': 500, 'output_tokens': 50, 'total_tokens': 550, 'input_token_details': {'cache_read': 0, 'cache_creation': 0}}
       )
    ]
}