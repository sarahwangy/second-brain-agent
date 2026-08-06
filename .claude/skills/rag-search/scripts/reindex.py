"""Decoupled reindex (CLI) — keeps the vector store in sync with the vault.

Stage (b) is agent-semantic: the chunking judgement is made by the agent in the
skill session (路 2), not by this script. So reindex splits into commands the
skill orchestrates:

  plan    scan the vault, detect changes by content hash, emit (JSON) each changed
          note's numbered blocks + the list of deleted notes. No LLM here.
  apply   read the agent's decision (JSON on stdin): for each note, a part is a
          contiguous BLOCK-INDEX range; slice each part verbatim, embed, upsert.
          Deleted notes are dropped. The agent supplies only block ranges — it
          never emits text, so the note is never altered (agent != author).
  auto    no-agent fallback: chunk every changed note with naive_parts.

Embedding uses the configured embedder (mock by default). Touches only the
gitignored store — no markdown, no JSONL log, no commit.

Run:  python reindex.py plan
      python reindex.py apply  < decision.json
      python reindex.py auto
      python reindex.py --selftest        # auto path
      python reindex.py --selftest-agent  # plan/apply path
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

from chunking import Part, naive_parts, parse_blocks
from config import Config, load_config
from embedder import get_embedder
from store import Store


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def iter_vault_notes(config: Config) -> dict[str, Path]:
    """vault-relative path -> absolute path for every indexable .md note."""
    root = Path(config.vault_root)
    notes: dict[str, Path] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in config.exclude_dirs]
        for name in filenames:
            if not name.endswith(".md") or name in config.exclude_files:
                continue
            abs_path = Path(dirpath) / name
            notes[str(abs_path.relative_to(root))] = abs_path
    return notes


def _rows_for(note_path, parts, content_hash, mtime, embedder):
    vectors = embedder.embed([p.text for p in parts]) if parts else []
    return [
        dict(note_path=note_path, chunk_index=i, heading=p.heading,
             key_text=p.text, vector=v, content_hash=content_hash, mtime=mtime)
        for i, (p, v) in enumerate(zip(parts, vectors))
    ]


# --- agent path (路 2) ---

def plan(config: Config) -> dict:
    """Scan + change-detect. Emit each changed note's numbered blocks for the
    agent, plus notes to delete. No embedding, no LLM."""
    store = Store(config)
    disk = iter_vault_notes(config)
    indexed = store.indexed_notes()
    changed = []
    for rel, abs_path in disk.items():
        content = abs_path.read_text(encoding="utf-8")
        content_hash = _hash(content)
        if indexed.get(rel) == content_hash:
            continue
        blocks = parse_blocks(content)
        changed.append({
            "note_path": rel,
            "content_hash": content_hash,
            "blocks": [
                {"index": b.index, "type": b.type, "title": b.title,
                 "section": b.section, "text": b.text}
                for b in blocks
            ],
        })
    deleted = [rel for rel in indexed if rel not in disk]
    return {"changed": changed, "deleted": deleted}


def _parts_from_ranges(blocks, lines, ranges) -> list[Part]:
    parts: list[Part] = []
    for rng in ranges:
        s, e = int(rng[0]), int(rng[1])
        if s > e or s < 0 or e >= len(blocks):
            raise ValueError(f"bad block range {rng} (note has {len(blocks)} blocks)")
        start_line, end_line = blocks[s].start_line, blocks[e].end_line
        text = "\n".join(lines[start_line : end_line + 1])
        heading = blocks[s].title if blocks[s].type == "heading" else blocks[s].section
        parts.append(Part(text=text, start_line=start_line, end_line=end_line, heading=heading or ""))
    return parts


def apply(config: Config, decision: dict) -> dict:
    """Apply the agent's decision:
    {notes: [{note_path, parts: [[start_block, end_block], ...]}], deleted: [...]}."""
    store = Store(config)
    embedder = get_embedder(config)
    stats = {"applied": 0, "deleted": 0, "parts": 0}
    for item in decision.get("notes", []):
        rel = item["note_path"]
        abs_path = Path(config.vault_root) / rel
        content = abs_path.read_text(encoding="utf-8")
        blocks = parse_blocks(content)
        parts = _parts_from_ranges(blocks, content.split("\n"), item["parts"])
        rows = _rows_for(rel, parts, _hash(content), os.path.getmtime(abs_path), embedder)
        store.upsert_note(rel, rows)
        stats["applied"] += 1
        stats["parts"] += len(rows)
    for rel in decision.get("deleted", []):
        store.delete_note(rel)
        stats["deleted"] += 1
    return stats


# --- no-agent fallback (auto) ---

def reindex(config: Config) -> dict:
    """Fallback: chunk every changed note with naive_parts (no agent)."""
    store = Store(config)
    embedder = get_embedder(config)
    disk = iter_vault_notes(config)
    indexed = store.indexed_notes()
    stats = {"indexed": 0, "skipped": 0, "deleted": 0, "parts": 0}
    for rel, abs_path in disk.items():
        content = abs_path.read_text(encoding="utf-8")
        content_hash = _hash(content)
        if indexed.get(rel) == content_hash:
            stats["skipped"] += 1
            continue
        parts = naive_parts(parse_blocks(content), content)
        rows = _rows_for(rel, parts, content_hash, os.path.getmtime(abs_path), embedder)
        store.upsert_note(rel, rows)
        stats["indexed"] += 1
        stats["parts"] += len(rows)
    for rel in indexed:
        if rel not in disk:
            store.delete_note(rel)
            stats["deleted"] += 1
    return stats


# --- self-tests ---

def _selftest() -> None:
    import dataclasses
    import shutil
    import tempfile

    tmp = tempfile.mkdtemp(prefix="rag-reindex-test-")
    vault = Path(tmp) / "vault"
    vault.mkdir()
    (vault / "alpha.md").write_text("alpha unique content", encoding="utf-8")
    (vault / "beta.md").write_text("## Beta\n\nbeta unique content", encoding="utf-8")
    cfg = dataclasses.replace(load_config(), vault_root=vault, store_dir=Path(tmp) / "store")
    try:
        assert (s := reindex(cfg))["indexed"] == 2 and s["parts"] >= 2, s
        assert (s := reindex(cfg))["skipped"] == 2 and s["indexed"] == 0, s
        (vault / "alpha.md").write_text("alpha unique content EDITED", encoding="utf-8")
        assert (s := reindex(cfg))["indexed"] == 1 and s["skipped"] == 1, s
        (vault / "beta.md").unlink()
        assert (s := reindex(cfg))["deleted"] == 1, s
        print("ok [auto]: indexes new, skips unchanged, re-indexes edits, drops deleted")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _selftest_agent() -> None:
    import dataclasses
    import shutil
    import tempfile

    tmp = tempfile.mkdtemp(prefix="rag-agent-test-")
    vault = Path(tmp) / "vault"
    vault.mkdir()
    (vault / "n.md").write_text("## A\n\naaa text\n\n## B\n\nbbb text", encoding="utf-8")
    cfg = dataclasses.replace(load_config(), vault_root=vault, store_dir=Path(tmp) / "store")
    try:
        p = plan(cfg)
        assert len(p["changed"]) == 1 and p["deleted"] == [], p
        types = [b["type"] for b in p["changed"][0]["blocks"]]
        assert types == ["heading", "paragraph", "heading", "paragraph"], types

        # simulate agent: two parts, each heading + its paragraph
        s = apply(cfg, {"notes": [{"note_path": "n.md", "parts": [[0, 1], [2, 3]]}], "deleted": []})
        assert s["applied"] == 1 and s["parts"] == 2, s
        assert Store(cfg).count() == 2

        # simulate agent merging strongly-related blocks into one part -> replaces prior rows
        s = apply(cfg, {"notes": [{"note_path": "n.md", "parts": [[0, 3]]}], "deleted": []})
        assert s["parts"] == 1 and Store(cfg).count() == 1, s

        # delete
        s = apply(cfg, {"notes": [], "deleted": ["n.md"]})
        assert s["deleted"] == 1 and Store(cfg).count() == 0, s
        print("ok [agent]: plan emits numbered blocks; apply slices block-ranges, merges, replaces, deletes")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    import json
    import sys

    args = sys.argv[1:]
    if args == ["--selftest"]:
        _selftest()
    elif args == ["--selftest-agent"]:
        _selftest_agent()
    elif args in (["plan"], ["apply"], ["auto"]):
        # RAG is best-effort. reindex is user-invoked: on a config / API / dependency
        # failure, report a clean reason (no traceback) and exit non-zero — the store
        # simply isn't refreshed; search still degrades to plaintext. (`plan` embeds
        # nothing, so it keeps working even with no embedder configured.)
        try:
            if args == ["plan"]:
                print(json.dumps(plan(load_config()), ensure_ascii=False))
            elif args == ["apply"]:
                print(json.dumps(apply(load_config(), json.load(sys.stdin))))
            else:  # auto
                s = reindex(load_config())
                print(f"indexed={s['indexed']} parts={s['parts']} skipped={s['skipped']} deleted={s['deleted']}")
        except Exception as exc:
            print(f"RAG_UNAVAILABLE: {type(exc).__name__}: {exc}")
            print("(store not refreshed — check rag-search config in .env; see SKILL.md 'Availability')")
            sys.exit(1)
    else:
        print("usage: reindex.py plan | apply | auto | --selftest | --selftest-agent")
