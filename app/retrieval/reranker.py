import sys
import os
from sentence_transformers import CrossEncoder
 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "ingestion"))
 
from hybrid_search import hybrid_search
 
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
 
_reranker_model = None
 
 
def get_reranker():
    global _reranker_model
    if _reranker_model is None:
        _reranker_model = CrossEncoder(RERANKER_MODEL_NAME)
    return _reranker_model
 
 
def rerank(query: str, candidates: list, top_k: int = 5):
    model = get_reranker()
 
    pairs = [[query, c["payload"]["text"]] for c in candidates]
    new_scores = model.predict(pairs)
 
    for candidate, score in zip(candidates, new_scores):
        candidate["rerank_score"] = float(score)
 
    reranked = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)
    return reranked[:top_k]
 
 
def search_with_rerank(query: str, retrieve_k: int = 10, final_k: int = 5):
    candidates = hybrid_search(query, top_k=retrieve_k)
    final_results = rerank(query, candidates, top_k=final_k)
    return final_results
 
 
if __name__ == "__main__":
    print("Search with re-ranking ready. Type a question (or 'exit' to quit).\n")
 
    while True:
        query = input("Your question: ")
        if query.lower() == "exit":
            break
 
        results = search_with_rerank(query)
 
        print("\nTop matching chunks (after re-ranking):\n")
        for r in results:
            print(f"Rerank Score: {r['rerank_score']:.4f} | Page: {r['payload']['page_number']}")
            print(r["payload"]["text"][:300])
            print("-" * 50)
        print()