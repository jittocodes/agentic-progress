from langgraph.graph import StateGraph
from langgraph.graph import MessagesState
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition
from pprint import pprint
from langchain.messages import HumanMessage
load_dotenv()

@tool
def multiply(a: int, b: int) -> int:
  """Takes a, b ( Integers ) and returns a value that is the multiplication of a and b """
  return a * b

llm = ChatOpenAI(model = 'gpt-5-nano')
llm_with_tools = llm.bind_tools([multiply])

llm_agent = create_agent(
  model='gpt-5-nano',
  tools = [multiply]
)

#Node
def tool_calling_llm(state: MessagesState):
  return {"messages" : [llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(MessagesState)

builder.add_node("llm_with_tools", tool_calling_llm)
builder.add_node("tools", ToolNode([multiply]))
builder.set_entry_point("llm_with_tools")
builder.add_conditional_edges(
  "llm_with_tools",
  tools_condition
)
builder.set_finish_point("tools")
graph = builder.compile()
pprint(graph.get_graph().draw_ascii())

messages = [HumanMessage(content = 'What is the result of 3 multiplied by 4')]

response = graph.invoke(
  {"messages" : messages}
)

for m in response['messages']:
  m.pretty_print()
