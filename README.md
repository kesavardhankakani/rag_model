# Local Workshop RAG Application

This project is a beginner-friendly but technically correct local Retrieval-Augmented Generation (RAG) workshop app for college students. It lets a user upload a PDF or DOCX file, extract text, split it into meaningful chunks, generate embeddings locally, retrieve the most relevant content by cosine similarity, and send only that context to a local Ollama model for a grounded answer.

## Why this project exists

The key teaching idea is simple:

Document
→ Extract
→ Clean
→ Chunk
→ Embed
→ Compare
→ Retrieve
→ Context
→ LLM
→ Answer

RAG is not just “read the file.” The system first finds relevant document text, then supplies that text as context to the LLM so the final answer is grounded in the uploaded document.

## Core concepts explained for students

- Embeddings represent semantic meaning as vectors.
- Cosine similarity measures how closely aligned two vectors are.
- Top-K retrieval chooses the most relevant document chunks.
- The LLM does not automatically know the document; it must receive the retrieved context first.
- The retrieved context is treated as reference data, not as hidden instructions.

## Tech stack

- Python 3.11+
- Streamlit for the UI
- PyMuPDF for PDF extraction
- python-docx for DOCX extraction
- sentence-transformers for local embeddings
- scikit-learn or NumPy for cosine similarity
- Ollama for local LLM inference

## Local model detection policy

The app checks the installed Ollama models at runtime and follows this order:

1. Use Qwen if any Qwen model is installed
2. Otherwise use Llama if any Llama model is installed
3. Otherwise show a friendly setup message and do not crash

This logic is intentionally flexible so students are not forced to use one exact model tag.

## Project structure

```text
rag_workshop/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── core/
│   ├── document_loader.py
│   ├── text_cleaner.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── ollama_client.py
│   ├── model_selector.py
│   └── rag_pipeline.py
├── ui/
│   ├── components.py
│   └── styles.py
├── data/
│   └── uploads/
└── tests/
    ├── test_chunking.py
    ├── test_embeddings.py
    ├── test_retrieval.py
    └── test_model_selection.py
```

## Setup

1. Create a virtual environment.
2. Install dependencies.
3. Install Ollama.
4. Pull a supported model, such as `qwen2.5` or `llama3.2`.
5. Start Streamlit and upload a document.

## Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ollama installation

Download and install Ollama from https://ollama.com.

After installing it, verify the service by running:

```bash
ollama list
```

If nothing is returned, install a model next.

## Model installation examples

### Qwen

```bash
ollama pull qwen2.5
```

### Llama

```bash
ollama pull llama3.2
```

The app accepts variations such as `qwen3`, `qwen2.5`, `llama3.1`, and `llama3.2` without hard-coding one exact tag.

## Run the app

```bash
streamlit run rag_workshop/app.py
```

## Workshop demo flow

1. Upload a syllabus or course PDF.
2. Inspect the extracted text and chunk count.
3. Ask a question like: “What are the eligibility requirements?”
4. View the retrieved chunks and similarity scores.
5. Inspect the model selection and answer generation.
6. Evaluate whether the final answer is grounded in the document.

## Example questions

- What are the prerequisites for this course?
- Which assignment is worth the most marks?
- What are the project deadlines?
- What are the attendance requirements?
- Where is the grading rubric described?

## Hallucination control

The app intentionally does not send unrelated document content to the LLM. If retrieval does not produce a strong match, it tells the user that the relevant information was not found instead of guessing.

## Troubleshooting

- Ollama not running: start the Ollama service and verify with `ollama list`.
- No model installed: use `ollama pull qwen2.5` or `ollama pull llama3.2`.
- PDF extraction failure: confirm that the PDF is a real text PDF and not an image-only scan.
- DOCX extraction failure: ensure the file is a valid DOCX document.
- Empty document: the app will display a clear message instead of crashing.
- Unsupported file type: upload PDF or DOCX only.

## Notes for teaching

This project is designed to help students understand the full RAG pipeline in an approachable way: document extraction, cleaning, chunking, embeddings, similarity search, retrieval, and grounded generation.

The goal is not to hide complexity but to make it understandable, local, transparent, and safe for workshop use.
