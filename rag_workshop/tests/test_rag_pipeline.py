from unittest.mock import patch

from rag_workshop.core.rag_pipeline import RAGPipeline


def make_pipeline(chunk_count):
    pipeline = RAGPipeline()
    pipeline.chunks = [
        {
            "chunk_id": f"chunk_{index:03d}",
            "text": f"Unique source passage {index}",
            "source_file": "course.pdf",
            "page_number": index + 1,
        }
        for index in range(chunk_count)
    ]
    pipeline.selected_model = "qwen2.5:3b"
    return pipeline


def test_whole_document_request_uses_every_chunk_without_similarity_filtering():
    pipeline = make_pipeline(3)
    pipeline.documents = [{
        "filename": "course.pdf",
        "pages": [{"number": 1, "text": "Deduplicated full-page source text."}],
    }]

    with (
        patch.object(pipeline, "refresh_model_selection", return_value="qwen2.5:3b"),
        patch("rag_workshop.core.rag_pipeline.retrieve_top_k") as retrieve_top_k,
        patch(
            "rag_workshop.core.rag_pipeline.generate_response",
            return_value={"response": "A complete explanation."},
        ) as generate_response,
    ):
        response = pipeline.answer_question("Explain the totoal PDF")

    retrieve_top_k.assert_not_called()
    prompt = generate_response.call_args.args[0]
    assert "Deduplicated full-page source text." in prompt
    assert response["document_overview"] is True
    assert len(response["retrieval"]) == 3
    assert generate_response.call_args.kwargs["num_ctx"] == 16384
    assert generate_response.call_args.kwargs["num_predict"] == 768
    assert generate_response.call_args.kwargs["timeout"] == 600


def test_large_document_overview_summarizes_all_batches_before_answering():
    pipeline = make_pipeline(33)
    for chunk in pipeline.chunks:
        chunk["text"] = (chunk["text"] + " detailed source material") * 60
    generated = [
        {"response": "Notes from batch one."},
        {"response": "Notes from batch two."},
        {"response": "Notes from batch three."},
        {"response": "Full document explanation."},
    ]

    with (
        patch.object(pipeline, "refresh_model_selection", return_value="qwen2.5:3b"),
        patch("rag_workshop.core.rag_pipeline.retrieve_top_k") as retrieve_top_k,
        patch("rag_workshop.core.rag_pipeline.generate_response", side_effect=generated) as generate_response,
    ):
        response = pipeline.answer_question("Explain the whole document")

    retrieve_top_k.assert_not_called()
    assert generate_response.call_count == 4
    final_prompt = generate_response.call_args.args[0]
    assert "Notes from batch one." in final_prompt
    assert "Notes from batch two." in final_prompt
    assert "Notes from batch three." in final_prompt
    assert generate_response.call_args.kwargs["num_ctx"] == 8192
    assert len(response["retrieval"]) == 33