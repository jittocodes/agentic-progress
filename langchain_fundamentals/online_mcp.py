import asyncio
from pprint import pprint
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
load_dotenv()

client = MultiServerMCPClient(
  {
      "time": {
        "transport" : "stdio",
        "command": "uvx",
        "args": [
          "mcp-server-time",
          "--local-timezone=America/New_York"
        ]
      }
    }
)

async def func():
  tools = await client.get_tools()

  agent = create_react_agent(
    model = 'gpt-5-nano',
    tools = tools
  )

  response = await agent.ainvoke(
    {'messages' : [HumanMessage('What time is it?')]}
  )

  pprint(response)

asyncio.run(func())
