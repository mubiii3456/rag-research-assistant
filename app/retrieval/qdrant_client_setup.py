import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
 
load_dotenv()
 
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
 
EMBEDDING_SIZE = 384
 
DEFAULT_COLLECTION = "default_documents"
UPLOADS_COLLECTION = "session_uploads"
 
 
def get_client() -> QdrantClient:
    return QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )
 
 
def create_collection_if_not_exists(client: QdrantClient, collection_name: str):
    existing_collections = [c.name for c in client.get_collections().collections]
 
    if collection_name in existing_collections:
        print(f"Collection '{collection_name}' already exists. Skipping creation.")
        return
 
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=EMBEDDING_SIZE, distance=Distance.COSINE),
    )
    print(f"Collection '{collection_name}' created.")
 
 
if __name__ == "__main__":
    client = get_client()
 
    print("Connecting to Qdrant...")
    print(client.get_collections())
 
    create_collection_if_not_exists(client, DEFAULT_COLLECTION)
    create_collection_if_not_exists(client, UPLOADS_COLLECTION)
 
    print("\nFinal collections in Qdrant:")
    print(client.get_collections())
 