import sys
import os
 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "ingestion"))
 
from embedder import embed_single_text
from qdrant_client_setup import get_client, DEFAULT_COLLECTION
 
 
def search_qdrant(query: str, collection_name: str = DEFAULT_COLLECTION, top_k: int = 3):
    client = get_client()
    query_vector = embed_single_text(query)
 
    results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
    ).points
 
    return results
 
 
if __name__ == "__main__":
    print("Connected to Qdrant. Type a question (or 'exit' to quit).\n")
 
    while True:
        query = input("Your question: ")
        if query.lower() == "exit":
            break
 
        results = search_qdrant(query)
 
        print("\nTop matching chunks:\n")
        for r in results:
            print(f"Score: {r.score:.4f} | Page: {r.payload['page_number']} | File: {r.payload['filename']}")
            print(r.payload["text"][:300])
            print("-" * 50)
        print()
 