from typing import TypedDict, Literal
import random
from langgraph.graph import StateGraph, START, END
from pprint import pprint

class State(TypedDict):
  graph_state: str

def node1(state):
  return {"graph_state" : state['graph_state'] + 'I am'}

def node2(state):
  return {"graph_state" : state['graph_state'] + ' happy!'}

def node3(state):
  return {"graph_state" : state['graph_state'] + ' sad!'}

def decide_mood(state) -> Literal["bad", "good"]:
  user_input = state['graph_state']

  if random.random() < 0.5:
    return "bad"

  return "good"

builder = StateGraph(State)

builder.add_node("node_1", node1)
builder.add_node("node_2", node2)
builder.add_node("node_3", node3)

builder.add_edge(START, "node_1")
builder.add_conditional_edges(
  "node_1",
  decide_mood,
  {
    "bad" : "node_3",
    "good" : "node_2"
  }
)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()

response = graph.invoke(
  {'graph_state' : "Hi, This is urumaki."}
)

pprint(response)
