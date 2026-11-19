#!/usr/bin/env python3
"""Entrypoint: write the 19 November 2026 world-news image to the output dir.

The image (entry.png, rendered from news.json by render.py) is bundled in
this repository, so the program needs no network at grade time. It copies
the file to $MAKEFUN_OUTPUT_DIR/entry.png (default /output), then verifies
the copy: PNG magic, at most 1024x1024 pixels, at most 1 MiB. Standard
library only; deterministic -- two runs write identical bytes.

Run locally: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576
MAX_DIM = 1024


def check_png(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    if head[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        raise SystemExit(f"image is {width}x{height}, over {MAX_DIM}x{MAX_DIM}")
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit(f"image is {size} bytes, over {MAX_BYTES}")
    return width, height, size


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    width, height, size = check_png(dst)
    print(f"wrote {dst}: {width}x{height} PNG, {size} bytes")


if __name__ == "__main__":
    main()
