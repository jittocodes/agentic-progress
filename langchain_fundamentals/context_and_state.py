from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool, ToolRuntime
from dotenv import load_dotenv
load_dotenv()
from pprint import pprint


@dataclass
class ColourContext:
  fav_colour: str = 'blue'
  least_fav_colour: str = 'yellow'

@tool
def get_favourite_color(runtime: ToolRuntime) -> str:
  """Get the fav colour from the tool runtime"""
  return runtime.context.fav_colour

@tool
def get_least_favourite_color(runtime: ToolRuntime) -> str:
  """Get the least fav colour from the tool runtime"""
  return runtime.context.least_fav_colour

agent = create_agent(
  model = 'gpt-5-nano',
  context_schema=ColourContext,
  tools = [get_favourite_color, get_least_favourite_color]
)

question = 'What is my fav colour and what is least fav colour, only answer with the answers, nothing more.'

response = agent.invoke(
  {'messages' : [HumanMessage(content=question)]},
  context= ColourContext()
)

pprint(response)

print("++++++++++++++++++")

pprint(response['messages'][-1].content)
