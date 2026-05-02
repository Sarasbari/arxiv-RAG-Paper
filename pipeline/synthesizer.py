import anthropic
from config.settings import CLAUDE_MODEL, MAX_TOKENS
from config.prompts import SYSTEM_PROMPT, CONTEXT_TEMPLATE, CHUNK_TEMPLATE
from pipeline.query_pipeline import retrieve


def format_chunks(chunks: list[dict]) -> str:
    """Format retrieved chunks into a readable context block."""
    parts = []
    for i, chunk in enumerate(chunks):
        m = chunk["metadata"]
        parts.append(CHUNK_TEMPLATE.format(
            index=i + 1,
            title=m.get("title", "Unknown"),
            year=m.get("year", "?"),
            authors=m.get("authors", "Unknown"),
            text=chunk["text"][:800],   # cap per-chunk length
        ))
    return "\n\n".join(parts)


def answer(query: str) -> tuple[str, list[dict]]:
    """
    Full Q&A pipeline:
    1. Retrieve relevant chunks
    2. Format context
    3. Call Claude API
    Returns (answer_text, source_chunks)
    """
    chunks = retrieve(query)

    if not chunks:
        return "No relevant papers found in the knowledge base.", []

    context = format_chunks(chunks)
    prompt = CONTEXT_TEMPLATE.format(chunks=context, query=query)

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text, chunks