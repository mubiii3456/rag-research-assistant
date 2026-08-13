import sys
import os
 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app", "retrieval"))
 
from qdrant_client_setup import get_client, DEFAULT_COLLECTION, EMBEDDING_SIZE
from qdrant_client.models import Distance, VectorParams
 
 
def clear_and_recreate_collection(collection_name: str):
    client = get_client()
    client.delete_collection(collection_name=collection_name)
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=EMBEDDING_SIZE, distance=Distance.COSINE),
    )
    print(f"Collection '{collection_name}' cleared and recreated.")
 
 
if __name__ == "__main__":
    clear_and_recreate_collection(DEFAULT_COLLECTION)
 