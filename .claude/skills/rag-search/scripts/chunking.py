"""Chunking for the rag-search reindex. Two stages:

  (a) THIS FILE's structural parse — `parse_blocks` splits a note into leaf
      structural blocks (frontmatter, heading, list_item, paragraph, code,
      blockquote), each a verbatim line range. Deterministic, zero-LLM. It gives
      stage (b) a stable anchor system (line ranges) to point at.

  (b) agent-semantic step (later) — an agent reads the note + these blocks and
      returns part boundaries (which blocks merge into one part). It outputs only
      boundaries; Python slices each part's text verbatim. Until that lands,
      `naive_parts` is a placeholder that groups blocks by H1/H2/H3 section so the
      rest of the pipeline can run.

Nothing here rewrites note text. Blocks and parts carry verbatim line-range
slices of the source — the mechanism behind `agent != author`.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+\S")
_FENCE_RE = re.compile(r"^\s*(```+|~~~+)")


@dataclass
class Block:
    index: int
    type: str                       # frontmatter | heading | list_item | paragraph | code | blockquote
    start_line: int                 # 0-based, inclusive
    end_line: int                   # 0-based, inclusive
    text: str                       # verbatim source (line-range slice)
    heading_level: int | None = None
    title: str | None = None        # heading text without the leading '#'s
    section: str = ""               # nearest enclosing heading title (context/display)


@dataclass
class Part:
    text: str                       # verbatim line-range slice (key + payload)
    start_line: int
    end_line: int
    heading: str


def _slice(lines: list[str], start: int, end: int) -> str:
    return "\n".join(lines[start : end + 1])


def parse_blocks(markdown: str) -> list[Block]:
    lines = markdown.split("\n")
    n = len(lines)
    blocks: list[Block] = []
    section = ""
    i = 0

    def emit(btype: str, start: int, end: int, level=None, title=None) -> None:
        blocks.append(
            Block(
                index=len(blocks),
                type=btype,
                start_line=start,
                end_line=end,
                text=_slice(lines, start, end),
                heading_level=level,
                title=title,
                section=section,
            )
        )

    # frontmatter: file opens with --- ... ---
    if n > 0 and lines[0].strip() == "---":
        j = 1
        while j < n and lines[j].strip() != "---":
            j += 1
        if j < n:  # closing fence found
            emit("frontmatter", 0, j)
            i = j + 1

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if stripped == "":
            i += 1
            continue

        # code fence — its interior is opaque (a '#' inside is not a heading)
        m = _FENCE_RE.match(line)
        if m:
            fence = m.group(1)[0] * 3
            j = i + 1
            while j < n and not lines[j].lstrip().startswith(fence):
                j += 1
            end = j if j < n else n - 1
            emit("code", i, end)
            i = end + 1
            continue

        # heading
        m = _HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            emit("heading", i, i, level=level, title=title)
            section = title
            i += 1
            continue

        # blockquote (callouts included)
        if stripped.startswith(">"):
            j = i
            while j < n and lines[j].strip().startswith(">"):
                j += 1
            emit("blockquote", i, j - 1)
            i = j
            continue

        # list item — one block per item (continuation lines fold in)
        if _LIST_RE.match(line):
            j = i + 1
            while j < n:
                nxt = lines[j]
                if nxt.strip() == "":
                    break
                if _LIST_RE.match(nxt) or _HEADING_RE.match(nxt) or _FENCE_RE.match(nxt):
                    break
                j += 1
            emit("list_item", i, j - 1)
            i = j
            continue

        # paragraph — consecutive non-blank lines until a structural edge
        j = i
        while j < n:
            nxt = lines[j]
            if nxt.strip() == "":
                break
            if j > i and (_HEADING_RE.match(nxt) or _LIST_RE.match(nxt) or _FENCE_RE.match(nxt)):
                break
            j += 1
        emit("paragraph", i, j - 1)
        i = j

    return blocks


def naive_parts(blocks: list[Block], markdown: str) -> list[Part]:
    """Stage-(b) placeholder: group blocks by H1/H2/H3 section. Frontmatter is
    excluded (metadata, not content). Replaced by the agent-semantic chunker."""
    lines = markdown.split("\n")
    parts: list[Part] = []
    current: list[Block] = []

    def flush() -> None:
        if not current:
            return
        start, end = current[0].start_line, current[-1].end_line
        text = _slice(lines, start, end)
        if text.strip():
            first = current[0]
            heading = first.title if first.type == "heading" else first.section
            parts.append(Part(text=text, start_line=start, end_line=end, heading=heading or ""))
        current.clear()

    for b in blocks:
        if b.type == "frontmatter":
            continue
        if b.type == "heading" and b.heading_level is not None and b.heading_level <= 3:
            flush()
        current.append(b)
    flush()
    return parts


if __name__ == "__main__":
    sample = """---
type: note
---

# My Title

> **Purpose**: test note.

## Section One

Some paragraph here.
Second line of it.

## Ideas

- idea alpha with substance
- idea beta, a different direction

## Code

```python
# this is code, not a heading
x = 1
```
"""
    blocks = parse_blocks(sample)
    print("=== blocks ===")
    for b in blocks:
        label = b.title if b.title else ""
        print(f"[{b.index}] {b.type:11} L{b.start_line}-{b.end_line} {label}")

    # frontmatter detected
    assert blocks[0].type == "frontmatter", "frontmatter not detected"
    # code-fence interior is not parsed as a heading
    assert all(b.title != "this is code, not a heading" for b in blocks), "parsed code as heading"
    assert any(b.type == "code" for b in blocks), "code block missing"
    # headings and levels
    titles = {b.title: b.heading_level for b in blocks if b.type == "heading"}
    assert titles.get("My Title") == 1 and titles.get("Ideas") == 2, "heading levels wrong"
    # list items split
    assert sum(1 for b in blocks if b.type == "list_item") == 2, "list items not split"

    parts = naive_parts(blocks, sample)
    print("\n=== naive parts ===")
    for p in parts:
        print(f"L{p.start_line}-{p.end_line} [{p.heading}] :: {p.text[:40]!r}")

    assert len(parts) == 4, f"expected 4 parts, got {len(parts)}"
    assert parts[0].heading == "My Title", "preamble part heading wrong"
    assert any(p.heading == "Ideas" for p in parts), "Ideas part missing"
    # verbatim: every part is a contiguous substring of the source
    assert all(p.text in sample for p in parts), "a part is not a verbatim slice"
    assert any("# this is code" in p.text for p in parts), "code content not preserved"
    print("\nok: frontmatter + code-fence safe, headings/lists parsed, parts are verbatim slices")
