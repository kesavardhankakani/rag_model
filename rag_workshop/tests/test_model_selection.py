from rag_workshop.core.model_selector import select_model


def test_select_model_prefers_qwen_when_present():
    models = ["llama3.1:latest", "qwen2.5:latest"]
    selected = select_model(models)
    assert selected == "qwen2.5:latest"


def test_select_model_falls_back_to_llama():
    models = ["llama3.2:latest"]
    selected = select_model(models)
    assert selected == "llama3.2:latest"


def test_select_model_returns_none_when_no_supported_model_exists():
    models = ["mistral:latest"]
    assert select_model(models) is None
