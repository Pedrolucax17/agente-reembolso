from typing import List, Dict, Any, Optional, TypedDict

from langchain_openai import OpenAIEmbeddings
from langgraph.graph import StateGraph, END
from tools import get_conn
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

def upsert_chunks(rows: List[Dict[str, Any]], client_id: Optional[str] = None, empresa: Optional[str] = None) -> int:
    """Upsert idempontente por (doc_path, chunk_ix). Retorna quantidade afetada."""
    if not rows:
        return 0
    with get_conn() as conn:
        with conn.cursor as cur:
            count = 0
            for r in rows:
                vec_lit = vec_to_literal(r["embedding"])
                cur.execute(
                    """insert into public.kb_chunk (doc_path, chunk_ix, content, embedding, meta, client_id, empresa)
                     values (%s, %s, %s, %s::vector(1536), %s::jsonb, %s::uuid, %s)
                     on conflict (doc_path, chunk_ix) 
                     do update set content=excluded.content, embedding=excluded.embedding, meta=excluded.meta,
                                  client_id=excluded.client_id, empresa=excluded.empresa, updated_at=now()
                     """,
                    (
                        r["doc_path"],
                        r["chunk_ix"],
                        r["content"],
                        vec_lit,
                        json_dumps(r.get("meta") or {}),
                        client_id,
                        empresa,
                    ),
                    prepare=False
                )
                count +=1
    return count

def ingest_dir(base_dir: str = "sql", *, strategy: str = "fixed", client_id: Optional[str] = None, empresa: Optional[str] = None, chunk_size: int = 800, chunk_overlap=200) -> int:
    """Pipeline: carrega .md, divide, embeda e upserta. Retorna total processado."""
    embedder = OpenAIEmbeddings(model="text-embedding-3-small")
    chunks = load_and_split_dir(base_dir, strategy=strategy, embedder=embedder, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    text = [it["content"] for it in chunks]
    vectors = embed_texts(text)
    rows = []
    for it, vec in zip(chunks, vectors):
        it2 = dict(it)
        it2["embedding"] = vec
        rows.append(it2)
    return upsert_chunks(rows, client_id=client_id, empresa=empresa)

def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


