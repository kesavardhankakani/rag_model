import numpy as np

from rag_workshop.core.embeddings import EmbeddingManager


def test_embedding_model_encodes_to_vector():
    manager = EmbeddingManager(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectors = manager.encode(["machine learning", "deep learning"])
    assert vectors.shape[0] == 2
    assert vectors.shape[1] > 0
    assert np.isfinite(vectors).all()


def test_embedding_manager_prefers_lightweight_fallback_by_default():
    manager = EmbeddingManager(model_name="sentence-transformers/all-MiniLM-L6-v2")
    assert manager.model is None
    assert manager.vectorizer is not None
