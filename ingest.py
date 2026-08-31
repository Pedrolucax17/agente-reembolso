from typing import List, Dict, Any, Optional, TypedDict

from langchain_openai import OpenAIEmbeddings
from langgraph.graph import StateGraph, END

from rag.loaders import load_and_split_dir, split_text
from json import dumps as json_dumps
import hashlib
from pathlib import Path
import mimetypes
import os

def vec_to_literal(v: List[float]) -> str:
    """Converte vetor de floats em literal aceito pelo pgvector: '[v1, v2, ...]'"""
    return "[" + ",".join(f"{x:.6f}" for x in v) + "]"

def embed_texts(texts: List[str]) -> List[List[float]]:
    """Gera embeddings para os textos (OpenAI)."""
    emb = OpenAIEmbeddings(model="text-embedding-3-small")
    return emb.embed_documents(texts)

