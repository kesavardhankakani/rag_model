from __future__ import annotations

import warnings

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover - optional runtime dependency
    SentenceTransformer = None


class EmbeddingManager:
    def __init__(self, model_name: str | None = None, *, use_sentence_transformers: bool = False):
        self.model_name = model_name
        self.model = None
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self._fitted = False

        if use_sentence_transformers and SentenceTransformer is not None and self.model_name:
            self._load_sentence_transformer()

    def _load_sentence_transformer(self):
        if self.model is not None or SentenceTransformer is None or not self.model_name:
            return

        try:
            self.model = SentenceTransformer(self.model_name)
        except Exception as exc:  # pragma: no cover - network or model loading issue
            warnings.warn(
                f"Could not load the SentenceTransformer model '{self.model_name}'. Falling back to TF-IDF embeddings. Error: {exc}",
                RuntimeWarning,
                stacklevel=2,
            )
            self.model = None

    def encode(self, texts):
        texts = [str(item) for item in texts]
        if not texts:
            return np.empty((0, 0), dtype=np.float32)

        if self.model is not None:
            vectors = self.model.encode(
                texts,
                normalize_embeddings=True,
                convert_to_numpy=True,
                show_progress_bar=False,
            )
            return np.asarray(vectors, dtype=np.float32)

        if not self._fitted:
            self.vectorizer.fit(texts)
            self._fitted = True

        vectors = self.vectorizer.transform(texts).toarray().astype(np.float32)
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return vectors / norms
