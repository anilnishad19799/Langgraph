from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
from .mcp_client import get_tools
from .graph_builder import build_graph

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to templates
TEMPLATES_DIR = Path(__file__).parent.parent / "frontend"
INDEX_HTML = TEMPLATES_DIR / "index.html"

checkpointer = InMemorySaver()
graph = None  # placeholder
graph_builder = None
tools = None  # we will set this on startup


# startup event
@app.on_event("startup")
async def startup_event():
    global tools, graph, graph_builder
    tools = await get_tools()
    if not tools:
        raise RuntimeError("Failed to load MCP tools!")
    logger.info(f"Tools initialized: {tools}")
    graph_builder = build_graph(tools)
    graph = graph_builder.compile(checkpointer=checkpointer)
    logger.info("Graph compiled!")


class QueryRequest(BaseModel):
    username: str
    thread_id: str
    query: str


@app.get("/")
async def get_index():
    """Serve the index.html page."""
    return FileResponse(INDEX_HTML)


@app.post("/ask")
async def ask(req: QueryRequest):
    state = {
        "messages": [HumanMessage(content=req.query)],
        "mem0_user_id": req.username,
    }
    config = {"configurable": {"thread_id": req.thread_id}}
    print("config", config)
    result = await graph.ainvoke(state, config=config)
    return {"response": result["messages"][-1].content}


# import asyncio
# from graph_builder import build_graph
# from langchain_core.messages import HumanMessage
# from langgraph.checkpoint.postgres import PostgresSaver
# from config import DB_URI
# from langgraph.checkpoint.memory import InMemorySaver

# checkpointer = InMemorySaver()


# async def main():
#     graph_builder = build_graph()
#     user_id = "demo_user_001"
#     state = {
#         "messages": [HumanMessage(content="What's the weather in New York?")],
#         "mem0_user_id": user_id,
#     }

#     config = {"configurable": {"thread_id": "1"}}

#     graph = graph_builder.compile(checkpointer=checkpointer)
#     result = await graph.ainvoke(state, config=config)
#     print(result["messages"][-1].content)


# if __name__ == "__main__":
#     asyncio.run(main())
