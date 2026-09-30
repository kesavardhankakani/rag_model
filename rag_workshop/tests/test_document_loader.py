from pathlib import Path

import fitz
from docx import Document

from rag_workshop.core.document_loader import extract_document


def test_extract_document_from_docx(tmp_path):
    doc_path = tmp_path / "sample.docx"
    doc = Document()
    doc.add_paragraph("This is a sample campus course document.")
    doc.add_paragraph("Eligibility requires enrollment and approval.")
    doc.save(str(doc_path))

    extracted = extract_document(doc_path)
    assert extracted.file_type == "docx"
    assert "Eligibility" in extracted.text


def test_extract_document_from_pdf(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Eligibility requires enrollment and approval.")
    doc.save(str(pdf_path))
    doc.close()

    extracted = extract_document(pdf_path)
    assert extracted.file_type == "pdf"
    assert "Eligibility" in extracted.text


def test_extract_document_rejects_empty_text(tmp_path):
    empty_doc = tmp_path / "empty.docx"
    doc = Document()
    doc.save(str(empty_doc))

    extracted = extract_document(empty_doc)
    assert extracted.text == ""
