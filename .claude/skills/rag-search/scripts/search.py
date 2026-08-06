"""Semantic search (CLI) — queries the vector store.

Embeds the query, finds nearest-neighbour parts in the store, and reports each hit
rolled up to its parent note. RAG **complements** plaintext + graph search; exact
-string / detail lookups still belong to plaintext search.

Run:  python search.py "your query"   # query the real store
      python search.py --selftest      # isolated temp-vault end-to-end check
"""
from __future__ import annotations

from config import Config, load_config
from embedder import get_embedder
from store import Store


def search(config: Config, query: str, k: int | None = None) -> list[dict]:
    k = config.search_top_k if k is None else k
    store = Store(config)
    embedder = get_embedder(config)
    qvec = embedder.embed([query])[0]
    return store.search(qvec, k)


def format_hits(hits: list[dict]) -> str:
    if not hits:
        return "(no matches)"
    lines = []
    for h in hits:
        dist = h.get("_distance", float("nan"))
        head = f" › {h['heading']}" if h.get("heading") else ""
        snippet = " ".join(h["key_text"].split())[:80]
        lines.append(f"[{dist:.3f}] {h['note_path']}{head}\n    {snippet}")
    return "\n".join(lines)


def _selftest() -> None:
    import dataclasses
    import shutil
    import tempfile
    from pathlib import Path

    from reindex import reindex

    tmp = tempfile.mkdtemp(prefix="rag-search-test-")
    vault = Path(tmp) / "vault"
    vault.mkdir()
    (vault / "alpha.md").write_text("alpha unique content", encoding="utf-8")
    (vault / "beta.md").write_text("beta unique content", encoding="utf-8")
    cfg = dataclasses.replace(
        load_config(), vault_root=vault, store_dir=Path(tmp) / "store"
    )
    try:
        reindex(cfg)
        # mock embedder has no semantics: an exact-text query retrieves its own part.
        hits = search(cfg, "alpha unique content", k=2)
        assert hits and hits[0]["note_path"] == "alpha.md", hits
        print("ok: query embeds, NN search returns the matching note")
        print(format_hits(hits))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if args == ["--selftest"]:
        _selftest()
    elif args:
        # RAG is best-effort: any config / API / dependency failure degrades to a clean
        # signal and exits 0, so the caller's workflow falls back to plaintext instead of
        # crashing. Distinct from "(no matches)", which means RAG ran clean but found nothing.
        try:
            cfg = load_config()
            hits = search(cfg, " ".join(args))
        except Exception as exc:
            print(f"RAG_UNAVAILABLE: {type(exc).__name__}: {exc}")
            print("(rag-search is optional — fall back to plaintext/grep; see SKILL.md 'Availability')")
            sys.exit(0)
        print(format_hits(hits))
        print(f"\n(round budget: SEARCH_MAX_ROUNDS={cfg.search_max_rounds} — agentic-retrieval cap; the agent owns the loop, see SKILL.md)")
    else:
        print('usage: python search.py "your query"  |  python search.py --selftest')
