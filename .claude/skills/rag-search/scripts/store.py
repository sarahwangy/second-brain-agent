"""LanceDB store for the rag-search toolkit.

One row per chunk. The store is a *derived, rebuildable* artifact living in the
gitignored `.rag-index/` dir — never the source of truth (the note is). The
decoupled reindex (step 4) drives it through these primitives.

Primitives:
- `upsert_note(note_path, rows)` — replace ALL of a note's rows (delete + add).
  Matches the reindex model: on a note change, wipe its entries and re-insert.
- `delete_note(note_path)` — drop a note's rows (e.g. note deleted from vault).
- `search(query_vector, k)` — k nearest neighbours across all chunks.
- `count()` — total chunk rows.
"""
from __future__ import annotations

from pathlib import Path

import lancedb
from lancedb.pydantic import LanceModel, Vector

from config import Config

TABLE_NAME = "chunks"


def make_chunk_schema(dim: int) -> type[LanceModel]:
    """Schema is dim-dependent, so build the LanceModel per configured dimension."""

    class ChunkRow(LanceModel):
        note_path: str        # vault-relative path of the parent note
        chunk_index: int      # 0-based position of the section within the note
        heading: str          # the section heading ("" for a heading-less note)
        key_text: str         # v1: the raw section text (the embedded + returned payload)
        vector: Vector(dim)   # embedding of key_text
        content_hash: str     # hash of the whole parent note — change detection
        mtime: float          # parent note file mtime — change detection

    return ChunkRow


class Store:
    def __init__(self, config: Config):
        self.config = config
        self.dim = config.embed_dim
        self.schema = make_chunk_schema(self.dim)
        Path(config.store_dir).mkdir(parents=True, exist_ok=True)
        self.db = lancedb.connect(str(config.store_dir))
        self.table = self.db.create_table(TABLE_NAME, schema=self.schema, exist_ok=True)

    @staticmethod
    def _path_filter(note_path: str) -> str:
        # SQL string literal — escape single quotes to keep the filter well-formed.
        return "note_path = '" + note_path.replace("'", "''") + "'"

    def delete_note(self, note_path: str) -> None:
        self.table.delete(self._path_filter(note_path))

    def upsert_note(self, note_path: str, rows: list[dict]) -> None:
        """Replace, don't accumulate: wipe the note's existing rows, then add the new set."""
        self.delete_note(note_path)
        if rows:
            self.table.add(rows)

    def search(self, query_vector: list[float], k: int = 5) -> list[dict]:
        # Explicit L2 (correct for normalized embeddings) — don't rely on LanceDB's default.
        return self.table.search(query_vector).metric("l2").limit(k).to_list()

    def count(self) -> int:
        return self.table.count_rows()

    def indexed_notes(self) -> dict[str, str]:
        """note_path -> content_hash for every indexed note (one hash per note)."""
        if self.table.count_rows() == 0:
            return {}
        tbl = self.table.to_arrow()
        paths = tbl.column("note_path").to_pylist()
        hashes = tbl.column("content_hash").to_pylist()
        return dict(zip(paths, hashes))


if __name__ == "__main__":
    # Mock round-trip — isolated temp store, cleaned up after.
    import dataclasses
    import shutil
    import tempfile

    from config import load_config
    from embedder import get_embedder

    cfg = load_config()
    tmp = tempfile.mkdtemp(prefix="rag-store-test-")
    cfg = dataclasses.replace(cfg, store_dir=Path(tmp))
    try:
        emb = get_embedder(cfg)
        texts = ["alpha section about cats", "beta section about dogs"]
        vecs = emb.embed(texts)
        rows = [
            dict(
                note_path="A.md",
                chunk_index=i,
                heading=f"H{i}",
                key_text=t,
                vector=v,
                content_hash="hash-v1",
                mtime=0.0,
            )
            for i, (t, v) in enumerate(zip(texts, vecs))
        ]

        store = Store(cfg)
        store.upsert_note("A.md", rows)
        assert store.count() == 2, "expected 2 rows after upsert"

        # Re-upsert must REPLACE, not append.
        store.upsert_note("A.md", rows)
        assert store.count() == 2, "upsert should replace a note's rows, not append"

        # NN search: querying with a chunk's own text returns that chunk first.
        q = emb.embed(["alpha section about cats"])[0]
        hits = store.search(q, k=2)
        assert hits[0]["key_text"] == texts[0], "nearest neighbour is not the matching chunk"

        store.delete_note("A.md")
        assert store.count() == 0, "delete_note should clear the note's rows"

        print("ok: upsert replaces, NN search returns self, delete clears")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
