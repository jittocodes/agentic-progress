from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated
from langchain.messages import AnyMessage
from langgraph.graph.message import add_messages

class MessageState(TypedDict):
  messages: Annotated[list[AnyMessage], add_messages]
  # Here instead of using a reducer you can use

class StateWithReduce(MessagesState):
  pass

# Reducers
# Appends to state
