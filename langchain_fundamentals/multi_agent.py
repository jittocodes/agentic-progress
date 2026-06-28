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

@tool
def square(x: float) -> float:
  """Calculate a square of a number"""

  return x ** 2

@tool
def square_root(x: float) -> float:
  """Calculates the square root of a number"""

  return x ** 0.5

subagent_1 = create_agent(
  'gpt-5-nano',
  tools = [square_root]
)

subagent_2 = create_agent(
  'gpt-5-nano',
  tools = [square]
)

@tool
def call_subagent_1(x: float) -> float:
  """Call subagent 1 in order to calculate the square root of a number"""
  response = subagent_1.invoke(
    {'messages' : [HumanMessage(content=f'Calculate the square root of {x}')]}
  )
  return response['messages'][-1].content

@tool
def call_subagent_2(x: float) -> float:
  """Call subagent 2 in order to calculate the square of a number"""
  response = subagent_2.invoke(
    {'messages' : [HumanMessage(content=f'Calculate the square of {x}')]}
  )
  return response['messages'][-1].content

main_agent = create_agent(
  'gpt-5-nano',
  tools= [call_subagent_1, call_subagent_2],
  system_prompt='You are a helpful assistant who can call subagents to calculate the square root or a square of a number'
)

pprint(
  main_agent.invoke(
    {'messages' : [HumanMessage('What is the square root of 2.67')]},
    config= {'configurable' : {'thread_id' : '1'}}
  )
)
