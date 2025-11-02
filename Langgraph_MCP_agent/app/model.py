from langchain.agents import create_agent
from .mcp_client import get_tools


async def get_model():
    tools = await get_tools()
    model = create_agent(
        model="gpt-4.1-mini",
        tools=tools,
    )

    return model
