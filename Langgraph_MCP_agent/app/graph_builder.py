import asyncio
from .state import State
from .memory_manager import memory
from .model import get_model
from .config import DB_URI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition


async def call_model(state: State):
    model = await get_model()
    msgs = state["messages"]
    uid = state["mem0_user_id"]

    context = ""
    if msgs:
        mems = memory.search(msgs[-1].content, user_id=uid, limit=2)
        if mems["results"]:
            context = "\n".join(f"- {m['memory']}" for m in mems["results"])

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

    """
    below comment code is for using with creat_agent model
    """
    # conversation_text = ""
    # for msg in state["messages"]:
    #     if isinstance(msg, HumanMessage):
    #         conversation_text += f"User: {msg.content}\n"
    #     elif isinstance(msg, AIMessage):
    #         conversation_text += f"AI: {msg.content}\n"

    # user_message = {"role": "user", "content": state['message']}
    # response = await model.ainvoke({"messages": [system_message, user_message]})
    # return {"messages": [response["messages"][-1]]}

    response = await model.ainvoke([system_message] + msgs)

    memory.add(
        [
            {"role": "user", "content": msgs[-1].content},
            {"role": "assistant", "content": response.content},
        ],
        user_id=uid,
    )

    return {"messages": [response]}


def build_graph(tools):
    graph_builder = StateGraph(State)
    graph_builder.add_node(call_model)
    graph_builder.add_node(ToolNode(tools))
    graph_builder.add_edge(START, "call_model")
    graph_builder.add_conditional_edges("call_model", tools_condition)
    graph_builder.add_edge("tools", "call_model")
    graph_builder.add_edge("call_model", END)
    return graph_builder
