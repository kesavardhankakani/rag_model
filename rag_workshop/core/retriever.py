from __future__ import annotations

import numpy as np


def cosine_similarity(vec_a, vec_b):
    a = np.asarray(vec_a, dtype=np.float32).reshape(-1)
    b = np.asarray(vec_b, dtype=np.float32).reshape(-1)
    norm_product = np.linalg.norm(a) * np.linalg.norm(b)
    if norm_product == 0:
        return 0.0
    return float(np.dot(a, b) / norm_product)


def retrieve_top_k(query_vector, document_vectors, chunks, top_k=3, min_similarity=0.0):
    query = np.asarray(query_vector, dtype=np.float32).reshape(1, -1)
    document_vectors = np.asarray(document_vectors, dtype=np.float32)

    if document_vectors.size == 0 or len(chunks) == 0:
        return []

    scores = []
    for idx, vector in enumerate(document_vectors):
        sim = cosine_similarity(query[0], vector)
        scores.append((idx, sim))

    ranked = sorted(scores, key=lambda item: item[1], reverse=True)
    results = []
    for idx, score in ranked[:top_k]:
        if score < min_similarity:
            continue
        chunk = chunks[idx]
        results.append({
            "chunk_id": chunk.get("chunk_id"),
            "text": chunk.get("text", ""),
            "source_file": chunk.get("source_file", ""),
            "page_number": chunk.get("page_number"),
            "score": float(score),
        })

    return results
