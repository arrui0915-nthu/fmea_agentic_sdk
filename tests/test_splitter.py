from pathlib import Path

import pytest

from src.my_splitter import (
    FmeaMarkdownError,
    load_all_documents,
    split_fmea_markdown,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _block(document_id: str, row: int = 3, extra: str = "") -> str:
    return f"""<!-- FMEA_ROW_START id={document_id} -->

## {document_id}

- source_excel: PVD_FMEA.xlsx
- source_sheet: fmea_pvd
- source_excel_row: {row}
- process: PVD
- potential_failure_mode: 膜厚異常
- potential_causes: 靶材壽命用盡
- current_process_controls: 設備警報
- recommended_actions: 定期保養
- severity_before: 8
- occurrence_before: 4
- detection_before: 1
- rpn_before: 32
{extra}
<!-- FMEA_ROW_END -->
"""


def test_marker_block_becomes_one_complete_document(tmp_path: Path) -> None:
    long_text = "完整內容" * 10_000
    path = tmp_path / "PVD_FMEA.md"
    path.write_text(_block("PVD-0001", extra=long_text), encoding="utf-8")

    documents = split_fmea_markdown(path)

    assert len(documents) == 1
    assert documents[0].document_id == "PVD-0001"
    assert long_text in documents[0].content
    assert documents[0].metadata["source_excel_row"] == 3
    assert documents[0].metadata["process_code"] == "PVD"
    assert documents[0].metadata["markdown_file"] == "PVD_FMEA.md"


def test_multiple_markers_never_merge(tmp_path: Path) -> None:
    path = tmp_path / "PVD_FMEA.md"
    path.write_text(_block("PVD-0001") + _block("PVD-0002", 4), encoding="utf-8")

    assert [d.document_id for d in split_fmea_markdown(path)] == [
        "PVD-0001",
        "PVD-0002",
    ]


def test_blank_numeric_metadata_becomes_none(tmp_path: Path) -> None:
    path = tmp_path / "PVD_FMEA.md"
    path.write_text(_block("PVD-0001").replace("rpn_before: 32", "rpn_before: "), encoding="utf-8")

    assert split_fmea_markdown(path)[0].metadata["rpn_before"] is None


@pytest.mark.parametrize(
    "content, expected",
    [
        (_block("PVD-0001").replace("<!-- FMEA_ROW_END -->", ""), "缺少 end marker"),
        (_block("PVD-0001").replace("<!-- FMEA_ROW_START id=PVD-0001 -->\n", ""), "沒有對應 start marker"),
    ],
)
def test_incomplete_markers_fail(tmp_path: Path, content: str, expected: str) -> None:
    path = tmp_path / "PVD_FMEA.md"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(FmeaMarkdownError, match=expected):
        split_fmea_markdown(path)


def test_duplicate_id_fails(tmp_path: Path) -> None:
    path = tmp_path / "PVD_FMEA.md"
    path.write_text(_block("PVD-0001") * 2, encoding="utf-8")

    with pytest.raises(FmeaMarkdownError, match="document ID 重複"):
        split_fmea_markdown(path)


def test_real_markdown_documents_exist_and_ids_are_globally_unique() -> None:
    grouped = load_all_documents(PROJECT_ROOT / "data" / "markdown")
    ids = [document.document_id for documents in grouped.values() for document in documents]

    assert len(ids) > 0
    assert len(ids) == len(set(ids))
