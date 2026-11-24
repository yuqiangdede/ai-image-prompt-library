import hashlib
import tempfile
import unittest
from pathlib import Path

from PIL import Image
from scripts.image_variants import image_variants, SIZES


class ImageVariantTests(unittest.TestCase):
    def test_variants_and_cache_preserve_original(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "cover.png"
            Image.new("RGBA", (1200, 800), (30, 60, 90, 100)).save(source)
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            dist, cache = root / "dist", root / "cache"
            variants = image_variants("cover.png", root, dist, cache)
            self.assertEqual(set(variants), {str(size) for size in SIZES})
            for size in SIZES:
                with Image.open(dist / variants[str(size)]) as img:
                    self.assertEqual(img.format, "WEBP")
                    self.assertEqual(max(img.size), size)
                    self.assertEqual(img.mode, "RGBA")
                    self.assertAlmostEqual(img.width / img.height, 1.5, delta=0.02)
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), digest)
            second = image_variants("cover.png", root, root / "other", cache)
            self.assertEqual(variants, second)
            self.assertTrue(all((root / "other" / path).is_file() for path in second.values()))

    def test_external_and_animated_are_not_mirrored(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(image_variants("https://example.com/a.png", root, root / "dist", root / "cache"), {})
            frames = [Image.new("RGB", (20, 20), color) for color in ("red", "blue")]
            frames[0].save(root / "animated.gif", save_all=True, append_images=frames[1:], duration=100, loop=0)
            self.assertEqual(image_variants("animated.gif", root, root / "dist", root / "cache"), {})


if __name__ == "__main__":
    unittest.main()
