from core.fetcher import fetch_papers
from core.extractor import extract_text
from core.chunker import chunk_text
from core.embedder import get_embed_model, embed_batch
from core.vectorstore import is_paper_indexed, add_chunks
from config.settings import DEFAULT_TOPICS, DEFAULT_FETCH_COUNT


def ingest_paper(paper: dict) -> int:
    """
    Full pipeline for one paper:
    fetch → extract → chunk → embed → store.
    Returns number of chunks added (0 if already indexed).
    """
    paper_id = paper["paper_id"]

    if is_paper_indexed(paper_id):
        print(f"  Skipping (already indexed): {paper['title'][:55]}")
        return 0

    # 1. Extract text
    text = extract_text(paper["pdf_path"])
    if not text:
        print(f"  Skipping (no text): {paper['title'][:55]}")
        return 0

    # 2. Semantic chunk
    embed_model = get_embed_model()
    chunks = chunk_text(text, paper, embed_model)
    if not chunks:
        print(f"  Skipping (no chunks): {paper['title'][:55]}")
        return 0

    # 3. Batch embed
    texts = [c["text"] for c in chunks]
    embeddings = embed_batch(texts)

    # 4. Store
    added = add_chunks(chunks, embeddings)
    print(f"  Indexed {added} chunks — {paper['title'][:55]}")
    return added


def run_ingestion(topics: list[str] = None, max_per_topic: int = DEFAULT_FETCH_COUNT):
    """
    Fetch and ingest papers for a list of topics.
    Safe to re-run — skips already-indexed papers.
    """
    topics = topics or DEFAULT_TOPICS
    total_papers = 0
    total_chunks = 0

    for topic in topics:
        print(f"\nTopic: {topic}")
        papers = fetch_papers(topic, max_results=max_per_topic)
        print(f"  Found {len(papers)} papers")

        for paper in papers:
            added = ingest_paper(paper)
            if added > 0:
                total_papers += 1
                total_chunks += added

    print(f"\nDone. {total_papers} new papers, {total_chunks} total chunks added.")


if __name__ == "__main__":
    run_ingestion()