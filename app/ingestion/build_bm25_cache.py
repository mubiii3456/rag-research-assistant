import sys
import os
import pickle
import time
 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "retrieval"))
 
from qdrant_client_setup import get_client, DEFAULT_COLLECTION
 
CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "retrieval", "bm25_cache.pkl")
 
 
def fetch_all_points_slowly(collection_name=DEFAULT_COLLECTION, batch_size=50):
    client = get_client()
    all_points = []
    next_offset = None
    batch_num = 0
 
    while True:
        batch_num += 1
        attempts = 0
        while attempts < 5:
            try:
                points, next_offset = client.scroll(
                    collection_name=collection_name,
                    limit=batch_size,
                    offset=next_offset,
                    with_payload=True,
                )
                break
            except Exception as e:
                attempts += 1
                print(f"Scroll batch {batch_num} failed (attempt {attempts}/5): {e}")
                time.sleep(2)
                if attempts == 5:
                    raise
 
        all_points.extend(points)
        print(f"Fetched batch {batch_num} ({len(all_points)} points so far)")
 
        if next_offset is None:
            break
 
    return all_points
 
 
if __name__ == "__main__":
    print("Fetching all points from Qdrant (this may take a while)...")
    points = fetch_all_points_slowly()
 
    simplified = [
        {"text": p.payload["text"], "page_number": p.payload["page_number"], "filename": p.payload["filename"]}
        for p in points
    ]
 
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(simplified, f)
 
    print(f"\nSaved {len(simplified)} points to local cache: {CACHE_FILE}")
 