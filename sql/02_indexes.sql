-- Indicie para localizar rapidamente um doc pelo caminho de origem
create index if not exists ix_kb_docs_source on public.kb_docs (source_path);

-- Índice para navegar do chunk até o documento de origem (FK)
create index if not exists ix_kb_chunks_doc_id on public.kb_chunks (doc_id);

-- Busca lexical / full-text - útil para hybrid search
create index if not exists ix_kb_chunks_fts on public.kb_chunks using gin (fts);

-- Busca vetorial por similaridade de coseno
create index if not exists ix_kb_chunks_embedding_hnsw
    on public.kb_chunks using hnsw (embedding vector_cosine_ops)
    with (m = 16, ef_construction = 64);
