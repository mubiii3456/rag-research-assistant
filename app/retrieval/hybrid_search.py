import sys
import os
from rank_bm25 import BM25Okapi
 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "ingestion"))
 
from embedder import embed_single_text
from qdrant_client_setup import get_client, DEFAULT_COLLECTION
 
 
def get_all_chunks_from_qdrant(collection_name: str = DEFAULT_COLLECTION):
    
    client = get_client()
    all_points = []
    next_offset = None
 
    while True:
        points, next_offset = client.scroll(
            collection_name=collection_name,
            limit=100,
            offset=next_offset,
            with_payload=True,
        )
        all_points.extend(points)
        if next_offset is None:
            break
 
    return all_points
 
 
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
    
    vector_results = vector_search(query, top_k=10)
 
    points = get_all_chunks_from_qdrant()
    bm25 = build_bm25_index(points)
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