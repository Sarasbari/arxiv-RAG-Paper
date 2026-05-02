import pypdf
from pathlib import Path


def extract_text(pdf_path: Path) -> str:
    """
    Extract raw text from a PDF file.
    Returns empty string if extraction fails.
    """
    try:
        reader = pypdf.PdfReader(str(pdf_path))
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())
        return "\n\n".join(pages)
    except Exception as e:
        print(f"  Extraction failed for {pdf_path.name}: {e}")
        return ""