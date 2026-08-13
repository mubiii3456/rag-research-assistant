import sys
import os
import uuid
from qdrant_client.models import PointStruct
 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "retrieval"))
 
from pdf_loader import load_pdf
from chunker import build_chunks_with_metadata
from embedder import embed_texts
from qdrant_client_setup import get_client, UPLOADS_COLLECTION
 
BATCH_SIZE = 20
 
 
def process_uploaded_pdf(file_path: str, session_id: str) -> int:
    pages = load_pdf(file_path)
    chunks = build_chunks_with_metadata(
        pages,
        filename=os.path.basename(file_path),
        source_type="user",
        session_id=session_id,
    )
    chunk_texts = [c["text"] for c in chunks]
 
    if not chunk_texts:
        return 0
 
    chunk_embeddings = embed_texts(chunk_texts)
 
    points = []
    for chunk, vector in zip(chunks, chunk_embeddings):
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "text": chunk["text"],
                "filename": chunk["filename"],
                "page_number": chunk["page_number"],
                "source_type": chunk["source_type"],
                "session_id": chunk["session_id"],
            },
        ))
 
    client = get_client()
    total = len(points)
 
    for i in range(0, total, BATCH_SIZE):
        batch = points[i:i + BATCH_SIZE]
        attempts = 0
        while attempts < 3:
            try:
                client.upsert(collection_name=UPLOADS_COLLECTION, points=batch)
                break
            except Exception:
                attempts += 1
                if attempts == 3:
                    raise
 
    return total
 
 
def get_session_chunks(session_id: str):
    client = get_client()
    from qdrant_client.models import Filter, FieldCondition, MatchValue
 
    results = client.scroll(
        collection_name=UPLOADS_COLLECTION,
        scroll_filter=Filter(
            must=[FieldCondition(key="session_id", match=MatchValue(value=session_id))]
        ),
        limit=1000,
        with_payload=True,
        with_vectors=True,
    )
    return results[0]
 