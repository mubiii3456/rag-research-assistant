import sys
import os
import streamlit as st
 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app", "retrieval"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app", "generation"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app", "ingestion"))
 
from reranker import search_with_rerank
from llm_generator import generate_answer
 
st.set_page_config(page_title="RAG Research Assistant", page_icon="📚", layout="wide")
 
st.title("📚 RAG Research Assistant")
st.caption("Ask questions about the LangChain v1 documentation")
 
if "messages" not in st.session_state:
    st.session_state.messages = []
 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("View source chunks"):
                for src in message["sources"]:
                    st.markdown(f"**Page {src['page_number']}**")
                    st.text(src["text"][:300])
                    st.divider()
 
query = st.chat_input("Ask a question about the document...")
 
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
 
    with st.chat_message("assistant"):
        with st.spinner("Searching and generating answer..."):
            chunks = search_with_rerank(query, retrieve_k=10, final_k=5)
            answer = generate_answer(query, chunks)
 
        st.markdown(answer)
 
        sources = [c["payload"] for c in chunks]
        with st.expander("View source chunks"):
            for src in sources:
                st.markdown(f"**Page {src['page_number']}**")
                st.text(src["text"][:300])
                st.divider()
 
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
    })
 