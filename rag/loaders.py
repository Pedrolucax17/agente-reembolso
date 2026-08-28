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

print(read_text(Path("rag/docs/anexo_iv_exclusoes.md")))

