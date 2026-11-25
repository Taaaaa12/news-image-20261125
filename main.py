#!/usr/bin/env python3
"""Entry program: copy the bundled front-page image to /output/entry.png.

Standard library only. Deterministic: writes the same bytes every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT)


if __name__ == "__main__":
    main()
