import sys
import os
from rank_bm25 import BM25Okapi
 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "ingestion"))
 
from embedder import embed_single_text
from qdrant_client_setup import get_client, DEFAULT_COLLECTION
_cached_points = None
_cached_bm25 = None
 
 
def get_all_chunks_from_qdrant(collection_name: str = DEFAULT_COLLECTION):
    import pickle

    cache_path = os.path.join(os.path.dirname(__file__), "bm25_cache.pkl")

    with open(cache_path, "rb") as f:
        cached_data = pickle.load(f)

    class FakePayloadWrapper:
        def __init__(self, payload):
            self.payload = payload

    return [FakePayloadWrapper(item) for item in cached_data]
 
 
def build_bm25_index(points):
    
    tokenized_corpus = [point.payload["text"].lower().split() for point in points]
    bm25 = BM25Okapi(tokenized_corpus)
    return bm25
 
 
def vector_search(query, collection_name=DEFAULT_COLLECTION, top_k=10):
    client = get_client()
    query_vector = embed_single_text(query)
    results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
    ).points
    return results
 
 
def keyword_search(query, bm25, points, top_k=10):
    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)
 
    
    scored_points = list(zip(scores, points))
    scored_points.sort(key=lambda x: x[0], reverse=True)
 
    return scored_points[:top_k]
 
 
def hybrid_search(query, top_k=5):
    global _cached_points, _cached_bm25

    vector_results = vector_search(query, top_k=10)

    if _cached_points is None or _cached_bm25 is None:
        _cached_points = get_all_chunks_from_qdrant()
        _cached_bm25 = build_bm25_index(_cached_points)

    points = _cached_points
    bm25 = _cached_bm25
    keyword_results = keyword_search(query, bm25, points, top_k=10)
 
    
    combined_scores = {}
 
    for r in vector_results:
        combined_scores[r.payload["text"]] = {
            "score": r.score * 0.6,  
            "payload": r.payload,
        }

    max_bm25_score = max([s for s, _ in keyword_results], default=1) or 1
    for score, point in keyword_results:
        normalized_score = score / max_bm25_score
        text = point.payload["text"]
        if text in combined_scores:
            combined_scores[text]["score"] += normalized_score * 0.4
        else:
            combined_scores[text] = {
                "score": normalized_score * 0.4,
                "payload": point.payload,
            }

    ranked = sorted(combined_scores.values(), key=lambda x: x["score"], reverse=True)
    return ranked[:top_k]


if __name__ == "__main__":
    print("Hybrid search ready. Type a question (or 'exit' to quit).\n")

    while True:
        query = input("Your question: ")
        if query.lower() == "exit":
            break

        results = hybrid_search(query)

        print("\nTop matching chunks (hybrid):\n")
        for r in results:
            print(f"Score: {r['score']:.4f} | Page: {r['payload']['page_number']}")
            print(r["payload"]["text"][:300])
            print("-" * 50)
        print()