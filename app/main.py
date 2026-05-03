import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from pipeline.synthesizer import answer
from core.vectorstore import get_stats
from config.settings import DEFAULT_TOPICS
from pipeline.ingest_pipeline import run_ingestion

st.set_page_config(page_title="arxiv-oracle", page_icon="📡", layout="wide")
st.title("📡 arxiv-oracle")
st.caption("Query 100+ research papers in plain English. Cited answers in seconds.")

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.header("Knowledge base")
    stats = get_stats()
    col1, col2 = st.columns(2)
    col1.metric("Papers", stats["total_papers"])
    col2.metric("Chunks", stats["total_chunks"])

    st.divider()

    with st.expander("Ingest more papers"):
        custom_topic = st.text_input("arxiv topic", placeholder="e.g. RLHF fine-tuning")
        if st.button("Ingest", use_container_width=True):
            topics = [custom_topic] if custom_topic else DEFAULT_TOPICS
            with st.spinner("Fetching and indexing..."):
                run_ingestion(topics=topics, max_per_topic=10)
            st.success("Done! Refresh stats.")

    st.divider()
    st.markdown("**Try these:**")
    examples = [
        "What chunking strategies work best for RAG?",
        "How does hybrid search improve retrieval?",
        "What embedding models are most efficient?",
        "How do rerankers improve answer quality?",
        "What is lost-in-the-middle problem?",
    ]
    for ex in examples:
        if st.button(ex, use_container_width=True, key=ex):
            st.session_state.query = ex

# ── Main query ───────────────────────────────────────────
query = st.text_input(
    "Ask a research question",
    value=st.session_state.get("query", ""),
    placeholder="e.g. What are the best chunking strategies for RAG?",
)

if query:
    with st.spinner("Retrieving and synthesizing..."):
        ans, sources = answer(query)

    st.markdown("### Answer")
    st.markdown(ans)

    if sources:
        with st.expander(f"View {len(sources)} source chunks"):
            for i, s in enumerate(sources):
                m = s["metadata"]
                st.markdown(f"**[{i+1}] {m['title']}** ({m['year']})  `score: {s['score']}`")
                st.caption(m["authors"])
                st.text(s["text"][:400] + ("..." if len(s["text"]) > 400 else ""))
                st.divider()