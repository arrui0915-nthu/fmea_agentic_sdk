"""Split existing FMEA Markdown files into one document per row marker block."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class FmeaDocument:
    document_id: str
    content: str
    metadata: dict[str, Any]


class FmeaMarkdownError(ValueError):
    """Raised when an FMEA Markdown file is structurally invalid."""


START_MARKER = re.compile(r"<!--\s*FMEA_ROW_START\s+id=([^\s>]+)\s*-->")
END_MARKER = re.compile(r"<!--\s*FMEA_ROW_END\s*-->")
TITLE = re.compile(r"^##[ \t]+(.+?)[ \t]*$", re.MULTILINE)
METADATA_ITEM = re.compile(
    r"^-[ \t]+([a-z][a-z0-9_]*):[ \t]*(.*)$",
    re.MULTILINE,
)

REQUIRED_SOURCE_METADATA = {
    "process",
    "source_excel",
    "source_sheet",
    "source_excel_row",
    "potential_failure_mode",
    "potential_causes",
    "current_process_controls",
    "recommended_actions",
    "severity_before",
    "occurrence_before",
    "detection_before",
    "rpn_before",
}

NUMERIC_METADATA = {
    "severity_before",
    "occurrence_before",
    "detection_before",
    "rpn_before",
    "severity_after",
    "occurrence_after",
    "detection_after",
    "rpn_after",
}


def _process_code_from_path(path: Path) -> str:
    stem = re.sub(r"(?i)_?FMEA$", "", path.stem)
    process_code = re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-").upper()
    if not process_code:
        raise FmeaMarkdownError(f"無法從 Markdown 檔名取得製程代碼: {path.name}")
    return process_code


def _parse_number(value: str) -> int | float | str | None:
    value = value.strip()
    if not value:
        return None
    try:
        number = float(value)
    except ValueError:
        return value
    return int(number) if number.is_integer() else number


def _parse_document(
    document_id: str,
    content: str,
    *,
    markdown_path: Path,
    process_code: str,
) -> FmeaDocument:
    title_match = TITLE.search(content)
    if title_match is None:
        raise FmeaMarkdownError(f"document {document_id} 缺少 Markdown 標題")
    title = title_match.group(1).strip()
    if title != document_id:
        raise FmeaMarkdownError(
            f"document ID 與標題不一致: marker={document_id}, title={title}"
        )

    metadata: dict[str, Any] = {
        key: value.replace("<br>", "\n").strip()
        for key, value in METADATA_ITEM.findall(content)
    }
    missing = sorted(REQUIRED_SOURCE_METADATA - metadata.keys())
    if missing:
        raise FmeaMarkdownError(
            f"document {document_id} 缺少 metadata: {', '.join(missing)}"
        )

    try:
        metadata["source_excel_row"] = int(metadata["source_excel_row"])
    except (TypeError, ValueError) as exc:
        raise FmeaMarkdownError(
            f"document {document_id} 的 source_excel_row 不是整數"
        ) from exc

    for field in NUMERIC_METADATA:
        if field in metadata:
            metadata[field] = _parse_number(str(metadata[field]))

    metadata.update(
        {
            "document_id": document_id,
            "process_code": process_code,
            "markdown_file": markdown_path.name,
        }
    )
    return FmeaDocument(
        document_id=document_id,
        content=content,
        metadata=metadata,
    )


def split_fmea_markdown(path: Path) -> list[FmeaDocument]:
    """Create one document per paired FMEA row marker block.

    Only ``FMEA_ROW_START`` and ``FMEA_ROW_END`` are boundaries. Content length
    and Markdown headings never trigger additional splitting.
    """

    path = Path(path)
    text = path.read_text(encoding="utf-8")
    process_code = _process_code_from_path(path)
    documents: list[FmeaDocument] = []
    document_ids: set[str] = set()
    active_id: str | None = None
    buffer: list[str] = []

    for line_number, line in enumerate(text.splitlines(keepends=True), start=1):
        stripped = line.strip()
        start_match = START_MARKER.fullmatch(stripped)
        end_match = END_MARKER.fullmatch(stripped)

        if start_match:
            if active_id is not None:
                raise FmeaMarkdownError(
                    f"第 {line_number} 行出現巢狀 start marker；"
                    f"document {active_id} 缺少 end marker"
                )
            active_id = start_match.group(1)
            if active_id in document_ids:
                raise FmeaMarkdownError(f"document ID 重複: {active_id}")
            buffer = []
            continue

        if end_match:
            if active_id is None:
                raise FmeaMarkdownError(
                    f"第 {line_number} 行的 end marker 沒有對應 start marker"
                )
            content = "".join(buffer).strip()
            documents.append(
                _parse_document(
                    active_id,
                    content,
                    markdown_path=path,
                    process_code=process_code,
                )
            )
            document_ids.add(active_id)
            active_id = None
            buffer = []
            continue

        if "FMEA_ROW_START" in line or "FMEA_ROW_END" in line:
            raise FmeaMarkdownError(f"第 {line_number} 行的 FMEA marker 格式錯誤")

        if active_id is not None:
            buffer.append(line)

    if active_id is not None:
        raise FmeaMarkdownError(f"document {active_id} 缺少 end marker")

    return documents


def load_all_documents(markdown_dir: Path) -> dict[str, list[FmeaDocument]]:
    """Load all Markdown knowledge bases and enforce globally unique IDs."""

    markdown_dir = Path(markdown_dir)
    if not markdown_dir.is_dir():
        raise FileNotFoundError(f"找不到 Markdown 目錄: {markdown_dir}")

    grouped: dict[str, list[FmeaDocument]] = {}
    global_ids: dict[str, str] = {}
    for path in sorted(markdown_dir.glob("*.md"), key=lambda item: item.name.casefold()):
        process_code = _process_code_from_path(path)
        if process_code in grouped:
            raise FmeaMarkdownError(
                f"多個 Markdown 對應到相同製程代碼 {process_code}: {path.name}"
            )
        documents = split_fmea_markdown(path)
        for document in documents:
            previous_file = global_ids.get(document.document_id)
            if previous_file is not None:
                raise FmeaMarkdownError(
                    f"全域 document ID 重複: {document.document_id} "
                    f"({previous_file}, {path.name})"
                )
            global_ids[document.document_id] = path.name
        grouped[process_code] = documents
    return grouped
