from platform import system
from statistics import mode
from langchain_mcp_adapters.client import MultiServerMCPClient
from typing import Dict, Any
from langchain.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain.agents import AgentState
from langchain.agents import create_agent

client = MultiServerMCPClient(
  {
    "travel_server": {
          "url": "https://mcp.kiwi.com",
          "transport" : "streamable_http"
        }
      }
)

db = SQLDatabase.from_uri('sqlite:///resources/Chinook.db')

@tool
def query_playlist_db(query: str) -> str:
  """Query the database for playlist information"""
  try:
    return db.run(query)
  except Exception as e:
    return f"Error querying the database: {e}"

class WeddingState(AgentState):
  origin: str
  destination: str
  guest_countr: int
  genre: str

async def setup():
  tools = await client.get_tools()


  travel_agent = create_agent(
    model = 'gpt-5-nano',
    tools = tools,
    system_prompt = """
      You are a travel agent, Search for flights to the designed desitnation wedding location.
      You are not allowed to ask any more follow up questions. you must find the best flight options based on the following:
        - Price (Lowest, Economy class)
        - Duration (Shortest)
        - Date (Time of the year which you believe is the best for a wedding at this location)
      To make things easy, only look for one ticket, one way.
      You may need to make multiple searches to iteratively find the best options.
      You will be give no extra information, only origin and destination. It is your job to think critically about the planning.
      Once you have found the best options, let the user know your shortlist of the options.
    """
  )

  playlist_agent = create_agent(

  )
