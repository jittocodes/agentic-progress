from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.messages import HumanMessage, ToolMessage
from langchain.tools import tool, ToolRuntime
from dotenv import load_dotenv
load_dotenv()
from pprint import pprint
from langchain.agents import AgentState
from langgraph.types import Command
from langgraph.checkpoint.memory import InMemorySaver

class CustomState(AgentState):
  favourite_color: str


## Write to state
@tool
def update_favourite_color(favourite_color: str, runtime: ToolRuntime) -> Command:
  """Update the favourite colour of the user in the state once they've revelead it"""

  return Command(
    update={
      "favourite_color" : favourite_color,
      "messages" : [ToolMessage(content = 'Successfully updates the fav colour', tool_call_id = runtime.tool_call_id)]
    }
  )

agent = create_agent(
  'gpt-5-nano',
  tools = [update_favourite_color],
  state_schema= CustomState,
  checkpointer=InMemorySaver()
)
config = {'configurable' : {'thread_id' : '1'}}
response = agent.invoke(
  {'messages' : [HumanMessage("my fav colour is red colour")]},
  config=config
)

pprint(response['messages'][-1].content)

response = agent.invoke(
  {'messages' : [HumanMessage("What is my fav colour")]},
  config=config
)

pprint(response['messages'][-1].content)
