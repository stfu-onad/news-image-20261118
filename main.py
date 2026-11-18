#!/usr/bin/env python3
"""Reproduce the front page for 18 November 2026.

This script ships a one-page newspaper front page as a 1024x1024 JPEG
(287,874 bytes) stored next to the script as ``entry.png``.  It copies
that file verbatim into the output directory and verifies it using
only the Python standard library.

The v2 front page is THE WORLD TODAY, Wednesday 18 November 2026:

The copy is deterministic: the same source bytes always produce the
same byte-identical output file, so re-running the script is safe.

* Lead story -- GULF IN FLAMES: US jets hit an Iranian missile site
  on Qeshm; Iran drones Bahrain and Kuwait.
* Second row -- NVIDIA $115.8B up 103% (a record quarter, with a
  $130B guide) and XI AND PUTIN MEET IN SHENZHEN ahead of Thursday's
  trilateral summit with Trump.
* Footer "Also Today" strip: Kerch Bridge span falls, Peltola wins
  Alaska 56-44, Ebola passes 11,000 cases, the US loses measles-free
  status, Voyager 1 reaches one light-day from Earth, and OpenAI
  launches GPT-6.2.

Usage::

    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys

EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1_048_576  # 1 MiB

# JPEG markers we care about while scanning the header.
SOI = b"\xff\xd8"          # Start Of Image
EOI = b"\xff\xd9"          # End Of Image
SOF_MARKERS = {0xC0, 0xC1, 0xC2}  # baseline / extended / progressive


def fail(message):
    """Print an error to stderr and exit non-zero."""
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def read_dimensions(data):
    """Walk JPEG markers and return (height, width) from the SOF segment.

    Raises ValueError when no Start-Of-Frame segment is found or the
    marker stream is malformed.
    """
    if not data.startswith(SOI):
        raise ValueError("file does not start with JPEG SOI bytes (FF D8)")
    if not data.endswith(EOI):
        raise ValueError("file does not end with JPEG EOI bytes (FF D9)")

    pos = 2  # skip the SOI marker
    while pos + 1 < len(data):
        if data[pos] != 0xFF:
            raise ValueError(f"expected marker prefix 0xFF at offset {pos}")
        marker = data[pos + 1]
        # Skip padding / fill bytes (0xFF repeats) and the standalone
        # restart markers, which carry no length field.
        if marker == 0xFF:
            pos += 1
            continue
        if marker == 0x00 or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        if marker == 0xD8:  # another SOI; shouldn't happen, but skip it
            pos += 2
            continue
        if marker == 0xD9:  # EOI reached without seeing an SOF
            break
        if pos + 4 > len(data):
            raise ValueError("truncated JPEG segment header")
        seg_len = int.from_bytes(data[pos + 2:pos + 4], "big")
        if seg_len < 2 or pos + 2 + seg_len > len(data):
            raise ValueError("JPEG segment length out of bounds")
        if marker in SOF_MARKERS:
            body = data[pos + 4:pos + 2 + seg_len]
            if len(body) < 5:
                raise ValueError("SOF segment too short to hold dimensions")
            height = int.from_bytes(body[1:3], "big")
            width = int.from_bytes(body[3:5], "big")
            return height, width
        pos += 2 + seg_len
    raise ValueError("no Start-Of-Frame (C0/C1/C2) marker found")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, "entry.png")

    try:
        with open(source, "rb") as handle:
            payload = handle.read()
    except OSError as exc:
        fail(f"cannot read source image {source}: {exc}")

    if len(payload) > MAX_BYTES:
        fail(f"source image is {len(payload)} bytes, over the 1 MiB limit")

    try:
        height, width = read_dimensions(payload)
    except ValueError as exc:
        fail(f"source image failed JPEG validation: {exc}")

    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail(
            f"source image is {width}x{height}, "
            f"expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )

    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(target, "wb") as handle:
            handle.write(payload)
    except OSError as exc:
        fail(f"cannot write output image {target}: {exc}")

    # Re-read the copy and confirm it is identical to the source.
    try:
        with open(target, "rb") as handle:
            copied = handle.read()
    except OSError as exc:
        fail(f"cannot re-read output image {target}: {exc}")

    if copied != payload:
        fail("output image differs from the source image")
    try:
        check_h, check_w = read_dimensions(copied)
    except ValueError as exc:
        fail(f"output image failed JPEG validation: {exc}")
    if (check_w, check_h) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail(f"output image is {check_w}x{check_h}, expected 1024x1024")

    print(f"Wrote {target} ({len(copied)} bytes, {check_w}x{check_h} JPEG)")


if __name__ == "__main__":
    main()
