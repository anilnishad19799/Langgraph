# mcp_client.py
import os
from langchain_mcp_adapters.client import MultiServerMCPClient

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            "args": [os.path.join(BASE_DIR, "server", "math_server.py")],
            "transport": "stdio",
        },
        "weather": {
            "command": "python",
            "args": [os.path.join(BASE_DIR, "server", "weather_server.py")],
            "transport": "stdio",
        },
    }
)


# Only define async function, no asyncio.run()
async def get_tools():
    return await client.get_tools()
