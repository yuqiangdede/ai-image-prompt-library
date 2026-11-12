# Panorama Generation · 全景生成

只需提供场景描述、普通参考图或现成的全景图，就能完成“生成 360° 全景资产 → 检查全景 → 构建 Three.js 可交互网页”的工作流。

## 使用方式

- **文字生成**：描述要呈现的空间、场景、时间、光照和风格，自动生成全景图。
- **参考图片生成**：上传照片/效果图，以主体和风格为锚点补齐画面外侧、天空与地面，生成合理连续的环视场景。
- **已有全景图**：直接检验、加载等距柱状全景图并生成网页。

详见 [`SKILL.md`](SKILL.md)。查看器模板在 `templates/index.html`，全景文件检查器在 `scripts/check_panorama.py`。

## 预期产物

```text
output/<scene-name>/
├── panorama.jpg
├── index.html
└── README.md
```

## 本条目封面

封面 `images/cover.gif` 为上传的天坛祈年殿动画示例，用于展示场景效果；它不是 2:1 全景球面纹理，不能直接代替生成的 `panorama.jpg`。

本图库保存完整 Skill 和配套资源，下载 ZIP 即可导入支持本地 Skills 的工具；无须依赖其他仓库。
