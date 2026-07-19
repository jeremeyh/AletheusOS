from aletheus.span.pipeline_runner import PipelineRunner

def test_pipeline_runner():
    result = PipelineRunner().execute()
    assert result["status"] == "ok"
    assert result["engine"]["providers"] >= 7
    assert result["engine"]["analyzers"] >= 3
