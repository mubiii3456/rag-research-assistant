"""
langchain_version.py
---------------------
This shows the SAME RAG pipeline (PDF -> chunks -> embeddings -> retrieval
-> LLM answer) built using LangChain instead of custom code.
 
Purpose: comparison only. This is NOT used by the main app.
The main app (app/) uses a fully custom implementation instead, built to
demonstrate a hands-on understanding of every RAG component:
chunking strategy, embedding generation, hybrid search, re-ranking, and
prompt construction.
 
Trade-off:
- Custom implementation: more code, but full control and understanding
  of every step (see /app for the real implementation used by this project).
- LangChain: far less code, faster to build, leverages a mature ecosystem,
  but abstracts away the internals shown here.
"""
 
import os
from dotenv import load_dotenv
 
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA
 
load_dotenv()
 
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
 
 
def build_qa_chain(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
 
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(documents)
 
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
 
    vectorstore = Qdrant.from_documents(
        chunks,
        embeddings,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name="langchain_demo",
    )
 
    llm = ChatOllama(model="minimax-m3:cloud")
 
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    )
 
    return qa_chain
 
 
if __name__ == "__main__":
    import sys
 
    if len(sys.argv) < 2:
        print("Usage: python langchain_version.py <path_to_pdf>")
        sys.exit(1)
 
    pdf_path = sys.argv[1]
    qa_chain = build_qa_chain(pdf_path)
 
    print("LangChain RAG ready. Type a question (or 'exit' to quit).\n")
 
    while True:
        query = input("Your question: ")
        if query.lower() == "exit":
            break
 
        result = qa_chain.invoke({"query": query})
        print("\nAnswer:\n")
        print(result["result"])
        print()