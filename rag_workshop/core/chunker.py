from __future__ import annotations

from typing import Any, Dict, List

from rag_workshop.core.text_cleaner import clean_text


def _split_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap must be non-negative")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    step = chunk_size - overlap
    chunks: List[str] = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start += step

    return chunks


def chunk_document(document: Dict[str, Any], chunk_size: int = 500, overlap: int = 80) -> List[Dict[str, Any]]:
    """Convert a document dict into chunk records with metadata."""
    filename = document.get("filename", "document")
    pages = document.get("pages") or [{"number": 1, "text": document.get("text", "")}]

    chunks: List[Dict[str, Any]] = []
    chunk_index = 1

    for page in pages:
        page_number = page.get("number", 1)
        page_text = clean_text(page.get("text", ""))
        if not page_text:
            continue

        for piece in _split_text(page_text, chunk_size=chunk_size, overlap=overlap):
            chunks.append({
                "chunk_id": f"chunk_{chunk_index:03d}",
                "text": piece,
                "source_file": filename,
                "page_number": page_number,
                "char_count": len(piece),
            })
            chunk_index += 1

    return chunks
