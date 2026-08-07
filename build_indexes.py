"""Build or refresh one FAISS index for each FMEA Markdown file."""

from openai import OpenAI

from src.config import ConfigurationError, load_settings
from src.faiss_knowledge_base import build_all_knowledge_bases


def main() -> None:
    try:
        settings = load_settings(require_chat=False, require_embedding=True)
    except ConfigurationError as exc:
        raise SystemExit(str(exc)) from exc

    client = OpenAI(
        api_key=settings.embedding_api_key,
        base_url=settings.embedding_base_url,
    )
    knowledge_bases = build_all_knowledge_bases(
        markdown_dir=settings.markdown_dir,
        index_dir=settings.index_dir,
        embedding_client=client,
        embedding_model=str(settings.embedding_model),
    )
    for process_code, knowledge_base in knowledge_bases.items():
        print(f"{process_code}: {knowledge_base.vector_count} vectors")


if __name__ == "__main__":
    main()
