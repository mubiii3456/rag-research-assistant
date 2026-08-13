import sys
import os
import uuid
import tempfile
import streamlit as st
 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app", "retrieval"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app", "generation"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app", "ingestion"))
 
from reranker import search_with_rerank
from llm_generator import generate_answer
from upload_handler import process_uploaded_pdf, get_session_chunks
from embedder import embed_single_text
from qdrant_client_setup import get_client, UPLOADS_COLLECTION
 
st.set_page_config(page_title="RAG Research Assistant", page_icon="📚", layout="wide")
 
MAX_FILE_SIZE_MB = 20
MAX_QUESTIONS_PER_SESSION = 30
 
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
 
if "messages" not in st.session_state:
    st.session_state.messages = []
 
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None
 
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
 
st.title("📚 RAG Research Assistant")
st.caption("Ask questions about AWS documentation, or upload your own PDF")
 
 
def clear_session_uploads(session_id):
    from qdrant_client.models import Filter, FieldCondition, MatchValue
 
    client = get_client()
    client.delete(
        collection_name=UPLOADS_COLLECTION,
        points_selector=Filter(
            must=[FieldCondition(key="session_id", match=MatchValue(value=session_id))]
        ),
    )
 
 
with st.sidebar:
    st.subheader("Document Source")
 
    scope = st.radio(
        "Search in:",
        ["Default Library", "My Upload", "Both"],
        index=0,
    )
 
    st.divider()
    st.subheader("Upload your own PDF")
 
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])
 
    if uploaded_file is not None and uploaded_file.name != st.session_state.uploaded_filename:
        file_size_mb = uploaded_file.size / (1024 * 1024)
 
        if file_size_mb > MAX_FILE_SIZE_MB:
            st.error(f"File too large ({file_size_mb:.1f} MB). Max allowed is {MAX_FILE_SIZE_MB} MB.")
        else:
            with st.spinner("Processing your document..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name
 
                try:
                    count = process_uploaded_pdf(tmp_path, st.session_state.session_id)
                except Exception as e:
                    count = 0
                    st.error(f"Could not process this PDF. It may be corrupted or unreadable. ({e})")
                finally:
                    os.unlink(tmp_path)
 
                if count > 0:
                    st.session_state.uploaded_filename = uploaded_file.name
                    st.success(f"Uploaded and indexed {count} chunks from {uploaded_file.name}")
                elif count == 0 and st.session_state.uploaded_filename != uploaded_file.name:
                    st.warning("No readable text found in this PDF. It may be empty, image-only, or scanned.")
 
    if st.session_state.uploaded_filename:
        st.info(f"Current upload: {st.session_state.uploaded_filename}")
        if st.button("Clear My Upload"):
            clear_session_uploads(st.session_state.session_id)
            st.session_state.uploaded_filename = None
            st.rerun()
 
    st.divider()
    st.caption(f"Questions asked this session: {st.session_state.question_count}/{MAX_QUESTIONS_PER_SESSION}")
 
 
def search_uploads_only(query, session_id, top_k=5):
    points = get_session_chunks(session_id)
    if not points:
        return []
 
    query_vector = embed_single_text(query)
 
    import numpy as np
    scored = []
    for p in points:
        vec = np.array(p.vector)
        q = np.array(query_vector)
        score = np.dot(vec, q) / (np.linalg.norm(vec) * np.linalg.norm(q))
        scored.append({"score": float(score), "payload": p.payload})
 
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
 
 
def run_search(query, scope, session_id):
    if scope == "Default Library":
        chunks = search_with_rerank(query, retrieve_k=10, final_k=5)
        return [{"payload": c["payload"]} for c in chunks]
 
    elif scope == "My Upload":
        results = search_uploads_only(query, session_id, top_k=5)
        return [{"payload": r["payload"]} for r in results]
 
    else:
        default_chunks = search_with_rerank(query, retrieve_k=6, final_k=3)
        upload_chunks = search_uploads_only(query, session_id, top_k=3)
        combined = [{"payload": c["payload"]} for c in default_chunks] + \
                   [{"payload": r["payload"]} for r in upload_chunks]
        return combined
 
 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("View source chunks"):
                for src in message["sources"]:
                    st.markdown(f"**{src['filename']} — Page {src['page_number']}**")
                    st.text(src["text"][:300])
                    st.divider()
 
query = st.chat_input("Ask a question...")
 
if query:
    query = query.strip()
 
    if not query:
        st.warning("Please type a question.")
    elif st.session_state.question_count >= MAX_QUESTIONS_PER_SESSION:
        st.warning("You've reached the question limit for this session. Please refresh to start a new session.")
    elif scope in ["My Upload", "Both"] and not st.session_state.uploaded_filename:
        st.warning("Please upload a PDF first, or switch to 'Default Library'.")
    else:
        st.session_state.question_count += 1
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
 
        with st.chat_message("assistant"):
            with st.spinner("Searching and generating answer..."):
                try:
                    chunks = run_search(query, scope, st.session_state.session_id)
 
                    if not chunks:
                        answer = "I couldn't find relevant information for that question in the selected document(s)."
                    else:
                        answer = generate_answer(query, chunks)
                except Exception as e:
                    chunks = []
                    answer = f"Something went wrong while generating the answer. Please try again. ({e})"
 
            st.markdown(answer)
 
            sources = [c["payload"] for c in chunks]
            if sources:
                with st.expander("View source chunks"):
                    for src in sources:
                        st.markdown(f"**{src['filename']} — Page {src['page_number']}**")
                        st.text(src["text"][:300])
                        st.divider()
 
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
        })