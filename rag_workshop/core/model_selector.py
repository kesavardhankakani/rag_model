from __future__ import annotations


def select_model(model_names):
    names = model_names or []
    for candidate in names:
        name = str(candidate).lower()
        if "qwen" in name:
            return candidate

    for candidate in names:
        name = str(candidate).lower()
        if "llama" in name:
            return candidate

    return None
