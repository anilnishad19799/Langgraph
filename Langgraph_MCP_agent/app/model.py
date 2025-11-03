from langchain.agents import create_agent
from .mcp_client import get_tools
from langchain.chat_models import init_chat_model


async def get_model():
    tools = await get_tools()
    model = init_chat_model("openai:gpt-3.5-turbo")
    return model.bind_tools(tools)

    # model = create_agent(
    #     model="gpt-4.1-mini",
    #     tools=tools,
    # )
