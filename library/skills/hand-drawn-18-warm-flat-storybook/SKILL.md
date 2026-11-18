---
name: hand-drawn-18-warm-flat-storybook
description: 圆润几何色块、蓝橙对比与大留白构成暖色扁平绘本。
---

# Hand Drawn 18｜暖色扁平绘本

独立拆分自 [threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles) 的第 18 号画风。此 Skill 用于依据描述构造原版画风提示词，图像由用户选定的生图工具生成。

## 使用方法

1. 按下方原版配方保留完整约束，不重写或混合另一套画风。
2. 把 `【主体】`、`【主色调】`、`【文字】` 等实际出现的输入项替换成用户需求；配方本身的强调标签不是输入项。
3. 用户明确给出画幅比例时遵循用户指定；未指定时不要硬注入比例。若本画风是分镜信息图，保留原配方所需的多格结构。
4. 输出完整可直接复制的 Prompt；需要锚点的特殊画风，按后文提示使用原项目的结构化正式流程。不要将文本预览当成正式验收。

## 原版配方（完整收录）

## 18. 暖色扁平绘本(warm-flat-storybook)

> 纯风格。比例:不传则不注入。占位符 `【主体】【构图】【文字】` 自动推断:【构图】默认 "full-body, centered in the lower-middle with huge calm negative space"(多人互动写 "compact overlapping group, full bodies visible, centered in the lower-middle with huge calm negative space");【文字】默认 "No text anywhere."。
>
> 出身:以一张家庭人物扁平绘本插画为标杆,经 2026-07-23 两轮同题校准 + 三项无参考图泛化测试定稿。首轮比较“纯平滑 / 轻纸纹 / 轻体积”三档,确认轻纸纹平涂最接近;第二轮修正父亲肩宽、成人脸型、短发几何块与阴影数量。最终在单人抱书、双人击掌、熊与狐狸共读三个异题材上保持同一图形语言。
>
> 命门:①**轮廓靠色块相接,不是描边**——只允许五官、手指、发丝出现极少深藏青细线;②**人物比例反主流萌系**——成人长颈、细长肢体、小手脚、窄椭圆脸或方下巴,宽体型角色可用巨大的胶囊躯干与圆弧手臂,严禁圆脸大头萌娃化;③**阴影是少量硬边同色形状**——每个大色块最多一深一浅,不要渐变体积;④**色板锁死**——暖米白底 + 深藏青 + 雾蓝 + 珊瑚橙 + 金橙 + 暖桃肤色,禁止额外色相;⑤**约七成留白**——主体压在画面下部中央,脚下只有一抹极淡椭圆影。
>
> 和 [#14 北欧绘本水粉](https://github.com/threerocks/hand-drawn-styles/blob/main/STYLES.md#14-北欧绘本水粉nordic-storybook)的区别:#14 依赖全画纸纹牙口、干刷水粉颗粒、低饱和安静人物;#18 是平滑数码平涂、鲜明蓝橙、高对比几何大色块和更强的动作弧线。
>
> 模板为已验证英文原文,占位符也填英文,不要转译。

```
Clean contemporary flat picture-book illustration built from large rounded geometric silhouettes.
Subject: 【主体】, 【构图】, against a vast empty warm near-white (#FDF6ED) background.
STYLE IDENTITY (follow exactly): almost no continuous outer contour lines; shapes meet through color contrast. Use only a few very thin dark-navy accent lines around hair, fingers and facial features, with occasional tiny pale rim accents on dark hair. Smooth matte local colors, not painterly.
SHAPE LANGUAGE: simplify every figure and object into a few bold rounded geometric masses with a clear readable silhouette. Use long soft action arcs and compact overlapping groups for interaction. A broad character may have an enormous wide capsule torso, massive rounded sloping shoulders and one large curved arm; a slender character has a long neck, narrow oval face, elongated limbs, small hands and small feet.
HUMAN FACES: adults have slightly elongated or angular faces, never round baby faces; children may have a slightly larger youthful head but remain slim, never chibi. Features are gently asymmetric and hand-shaped: two tiny vertical navy oval eyes, thin expressive eyebrows, one prominent simple nose shape, one clean curved mouth, and small coral cheek patches. Hair is built from only a few solid rounded or geometric dark-navy masses with at most one or two accent strands. No large glossy eyes.
ANIMALS: translate the same shape language into broad capsule torsos or slender elongated bodies, tiny oval eyes, simple geometric muzzles, small paws and one or two bold silhouette features; never render fur, plush fibers or mascot-like 3D volume.
SHADING (strict): mostly flat. On each large clothing, hair, body or object area use at most ONE darker same-hue graphic shadow shape and optionally ONE lighter same-hue shape, both broad and clean-edged. No smooth gradient inside subjects, no realistic light modeling.
PALETTE (strict): deep navy #2A4A71, dark navy #172F4E, misty cornflower blue #7B9AD3, coral orange #D25F30, golden orange #F49441, warm peach skin accents, and the warm near-white background only. Reassign these colors to suit the subject, but introduce no green, purple, pink, brown, pure black or extra accent hue.
BACKGROUND & GROUND: huge calm negative space, no scenery unless explicitly requested; one barely visible pale warm-grey oval contact shadow under the feet or seated group, no other cast shadows.
TEXTURE: barely perceptible fine uncoated-paper softness across the whole image, including the empty background; never grainy and never visibly brushed.
MOOD: intimate, playful, emotionally warm, elegant modern children’s storybook.
AVOID: generic corporate vector clip-art, stock infographic people, mainstream round cartoon faces, chibi proportions, thick outlines, strong gradients, glossy airbrush, 3D, gouache, watercolor, pencil, dry brush, anime eyes, detailed or decorative background.
【文字】
```

## 来源与许可

- 原作者项目：[threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles)；原始条目：[STYLES.md · 18](https://github.com/threerocks/hand-drawn-styles/blob/b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b/STYLES.md)。
- 来源版本：`b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b`；源文件按 MIT 许可使用，详见随包附带的 `LICENSE`。
- 效果图：[官方样例](https://hand-drawn-images.pages.dev/hand-drawn/examples/18-warm-flat-storybook.png)，仅链接展示，不复制第三方图片到本仓库。
- 如需完整脚本、参考图下载、校验和正式生产调用包，请使用 [上游完整版 Skill](https://github.com/threerocks/hand-drawn-styles)。
