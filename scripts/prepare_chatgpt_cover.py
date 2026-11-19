#!/usr/bin/env python3
"""Prepare an image for the gallery's GitHub Git Data API upload.

Outputs an unresized WebP, a line-wrapped Base64 text bridge, and a JSON
manifest containing the expected Git blob SHA-1. Requires Pillow for image
conversion (pip install Pillow). Does not connect to GitHub or upload files.

Example:
    python scripts/prepare_chatgpt_cover.py \
      /path/to/generated-image.png \
      --output /tmp/gallery-upload/cover.webp
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import shutil
import textwrap


def git_blob_sha(data: bytes) -> str:
    """Git's blob-object SHA-1, not the ordinary SHA-1 of file bytes."""
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def prepare(source: Path, output: Path, quality: int, line_width: int) -> dict:
    if not source.is_file():
        raise FileNotFoundError(f"Source image not found: {source}")
    if line_width < 4 or line_width % 4:
        raise ValueError("--line-width must be a positive multiple of 4")
    if not 1 <= quality <= 100:
        raise ValueError("--quality must be between 1 and 100")
    if source.resolve() == output.resolve():
        raise ValueError("--output must differ from the source image")

    try:
        from PIL import Image, ImageOps
    except ImportError as exc:
        raise SystemExit("Pillow required: python -m pip install Pillow") from exc

    output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as raw:
        corrected = ImageOps.exif_transpose(raw)
        size_before = corrected.size
        if source.suffix.lower() == ".webp":
            # Preserve existing WebP bytes when they already meet requirements.
            shutil.copyfile(source, output)
        else:
            has_alpha = "A" in corrected.getbands() or "transparency" in corrected.info
            corrected = corrected.convert("RGBA" if has_alpha else "RGB")
            corrected.save(output, format="WEBP", quality=quality, method=6)

    with Image.open(output) as image:
        size_after = image.size
        if image.format != "WEBP":
            raise ValueError("Output is not a valid WebP image")
    if size_before != size_after:
        raise ValueError(f"Pixel dimensions changed: {size_before} -> {size_after}")

    data = output.read_bytes()
    size_limit = 8 * 1024 * 1024
    if not data or len(data) > size_limit:
        raise ValueError(f"WebP is empty or exceeds 8 MiB: {len(data)} bytes")

    encoded = base64.b64encode(data).decode("ascii")
    bridge_path = output.with_name(output.name + ".b64.txt")
    bridge_lines = textwrap.wrap(encoded, width=line_width)
    bridge_path.write_text("\n".join(bridge_lines) + "\n", encoding="ascii")
    # Re-read and verify that the bridge, not merely the source bytes, is intact.
    rebuilt = base64.b64decode("".join(bridge_path.read_text(encoding="ascii").split()), validate=True)
    if rebuilt != data:
        raise ValueError("Base64 bridge round-trip failed")

    manifest = {
        "source_path": str(source),
        "webp_path": str(output),
        "bridge_path": str(bridge_path),
        "width": size_after[0],
        "height": size_after[1],
        "webp_bytes": len(data),
        "base64_chars": len(encoded),
        "base64_lines": len(bridge_lines),
        "git_blob_sha1": git_blob_sha(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    manifest_path = output.with_name(output.name + ".manifest.json")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="PNG, JPEG or WebP source image")
    parser.add_argument("--output", type=Path, required=True, help="Destination WebP path")
    parser.add_argument("--quality", type=int, default=93, help="WebP quality, default 93")
    parser.add_argument("--line-width", type=int, default=960, help="Base64 chars per line (multiple of 4)")
    args = parser.parse_args()
    result = prepare(args.source, args.output, args.quality, args.line_width)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
