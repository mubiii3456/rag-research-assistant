# LangChain Comparison
 
This folder shows the same RAG pipeline built with LangChain, for comparison against the custom implementation used in `/app`.
 
## Why the main project uses a custom implementation
 
The custom pipeline (`/app`) was built manually — PDF loading, chunking, embeddings, hybrid search (vector + BM25), and cross-encoder re-ranking — to develop a hands-on understanding of every step in a RAG system, rather than relying on a framework's abstractions.
 
## Why this comparison exists
 
LangChain is the industry-standard framework for building RAG pipelines quickly. This file (`langchain_version.py`) implements the same PDF -> chunk -> embed -> retrieve -> answer flow in a fraction of the code, using `RecursiveCharacterTextSplitter`, `HuggingFaceEmbeddings`, `Qdrant`, and `RetrievalQA`.
 
## Trade-off summary
 
| | Custom implementation (`/app`) | LangChain (`langchain_version.py`) |
|---|---|---|
| Lines of code | ~500+ across modules | ~40 |
| Development speed | Slower | Much faster |
| Understanding of internals | Full control and visibility into every step | Abstracted away |
| Customization | Full (hybrid search, re-ranking, dual collections) | Limited to what LangChain exposes |
| Best suited for | portfolio depth, fine-grained control | Rapid prototyping, production speed |
 
This file is not used by the main application — it exists purely as a reference implementation for comparison.