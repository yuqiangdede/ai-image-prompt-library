---
name: hand-drawn-17-inked-storybook
description: 以钢笔墨线定形，搭配清透淡彩与局部排线的绘本画风。
---

# Hand Drawn 17｜墨线绘本

独立拆分自 [threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles) 的第 17 号画风。此 Skill 用于依据描述构造原版画风提示词，图像由用户选定的生图工具生成。

## 使用方法

1. 按下方原版配方保留完整约束，不重写或混合另一套画风。
2. 把 `【主体】`、`【主色调】`、`【文字】` 等实际出现的输入项替换成用户需求；配方本身的强调标签不是输入项。
3. 用户明确给出画幅比例时遵循用户指定；未指定时不要硬注入比例。若本画风是分镜信息图，保留原配方所需的多格结构。
4. 输出完整可直接复制的 Prompt；需要锚点的特殊画风，按后文提示使用原项目的结构化正式流程。不要将文本预览当成正式验收。

## 原版配方（完整收录）

## 17. 墨线绘本(inked-storybook)

> 纯风格。比例:不传则不注入。占位符 `【主体】【构图】【背景色】【配色】【文字】` 自动推断:【构图】默认 "head-and-shoulders portrait"(可换 waist-up 等);【背景色】默认 "warm peach fading to pale cream near the top"(可换 "pale sky-blue with hints of soft cream" / "dusty earth-brown with a slice of pale blue-grey" 等,始终是单一氛围渐变);【配色】填一句 2–4 色的协调短语,人物主色与背景呼应或互补,如 "sky-blue hair, soft pink shirt, warm peach background";【文字】默认 "No text anywhere."。
>
> 出身:Midjourney --sref 3865390274 的 gpt-image 复刻(2026-07-16 三张标杆图两轮对照定稿:蓝发丸子头对标图1、红帽墨镜单色系对标图3双双过局部级复核,另加男孩主体泛化验证)——"富有表现力的绘本角色 + 绘画质感 + 温暖手工感"。本质是"钢笔速写线稿 × 绘本淡彩":墨线定形、起稿线外露、发丝逐根勾,底下是干净透亮的柔和数码上色,水彩刷涂背景 + 奶白纸边毛刷框。适合角色立绘、故事绘本、头像、i2v 动画锚图。
> 命门(两轮翻车教训,五条都必须写死):**①上色**必须写"clean bright digital painting + NO 彩铅颗粒填色 + NO 画布纹",否则整张退化成灰扑扑的彩铅速写(首轮翻车);**②排线只做点缀**——腮红斜排线(脸颊+鼻梁)、帽子/衣服暗部交叉排线、背景少量干刷刮痕是本风格的签名细节,必须以"sparse deliberate accents in a darker shade of the local color"单独成段写进去;但禁止排线铺满色块(那是①的彩铅病)——"点缀排线"与"排线填色"一存一废是本配方的走钢丝处;**③线色随区域**——蓝发用深藏青线、红衣用深栗红线、皮肤用暖褐线,整体读作深褐黑,不是统一纯黑;**④背景与边框**——背景是"松散水彩刷涂+可见笔痕",不能死平也不能出细节云;边框必须"大块毛边矩形+四边平整奶白纸边+一两道白刷痕压进画面",写成模糊淡出就只剩羽化暗角;**⑤眼与发是身份特征**——虹膜几乎占满眼眶、只留眼角一点眼白;头发是"深色墨线逐根顺发流+浅色提亮丝两层"、轮廓外适量飞丝,且要写明"优雅、不是乱麻"(否则出满头乱线)。
> 和 [#12 暖光童画](https://github.com/threerocks/hand-drawn-styles/blob/main/STYLES.md#12-暖光童画动画概念暖绘)同属 MJ 绘本 sref 复刻,区别:#12 是水粉厚涂 vis-dev(几乎无线稿、头发画成大体积块、青橙互补锁死);#17 线稿主导(墨线是画面的骨架)、上色轻薄透亮、配色每图一套协调即可,气质是"速写手账页"而非"厚涂概念稿"。
> 模板为已验证英文原文,占位符也填英文,不要转译。填【配色】时顺手把 LINES 段里的线色示例改成与实际配色对应(如金发→deep umber lines on the blonde hair)。

```
Expressive storybook character illustration — confident sketchy ink linework over clean soft digital painting.
Subject: 【主体】, 【构图】.
STYLE RECIPE (follow exactly):
LINES: every shape is defined by confident loose sketchy ink lines of slightly varying thickness; line color is keyed to each region — a much darker shade of the underlying local color (deep navy lines on blue hair, deep maroon lines on red fabric, warm sepia around the skin), overall reading as dark sepia-black; a few overlapping construction strokes are left visible but the drawing stays elegant, NOT a chaotic scribble mess; hair is drawn as smooth flowing individual strand lines following the hair volume, with a moderate number of fine whippy flyaway strands escaping the silhouette, plus a few lighter-tint painted highlight strands over the darker hair masses; clothing folds are a few loose quick line strokes.
ACCENT HATCHING (signature detail): sparse deliberate hatch strokes in a darker shade of the local color appear ONLY as accents — fine diagonal blush hatching on the cheeks and across the nose bridge, light cross-hatch shading in hat/clothing shadow areas, and a few faint scratchy dry-brush marks in the background wash; everything else stays smooth.
COLOR: underneath the lines the coloring is clean bright digital painting — smooth soft airbrushed gradients, fresh luminous colors, absolutely NO grainy colored-pencil fill, NO canvas texture; skin is smooth with soft rosy airbrushed blush underneath the blush hatching.
EYES (critical): enormous round expressive eyes; the glossy dark-brown irises are VERY large and fill almost the entire eye with only tiny white sclera corners showing, one bright white highlight dot per eye, thick dark painterly upper lash line, bold expressive eyebrows. Tiny nose, small soft lips slightly parted, pointed chin, long slender neck.
BACKGROUND: a loose atmospheric watercolor wash of 【背景色】, with visible soft brush streaks and gentle uneven mottling — painterly but low-detail, NO detailed scenery, NO detailed clouds.
FRAME (signature, must have): the painting fills a large rough-edged rectangle that does NOT reach the image edges; all four sides show a flat, clean, pale warm-cream blank paper margin; the boundary between painting and margin is ragged dry-brush streaks, with one or two loose pale streaks overlapping into the painting, like a hand-painted page from an artist's sketchbook; only the faintest paper grain overall.
Palette: 【配色】 — restrained and harmonized. 【文字】
```

## 来源与许可

- 原作者项目：[threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles)；原始条目：[STYLES.md · 17](https://github.com/threerocks/hand-drawn-styles/blob/b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b/STYLES.md)。
- 来源版本：`b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b`；源文件按 MIT 许可使用，详见随包附带的 `LICENSE`。
- 效果图：[官方样例](https://hand-drawn-images.pages.dev/hand-drawn/examples/17-inked-storybook.png)，仅链接展示，不复制第三方图片到本仓库。
- 如需完整脚本、参考图下载、校验和正式生产调用包，请使用 [上游完整版 Skill](https://github.com/threerocks/hand-drawn-styles)。
