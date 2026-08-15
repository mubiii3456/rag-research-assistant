import sys
import os
import uuid
import tempfile
import streamlit as st
 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app", "retrieval"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app", "generation"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app", "ingestion"))
 
from reranker import search_with_rerank
from llm_generator import generate_answer, generate_answer_stream
from upload_handler import process_uploaded_pdf, get_session_chunks
from embedder import embed_single_text
from qdrant_client_setup import get_client, DEFAULT_COLLECTION, UPLOADS_COLLECTION
from chat_db import init_db, save_message, load_messages, get_all_sessions
 
st.set_page_config(page_title="AWS RAG Assistant", page_icon="◆", layout="wide")
init_db()
 
MAX_FILE_SIZE_MB = 20
MAX_QUESTIONS_PER_SESSION = 30
 
# ---------------------------------------------------------------------------
# Visual design: deep indigo-navy console, cyan = retrieval, amber = answers
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
 
:root {
    --bg: #0F1729;
    --surface: #1A2438;
    --surface-hover: #202D47;
    --border: #2A3752;
    --cyan: #38BDF8;
    --amber: #FBBF24;
    --text: #E8EDF5;
    --muted: #8B96AB;
}
 
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
 
.stApp {
    background:
        radial-gradient(ellipse 900px 500px at 15% -10%, rgba(56,189,248,0.10), transparent),
        radial-gradient(ellipse 700px 400px at 100% 10%, rgba(251,191,36,0.06), transparent),
        var(--bg);
}
 
/* Header */
h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, var(--cyan), #7DD3FC 45%, var(--amber));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
h1 + div p { color: var(--muted) !important; font-size: 0.95rem !important; }
 
/* Signature: animated scan-line under the title */
.scan-line {
    height: 2px;
    width: 100%;
    margin: 0.4rem 0 1.6rem 0;
    background: linear-gradient(90deg, transparent, var(--cyan), var(--amber), transparent);
    background-size: 200% 100%;
    animation: scan 3.5s ease-in-out infinite;
    border-radius: 2px;
    opacity: 0.7;
}
@keyframes scan {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}
 
/* Sidebar = control panel */
section[data-testid="stSidebar"] {
    background: #0C1220;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted) !important;
}
 
/* Buttons: quiet by default, glow on hover */
.stButton > button {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.15s ease;
    text-align: left;
}
.stButton > button:hover {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 1px var(--cyan), 0 0 16px rgba(56,189,248,0.25);
    transform: translateY(-1px);
}
 
/* Radio (Document Source) as pill-like segmented control */
div[role="radiogroup"] label {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 6px 10px;
    margin-bottom: 4px;
    transition: all 0.15s ease;
}
div[role="radiogroup"] label:hover { border-color: var(--cyan); }
 
/* Chat bubbles: console cards with animated entrance */
div[data-testid="stChatMessage"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 4px 6px !important;
    animation: rise 0.35s ease-out;
}
@keyframes rise {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}
 
/* User message: amber accent edge | assistant: cyan accent edge */
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
    border-left: 3px solid var(--amber) !important;
}
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
    border-left: 3px solid var(--cyan) !important;
}
 
/* Source cards -> terminal styling */
.stExpander {
    background: #0C1220 !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
.stExpander summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    color: var(--cyan) !important;
}
.stExpander p, .stExpander pre {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    color: var(--muted) !important;
}
 
/* Chat input */
[data-testid="stChatInput"] {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    background: var(--surface) !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 1px var(--cyan), 0 0 20px rgba(56,189,248,0.2) !important;
}
 
/* File uploader */
[data-testid="stFileUploaderDropzone"] {
    background: var(--surface) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 10px !important;
}
 
/* Progress caption pill (questions used) */
.usage-pill {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 4px 12px;
}
 
/* Success / warning / error boxes, quieter */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)
 
query_params = st.query_params
 
if "user_id" not in st.session_state:
    if "uid" in query_params:
        st.session_state.user_id = query_params["uid"]
    else:
        new_uid = str(uuid.uuid4())
        st.session_state.user_id = new_uid
        st.query_params["uid"] = new_uid
 
if "session_id" not in st.session_state:
    if "sid" in query_params:
        st.session_state.session_id = query_params["sid"]
    else:
        new_id = str(uuid.uuid4())
        st.session_state.session_id = new_id
        st.query_params["sid"] = new_id
 
if "messages" not in st.session_state:
    st.session_state.messages = load_messages(st.session_state.session_id)
 
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None
 
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
 
