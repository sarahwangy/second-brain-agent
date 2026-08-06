#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["youtube-transcript-api"]
# ///
"""Fetch a YouTube transcript by URL or video ID and print it.

Run via uv (auto-installs the dependency from the inline metadata above):

    uv run fetch_transcript.py "<youtube-url-or-id>" [--languages en,zh] [--timestamps] [--json]

Output: plain transcript text on stdout (one snippet per line). On failure,
a clear message on stderr and a non-zero exit code — never partial garbage.
"""
import argparse
import json
import re
import sys

_ID_RE = re.compile(r"[0-9A-Za-z_-]{11}")
_URL_PATTERNS = [
    re.compile(r"(?:v=|/v/|/embed/|/shorts/|/live/|youtu\.be/)([0-9A-Za-z_-]{11})"),
]


def extract_video_id(s: str):
    """Return an 11-char video ID from a raw ID or any common YouTube URL form."""
    s = s.strip()
    if _ID_RE.fullmatch(s):
        return s
    for pat in _URL_PATTERNS:
        m = pat.search(s)
        if m:
            return m.group(1)
    return None


def _to_raw(fetched):
    """Normalize a fetched transcript (v1.x object, legacy list, or iterable) to dicts."""
    if hasattr(fetched, "to_raw_data"):
        return fetched.to_raw_data()
    if isinstance(fetched, list):
        return fetched
    return [{"text": s.text, "start": s.start, "duration": s.duration} for s in fetched]


def get_snippets(video_id: str, languages):
    """Fetch transcript snippets, working across youtube-transcript-api v0.x and v1.x."""
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    if hasattr(api, "fetch"):  # v1.x instance API
        try:
            return _to_raw(api.fetch(video_id, languages=languages))
        except Exception:
            for t in api.list(video_id):  # fall back to any available language
                return _to_raw(t.fetch())
            raise
    # legacy <1.0 static API
    try:
        return YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
    except Exception:
        for t in YouTubeTranscriptApi.list_transcripts(video_id):
            return _to_raw(t.fetch())
        raise


def main():
    ap = argparse.ArgumentParser(description="Fetch a YouTube transcript by URL or video ID.")
    ap.add_argument("url", help="YouTube URL or 11-character video ID")
    ap.add_argument("--languages", default="en",
                    help="comma-separated preferred languages, in order (default: en); falls back to any available")
    ap.add_argument("--timestamps", action="store_true", help="prefix each line with [mm:ss]")
    ap.add_argument("--json", action="store_true", help="emit raw JSON snippets (text/start/duration)")
    args = ap.parse_args()

    video_id = extract_video_id(args.url)
    if not video_id:
        print(f"error: could not extract a video ID from: {args.url}", file=sys.stderr)
        sys.exit(2)

    languages = [x.strip() for x in args.languages.split(",") if x.strip()] or ["en"]
    try:
        snippets = get_snippets(video_id, languages)
    except Exception as e:
        print(f"error: failed to fetch transcript for {video_id}: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps({"video_id": video_id, "snippets": snippets}, ensure_ascii=False, indent=2))
        return

    out = []
    for sn in snippets:
        text = str(sn["text"]).replace("\n", " ").strip()
        if not text:
            continue
        if args.timestamps:
            start = int(sn.get("start", 0))
            out.append(f"[{start // 60:02d}:{start % 60:02d}] {text}")
        else:
            out.append(text)
    print("\n".join(out))


if __name__ == "__main__":
    main()
