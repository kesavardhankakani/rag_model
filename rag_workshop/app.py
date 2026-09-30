from __future__ import annotations

from html import escape
from pathlib import Path

import streamlit as st

from rag_workshop.core.ollama_client import detect_ollama_models
from rag_workshop.core.rag_pipeline import RAGPipeline
from rag_workshop.ui.components import render_retrieval_details
from rag_workshop.ui.styles import load_css


ROOT_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = ROOT_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def get_pipeline() -> RAGPipeline:
    if "pipeline" not in st.session_state:
        st.session_state.pipeline = RAGPipeline()
    return st.session_state.pipeline


st.set_page_config(page_title="tutor.ai", page_icon="✦", layout="wide")
load_css()

st.markdown(
    """
    <header class="workspace-header">
        <div class="brand-lockup">
            <span class="brand-mark">t.</span>
            <span class="brand-name">tutor<span>.ai</span></span>
        </div>
        <div class="workspace-mode"><span class="mode-dot"></span> PRIVATE LOCAL WORKSPACE</div>
    </header>
    <section class="welcome-row">
        <div>
            <div class="eyebrow">DOCUMENT LEARNING</div>
            <h1>Your study workspace</h1>
            <p>Bring your notes in. Get clear answers grounded in your own material.</p>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

pipeline = get_pipeline()
ollama_models = detect_ollama_models()
model_name = pipeline.refresh_model_selection() or "No supported model detected"

model_status = "OLLAMA CONNECTED" if ollama_models else "OLLAMA OFFLINE"
st.markdown(
    f"<div class='model-line'><span class='model-indicator {'online' if ollama_models else 'offline'}'></span>"
    f"<span>{model_status}</span><span class='model-divider'></span>"
    f"<span class='model-label'>ACTIVE MODEL</span><strong>{escape(str(model_name))}</strong></div>",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Settings")
    if st.session_state.get("answer_detail_settings_version", 0) < 1:
        prior_defaults = {"top_k": (3, 5), "chunk_size": (500, 800), "chunk_overlap": (80, 100)}
        for setting, (old_default, new_default) in prior_defaults.items():
            if st.session_state.get(setting) == old_default:
                st.session_state[setting] = new_default
        st.session_state.answer_detail_settings_version = 1

    if "top_k" not in st.session_state:
        st.session_state.top_k = 5
    if "min_similarity" not in st.session_state:
        st.session_state.min_similarity = 0.12
    if "chunk_size" not in st.session_state:
        st.session_state.chunk_size = 800
    if "chunk_overlap" not in st.session_state:
        st.session_state.chunk_overlap = 100
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.2

    st.session_state.top_k = st.slider("Top-K retrieval", 1, 10, st.session_state.top_k)
    st.session_state.min_similarity = st.slider("Similarity threshold", 0.0, 0.9, st.session_state.min_similarity, 0.01)
    st.session_state.chunk_size = st.slider("Chunk size", 150, 1200, st.session_state.chunk_size, 50)
    st.session_state.chunk_overlap = st.slider("Chunk overlap", 0, 250, st.session_state.chunk_overlap, 10)
    st.session_state.temperature = st.slider("Temperature", 0.0, 1.0, st.session_state.temperature, 0.05)

    st.markdown("**Selected Ollama model**")
    st.text_input("Current model", value=str(model_name), disabled=True)

    if not ollama_models:
        st.warning("Ollama was not detected. Install Ollama locally and run a Qwen or Llama model to enable generation.")
    else:
        st.info("Available local models: " + ", ".join(ollama_models))

st.markdown("<div class='section-kicker upload-kicker'>YOUR DOCUMENTS</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload a PDF or DOCX", type=["pdf", "docx"])

if uploaded_file is not None:
    file_path = UPLOAD_DIR / uploaded_file.name
    file_path.write_bytes(uploaded_file.getvalue())

    try:
        with st.spinner("Extracting text, chunking content, and generating embeddings..."):
            result = pipeline.index_document(str(file_path), chunk_size=st.session_state.chunk_size, overlap=st.session_state.chunk_overlap)
        st.success(f"Indexed {result['filename']} successfully.")
        st.info(f"Characters: {result['char_count']}; pages: {result['page_count']}; chunks: {result['chunk_count']}")
    except Exception as exc:
        st.error(f"Could not process the document: {exc}")


if "last_retrieval" not in st.session_state:
    st.session_state.last_retrieval = []
if "last_retrieval_scope" not in st.session_state:
    st.session_state.last_retrieval_scope = "top_k"

last_retrieval = st.session_state.last_retrieval
retrieval_scores = [item["score"] for item in last_retrieval if item.get("score") is not None]
best_score = max(retrieval_scores, default=0.0)
embedding_label = "MiniLM" if pipeline.embedding_manager.model is not None else "TF-IDF"
retrieval_value = (
    f"{len(last_retrieval)} passages"
    if st.session_state.last_retrieval_scope == "document"
    else f"{len(last_retrieval)} / {st.session_state.top_k}"
)
retrieval_detail = (
    "Whole PDF analyzed"
    if st.session_state.last_retrieval_scope == "document"
    else f"Best match {best_score:.0%}" if last_retrieval else "Waiting for a question"
)

st.markdown("<div class='section-kicker'>WORKSPACE OVERVIEW</div>", unsafe_allow_html=True)
status_cols = st.columns(4, gap="small")
stats = [
    ("DOCUMENTS", str(len(pipeline.documents)), "Currently indexed"),
    ("CHUNKS", str(len(pipeline.chunks)), "Searchable passages"),
    ("EMBEDDINGS", embedding_label if pipeline.chunk_vectors.size else "Idle", "Local vector index"),
    ("RETRIEVAL", retrieval_value, retrieval_detail),
]
for column, (label, value, detail) in zip(status_cols, stats):
    with column:
        stat_markup = (
            f"<div class='stat-card'><div class='stat-label'>{label}</div>"
            f"<div class='stat-value'>{value}</div><div class='stat-detail'>{detail}</div></div>"
        )
        if label == "RETRIEVAL":
            retrieval_stat_placeholder = st.empty()
            retrieval_stat_placeholder.markdown(stat_markup, unsafe_allow_html=True)
        else:
            st.markdown(stat_markup, unsafe_allow_html=True)

st.markdown("<div class='section-kicker conversation-kicker'>ASK YOUR DOCUMENTS</div>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Ask a question about the uploaded document")
if question:
    if not pipeline.chunks:
        st.warning("Please upload and index a document before asking a question.")
    else:
        with st.spinner("Retrieving the most relevant chunks and generating a grounded answer..."):
            response = pipeline.answer_question(
                question,
                top_k=st.session_state.top_k,
                min_similarity=st.session_state.min_similarity,
                temperature=st.session_state.temperature,
            )
            st.session_state.last_retrieval = response.get("retrieval", [])
            st.session_state.last_retrieval_scope = "document" if response.get("document_overview") else "top_k"
            last_retrieval = st.session_state.last_retrieval
            retrieval_scores = [item["score"] for item in last_retrieval if item.get("score") is not None]
            best_score = max(retrieval_scores, default=0.0)
            retrieval_value = (
                f"{len(last_retrieval)} passages"
                if st.session_state.last_retrieval_scope == "document"
                else f"{len(last_retrieval)} / {st.session_state.top_k}"
            )
            retrieval_detail = (
                "Whole PDF analyzed"
                if st.session_state.last_retrieval_scope == "document"
                else f"Best match {best_score:.0%}" if last_retrieval else "No matching passages"
            )
            retrieval_stat_placeholder.markdown(
                f"<div class='stat-card'><div class='stat-label'>RETRIEVAL</div>"
                f"<div class='stat-value'>{retrieval_value}</div>"
                f"<div class='stat-detail'>{retrieval_detail}</div></div>",
                unsafe_allow_html=True,
            )

        st.session_state.chat_history.append({"role": "user", "content": question})
        st.session_state.chat_history.append({"role": "assistant", "content": response["answer"]})

        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            st.write(response["answer"])

        if response.get("document_overview"):
            source_pages = sorted({
                (item["source_file"], item["page_number"])
                for item in response.get("retrieval", [])
            })
            with st.expander(f"Whole document analyzed · {len(response.get('retrieval', []))} passages"):
                for source_file, page_number in source_pages:
                    st.write(f"{source_file} · page {page_number}")
        elif response.get("retrieval"):
            with st.expander("View retrieved context and similarity scores"):
                render_retrieval_details(response["retrieval"])
        else:
            st.info("The system did not find enough relevant document context for this question.")

        if response.get("model"):
            st.caption(f"Model used: {response['model']}")
        else:
            st.caption("Model used: no supported Ollama model detected")

if st.button("Clear chat"):
    st.session_state.chat_history = []
    st.rerun()
