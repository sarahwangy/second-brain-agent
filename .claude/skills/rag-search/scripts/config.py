"""Central configuration for the rag-search toolkit.

Single source of truth for: embedding provider settings, project/vault paths,
and the (gitignored) LanceDB store location. Values come from the project-root
`.env` (see `.env.example`); sane defaults keep the offline mock path working
with no `.env` present at all.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# scripts/ -> rag-search/ -> skills/ -> .claude/ -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[4]

load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Config:
    # --- embedding ---
    embed_provider: str        # "mock" (offline, default) | "api" (OpenAI-compatible)
    embed_base_url: str | None
    embed_api_key: str | None
    embed_model: str
    embed_dim: int
    embed_send_dimensions: bool   # send embed_dim as the API `dimensions` param (Matryoshka)
    # --- paths ---
    project_root: Path
    vault_root: Path           # the Obsidian vault == project root
    store_dir: Path            # gitignored LanceDB store
    # --- vault scan (which .md files count as knowledge notes) ---
    exclude_dirs: frozenset[str]    # directory names never indexed
    exclude_files: frozenset[str]   # project meta docs, not knowledge notes
    # --- search ---
    search_top_k: int               # how many part-level hits search returns
    search_max_rounds: int          # max agentic retrieval rounds before the agent must stop


def load_config() -> Config:
    return Config(
        embed_provider=os.getenv("EMBED_PROVIDER", "mock").strip().lower(),
        embed_base_url=os.getenv("EMBED_BASE_URL") or None,
        embed_api_key=os.getenv("EMBED_API_KEY") or None,
        embed_model=os.getenv("EMBED_MODEL", "BAAI/bge-m3"),
        embed_dim=int(os.getenv("EMBED_DIM", "1024")),
        embed_send_dimensions=os.getenv("EMBED_SEND_DIMENSIONS", "true").strip().lower() == "true",
        project_root=PROJECT_ROOT,
        vault_root=PROJECT_ROOT,
        store_dir=PROJECT_ROOT / ".rag-index",
        exclude_dirs=frozenset({
            ".git", ".claude", ".venv", ".obsidian", ".rag-index",
            ".import-staging", "Templates", "Sources", "user_level_file_template",
        }),
        exclude_files=frozenset({"CLAUDE.md", "README.md", "IMPLEMENTATION_PLAN.md", "WORKSHOP_PRESETUP.md"}),
        search_top_k=int(os.getenv("SEARCH_TOP_K", "5")),
        search_max_rounds=int(os.getenv("SEARCH_MAX_ROUNDS", "3")),
    )


if __name__ == "__main__":
    cfg = load_config()
    for field in cfg.__dataclass_fields__:
        value = getattr(cfg, field)
        if field == "embed_api_key" and value:
            value = "***set***"
        print(f"{field:16} = {value}")
