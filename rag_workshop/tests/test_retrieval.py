import numpy as np

from rag_workshop.core.retriever import cosine_similarity, retrieve_top_k


def test_cosine_similarity_returns_one_for_same_vector():
    vec_a = np.array([1.0, 0.0])
    vec_b = np.array([1.0, 0.0])
    sim = cosine_similarity(vec_a, vec_b)
    assert abs(sim - 1.0) < 1e-6


def test_retrieve_top_k_returns_best_matches():
    query = np.array([1.0, 0.0])
    doc_vectors = np.array([
        [0.9, 0.1],
        [0.1, 0.9],
        [0.0, 1.0],
    ])
    chunks = [
        {"chunk_id": "c1", "text": "alpha", "source_file": "a.pdf", "page_number": 1},
        {"chunk_id": "c2", "text": "beta", "source_file": "a.pdf", "page_number": 2},
        {"chunk_id": "c3", "text": "gamma", "source_file": "a.pdf", "page_number": 3},
    ]
    results = retrieve_top_k(query, doc_vectors, chunks, top_k=2, min_similarity=0.0)
    assert results[0]["chunk_id"] == "c1"
    assert len(results) == 2
