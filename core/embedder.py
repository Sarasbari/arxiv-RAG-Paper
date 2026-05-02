from llama_index.embeddings.ollama import OllamaEmbedding
from config.settings import EMBED_MODEL

# singleton — created once, reused everywhere
_embed_model = None


def get_embed_model() -> OllamaEmbedding:
    """Return (or create) the shared embedding model instance."""
    global _embed_model
    if _embed_model is None:
        _embed_model = OllamaEmbedding(model_name=EMBED_MODEL)
    return _embed_model


def embed_text(text: str) -> list[float]:
    """Embed a single string. Returns vector."""
    return get_embed_model().get_text_embedding(text)


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed a list of strings. Returns list of vectors."""
    return get_embed_model().get_text_embedding_batch(texts)