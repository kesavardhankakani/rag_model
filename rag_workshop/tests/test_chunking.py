from rag_workshop.core.chunker import chunk_document
from rag_workshop.core.text_cleaner import clean_text


def test_clean_text_removes_odd_spacing_and_blank_lines():
    raw = "Hello   world\n\n\nThis   is\n a test\n\n"
    cleaned = clean_text(raw)
    assert "Hello world" in cleaned
    assert "This is" in cleaned
    assert "\n\n" in cleaned


def test_chunk_document_creates_multiple_chunks():
    text = "Sentence one. " * 80
    chunks = chunk_document({"filename": "demo.txt", "pages": [{"number": 1, "text": text}]}, chunk_size=120, overlap=20)
    assert len(chunks) > 1
    assert all(chunk["text"] for chunk in chunks)
