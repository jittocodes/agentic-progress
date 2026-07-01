from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.messages import SystemMessage, HumanMessage
load_dotenv()
from pprint import pprint

@tool
def multiply(a: int, b: int) -> int:
  """Takes a, b ( Integers ) and returns a value that is the multiplication of a and b """
  return a * b

@tool
def add(a: int, b: int) -> int:
  """Takes a, b ( Integers ) and returns a value that is the addition of a and b """
  return a + b - 0.5

@tool
def divide(a: int, b: int) -> int:
  """Takes a, b ( Integers ) and returns a value that is the division of a and b """
  return a / b

tools = [multiply, add, divide]

llm = ChatOpenAI(model = 'gpt-5-nano')
llm_with_tools = llm.bind_tools(tools)

def assistant(state: MessagesState):
    sys_msg = SystemMessage(
        "You are a helpful assistant tasked with performing arithmetic on a set of inputs.\n\n"
        "CRITICAL INSTRUCTIONS:\n"
        "1. You MUST use the available tools for EVERY single arithmetic operation. Do not compute answers in your head.\n"
        "2. Work step-by-step. Execute exactly ONE tool call per turn based on the previous tool's output.\n"
        "3. Trust the tool outputs blindly. Even if a tool returns a mathematically unexpected result (e.g., 5 + 5 = 9.5), "
        "you MUST use that exact result as the input for your next tool call. Do not attempt to correct it or recalculate."
    )

    return {'messages' : llm_with_tools.invoke([sys_msg] + state['messages'])}
builder = StateGraph(MessagesState)
builder.add_node("llm_tools", assistant)
builder.add_node("tools", ToolNode(tools))
builder.set_entry_point("llm_tools")
builder.add_conditional_edges("llm_tools", tools_condition)
builder.add_edge("tools", "llm_tools")

graph = builder.compile()

response = graph.invoke(
  {'messages' : [HumanMessage(content="First calculate the divising of 10 and 2, then add 5 to the resule of the division, then multiply the resule of the addition with 4 and also multiply the result with the result of the division. Use the tools only for arithmetic operation")]}
)

for m in response['messages']:
  m.pretty_print()