st.title("◆ AWS Research Assistant")
st.caption("Ask questions about AWS documentation, or bring your own PDF to the conversation.")
st.markdown('<div class="scan-line"></div>', unsafe_allow_html=True)
 
 
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
    st.subheader("Document source")
 
    scope = st.radio(
        "Search in",
        ["Default Library", "My Upload", "Both"],
        index=0,
        label_visibility="collapsed",
    )
 
    st.divider()
    st.subheader("Add your own PDF")
 
    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"],
        label_visibility="collapsed",
        help=f"Up to {MAX_FILE_SIZE_MB}MB per file · PDF only",
    )
 
    if uploaded_file is not None and uploaded_file.name != st.session_state.uploaded_filename:
        file_size_mb = uploaded_file.size / (1024 * 1024)
 
        if file_size_mb > MAX_FILE_SIZE_MB:
            st.error(f"That file is {file_size_mb:.1f}MB. Please upload something under {MAX_FILE_SIZE_MB}MB.")
        else:
            with st.spinner("Reading and indexing your document..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name
 
                try:
                    count = process_uploaded_pdf(tmp_path, st.session_state.session_id)
                except Exception as e:
                    count = 0
                    st.error(f"Couldn't read this PDF — it may be corrupted. ({e})")
                finally:
                    os.unlink(tmp_path)
 
                if count > 0:
                    st.session_state.uploaded_filename = uploaded_file.name
                    st.success(f"Indexed {count} sections from {uploaded_file.name}")
                elif count == 0 and st.session_state.uploaded_filename != uploaded_file.name:
                    st.warning("No readable text found. This PDF may be scanned or image-only.")
 
    if st.session_state.uploaded_filename:
        st.info(f"Active upload: {st.session_state.uploaded_filename}")
        if st.button("Remove upload"):
            clear_session_uploads(st.session_state.session_id)
            st.session_state.uploaded_filename = None
            st.rerun()
 
    st.divider()
    st.markdown(
        f'<span class="usage-pill">{st.session_state.question_count} / {MAX_QUESTIONS_PER_SESSION} questions used</span>',
        unsafe_allow_html=True,
    )
 
    st.divider()
    st.subheader("Conversations")
 
    if st.button("＋ New chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.session_id = new_id
        st.session_state.messages = []
        st.query_params["sid"] = new_id
        st.rerun()
 
    all_sessions = get_all_sessions(st.session_state.user_id)
 
    for s in all_sessions:
        label = s["title"] if s["title"] else "New chat"
        is_current = s["session_id"] == st.session_state.session_id
        button_label = f"● {label}" if is_current else label
 
        if st.button(button_label, key=f"session_{s['session_id']}", use_container_width=True):
            st.session_state.session_id = s["session_id"]
            st.session_state.messages = load_messages(s["session_id"])
            st.query_params["sid"] = s["session_id"]
            st.rerun()
 
 
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
 
 
def build_search_query(query, messages):
    recent_user_messages = [m["content"] for m in messages[-4:] if m["role"] == "user"]
    if recent_user_messages:
        context_str = " ".join(recent_user_messages[-2:])
        return f"{context_str} {query}"
    return query
 
 
def run_search(query, scope, session_id, messages):
    search_query = build_search_query(query, messages)
 
    if scope == "Default Library":
        chunks = search_with_rerank(search_query, retrieve_k=10, final_k=5)
        return [{"payload": c["payload"]} for c in chunks]
 
    elif scope == "My Upload":
        results = search_uploads_only(search_query, session_id, top_k=5)
        return [{"payload": r["payload"]} for r in results]
 
    else:
        default_chunks = search_with_rerank(search_query, retrieve_k=6, final_k=3)
        upload_chunks = search_uploads_only(search_query, session_id, top_k=3)
        combined = [{"payload": c["payload"]} for c in default_chunks] + \
                   [{"payload": r["payload"]} for r in upload_chunks]
        return combined
 
 
if not st.session_state.messages:
    st.markdown(
        """
        <div style="text-align:center; padding: 3rem 1rem; color: var(--muted);">
            <div style="font-size:2rem; margin-bottom:0.5rem;">◆</div>
            <div style="font-family:'Space Grotesk', sans-serif; font-size:1.1rem; color:#E8EDF5;">
                Start a conversation
            </div>
            <div style="font-size:0.9rem; margin-top:0.3rem;">
                Ask about AWS services, or upload your own PDF from the sidebar.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("Sources"):
                for src in message["sources"]:
                    st.markdown(f"**{src['filename']} — page {src['page_number']}**")
                    st.text(src["text"][:300])
                    st.divider()
 
query = st.chat_input("Ask a question...")
 
if query:
    query = query.strip()
 
    if not query:
        st.warning("Type a question to continue.")
    elif st.session_state.question_count >= MAX_QUESTIONS_PER_SESSION:
        st.warning("You've reached the question limit for this session. Refresh to start a new one.")
    elif scope in ["My Upload", "Both"] and not st.session_state.uploaded_filename:
        st.warning("Upload a PDF first, or switch to 'Default Library'.")
    else:
        st.session_state.question_count += 1
        st.session_state.messages.append({"role": "user", "content": query})
        save_message(st.session_state.session_id, st.session_state.user_id, "user", query)
        with st.chat_message("user"):
            st.markdown(query)
 
        with st.chat_message("assistant"):
            with st.spinner("Retrieving relevant sections..."):
                chunks = run_search(query, scope, st.session_state.session_id, st.session_state.messages)
 
            try:
                if not chunks:
                    answer = "I couldn't find relevant information for that question in the selected document(s)."
                    st.markdown(answer)
                else:
                    history = [
                        {"question": m["content"], "answer": st.session_state.messages[i + 1]["content"]}
                        for i, m in enumerate(st.session_state.messages[:-1])
                        if m["role"] == "user" and i + 1 < len(st.session_state.messages)
                        and st.session_state.messages[i + 1]["role"] == "assistant"
                    ]
 
                    placeholder = st.empty()
                    full_answer = ""
                    for token in generate_answer_stream(query, chunks, conversation_history=history):
                        full_answer += token
                        placeholder.markdown(full_answer)
                    answer = full_answer
 
            except Exception as e:
                chunks = []
                answer = f"Something went wrong while generating the answer. Please try again. ({e})"
                st.markdown(answer)
 
            sources = [c["payload"] for c in chunks]
            if sources:
                with st.expander("Sources"):
                    for src in sources:
                        st.markdown(f"**{src['filename']} — page {src['page_number']}**")
                        st.text(src["text"][:300])
                        st.divider()
 
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
        })
        save_message(st.session_state.session_id, st.session_state.user_id, "assistant", answer)
 