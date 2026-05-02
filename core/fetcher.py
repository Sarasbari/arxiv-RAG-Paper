import arxiv
from pathlib import Path
from config.settings import PAPERS_DIR, DEFAULT_FETCH_COUNT


def fetch_papers(query: str, max_results: int = DEFAULT_FETCH_COUNT) -> list[dict]:
    """
    Search arxiv and download PDFs.
    Returns list of paper metadata dicts.
    """
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    papers = []
    for result in search.results():
        paper_id = result.entry_id.split("/")[-1]
        pdf_path = PAPERS_DIR / f"{paper_id}.pdf"

        if not pdf_path.exists():
            try:
                result.download_pdf(dirpath=str(PAPERS_DIR), filename=pdf_path.name)
                print(f"  Downloaded: {result.title[:60]}")
            except Exception as e:
                print(f"  Failed to download {paper_id}: {e}")
                continue

        papers.append({
            "paper_id": paper_id,
            "title":    result.title,
            "authors":  [a.name for a in result.authors],
            "year":     result.published.year,
            "abstract": result.summary[:500],
            "pdf_path": pdf_path,
        })

    return papers