import unittest
from scripts.usage_categories import classified_tags, GENERATION, OPTIMIZATION

class UsageCategoryTests(unittest.TestCase):
    def test_existing(self):
        self.assertEqual(classified_tags({"tags": ["人像"]}, "studio-pose-transfer-shh"), [OPTIMIZATION, "人像"])
        self.assertEqual(classified_tags({"tags": ["摄影"]}, "summer-sunlit-cinematic-fine-art-portrait"), [GENERATION, "摄影"])
        self.assertEqual(classified_tags({}, "hand-drawn-01-minimal-line"), [GENERATION])
    def test_explicit_and_idempotent(self):
        meta = {"tags": ["人像", GENERATION, "人像"]}
        tags = classified_tags(meta, "studio-pose-transfer-shh")
        self.assertEqual(tags, [GENERATION, "人像"])
        self.assertEqual(classified_tags({"tags": tags}, "studio-pose-transfer-shh"), tags)
    def test_new(self):
        self.assertEqual(classified_tags({}, "new-photo", "在完全锁定原始照片主体的前提下调色"), [OPTIMIZATION])
        self.assertEqual(classified_tags({}, "new-flower", "创作一张花卉摄影作品"), [GENERATION])
        self.assertEqual(classified_tags({}, "new-optional", "无需上传参考图，直接生成"), [GENERATION])
    def test_conflicting_tags(self):
        tags = classified_tags({"tags": [GENERATION, OPTIMIZATION, "人像"]}, "studio-pose-transfer-shh")
        self.assertEqual(tags, [OPTIMIZATION, "人像"])
