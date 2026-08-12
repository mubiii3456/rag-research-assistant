def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list[str]:
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
 
    chunks = []
    start = 0
    text_length = len(text)
 
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()
 
        if chunk:
            chunks.append(chunk)
 
        start += (chunk_size - overlap)
 
    return chunks
 
 
def build_chunks_with_metadata(
    pages_data: list[dict],
    filename: str,
    source_type: str = "default",
    session_id: str | None = None,
    chunk_size: int = 800,
    overlap: int = 150,
) -> list[dict]:
    all_chunks = []
 
    for page in pages_data:
        page_chunks = chunk_text(page["text"], chunk_size=chunk_size, overlap=overlap)
 
        for chunk in page_chunks:
            all_chunks.append({
                "text": chunk,
                "filename": filename,
                "page_number": page["page_number"],
                "source_type": source_type,
                "session_id": session_id,
            })
 
    return all_chunks
 
 
if __name__ == "__main__":
    from pdf_loader import load_pdf
    import sys
 
    if len(sys.argv) < 2:
        print("Usage: python chunker.py <path_to_pdf>")
        sys.exit(1)
 
    pdf_path = sys.argv[1]
    pages = load_pdf(pdf_path)
    chunks = build_chunks_with_metadata(pages, filename=pdf_path, source_type="default")
 
    print(f"Created {len(chunks)} chunks from {len(pages)} pages.\n")
    if chunks:
        print("--- Preview of Chunk 1 ---")
        print(chunks[0])
 