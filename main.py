#!/usr/bin/env python3
# main.py — entrypoint for the news-image-20261125 entry.
#
# The graded artefact is the newspaper front page entry.png (1024 by
# 1024 pixels, six stories from Wednesday 25 November 2026). The picture
# was rendered locally by draw_entry.py; this script only places a copy
# of it where the grader expects it, using nothing but the standard
# library, so it runs the same in any container.
#
# Run it with MAKEFUN_OUTPUT_DIR pointing at the output folder:
#     MAKEFUN_OUTPUT_DIR=out python3 main.py
from os import environ
from pathlib import Path

PICTURE = Path(__file__).resolve().parent / "entry.png"
FALLBACK_DIR = "/output"


def place_picture() -> int:
    """Copy entry.png into the output directory; 1 when it is missing."""
    destination_root = Path(environ.get("MAKEFUN_OUTPUT_DIR") or FALLBACK_DIR)
    if not PICTURE.is_file():
        print(f"entry image not found: {PICTURE}")
        return 1
    destination_root.mkdir(parents=True, exist_ok=True)
    target = destination_root / PICTURE.name
    target.write_bytes(PICTURE.read_bytes())
    return 0


if __name__ == "__main__":
    raise SystemExit(place_picture())
