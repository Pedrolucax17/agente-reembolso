from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)

def list_md_files(base_dir: str | Path) -> List[Path]:
    """Lista arquivos .md recursivamente a partir de base_dir"""
    base = Path(base_dir)
    return sorted([p for p in base.rglob("*.md") if p.is_file()])

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def split_fixed(text: str, chunk_size: int = 800, chunk_overlap=200) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return splitter.split_text(text)

def split_markdown(text: str, *, chunk_size: int = 800, chunk_overlap=200 ) -> List[str]:
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")]
    )
    docs = splitter.split_text(text)
    return [d.page_content for d in docs]

def split_text(text: str, strategy: str = "fixed", *, embedder=None, chunk_size: int=800, chunk_overlap: int=200) -> Tuple[List[str], str]:
    """Divide texto em chunks conforme a estratégia
    Retorna (chunks, strategy_resolvida)
    """
    s = (strategy or "").lower()
    if not s:
        raise RuntimeError("Estratégia de chunking não informada (fixed/markdown)")
    if s == "fixed":
        return split_fixed(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap), "fixed"
    if s == "markdown":
        return split_markdown(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap), "markdown"

    raise RuntimeError(f"Estratégia de chunking inválida: {strategy}")

