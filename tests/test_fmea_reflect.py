from pathlib import Path

from agentic_sdk import ResponseCheckReflect

from src.config import Settings
from src.workflow import build_workflow


def test_workflow_uses_simple_response_check_reflect() -> None:
    settings = Settings(
        chat_api_key="test-key",
        chat_base_url="http://localhost/v1",
        chat_model="test-model",
        embedding_api_key=None,
        embedding_base_url=None,
        embedding_model=None,
        markdown_dir=Path("unused-markdown"),
        index_dir=Path("unused-indexes"),
    )

    workflow = build_workflow({}, settings=settings)

    assert type(workflow.modules["reflect"]) is ResponseCheckReflect
