---
name: hand-drawn-06-pen-scribble
description: 单色圆珠笔以缠绕线密度表现形体，适合肖像和动物速写。
---

# Hand Drawn 6｜圆珠笔单线涂鸦

独立拆分自 [threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles) 的第 6 号画风。此 Skill 用于依据描述构造原版画风提示词，图像由用户选定的生图工具生成。

## 使用方法

1. 按下方原版配方保留完整约束，不重写或混合另一套画风。
2. 把 `【主体】`、`【主色调】`、`【文字】` 等实际出现的输入项替换成用户需求；配方本身的强调标签不是输入项。
3. 用户明确给出画幅比例时遵循用户指定；未指定时不要硬注入比例。若本画风是分镜信息图，保留原配方所需的多格结构。
4. 输出完整可直接复制的 Prompt；需要锚点的特殊画风，按后文提示使用原项目的结构化正式流程。不要将文本预览当成正式验收。

## 原版配方（完整收录）

## 6. 圆珠笔单线涂鸦(scribble)

> 纯风格。比例:不传则不注入。占位符 `【主体】` 自动推断。偏艺术速写向,适合肖像/动物。

```
用单一黑色圆珠笔画的潦草涂鸦速写,描绘【主体】。
大量快速、随性、来回缠绕的细线条,线条不闭合、带偶然性,靠线的疏密缠绕表现明暗与体积,一气呵成的速写感。
纯单色——黑色墨线 + 白纸,无平涂色块,无数字渐变。
自由、即兴、艺术化的手稿气质,而非工整插画。
```

## 来源与许可

- 原作者项目：[threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles)；原始条目：[STYLES.md · 6](https://github.com/threerocks/hand-drawn-styles/blob/b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b/STYLES.md)。
- 来源版本：`b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b`；源文件按 MIT 许可使用，详见随包附带的 `LICENSE`。
- 效果图：[官方样例](https://hand-drawn-images.pages.dev/hand-drawn/examples/06-pen-scribble.png)，仅链接展示，不复制第三方图片到本仓库。
- 如需完整脚本、参考图下载、校验和正式生产调用包，请使用 [上游完整版 Skill](https://github.com/threerocks/hand-drawn-styles)。
