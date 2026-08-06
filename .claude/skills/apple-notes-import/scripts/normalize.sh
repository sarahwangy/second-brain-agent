#!/usr/bin/env bash
# normalize.sh — deterministic HTML -> markdown pass for apple-notes-import.
#
# Converts every <outDir>/raw/<index>.html dumped by dump_notes.applescript into
# <outDir>/md/<index>.md using pandoc. This is the *format* layer only; all semantic
# judgment (four-actions, SSOT, wikilinks, templates) stays with the agent afterward.
#
# pandoc flags:
#   -f html           source is Apple Notes' HTML body
#   -t gfm-raw_html   GitHub-flavored markdown (closest to Obsidian); drop un-convertible raw HTML
#                     instead of passing it through, so notes don't carry stray <div>/<span> tags
#   --wrap=none       never hard-wrap — preserve the user's words on single logical lines
#
# Usage:  normalize.sh <absolute-output-dir>
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "usage: normalize.sh <absolute-output-dir>" >&2
  exit 2
fi
STAGING="$1"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "ERROR: pandoc not found on PATH. Install it (brew install pandoc) before importing." >&2
  exit 3
fi

mkdir -p "$STAGING/md"

shopt -s nullglob
count=0
for html in "$STAGING"/raw/*.html; do
  base="$(basename "$html" .html)"
  pandoc -f html -t gfm-raw_html --wrap=none "$html" -o "$STAGING/md/$base.md"
  count=$((count + 1))
done

echo "normalized $count note(s) -> $STAGING/md"
