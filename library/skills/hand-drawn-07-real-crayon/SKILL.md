---
name: hand-drawn-07-real-crayon
description: 手机拍摄儿童真实蜡笔纸页，保留纸面、漏白及蜡质笔触。
---

# Hand Drawn 7｜蜡笔实拍

独立拆分自 [threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles) 的第 7 号画风。此 Skill 用于依据描述构造原版画风提示词，图像由用户选定的生图工具生成。

## 使用方法

1. 按下方原版配方保留完整约束，不重写或混合另一套画风。
2. 把 `【主体】`、`【主色调】`、`【文字】` 等实际出现的输入项替换成用户需求；配方本身的强调标签不是输入项。
3. 用户明确给出画幅比例时遵循用户指定；未指定时不要硬注入比例。若本画风是分镜信息图，保留原配方所需的多格结构。
4. 输出完整可直接复制的 Prompt；需要锚点的特殊画风，按后文提示使用原项目的结构化正式流程。不要将文本预览当成正式验收。

## 原版配方（完整收录）

## 7. 蜡笔实拍(真·儿童手涂纸张)

> 纯风格。比例:不传则不注入。占位符 `【主体】【主色调】【标题词】` 自动推断。
>
> 和 [#2 蜡笔童涂](https://github.com/threerocks/hand-drawn-styles/blob/main/STYLES.md#2-蜡笔童涂5岁小孩坏画) 的区别:#2 是"小孩自己画的坏画"(偏插画);#7 是"一张真蜡笔纸的照片",命门在实拍纸感 + 强制露白(每块色露白约 40–50%) + 蜡质方向笔触 + 反数字滤镜(经 gpt-image 实测)。

```
A cellphone PHOTO of a real drawing made by a 5-year-old with wax crayons on a slightly wrinkled sheet of white printer paper. It must look photographed on real paper — visible paper texture and faint wrinkles, clean bright white paper — NOT a digital illustration.
Brightly and evenly lit, shot in soft bright daylight, well-exposed and high-key: the white paper reads clean and bright and FILLS almost the whole frame, with little or no surrounding desk or surface visible; only very soft barely-there wrinkle shadows, NO dark or moody shadows, NO underexposure, NO dim indoor lighting, NO grey or yellow cast.
Flat naive composition. Subject: 【主体】.

Genuinely crude and childish, like a real 5-year-old who can barely draw — NOT a skilled adult imitating a child: shaky wobbly outlines that wander and don't close; clumsy wrong proportions; lumpy, barely-recognizable shapes; if there is a face, eyes different sizes and a crooked smile.

The CRAYON COLORING must look genuinely real (most important):
- a real kid has NO control over pressure — some strokes pressed hard and dark, others barely touch the paper, with no consistency; waxy build-up in the heavy spots, faint streaks in the light ones, small smudges
- coloring is sparse and scribbly — bare white paper shows THROUGH everywhere, even inside the colored shapes (roughly 50–65% of each colored area left unfilled, white and streaky)
- black crayon is used mainly for the thin wobbly outlines rather than filling big solid areas
- strokes go in different directions, overlapping and broken, like a kid scribbling with no plan; color clearly overflows past the outlines in several places
- bright primary crayon colors (【主色调】, red, yellow, blue, green, orange, pink); absolutely NO smooth even fill, NO gradient, NO blending, NO uniform digital crayon-filter texture
- a wobbly hand-lettered title "【标题词】" in uneven multicolor capital letters on a crooked baseline

Avoid anything cute, polished, symmetric or professionally illustrated. It must look like a genuine photo of a real child's messy, sparse crayon page.
```

## 来源与许可

- 原作者项目：[threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles)；原始条目：[STYLES.md · 7](https://github.com/threerocks/hand-drawn-styles/blob/b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b/STYLES.md)。
- 来源版本：`b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b`；源文件按 MIT 许可使用，详见随包附带的 `LICENSE`。
- 效果图：[官方样例](https://hand-drawn-images.pages.dev/hand-drawn/examples/07-real-crayon.png)，仅链接展示，不复制第三方图片到本仓库。
- 如需完整脚本、参考图下载、校验和正式生产调用包，请使用 [上游完整版 Skill](https://github.com/threerocks/hand-drawn-styles)。
