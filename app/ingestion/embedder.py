from sentence_transformers import SentenceTransformer
 
MODEL_NAME = "all-MiniLM-L6-v2"
 
_model = None
 
 
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model
 
 
def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_model()
    embeddings = model.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()
 
 
def embed_single_text(text: str) -> list[float]:
    return embed_texts([text])[0]
 
 
if __name__ == "__main__":
    sample_texts = [
        "LangChain is a framework for building LLM applications.",
        "Qdrant is a vector database used for similarity search.",
    ]
 
    vectors = embed_texts(sample_texts)
 
    print(f"Generated {len(vectors)} embeddings.")
    print(f"Each embedding has {len(vectors[0])} dimensions.")
    print("\nFirst 5 numbers of embedding 1:")
    print(vectors[0][:5])
 