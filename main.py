"""Copy the bundled news image to the grader's output folder.

The entry image already lives in this repository as entry.png, next to
this script. The grader runs this program with no network, the repo
mounted read-only, and a writable output directory. This script finds
that directory from MAKEFUN_OUTPUT_DIR (falling back to /output),
duplicates entry.png there byte for byte, and refuses to finish
silently if the copy comes out a different size.
"""

import os
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
DEST_NAME = "entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
CHUNK_SIZE = 1024 * 64


def locate_source() -> Path:
    here = Path(__file__).resolve().parent
    candidate = here / SOURCE_NAME
    if not candidate.is_file():
        raise SystemExit(f"missing source image: {candidate}")
    return candidate


def locate_destination() -> Path:
    raw_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    folder = Path(raw_dir).expanduser()
    folder.mkdir(parents=True, exist_ok=True)
    return folder / DEST_NAME


def duplicate(source: Path, target: Path) -> int:
    total = 0
    with source.open("rb") as reader, target.open("wb") as writer:
        head = reader.read(len(PNG_SIGNATURE))
        if head != PNG_SIGNATURE:
            raise SystemExit("source image is not a PNG file")
        writer.write(head)
        total += len(head)
        while True:
            block = reader.read(CHUNK_SIZE)
            if not block:
                break
            writer.write(block)
            total += len(block)
    if target.stat().st_size != source.stat().st_size:
        target.unlink(missing_ok=True)
        raise SystemExit("copied file size does not match the source")
    return total


def main() -> int:
    source = locate_source()
    target = locate_destination()
    copied = duplicate(source, target)
    print(f"wrote {target} ({copied} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
