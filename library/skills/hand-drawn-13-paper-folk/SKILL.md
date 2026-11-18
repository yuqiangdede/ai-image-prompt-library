---
name: hand-drawn-13-paper-folk
description: 北欧民俗纸雕风，层叠厚纸、造型纸艺与柔和投影。
---

# Hand Drawn 13｜北欧纸雕

独立拆分自 [threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles) 的第 13 号画风。此 Skill 用于依据描述构造原版画风提示词，图像由用户选定的生图工具生成。

## 使用方法

1. 按下方原版配方保留完整约束，不重写或混合另一套画风。
2. 把 `【主体】`、`【主色调】`、`【文字】` 等实际出现的输入项替换成用户需求；配方本身的强调标签不是输入项。
3. 用户明确给出画幅比例时遵循用户指定；未指定时不要硬注入比例。若本画风是分镜信息图，保留原配方所需的多格结构。
4. 输出完整可直接复制的 Prompt；需要锚点的特殊画风，按后文提示使用原项目的结构化正式流程。不要将文本预览当成正式验收。

## 原版配方（完整收录）

## 13. 北欧纸雕(paper-folk)

> 纯风格。比例:不传则不注入。占位符 `【主体】【构图】【底色】【点缀元素】` 自动推断:【构图】默认 "centered, waist-up"(全身叙事场景写 "full-body scene");【底色】默认 "warm ochre-brown"(可换 muted olive-grey / dusty mauve-purple 等低饱和土色,同组图统一一种);【点缀元素】默认 "one stylized folk cloud, a few stylized leaves and one rolled paper spiral"。
>
> 出身:Midjourney --sref 1399033614 的 gpt-image 复刻(2026-07-16 五张对照迭代定稿,refB 终评 96+):层叠纸雕 × 斯堪的纳维亚民俗图案 × 编辑设计配色,手工、温暖、个性。适合人物立绘、民俗动物、叙事场景。
> 命门(两轮翻车点,五条都必须写死):**① NOT flat papercut**——不写就出平面对称剪纸花边(第一版翻车原因);本风格是"立体纸雕塑的柔光渲染/实拍",不是剪纸;**②头是定格木偶式立体雕塑头**——不写死就出"平面贴片脸+画上去的三角鼻"(第二轮翻车原因):刘海是有体积的圆顶并在额头投影、鼻子是物理凸出的纸楔(一侧受光一侧投影);**③留白 + 不对称 editorial 构图**——不写死模型会把画面填满变成装饰壁纸;**④立体感三件套**:部件物理垫高 + 大而柔的真实投影 + 左上柔光 + 背景方向性明暗渐变,丢一样就"变平";**⑤脸的身份特征**:闭眼细弧线 + 圆形腮红贴片,眼睛一睁开就串味。
> 满分打法(codex/gpt-image 通道):生成前先用 view_image 看 [examples/13-paper-folk.png](https://hand-drawn-images.pages.dev/hand-drawn/examples/13-paper-folk.png) 和 [examples/13-paper-folk-musician.png](https://hand-drawn-images.pages.dev/hand-drawn/examples/13-paper-folk-musician.png) 做风格锚定(只学风格不抄构图),再走本模板——实测比纯文字模板再高一档(96+ vs ~90)。
> 模板为已验证英文原文,占位符也填英文,不要转译。

```
A sculptural 3D paper-craft diorama artwork, rendered like a soft 3D render of a handcrafted layered paper sculpture, NOT flat papercut, NOT symmetrical ornament.
Subject: 【主体】, 【构图】, against a large plain textured 【底色】 cardstock backdrop with generous empty negative space around the subject.
CHARACTER RECIPE (for any figure): THE HEAD IS SCULPTURAL — a smooth rounded three-dimensional sculpted form like a stop-motion puppet, softly shaded with real volume, NOT a flat paper cutout face; the bangs are a smooth volumetric dome of thick curved paper sweeping across the forehead and casting a soft shadow on it; the nose is a small 3D paper wedge physically protruding from the face, catching light on one side and casting a tiny shadow on the other; gently rounded cheeks with soft rosy blush circles; closed eyes as thin calm curved lines; tiny serene lips; hair and clothing built from thick curved paper ribbons, rolled quilling spirals, pleated paper fans and layered scalloped paper feathers like overlapping bird plumage; some pieces carry embossed damask folk patterns.
FOLK ELEMENTS: a few Scandinavian folk-art paper pieces placed beside the subject —【点缀元素】— sparse, asymmetric editorial composition with lots of breathing room.
MATERIAL: every piece is matte felt-like cardstock with visible embossed fiber texture and fine swirling filigree embossing, slightly curled edges.
DEPTH & LIGHT (most important): strong sculptural depth — elements physically raised several millimeters off the background, casting large soft realistic drop shadows onto the wall and onto each other; soft warm studio lighting from upper left; the plain background has a soft directional light gradient — noticeably brighter toward the upper left, gently darker in the lower corners (gentle vignette).
PALETTE: muted jewel tones — mustard yellow, ochre, coral orange, magenta pink, lilac purple, slate blue, teal — on a warm earthy backdrop.
Warm handcrafted editorial illustration mood. No text.
```

## 来源与许可

- 原作者项目：[threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles)；原始条目：[STYLES.md · 13](https://github.com/threerocks/hand-drawn-styles/blob/b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b/STYLES.md)。
- 来源版本：`b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b`；源文件按 MIT 许可使用，详见随包附带的 `LICENSE`。
- 效果图：[官方样例](https://hand-drawn-images.pages.dev/hand-drawn/examples/13-paper-folk.png)，仅链接展示，不复制第三方图片到本仓库。
- 如需完整脚本、参考图下载、校验和正式生产调用包，请使用 [上游完整版 Skill](https://github.com/threerocks/hand-drawn-styles)。
