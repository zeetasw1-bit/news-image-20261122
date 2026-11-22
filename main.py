#!/usr/bin/env python3
"""Copy the bundled front-page image to the grader's output directory.

The entry image (entry.png, in this repository) sums up the world's news
of Sunday 22 November 2026. This program only places that image at
/output/entry.png: it is deterministic, uses the standard library only,
touches no network and calls no model. The image itself is drawn by
generate_image.py (Pillow), kept in this repository for reference.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    if not os.path.isfile(SOURCE):
        print("entry.png not found beside main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    print("wrote %s (%d bytes)" % (target, os.path.getsize(target)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
