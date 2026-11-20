#!/usr/bin/env python3
"""Entry point for news-image-20261120, variant C 'Timeline + Proof'.

Pure-stdlib byte relay: copies the committed entry.png (drawn with PIL by
draw.py at build time) into $MAKEFUN_OUTPUT_DIR. No PIL import, no network,
no randomness — two runs produce byte-identical output.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(HERE, "output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        print("error: entry.png missing next to main.py", file=sys.stderr)
        return 1
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
