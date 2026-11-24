"""Generate content-addressed WebP display images; never modify originals."""
import hashlib
import os
import shutil
from pathlib import Path

from PIL import Image, ImageOps

SIZES = (160, 320, 640, 1080)
VERSION = "webp-v1-q82"


def image_variants(path, root, dist, cache):
    if not path or path.startswith("https://"):
        return {}
    source = root / path
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    result = {}
    try:
        with Image.open(source) as original:
            # Keep animated GIF/WebP behavior rather than silently flatten it.
            if getattr(original, "is_animated", False):
                return {}
            for size in SIZES:
                filename = f"{digest}-{VERSION}-{size}.webp"
                relative = Path("thumbnails") / filename
                target = dist / relative
                cached = cache / filename
                if not cached.is_file():
                    image = ImageOps.exif_transpose(original)
                    image = image.convert("RGBA" if "A" in image.getbands() or "transparency" in image.info else "RGB")
                    image.thumbnail((size, size), Image.Resampling.LANCZOS)
                    cached.parent.mkdir(parents=True, exist_ok=True)
                    tmp = cached.with_suffix(".tmp")
                    image.save(tmp, "WEBP", quality=82, method=4)
                    os.replace(tmp, cached)
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists():
                    shutil.copyfile(cached, target)
                result[str(size)] = relative.as_posix()
    except (OSError, ValueError, Image.DecompressionBombError) as exc:
        print(f"WARN: display image fallback for {path}: {exc}")
    return result
