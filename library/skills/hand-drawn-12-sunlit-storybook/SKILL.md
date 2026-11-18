---
name: hand-drawn-12-sunlit-storybook
description: 暖光动画概念水粉插画，可选纸边留白或满幅叙事场景。
---

# Hand Drawn 12｜暖光童画

独立拆分自 [threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles) 的第 12 号画风。此 Skill 用于依据描述构造原版画风提示词，图像由用户选定的生图工具生成。

## 使用方法

1. 按下方原版配方保留完整约束，不重写或混合另一套画风。
2. 把 `【主体】`、`【主色调】`、`【文字】` 等实际出现的输入项替换成用户需求；配方本身的强调标签不是输入项。
3. 用户明确给出画幅比例时遵循用户指定；未指定时不要硬注入比例。若本画风是分镜信息图，保留原配方所需的多格结构。
4. 输出完整可直接复制的 Prompt；需要锚点的特殊画风，按后文提示使用原项目的结构化正式流程。不要将文本预览当成正式验收。

## 原版配方（完整收录）

## 12. 暖光童画(动画概念暖绘)

> 纯风格。比例:不传则不注入。占位符 `【主体】【构图】【场景】【背景元素】【文字】` 自动推断:【构图】默认"waist-up portrait"半身像;【场景】二选一(见下);【背景元素】只在留白纸边档使用,默认为空(整个占位符直接删掉),要加景物时填成英文接续短语,如" and loose sketchy green plant strokes"(必须是松散干刷笔触,保持概念稿式潦草);【文字】默认"No text anywhere."。
>
> 出身:Midjourney 双 --sref 组合画风的 gpt-image 复刻(2026-07-16 对照四张标杆图三轮迭代定稿,含换主体与满幅场景两档验证)。本质是"现代动画电影视觉开发稿(vis-dev)× 绘本水粉":大眼大虹膜角色 + 蓬软发团飞丝 + 青蓝×橙红互补 + 干刷水粉笔触,Pixar/Disney 概念设定稿气质。天然适配角色立绘、故事绘本、i2v 动画锚图。
> 命门(每条都踩过坑,必须写死):**①哑光+笔触可读**——整画 MATTE 传统水粉质感,头发和衣服内部要有大块方向可读的排刷笔触,严禁光滑喷绘和数字渐变(第一、二版翻车主因:出图偏"平滑数字插画",MJ 原版的干涩笔触指纹全丢);**②头发**写"少数大块柔软体积由可见方向笔触塑形 + 轮廓上叠单根飞丝",否则出满头细密小卷;**③虹膜**写"平涂图形化、非 3D 亮球、只留一个小高光",否则出亮晶晶圆球眼;**④五官**允许轻微不对称的手绘感,否则出完美对称萌娃脸;**⑤场景两档**:留白纸边档的身份特征是四边露白纸+粉蓝奶油黄干擦背景;满幅档必须写死 HIGH-KEY 高调明亮(奶白+粉蓝、道具虚化淡出),否则出暗琥珀色油画室内(满幅第一版翻车原因)。
> 模板为已验证的英文原文,不要转译成中文(转译等于换了一套未验证配方)。
>
> `【场景】` 二选一,整段照抄:
> - **留白纸边档(默认)**:`SCENE: background painted with long rough vertical and diagonal dry-brush streaks in pastel sky-blue with soft cream-yellow scuffed patches【背景元素】, bristle marks and broken paint edges visible, deliberately unfinished with raw white paper showing around the border like a concept sketch.`
> - **满幅场景档**(要完整环境时,如室内/街景):`TONAL KEY (most important): HIGH-KEY, light and airy — the whole image stays bright, milky and pastel like soft morning light; large areas wash out into soft creamy-white and pale powder-blue; NEVER darken the room, no deep warm shadows, no moody amber interior, background contrast stays low and faded. SCENE (full-bleed, edge to edge, NO white paper border): <一句英文场景描述,如 a cozy art studio interior with a pale chalkboard and jars of brushes on a light wooden counter> — painted LOOSELY with soft out-of-focus depth: props are blurry pale dry-brush suggestions with lost edges, never crisp; soft white window light floods one side.`

```
Character concept art in a modern animated-feature visual-development style, traditional gouache painting look.
Subject: 【主体】, 【构图】.
【场景】
STYLE RECIPE (follow exactly): MATTE traditional gouache finish over the whole image — absolutely NO glossy airbrush smoothness, NO digital gradient polish; the paint layer must read as real bristle-brush work: chunky directional brushstrokes clearly visible INSIDE the hair masses and clothing, each stroke direction readable like thick gouache dragged by a flat bristle brush; FACE: soft clean shading with sculptural plane changes on cheeks and nose, features slightly asymmetric and hand-painted (NOT a perfectly symmetric doll face), rosy blush, subtle freckles, tiny pointed chin, slender neck; EYES: enormous expressive eyes, the dark irises are VERY large and fill most of the eye, irises painted FLAT and graphic with subtle color variation — NOT shiny 3D orbs, only one small white highlight; thick dark painterly upper lash line, bold expressive eyebrows; HAIR: a few BIG soft volumetric masses shaped by visible directional strokes (NOT detailed ringlet curls), many fine individual flyaway strands drawn on top of the silhouette, warm golden rim light glowing on the hair edges; palette: complementary teal and denim blue against warm orange, soft pastel, gentle warm light, storybook charm, Pixar-Disney visual development art quality.
【文字】
```

## 来源与许可

- 原作者项目：[threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles)；原始条目：[STYLES.md · 12](https://github.com/threerocks/hand-drawn-styles/blob/b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b/STYLES.md)。
- 来源版本：`b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b`；源文件按 MIT 许可使用，详见随包附带的 `LICENSE`。
- 效果图：[官方样例](https://hand-drawn-images.pages.dev/hand-drawn/examples/12-sunlit-storybook.png)，仅链接展示，不复制第三方图片到本仓库。
- 如需完整脚本、参考图下载、校验和正式生产调用包，请使用 [上游完整版 Skill](https://github.com/threerocks/hand-drawn-styles)。
