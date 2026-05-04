from sentence_transformers import SentenceTransformer
from config.settings import EMBED_MODEL

# singleton — created once, reused everywhere
_embed_model = None


def get_embed_model() -> SentenceTransformer:
    """Return (or create) the shared embedding model instance."""
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(EMBED_MODEL)
    return _embed_model


def embed_text(text: str) -> list[float]:
    """Embed a single string. Returns vector."""
    model = get_embed_model()
    return model.encode(text).tolist()


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed a list of strings. Returns list of vectors."""
    model = get_embed_model()
    # Performance fix: explicit batch_size prevents memory spikes on large documents
    return model.encode(texts, batch_size=32, show_progress_bar=False).tolist()