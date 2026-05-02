from llama_index.core import Document
from llama_index.core.node_parser import SemanticSplitterNodeParser
from config.settings import CHUNK_BREAKPOINT_PERCENTILE, CHUNK_BUFFER_SIZE


def chunk_text(text: str, metadata: dict, embed_model) -> list[dict]:
    """
    Semantically split text into chunks.
    Each chunk carries the paper's metadata.
    Returns list of {text, metadata} dicts.
    """
    if not text.strip():
        return []

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