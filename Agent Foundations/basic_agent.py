from langchain.agents import structured_output
from langchain_openai import OpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Answer(BaseModel):
  summary: str
  confidence: float

@tool
def calculate_aread(a : float) -> float:
  """This tool calculates area and returns the area

  Input:
    a : Number to calculate the area for.

  Returns:
    float: Area Calculated
  """

  return a * 0.07

@tool
def search_internet(query: str) -> str:
  """This tool searches the internet and returns the search result"""
  return f"{query} means, its a life meaning"

tools = [search_internet, calculate_aread]

agent = create_agent(
  model = 'gpt-4.1',
  tools= tools,
  system_prompt=("""
You are a helpful assistant.
Use tools when needed.
Only answer using information explicitly returned by tools.
If the tool result is insufficient, say that clearly.
Be concise and accurate.
"""
    ),
  response_format=Answer
)

result = agent.invoke(
  {'messages' : [
    {'role' : 'user', 'content' : 'I have a plot, but confused on what the area is for it, they told me its 34, can you tell me the area. Give only number nothing else.'}
  ]}
)

# print(result)

# print(result["structured_response"])

for msg in result["messages"]:
    print(type(msg).__name__, getattr(msg, "content", ""))

