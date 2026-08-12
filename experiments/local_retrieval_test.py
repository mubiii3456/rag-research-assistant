import sys
import numpy as np
from pdf_loader import load_pdf
from chunker import build_chunks_with_metadata
from embedder import embed_texts, embed_single_text
 
 
def cosine_similarity(vec_a, vec_b):
    a = np.array(vec_a)
    b = np.array(vec_b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
 
 
def search(query, chunks, chunk_embeddings, top_k=3):
    query_vector = embed_single_text(query)
 
    scored_chunks = []
    for chunk, chunk_vector in zip(chunks, chunk_embeddings):
        score = cosine_similarity(query_vector, chunk_vector)
        scored_chunks.append((score, chunk))
 
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return scored_chunks[:top_k]
 
 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python local_retrieval_test.py <path_to_pdf>")
        sys.exit(1)
 
    pdf_path = sys.argv[1]
 
    print("Loading PDF...")
    pages = load_pdf(pdf_path)
 
    print("Chunking text...")
    chunks = build_chunks_with_metadata(pages, filename=pdf_path, source_type="default")
    chunk_texts = [c["text"] for c in chunks]
 
    print(f"Generating embeddings for {len(chunk_texts)} chunks...")
    chunk_embeddings = embed_texts(chunk_texts)
 
    print("\nReady. Type a question about the PDF (or 'exit' to quit).\n")
 
    while True:
        query = input("Your question: ")
        if query.lower() == "exit":
            break
 
        results = search(query, chunks, chunk_embeddings, top_k=3)
 
        print("\nTop matching chunks:\n")
        for score, chunk in results:
            print(f"Score: {score:.4f} | Page: {chunk['page_number']}")
            print(chunk["text"][:300])
            print("-" * 50)
        print()
 