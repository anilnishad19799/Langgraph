from mem0 import Memory
from qdrant_client import QdrantClient
from .config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

print("*" * 100)
print("QDRANT_URL", QDRANT_URL)
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": COLLECTION_NAME,
            "host": QDRANT_URL.split("//")[-1].split(":")[0],
            "port": 6333,
            "api_key": QDRANT_API_KEY,
        },
    }
}

memory = Memory.from_config(config)

# Ensure user_id index exists
qdrant_client.create_payload_index(
    collection_name=COLLECTION_NAME, field_name="user_id", field_schema="keyword"
)
