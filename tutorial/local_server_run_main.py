from langgraph_sdk import get_client
import asyncio
from dotenv import load_dotenv

load_dotenv()
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"  # ✅ correct key name
os.environ["LANGSMITH_API_KEY"] = (
    "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"  # ✅ your actual API key
)
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"  # default endpoint
os.environ["LANGCHAIN_PROJECT"] = "my-local-agent"  # optional project name

client = get_client(url="http://localhost:2024")


async def main():
    async for chunk in client.runs.stream(
        None,  # Threadless run
        "agent",  # Name of assistant. Defined in langgraph.json.
        input={
            "messages": [
                {
                    "role": "human",
                    "content": "What is LangGraph?",
                }
            ],
        },
    ):
        print(f"Receiving new event of type: {chunk.event}...")
        print(chunk.data)
        print("\n\n")


asyncio.run(main())
