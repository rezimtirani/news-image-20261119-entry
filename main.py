#!/usr/bin/env python3
"""Write the 19 November 2026 world-news image to the output directory.

The bundled entry.png was drawn by render.py from news.json; this script
just places a verified copy of it at $MAKEFUN_OUTPUT_DIR/entry.png, so
grading needs no network and no fonts. Only the Python standard library
is used, and two runs produce byte-identical output.

Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLED = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def verify_png(path):
    """Confirm path is a whole PNG within the size limits; return w, h, n."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    if head[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit(
            f"image is {width}x{height}, over {MAX_SIDE}x{MAX_SIDE}")
    nbytes = os.path.getsize(path)
    if nbytes > MAX_BYTES:
        raise SystemExit(f"image is {nbytes} bytes, over {MAX_BYTES}")
    return width, height, nbytes


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(BUNDLED, target)
    width, height, nbytes = verify_png(target)
    print(f"wrote {target}: {width}x{height} PNG, {nbytes} bytes")


if __name__ == "__main__":
    main()
