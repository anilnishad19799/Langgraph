import os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv(
    "DB_URI", "postgresql://postgres:postgres@localhost:5432/langgraph_db"
)

QDRANT_URL = os.getenv("QDRANT_URL", "https://your-qdrant-instance:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "your_api_key")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "mem0_yt")
