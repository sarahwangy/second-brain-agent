# Notion → Obsidian block mapping

Lookup for normalizing Notion block JSON (from `API-get-block-children`) into clean Obsidian
markdown. Load this during step 2 of the skill. Goal: faithful migration of the user's content —
preserve text verbatim, drop Notion-only chrome that has no Obsidian equivalent.

## Block types

| Notion `type` | Obsidian markdown | Notes |
|---|---|---|
| `paragraph` | plain paragraph | Blank line between blocks. |
| `heading_1` / `heading_2` / `heading_3` | `#` / `##` / `###` | Obsidian has only 6 levels; map 1:1. |
| `bulleted_list_item` | `- item` | Indent 2 spaces per nesting level (recurse `has_children`). |
| `numbered_list_item` | `1. item` | Markdown auto-numbers; emit `1.` for each. |
| `to_do` | `- [ ]` / `- [x]` | `checked: true` → `[x]`. |
| `toggle` | `> [!note]- Title` foldable callout | Toggle title = callout title; children = callout body. |
| `quote` | `> text` | |
| `callout` | `> [!note] text` | Map the emoji/icon to a callout type loosely (info/tip/warning); default `note`. Drop color. |
| `code` | ` ```lang … ``` ` | Use the block's `language`; fall back to no language. |
| `divider` | `---` | |
| `equation` (block) | `$$ … $$` | Obsidian renders LaTeX. |
| `table` + `table_row` | markdown table | First row = header if `has_column_header`. Escape `\|` in cells. |
| `image` | `![alt](url)` | **Caveat below** — Notion-hosted URLs expire. |
| `file` / `pdf` / `video` / `audio` | `[name](url)` link | Same expiry caveat; download to `Sources/` if persistence matters. |
| `bookmark` / `link_preview` / `embed` | `[title](url)` | Use caption/url as link text. |
| `child_page` | `[[Page Title]]` + queue as separate note | Handled by workflow step 2/4 — one note per page. |
| `child_database` | best-effort list of `[[row]]` links | **Limitation below** — flag to user. |
| `column_list` / `column` | flatten to sequential blocks | Obsidian has no columns; render top-to-bottom. |
| `synced_block` | inline its resolved children | Render the source content once. |
| `table_of_contents` / `breadcrumb` | drop | Navigation chrome; no equivalent. |
| `unsupported` / unknown | drop, and note it in the import summary | Never fabricate content for a block you can't read. |

## Rich-text inline formatting

Within any block's `rich_text` array, map `annotations`:

| Notion annotation | Obsidian | Notes |
|---|---|---|
| `bold` | `**text**` | |
| `italic` | `*text*` | |
| `strikethrough` | `~~text~~` | |
| `code` | `` `text` `` | |
| `link` (`text.link.url`) | `[text](url)` | |
| `underline` | leave as plain text | No native Obsidian underline; do not inject HTML. |
| `color` | leave as plain text | Drop — no proactive structure/styling. |

## Mentions (inside `rich_text`)

| Mention type | Obsidian | Notes |
|---|---|---|
| page mention | `[[Page Title]]` | Resolve to that page's mapped note title from the manifest. Stub link is fine if the page is out of scope. |
| database mention | `[[Database Title]]` or plain text | Per `linking.md` substance judgment. |
| user mention | plain text name | No vault representation for people unless a note exists. |
| date mention | plain text date | Do not invent a property/frontmatter field. |

**Language fidelity for links.** Never translate mention text. Link to the target note's
own-language title; for readability across languages an alias is fine: `[[Context Management|上下文管理]]`.

## Caveats — surface these to the user

- **Expiring media URLs.** Notion-hosted `image`/`file` URLs are signed and expire (~1h). For a
  durable migration, download referenced media into `Sources/` (gitignored, vault-synced) and
  embed with `![[Sources/...]]`. If skipped, note that media links will rot.
- **Inline databases (`child_database`).** A Notion database is structured rows + properties with no
  clean atomic-note equivalent. Do not silently flatten a large database into prose. Flag it at
  review time and let the user decide (skip, link out, or handle separately).
- **Lost styling is intentional.** Colors, backgrounds, and column layouts are dropped by design —
  the vault stores meaning as wikilinked atomic notes, not Notion's visual structure.
