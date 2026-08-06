"""Embedding abstraction for the rag-search toolkit.

Two interchangeable implementations behind one `embed(texts) -> vectors` call:

- `MockEmbedder` — deterministic hash-based unit vectors. Offline, no API key;
  the same text always yields the same vector. Used to build and test the whole
  chunk -> store -> search chain before a provider is chosen.
- `APIEmbedder` — any OpenAI-compatible embeddings endpoint (provider set in
  `.env`). The `openai` import is lazy so the mock path never depends on it.

`get_embedder(config)` returns the implementation selected by `EMBED_PROVIDER`.
"""
from __future__ import annotations

import hashlib
import struct
from typing import Protocol

from config import Config


class Embedder(Protocol):
    dim: int

    def embed(self, texts: list[str]) -> list[list[float]]: ...


def _l2_normalize(vec: list[float]) -> list[float]:
    norm = sum(x * x for x in vec) ** 0.5
    if norm == 0.0:
        return vec
    return [x / norm for x in vec]


class MockEmbedder:
    """Deterministic, offline embedder. No real semantics — just a stable,
    correctly shaped unit vector per text so the pipeline can be exercised end
    to end (a text reliably retrieves itself)."""

    def __init__(self, dim: int = 1024):
        self.dim = dim

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._one(t) for t in texts]

    def _one(self, text: str) -> list[float]:
        vec: list[float] = []
        counter = 0
        while len(vec) < self.dim:
            digest = hashlib.sha256(f"{counter}:{text}".encode("utf-8")).digest()
            for i in range(0, len(digest), 4):
                if len(vec) >= self.dim:
                    break
                n = struct.unpack("<I", digest[i : i + 4])[0]
                vec.append(n / 0xFFFFFFFF * 2.0 - 1.0)  # -> [-1, 1]
            counter += 1
        return _l2_normalize(vec)


class APIEmbedder:
    """OpenAI-compatible embeddings endpoint. base_url/api_key/model/dim from `.env`."""

    def __init__(self, base_url, api_key, model, dim, send_dimensions=True):
        if not api_key:
            raise ValueError(
                "APIEmbedder requires EMBED_API_KEY "
                "(set EMBED_PROVIDER=mock to run offline)"
            )
        from openai import OpenAI  # lazy: the mock path must not require openai

        self._client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
        self.dim = dim
        self.send_dimensions = send_dimensions

    def embed(self, texts: list[str]) -> list[list[float]]:
        kwargs = {"model": self.model, "input": texts}
        if self.send_dimensions:
            # Matryoshka: OpenAI v3 models truncate + renormalize to `dimensions`.
            kwargs["dimensions"] = self.dim
        resp = self._client.embeddings.create(**kwargs)
        return [item.embedding for item in resp.data]


def get_embedder(config: Config) -> Embedder:
    if config.embed_provider == "api":
        return APIEmbedder(
            base_url=config.embed_base_url,
            api_key=config.embed_api_key,
            model=config.embed_model,
            dim=config.embed_dim,
            send_dimensions=config.embed_send_dimensions,
        )
    return MockEmbedder(dim=config.embed_dim)


if __name__ == "__main__":
    # Smoke test — offline mock path.
    from config import load_config

    cfg = load_config()
    emb = get_embedder(cfg)
    print(f"provider = {type(emb).__name__}, dim = {emb.dim}")

    a1, a2, b = emb.embed(["hello world", "hello world", "a different note"])
    assert len(a1) == emb.dim, "wrong dimension"
    assert a1 == a2, "not deterministic"
    assert a1 != b, "distinct inputs collided"
    norm = sum(x * x for x in a1) ** 0.5
    assert abs(norm - 1.0) < 1e-6, f"not unit-normalized: {norm}"
    print("ok: deterministic, correct dim, distinct inputs differ, unit-normalized")
