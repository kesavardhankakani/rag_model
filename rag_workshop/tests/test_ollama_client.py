from unittest.mock import Mock, patch

from rag_workshop.core.ollama_client import generate_response


@patch("rag_workshop.core.ollama_client.requests.post")
def test_generate_response_uses_long_answer_token_budget(mock_post):
    mock_post.return_value = Mock(status_code=200)
    mock_post.return_value.json.return_value = {"response": "Detailed answer", "model": "qwen2.5:3b"}

    result = generate_response("Explain the topic", model_name="qwen2.5:3b")

    payload = mock_post.call_args.kwargs["json"]
    assert payload["options"]["num_predict"] == 1536
    assert mock_post.call_args.kwargs["timeout"] == 240
    assert result["response"] == "Detailed answer"