---
name: hand-drawn-05-ms-paint
description: 鼠标绘制的笨拙 MS Paint 数字涂鸦，支持照片转绘。
---

# Hand Drawn 5｜MS Paint 烂涂鸦

独立拆分自 [threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles) 的第 5 号画风。此 Skill 用于依据描述构造原版画风提示词，图像由用户选定的生图工具生成。

## 使用方法

1. 按下方原版配方保留完整约束，不重写或混合另一套画风。
2. 把 `【主体】`、`【主色调】`、`【文字】` 等实际出现的输入项替换成用户需求；配方本身的强调标签不是输入项。
3. 用户明确给出画幅比例时遵循用户指定；未指定时不要硬注入比例。若本画风是分镜信息图，保留原配方所需的多格结构。
4. 输出完整可直接复制的 Prompt；需要锚点的特殊画风，按后文提示使用原项目的结构化正式流程。不要将文本预览当成正式验收。

## 原版配方（完整收录）

## 5. MS Paint 烂涂鸦(the worse, the better)

> 纯风格。比例:不传则不注入。占位符 `【主体】` 自动推断。
>
> 这是 OpenAI 官方模板那个病毒级"故意画烂"风(被称「第二个吉卜力」)。**它的最强效果来自图生图**:把第一句换成「把这张照片重画成…」并随 prompt 附一张真实照片,效果远胜纯文生图。文生图也成立(见样图)。

```
把【主体】画成极其笨拙、潦草、可怜兮兮的烂涂鸦,像是用鼠标在 MS Paint 里一笔一笔硬画出来的。
线条歪扭、抖动、断断续续;比例荒谬地不对,该圆的不圆、该直的不直。
填色是大块粗糙的纯色,明显涂出边界、有像素锯齿、低质量数字感。
整体"明明想画对却处处不对劲",越烂越好笑;纯白背景,构图随意。
不要任何专业感、精修、写实光影、渐变或漂亮细节——刻意地丑、刻意地业余。
```

## 来源与许可

- 原作者项目：[threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles)；原始条目：[STYLES.md · 5](https://github.com/threerocks/hand-drawn-styles/blob/b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b/STYLES.md)。
- 来源版本：`b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b`；源文件按 MIT 许可使用，详见随包附带的 `LICENSE`。
- 效果图：[官方样例](https://hand-drawn-images.pages.dev/hand-drawn/examples/05-ms-paint.png)，仅链接展示，不复制第三方图片到本仓库。
- 如需完整脚本、参考图下载、校验和正式生产调用包，请使用 [上游完整版 Skill](https://github.com/threerocks/hand-drawn-styles)。
