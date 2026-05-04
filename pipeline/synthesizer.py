from google import genai
from config.settings import GEMINI_MODEL, MAX_TOKENS
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
    3. Call Gemini API
    Returns (answer_text, source_chunks)
    """
    chunks = retrieve(query)

    if not chunks:
        return "No relevant papers found in the knowledge base.", []

    context = format_chunks(chunks)
    prompt = CONTEXT_TEMPLATE.format(chunks=context, query=query)

    try:
        client = genai.Client()
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "max_output_tokens": MAX_TOKENS,
            },
        )
        return response.text, chunks
    except Exception as e:
        # Loophole fix: Prevent unhandled API errors (like quota exceeded) from crashing the app
        return f"⚠️ **Failed to generate answer.** Please check your API key and quota. Error details: `{str(e)}`", chunks