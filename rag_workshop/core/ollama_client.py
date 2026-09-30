from __future__ import annotations

import requests


def detect_ollama_models(base_url: str = "http://localhost:11434"):
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=2)
        if response.status_code != 200:
            return []
        payload = response.json()
        models = payload.get("models", [])
        return [model.get("name") for model in models if model.get("name")]
    except Exception:
        return []


def is_ollama_available(base_url: str = "http://localhost:11434") -> bool:
    return bool(detect_ollama_models(base_url))


def generate_response(
    prompt: str,
    model_name: str,
    temperature: float = 0.2,
    base_url: str = "http://localhost:11434",
    num_predict: int = 1536,
    num_ctx: int = 4096,
    timeout: int = 240,
):
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": float(temperature),
            "num_predict": int(num_predict),
            "num_ctx": int(num_ctx),
        },
    }
    response = requests.post(f"{base_url}/api/generate", json=payload, timeout=timeout)
    if response.status_code != 200:
        raise RuntimeError(f"Ollama request failed with status {response.status_code}: {response.text}")
    data = response.json()
    return {"response": data.get("response", "").strip(), "model": model_name}
