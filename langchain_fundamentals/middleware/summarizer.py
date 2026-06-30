from langchain_fundamentals.initchat import model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import SummarizationMiddleware

agents = create_agent(
  model='gpt-5-nano',
  checkpointer=InMemorySaver(),
  middleware=SummarizationMiddleware(
    model='gpt-4o-mini',
    trigger=('tokens', 100),
    keep=('messages', 1)
  )
)
