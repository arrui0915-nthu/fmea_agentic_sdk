"""Environment configuration for the FMEA RAG application."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


class ConfigurationError(ValueError):
    """Raised when required, non-secret configuration is missing or invalid."""


@dataclass(frozen=True)
class Settings:
    chat_api_key: str | None
    chat_base_url: str | None
    chat_model: str | None
    embedding_api_key: str | None
    embedding_base_url: str | None
    embedding_model: str | None
    markdown_dir: Path
    index_dir: Path


def _read(name: str) -> str | None:
    value = os.getenv(name)
    return value.strip() if value and value.strip() else None


def _validate_base_url(name: str, value: str | None) -> None:
    if value is None:
        return
    lowered = value.rstrip("/").casefold()
    forbidden_suffixes = ("/chat/completions", "/embeddings")
    if lowered.endswith(forbidden_suffixes):
        raise ConfigurationError(
            f"{name} 必須是 OpenAI-compatible base URL，"
            "不可包含 /chat/completions 或 /embeddings。"
        )


def load_settings(
    *,
    require_chat: bool = True,
    require_embedding: bool = True,
) -> Settings:
    """Load .env and validate only the credentials needed by the caller."""

    load_dotenv()
    settings = Settings(
        chat_api_key=_read("AZURE_CHAT_API_KEY"),
        chat_base_url=_read("AZURE_CHAT_BASE_URL"),
        chat_model=_read("AZURE_CHAT_MODEL"),
        embedding_api_key=_read("AZURE_EMBEDDING_API_KEY"),
        embedding_base_url=_read("AZURE_EMBEDDING_BASE_URL"),
        embedding_model=_read("AZURE_EMBEDDING_MODEL"),
        markdown_dir=Path(_read("FMEA_MARKDOWN_DIR") or "./data/markdown"),
        index_dir=Path(_read("FMEA_INDEX_DIR") or "./data/indexes"),
    )

    missing: list[str] = []
    if require_chat:
        for name, value in (
            ("AZURE_CHAT_API_KEY", settings.chat_api_key),
            ("AZURE_CHAT_BASE_URL", settings.chat_base_url),
            ("AZURE_CHAT_MODEL", settings.chat_model),
        ):
            if value is None:
                missing.append(name)
    if require_embedding:
        for name, value in (
            ("AZURE_EMBEDDING_API_KEY", settings.embedding_api_key),
            ("AZURE_EMBEDDING_BASE_URL", settings.embedding_base_url),
            ("AZURE_EMBEDDING_MODEL", settings.embedding_model),
        ):
            if value is None:
                missing.append(name)
    if missing:
        raise ConfigurationError(
            "缺少必要環境變數: " + ", ".join(missing) + "。請參考 .env.example。"
        )

    _validate_base_url("AZURE_CHAT_BASE_URL", settings.chat_base_url)
    _validate_base_url("AZURE_EMBEDDING_BASE_URL", settings.embedding_base_url)
    return settings
