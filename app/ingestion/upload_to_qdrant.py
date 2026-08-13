import sys
import os
import uuid
from qdrant_client.models import PointStruct
 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "retrieval"))
 
from pdf_loader import load_pdf
from chunker import build_chunks_with_metadata
from embedder import embed_texts
from qdrant_client_setup import get_client, DEFAULT_COLLECTION
 
BATCH_SIZE = 20
 
 
def upload_pdf_to_qdrant(pdf_path: str, collection_name: str = DEFAULT_COLLECTION):
    print("Loading PDF...")
    pages = load_pdf(pdf_path)
 
    print("Chunking text...")
    chunks = build_chunks_with_metadata(pages, filename=pdf_path, source_type="default")
    chunk_texts = [c["text"] for c in chunks]
 
    print(f"Generating embeddings for {len(chunk_texts)} chunks...")
    chunk_embeddings = embed_texts(chunk_texts)
 
    print("Preparing points for Qdrant...")
    points = []
    for chunk, vector in zip(chunks, chunk_embeddings):
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "text": chunk["text"],
                "filename": chunk["filename"],
                "page_number": chunk["page_number"],
                "source_type": chunk["source_type"],
                "session_id": chunk["session_id"],
            },
        )
        points.append(point)
 
    client = get_client()
    total = len(points)
    print(f"Uploading {total} points to Qdrant collection '{collection_name}' in batches of {BATCH_SIZE}...")
 
    for i in range(0, total, BATCH_SIZE):
        batch = points[i:i + BATCH_SIZE]
        attempts = 0
        while attempts < 3:
            try:
                client.upsert(collection_name=collection_name, points=batch)
                print(f"Uploaded batch {i // BATCH_SIZE + 1} ({i + len(batch)}/{total})")
                break
            except Exception as e:
                attempts += 1
                print(f"Batch {i // BATCH_SIZE + 1} failed (attempt {attempts}/3): {e}")
                if attempts == 3:
                    raise
 
    print("Upload complete.")
    return total
 
 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload_to_qdrant.py <path_to_pdf>")
        sys.exit(1)
 
    pdf_path = sys.argv[1]
    count = upload_pdf_to_qdrant(pdf_path)
    print(f"\n{count} chunks stored permanently in Qdrant.")