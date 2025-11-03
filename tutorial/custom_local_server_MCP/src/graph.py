from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model
import asyncio
from dotenv import load_dotenv
import json
from PIL import Image
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from mem0 import Memory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph
from mem0 import Memory
from qdrant_client import QdrantClient
from pydantic import BaseModel, Field
from langchain.agents.structured_output import ToolStrategy
from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore
from dotenv import load_dotenv

load_dotenv()


# checkpointer = InMemorySaver()
DB_URI = "postgresql://postgres:postgres@localhost:5432/langgraph_db"
checkpointer = PostgresSaver.from_conn_string(DB_URI)


client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["math_server.py"],
            "transport": "stdio",
        },
        "weather": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["weather_server.py"],
            "transport": "stdio",
        },
    }
)


async def get_tools():
    tools = await client.get_tools()
    return tools


tools = asyncio.run(get_tools())


class State(TypedDict):
    """Conversation state passed between nodes"""

    messages: Annotated[
        list[BaseMessage], add_messages
    ]  # chat history for this request
    mem0_user_id: str


qdrant_client = QdrantClient(
    url="https://a92a20e5-49ff-4a82-8365-49bdb11ce639.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.KlvM6TDdSV_v3rZj9hQh5vvsEGOJNrsx8TThjp1N7OA",
)

collection_name = "mem0_yt"
userdata = {
    "Qdrant_API_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.KlvM6TDdSV_v3rZj9hQh5vvsEGOJNrsx8TThjp1N7OA"
}

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": collection_name,
            "host": "a92a20e5-49ff-4a82-8365-49bdb11ce639.us-east4-0.gcp.cloud.qdrant.io",
            "port": 6333,
            "api_key": userdata.get("Qdrant_API_KEY"),
        },
    }
}
memory = Memory.from_config(config)

# Mem0 filters by user_id when searching, so Qdrant needs a keyword index on that field. If you skip this step you’ll get:
# 400 Bad Request – Index required but not found for "user_id" of type [keyword]
qdrant_client.create_payload_index(
    collection_name=collection_name, field_name="user_id", field_schema="keyword"
)


# --------------------- Using Create react agent ---------------------#


class WeatherInfo(BaseModel):
    """Contact information for a person."""

    city: str = Field(description="City name in query")
    weather_status: str = Field(description="Actual weather status")


class MathInfo(BaseModel):
    """Contact information for a person."""

    problem: str = Field(description="Actual Math problem given by user ")
    output: str = Field(description="Actual output")


from typing import Union

model = create_agent(
    model="gpt-4.1-mini",
    tools=tools,
    # response_format=ToolStrategy(Union[WeatherInfo, MathInfo]),
    # response_format=WeatherInfo
)


async def call_model(state: dict):
    global memory
    msgs = state["messages"]
    uid = state["mem0_user_id"]

    # Retrieve top 2 relevant memories
    print("msgs", msgs)
    if msgs:
        mems = memory.search(msgs[-1].content, user_id=uid, limit=2)
        context = (
            "\n".join(f"- {m['memory']}" for m in mems["results"])
            if mems["results"]
            else ""
        )
    else:
        context = ""

    system_message = {
        "role": "system",
        "content": f"""
        You are a helpful assistant.
        Tools available:
        1. Math tool – for calculations.
        2. Weather tool – for weather queries.
        Use tools only when needed; otherwise respond naturally.
        Memory context:
        {context}
        """,
    }

    user_message = {"role": "user", "content": msgs[-1].content}
    print("user_message", user_message)
    print("msgs", msgs)

    # Invoke model
    response = await model.ainvoke({"messages": [system_message, user_message]})

    # Persist memory
    memory.add(
        [
            {"role": "user", "content": user_message["content"]},
            {"role": "assistant", "content": response["messages"][-1].content},
        ],
        user_id=uid,
    )

    # Return a dict (LangGraph expects a dict)
    return {"messages": [response["messages"][-1]]}


# builder = StateGraph(MessagesState)
graph_builder = StateGraph(State)
graph_builder.add_node(call_model)
graph_builder.add_node(ToolNode(tools))
graph_builder.add_edge(START, "call_model")
graph_builder.add_conditional_edges(
    "call_model",
    tools_condition,
)
graph_builder.add_edge("tools", "call_model")
graph = graph_builder.compile(checkpointer=checkpointer)
# graph = graph_builder.compile()
