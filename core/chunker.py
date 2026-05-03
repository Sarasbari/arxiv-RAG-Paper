from llama_index.core import Document
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.base.embeddings.base import BaseEmbedding
from config.settings import CHUNK_BREAKPOINT_PERCENTILE, CHUNK_BUFFER_SIZE


class SentenceTransformerBridge(BaseEmbedding):
    """Adapts sentence-transformers to LlamaIndex's BaseEmbedding interface."""

    def __init__(self, st_model):
        super().__init__(model_name=st_model.get_sentence_embedding_dimension().__str__())
        self._st_model = st_model

    def _get_text_embedding(self, text: str) -> list[float]:
        return self._st_model.encode(text).tolist()

    def _get_query_embedding(self, query: str) -> list[float]:
        return self._st_model.encode(query).tolist()

    async def _aget_query_embedding(self, query: str) -> list[float]:
        return self._get_query_embedding(query)


def chunk_text(text: str, metadata: dict, embed_model) -> list[dict]:
    """
    Semantically split text into chunks.
    Each chunk carries the paper's metadata.
    Returns list of {text, metadata} dicts.

    embed_model can be a SentenceTransformer instance — it will be
    wrapped automatically for LlamaIndex compatibility.
    """
    if not text.strip():
        return []

    # Wrap sentence-transformers model for LlamaIndex
    from sentence_transformers import SentenceTransformer
    if isinstance(embed_model, SentenceTransformer):
        embed_model = SentenceTransformerBridge(embed_model)

    doc = Document(text=text, metadata=metadata)

    splitter = SemanticSplitterNodeParser(
        buffer_size=CHUNK_BUFFER_SIZE,
        breakpoint_percentile_threshold=CHUNK_BREAKPOINT_PERCENTILE,
        embed_model=embed_model,
    )

    nodes = splitter.get_nodes_from_documents([doc])

    chunks = []
    for i, node in enumerate(nodes):
        if len(node.text.strip()) < 100:   # skip tiny fragments
            continue
        chunks.append({
            "text":     node.text.strip(),
            "metadata": {**metadata, "chunk_index": i},
        })

    return chunks