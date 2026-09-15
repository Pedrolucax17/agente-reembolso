create extension if not exists vector;

--kb_docs: staging do documento original (arquivo inteiro)
create table if not exists public.kb_docs (
    id bigserial primary key,
    source_path text not null,
    source_hash text not null,
    mime_type text not null default 'text/markdown',
    content text not null,
    meta jsonb not null default '{}'::jsonb,
    create_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique (source_path, source_hash)
);

-- kb_chunks: pedaços do documento, prontos para embedding e busca (vetorial + full-text). Cada chunk pertence a um doc.
create table if not exists public.kb_chunks (
  id bigserial primary key,
  doc_id bigint not null references public.kb_docs(id) on delete cascade,
  chunk_ix int not null,
  content text not null,
  embedding vector(1536) not null,
  fts tsvector generated always as (to_tsvector('portuguese', coalesce(content, ''))) stored,
  meta jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (doc_id, chunk_ix)
);

create or replace function public.kb_touch_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at := now();
  return new;
end;
$$;

drop trigger if exists kb_docs_set_updated_at on public.kb_docs;
create trigger kb_docs_set_updated_at
before update on public.kb_docs
for each row execute function public.kb_touch_updated_at();

drop trigger if exists kb_chunks_set_updated_at on public.kb_chunks;
create trigger kb_chunks_set_updated_at
before update on public.kb_chunks
for each row execute function public.kb_touch_updated_at();