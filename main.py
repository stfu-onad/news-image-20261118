#!/usr/bin/env python3
"""news-image-20261118 — reproduce the front page for 18 November 2026.

The artwork (a one-page newspaper front page, 1024x1024 JPEG) is stored
next to this file as entry.png. Running this script copies it verbatim
into the output directory and then checks, using only the Python
standard library, that the copy is a complete, well-formed JPEG of the
expected size. No pixels are generated or altered here: the point of
the program is a byte-for-byte, deterministic reproduction.

Usage:
    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT = os.path.join(OUTPUT_DIR, "entry.png")

EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_FILE_SIZE = 1_048_576  # 1 MiB, the competition limit


def read_jpeg_dimensions(path):
    """Return (width, height) by scanning JPEG markers for the SOF frame.

    Walks the marker stream until a Start-Of-Frame marker (baseline,
    extended sequential, or progressive) is found, then reads the
    height and width stored there. Raises ValueError on malformed data.
    """
    with open(path, "rb") as handle:
        blob = handle.read()

    if len(blob) < 4 or blob[0] != 0xFF or blob[1] != 0xD8:
        raise ValueError("not a JPEG: missing SOI marker (FF D8)")

    # A complete JPEG ends with the EOI marker FF D9.
    if blob[-2] != 0xFF or blob[-1] != 0xD9:
        raise ValueError("not a complete JPEG: missing EOI marker (FF D9)")

    pos = 2  # just past SOI
    while pos + 1 < len(blob):
        if blob[pos] != 0xFF:
            raise ValueError("bad marker prefix at offset %d" % pos)
        marker = blob[pos + 1]
        # Skip padding 0xFF bytes and stuffed 0x00 bytes.
        while marker == 0xFF:
            pos += 1
            marker = blob[pos + 1]
        if marker == 0x00 or marker == 0x01:
            pos += 2
            continue
        # Standalone markers carry no length field.
        if marker == 0xD8 or 0xD0 <= marker <= 0xD9:
            pos += 2
            continue
        if pos + 4 > len(blob):
            raise ValueError("truncated segment header")
        length = struct.unpack(">H", blob[pos + 2:pos + 4])[0]
        if length < 2 or pos + 2 + length > len(blob):
            raise ValueError("truncated segment at marker FF %02X" % marker)
        # SOF0 (baseline), SOF1 (extended), SOF2 (progressive).
        if marker in (0xC0, 0xC1, 0xC2):
            payload = blob[pos + 4:pos + 2 + length]
            if len(payload) < 5:
                raise ValueError("truncated SOF segment")
            height = struct.unpack(">H", payload[1:3])[0]
            width = struct.unpack(">H", payload[3:5])[0]
            return width, height
        pos += 2 + length

    raise ValueError("no SOF marker found; cannot determine dimensions")


def main():
    if not os.path.isfile(SOURCE):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1

    # Sanity-check the artwork itself before copying anything.
    src_width, src_height = read_jpeg_dimensions(SOURCE)
    assert (src_width, src_height) == (EXPECTED_WIDTH, EXPECTED_HEIGHT), (
        "source is %dx%d, expected %dx%d"
        % (src_width, src_height, EXPECTED_WIDTH, EXPECTED_HEIGHT)
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)

    # Determinism: the copy must be byte-identical to the source.
    with open(SOURCE, "rb") as handle:
        source_bytes = handle.read()
    with open(OUTPUT, "rb") as handle:
        output_bytes = handle.read()
    assert source_bytes == output_bytes, "output differs from entry.png"

    # Integrity: valid JPEG markers, expected dimensions, size limit.
    width, height = read_jpeg_dimensions(OUTPUT)
    assert (width, height) == (EXPECTED_WIDTH, EXPECTED_HEIGHT), (
        "unexpected dimensions %dx%d" % (width, height)
    )
    size = len(output_bytes)
    assert size <= MAX_FILE_SIZE, "output %d bytes exceeds 1 MiB" % size

    print("wrote %s (%d bytes, %dx%d JPEG)" % (OUTPUT, size, width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
