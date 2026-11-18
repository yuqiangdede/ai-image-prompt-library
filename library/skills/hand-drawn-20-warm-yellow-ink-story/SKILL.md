---
name: hand-drawn-20-warm-yellow-ink-story
description: 暖白纸、黑色干墨排线和芥末黄，描绘单一接触动作与情绪关系。
---

# Hand Drawn 20｜暖黄墨线情绪小剧场

独立拆分自 [threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles) 的第 20 号画风。此 Skill 用于依据描述构造原版画风提示词，图像由用户选定的生图工具生成。

## 使用方法

1. 按下方原版配方保留完整约束，不重写或混合另一套画风。
2. 把 `【主体】`、`【主色调】`、`【文字】` 等实际出现的输入项替换成用户需求；配方本身的强调标签不是输入项。
3. 用户明确给出画幅比例时遵循用户指定；未指定时不要硬注入比例。若本画风是分镜信息图，保留原配方所需的多格结构。
4. 输出完整可直接复制的 Prompt；需要锚点的特殊画风，按后文提示使用原项目的结构化正式流程。不要将文本预览当成正式验收。

> **正式生产注意**：本风格有强制的参考图、结构化调用或验收合同。单独复制下方文本只能作为预览，不能替代上游的正式 JSON 调用包和验证。请安装原始完整仓库，按 [PROTOCOL.md](https://github.com/threerocks/hand-drawn-styles/blob/main/PROTOCOL.md) 执行该风格的正式流程（包括固定画风锚点、参考图顺序和验收）；缺少条件时不得标记生产级通过。

**上游正式调用示例**：

```bash
python3 scripts/render_prompt.py --style 20 --subject '描述要画的内容' --format json
```

## 原版配方（完整收录）

## 20. 暖黄墨线情绪小剧场(warm-yellow-ink-story)

> 别名:`warm-yellow-ink-story`、`yellow-ink-story`、`mustard-ink-story`、`暖黄墨线`。纯风格。比例:不传则不注入。占位符 `【主体】【文字】` 自动推断。正式生产必须附带 [assets/style-20/anchor-warm-yellow-ink-story.png](https://hand-drawn-images.pages.dev/hand-drawn/assets/style-20/anchor-warm-yellow-ink-story.png)，默认无字。
>
> 研发边界:本配方从十张外部参考中抽取暖白负空间、干性黑色墨线、方向性黑色排线、芥末黄、淡珊瑚腮红、紧凑形体和单动作叙事机制。原创锚点、样图、默认人物、动物和动作均为本轮新设计；不保存或分发外部参考，不复现作者名、账号、水印、固定黄兜帽角色、原作文案或原图布局。
>
> 命门:①**锚点是主视觉真源**——每次基础生成都必须传入原创锚点，锚点按 1156×1361 解码像素 SHA-256 固定；②**形体紧凑但不是三维 Q 版**——圆方头约占总高度三分之一至二分之一，短颈或无颈、块状短躯干、短而松弛的四肢、钩形或连指手、圆钝袜形脚；③**脸只留最少信息**——小点或短竖线眼、极短弯嘴、可省略的小鼻点和两团低压淡珊瑚腮红，情绪主要靠倾斜、距离和接触动作；④**黑色不是矢量块**——轮廓有真实干性墨线的压力变化、断续和少量回描，头发与深色下装由方向性排线组成并保留不规则纸白缝；⑤**暖白、墨黑、芥末黄、淡珊瑚四色**——黄色只承担一至两个焦点，不出现大面积蓝紫色、渐变或彩色背景；⑥**白底承担构图**——只讲一个动作，最多两件必要道具，主体位于中下部，禁止完整室内、风景和投影系统。
>
> 正式生产合同要求如下。第一阶段按顶层 prompt 和正式锚点直接生成 `final-candidate`；随后必须运行 `validate_style_20_asset.py`，同时通过像素色板、主体内容锁、8 项人工评分和硬失败检查，才能标记为 final。候选不合格时整张拒收并从基础生成重新开始，禁止用通用画风迁移编辑修补。锚点失效、模型快照无法锁定、高保真参考图不可用或验收器缺失时，正式生产失败关闭。
>
> `【文字】` 正式生产固定填 `No text anywhere.`。标题、文案和排版应在无字底图验收后单独处理。
>
> 模板为已验证英文原文，占位符中的主体也建议使用具体英文动作描述；不要转译、缩写或追加第二套画风规则。

```
Image 1 is the only approved style-only anchor. Transfer its visual grammar, not its people, hair, clothes, animal, props, positions or actions.

SUBJECT: 【主体】.

Create one original minimalist warm-yellow ink story vignette on a flat warm-white drawing-paper field. The paper has only extremely subtle even fiber softness: no photographed sheet, desk, folds, paper edge, cast shadow or vignette.

COMPOSITION: place one compact, immediately readable action in the lower-middle with large calm empty space around and above it. Use no scenery or decorative filler. Include at most two props that directly participate in the action. A single slightly crooked black ground line or a few loose graphite contact marks are allowed only when needed.

SHAPE LANGUAGE: human figures use softly irregular rounded-square pale faces; heads occupy roughly 38–45% of figure height; necks are absent or nearly absent; torsos are compact and blunt; limbs are very short, simple and relaxed; hands stay tiny and subordinate, using only a few short non-anatomical marks; feet are rounded sock-like blocks. Keep clear age and size differences, and give recurring figures different head shapes, shoulder widths, hair silhouettes and postures. Animals inherit the compact proportions and tiny face while retaining every silhouette required to read the species; never force human clothing structure onto an animal. No chibi sphere heads, mascot volume or realistic anatomy.

FACES: use two tiny black dots or short vertical eyes, one very short uneven curved mouth, an optional tiny nose mark and two faint uneven coral-pink cheek smudges. Emotion comes mainly from head tilt, body distance, touch and gesture. No eye whites, irises, highlights, eyelashes, detailed lips, airbrushed skin or copy-pasted smiles.

LINE AND BLACK MASSES: use fine-to-medium near-black dry ink contours with small pressure changes, occasional broken ends, slight wobble, sparse retracing and a few flyaway hair lines. Hair and dark lower garments must be built from visible directional dry strokes with irregular white gaps, starts, stops and crossing passes. Never use clean vector paths, a uniform thick outline, smooth solid-black silhouettes or one repeated digital noise texture.

COLOR AND MATERIAL: use only warm-white paper, near-black ink, one muted warm mustard yellow around #E6C45C and tiny coral-pink cheek marks around #E78E84. Yellow fill is lightly uneven, matte and dry, and appears on at most two clothing or prop areas. Do not introduce blue, purple, cyan, large green or red areas, gradients, rainbow clothing or a colored background.

STORY DISCIPLINE: tell one relationship or action through posture and contact. Keep symbols secondary. Hands may use a few short finger marks only when they stay visually subordinate; reject oversized hands, anatomical joints, fingernails and realistic articulation. Remove shoe construction lines, sock seams, garment ribbing, repeated clothing stripes, decorative stitching, small buttons, realistic joint creases and mechanically precise prop construction. Keep only the minimum inner lines required to identify the action and objects.

ORIGINALITY BOUNDARY: do not recreate any supplied character, paired yellow-hoodie combination, recognizable hairstyle, outfit, pose, composition, text, watermark or account identity. Add no title, logo, signature, caption, speech bubble, hearts, stars, flowers or unrelated ornament.

AVOID: commercial children's-book polish; vector clip-art; generic cute storybook; chibi; anime; 3D; glossy rendering; smooth black fills; fluorescent yellow; detailed room or landscape; photographic paper scene.

【文字】
```

## 来源与许可

- 原作者项目：[threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles)；原始条目：[STYLES.md · 20](https://github.com/threerocks/hand-drawn-styles/blob/b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b/STYLES.md)。
- 来源版本：`b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b`；源文件按 MIT 许可使用，详见随包附带的 `LICENSE`。
- 效果图：[官方样例](https://hand-drawn-images.pages.dev/hand-drawn/assets/style-20/anchor-warm-yellow-ink-story.png)，仅链接展示，不复制第三方图片到本仓库。
- 如需完整脚本、参考图下载、校验和正式生产调用包，请使用 [上游完整版 Skill](https://github.com/threerocks/hand-drawn-styles)。
