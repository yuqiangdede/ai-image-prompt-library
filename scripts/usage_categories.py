"""Canonical, mutually exclusive gallery usage tags."""
import json
import re
from pathlib import Path

GENERATION = "生图类"
OPTIMIZATION = "优化类"
USAGE_TAGS = (GENERATION, OPTIMIZATION)
ROOT = Path(__file__).resolve().parents[1]

# Reviewed existing reference-image workflows. Pure text prompts are not
# optimization merely because their example looks like a photograph.
OPTIMIZATION_SLUGS = frozenset("""
autumn-1970s-cinematic-fashion-portrait basketball-stands-broadcast-candid
battlefield-assault-pencil-storyboard black-and-white-editorial-portrait
black-white-four-pose-fine-art-portrait black-white-mens-fashion-nine-grid
double-layer-fashion-portrait-poster haidayu-person-epic-silhouette
luxury-commercial-fashion-studio-portrait map-arrow-to-real-world-view
night-train-neon-cinematic-portrait photo-lineart-travel-poster
photo-mogu-boneless-diptych photo-shadow-puppet-diptych
photo-to-expressive-charcoal-sketch photo-to-hand-drawn-isometric-map
pink-purple-geometric-fashion-portrait professional-business-studio-portrait
rainy-city-overpass-cinematic-film-still sky-memory-post-internet-lofi-diptych
studio-pose-transfer-shh urban-street-botanical-stipple-diptych
vintage-color-lithograph-poster vintage-travel-watercolor-photo
water-margin-heroes-selfie heytea-doodle-poster photo-abstract-editorial
photo-relic-editorial xxd-panel-115
""".split())

GENERATION_SLUGS = frozenset("""
summer-sunlit-cinematic-fine-art-portrait peach-coral-floral-ballroom-fashion-portrait
mono-color panorama-generation yingzao regional-culture-map-ink-illustration
oriental-editorial-poster
""".split())

def usage_tag(meta, slug, body=""):
    tags = meta.get("tags", [])
    explicit = [tag for tag in USAGE_TAGS if tag in tags]
    if len(explicit) == 1:
        return explicit[0]
    if slug in OPTIMIZATION_SLUGS:
        return OPTIMIZATION
    if slug in GENERATION_SLUGS or slug.startswith("hand-drawn-"):
        return GENERATION
    words = " ".join([meta.get("title", ""), meta.get("description", ""),
                      meta.get("category", ""), *[t for t in tags if t not in USAGE_TAGS]])
    if re.search(r"无需上传|无需参考图|纯文生图|参考图可选|不需要参考图", words + " " + body[:1500]):
        return GENERATION
    if re.search(r"修图|后期调色|光影重塑|人像优化|照片修复|照片转绘|图像编辑|姿态迁移|身份锁定|风格迁移|照片转|以原图|保留原图|参考图转|图生图", words):
        return OPTIMIZATION
    if re.search(r"上传.{0,35}(照片|参考图|参考图片|原图|截图)|(?:根据|基于|将|以).{0,20}(上传的|上传|原始|原有)(照片|图片|参考图|原图)|锁定原始照片|保留原始照片|reference photo|uploaded image", body[:2200], re.I):
        return OPTIMIZATION
    return GENERATION

def classified_tags(meta, slug, body=""):
    tag = usage_tag(meta, slug, body)
    return [tag] + list(dict.fromkeys(t for t in meta.get("tags", []) if t not in USAGE_TAGS))

def migrate(root=ROOT):
    counts = {tag: 0 for tag in USAGE_TAGS}
    for directory, filename in (("prompts", "prompt.md"), ("skills", "SKILL.md")):
        for path in sorted((root / "library" / directory).glob("*/meta.json")):
            meta = json.loads(path.read_text(encoding="utf-8"))
            body = (path.parent / filename).read_text(encoding="utf-8")
            tags = classified_tags(meta, path.parent.name, body)
            counts[tags[0]] += 1
            if meta.get("tags") != tags:
                meta["tags"] = tags
                path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Usage classification:", counts)
    return counts

if __name__ == "__main__":
    migrate()
