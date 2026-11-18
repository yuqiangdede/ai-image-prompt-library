---
name: hand-drawn-03-ghibli
description: 柔和手绘动画与水彩暖光，单一焦点、简化背景并避免碎片化。
---

# Hand Drawn 3｜吉卜力风

独立拆分自 [threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles) 的第 3 号画风。此 Skill 用于依据描述构造原版画风提示词，图像由用户选定的生图工具生成。

## 使用方法

1. 按下方原版配方保留完整约束，不重写或混合另一套画风。
2. 把 `【主体】`、`【主色调】`、`【文字】` 等实际出现的输入项替换成用户需求；配方本身的强调标签不是输入项。
3. 用户明确给出画幅比例时遵循用户指定；未指定时不要硬注入比例。若本画风是分镜信息图，保留原配方所需的多格结构。
4. 输出完整可直接复制的 Prompt；需要锚点的特殊画风，按后文提示使用原项目的结构化正式流程。不要将文本预览当成正式验收。

## 原版配方（完整收录）

## 3. 吉卜力风

> 纯风格。比例:不传则不注入。
>
> 注意:gpt-image(Codex/ChatGPT)上若用"lush/detailed"会出"稀碎感"(过度堆细节、天空云朵零碎)。已改为反堆细节——单一焦点、简化背景、大色块平滑渐变、云少而整(经 gpt-image 实测)。

```
Studio Ghibli style hand-drawn anime illustration of 【主体】.
Clean, uncluttered composition with ONE clear focal subject; simplified background, generous calm negative space — avoid busy, fragmented, over-detailed or scattered compositions.
Render any large areas (sky, water, fields, walls) as smooth, even watercolor gradients — no patchy, mottled, speckled or grainy texture. Any clouds should be a few large, simple, soft, cohesive shapes — not many small scattered puffs or broken fragments.
Soft hand-painted watercolor look with smooth gentle gradients and soft cel-shading; warm cinematic light diffusing softly from above with a tender glow.
Bright yet harmonious, lightly saturated palette; dreamy, nostalgic, heartwarming mood.
Clean delicate linework, painterly hand-drawn feel — not 3D, not photoreal, not a digital vector, not cluttered, not fragmented.
```

## 来源与许可

- 原作者项目：[threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles)；原始条目：[STYLES.md · 3](https://github.com/threerocks/hand-drawn-styles/blob/b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b/STYLES.md)。
- 来源版本：`b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b`；源文件按 MIT 许可使用，详见随包附带的 `LICENSE`。
- 效果图：[官方样例](https://hand-drawn-images.pages.dev/hand-drawn/examples/03-ghibli.png)，仅链接展示，不复制第三方图片到本仓库。
- 如需完整脚本、参考图下载、校验和正式生产调用包，请使用 [上游完整版 Skill](https://github.com/threerocks/hand-drawn-styles)。
