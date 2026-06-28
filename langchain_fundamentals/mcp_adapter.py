from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import asyncio
import pprint
from dotenv import load_dotenv
load_dotenv()

client = MultiServerMCPClient({
    "local_server": {
        "transport": "stdio",
        "command": "python",
        "args": ["/Users/insecupa/Documents/Coding/ai-engineering-projects/langchain_fundamentals/mcp_server.py"]
    }
})

async def func():
    tools = await client.get_tools()
    prompt = await client.get_prompt("local_server", "prompt")
    print(prompt[0].content)

    llm = ChatOpenAI(model="gpt-4o-mini")

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=prompt[0].content
    )

    response = await agent.ainvoke(
        {"messages": [HumanMessage(content="Tell me about the langchain-mcp-adapters library")]},
        config={"configurable": {"thread_id": "1"}}
    )

    pprint.pprint(response)

asyncio.run(func())
