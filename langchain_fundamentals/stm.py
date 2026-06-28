from langchain_openai import OpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from dotenv import load_dotenv

agent = create_agent(
  'gpt-5o-nano',
  checkpointer= InMemorySaver()
)

question = HumanMessage(content="Hello! My name is mushu! I like to play a local game called MushuMushu.")
config = {"configurable" : {"thread_id" : "1"}}

response = agent.invoke(
  {'messages' : [question]},
  config
)

print(response['messages'][-1].content)

question = HumanMessage('Whats my name and whats my favorite game? only answer with What? : Ans.')

response = agent.invoke(
  {'messages' : [question]},
  config
)

print(response['messages'][-1].content)
