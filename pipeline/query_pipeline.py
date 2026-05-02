from core.embedder import embed_text
from core.vectorstore import query_chunks
from config.settings import TOP_K


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    """
    Embed query → retrieve top_k chunks from ChromaDB.
    Returns list of {text, metadata, score} dicts.
    """
    query_embedding = embed_text(query)
    chunks = query_chunks(query_embedding, top_k=top_k)
    return chunks