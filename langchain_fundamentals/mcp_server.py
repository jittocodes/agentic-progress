from dotenv import load_dotenv
load_dotenv()

from mcp.server.fastmcp import FastMCP
from typing import Dict, Any
from requests import get

mcp = FastMCP("mcp_server")

@mcp.tool()
def search_local_dict(query: str) -> Dict[str, Any]:
  """Search Local Dict for a query"""

  results = {
    "ok" : "Not okay",
    "Chookay" : "okok",
    "query" : "peri peri"
  }

  return results[query]

@mcp.resource("github://langchain-ai/langchain-mcp-adapters/blob/main/README.md")
def github_file():
  """
  Resource for accessing angchain-ai/langchain-mcp-adapters/blob/main/README.md
  """

  url = f'https://raw.githubusercontent.com/langchain-ai/langchainjs/refs/heads/main/libs/langchain-mcp-adapters/README.md'

  try:
    resp = get(url)
    return resp.text
  except Exception as e:
    return f"Error: {str(e)}"


@mcp.prompt()
def prompt():
  """Analyze data from a lanchain-ai repo with comprehensive insights"""
  return """
    You are a helpful assistant that answerss user questions about LangChain, LangGraph and LangSmith

    You can use the following tools/resources to answer user questions:
    - search_local_dict: Searches a local dict for a query.
    - github_file: Access the langchain-ai repo files

    If the user answers question that is not related to LangChain, LangGraph or LangSmith, you should say 'I'm Sorry, I cant help you with that'

    You may try multiple tool and resources calls to answer the users question.
  """

if __name__ == '__main__':
  mcp.run(transport="stdio")
