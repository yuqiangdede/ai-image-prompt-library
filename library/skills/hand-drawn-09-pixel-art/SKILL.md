---
name: hand-drawn-09-pixel-art
description: 统一硬边方形像素、有限色板与抖动，模拟复古游戏视觉。
---

# Hand Drawn 9｜复古像素

独立拆分自 [threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles) 的第 9 号画风。此 Skill 用于依据描述构造原版画风提示词，图像由用户选定的生图工具生成。

## 使用方法

1. 按下方原版配方保留完整约束，不重写或混合另一套画风。
2. 把 `【主体】`、`【主色调】`、`【文字】` 等实际出现的输入项替换成用户需求；配方本身的强调标签不是输入项。
3. 用户明确给出画幅比例时遵循用户指定；未指定时不要硬注入比例。若本画风是分镜信息图，保留原配方所需的多格结构。
4. 输出完整可直接复制的 Prompt；需要锚点的特殊画风，按后文提示使用原项目的结构化正式流程。不要将文本预览当成正式验收。

## 原版配方（完整收录）

## 9. 复古像素

> 纯风格,无内置版式。比例:不传则不注入。占位符 `【主体】【主色调】` 自动推断。
>
> 命门:硬方块像素 + 统一像素网格 + 有限调色板 + 抖动(dithering)代替渐变 + 零抗锯齿。最常踩的坑是模型出"高清图套像素滤镜"的假像素(柔边、渐变、上千色)——负向约束必须写死。

```
复古像素风(pixel art)插画,像 8-bit / 16-bit 老游戏里的精灵图(sprite),由一颗颗清晰的方形像素手工摆出来,不是高清插画加像素滤镜。
主体:【主体】。
像素:低分辨率观感,所有边缘都是硬朗的方块像素阶梯,像素大小一致、对齐同一网格;绝对没有抗锯齿、没有模糊、没有平滑渐变。
配色:有限调色板(retro 风,约 8–16 色,以【主色调】为主),色块平涂;需要明暗过渡时用"抖动(dithering)"棋盘点阵,而不是渐变。
轮廓:用清晰的深色像素描边或高对比色块区分主体;造型简洁、辨识度高,像素图标 / 游戏角色感。
背景:单一平涂纯色或极简像素背景,不喧宾夺主。
严禁:抗锯齿、柔边、模糊、平滑渐变、高清写实、3D 渲染、矢量光滑曲线、把高清图直接套像素滤镜的假像素感。
```

## 来源与许可

- 原作者项目：[threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles)；原始条目：[STYLES.md · 9](https://github.com/threerocks/hand-drawn-styles/blob/b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b/STYLES.md)。
- 来源版本：`b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b`；源文件按 MIT 许可使用，详见随包附带的 `LICENSE`。
- 效果图：[官方样例](https://hand-drawn-images.pages.dev/hand-drawn/examples/09-pixel-art.png)，仅链接展示，不复制第三方图片到本仓库。
- 如需完整脚本、参考图下载、校验和正式生产调用包，请使用 [上游完整版 Skill](https://github.com/threerocks/hand-drawn-styles)。
