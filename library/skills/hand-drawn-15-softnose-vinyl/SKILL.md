---
name: hand-drawn-15-softnose-vinyl
description: 大垂管鼻、小眼睛、哑光软胶与街头穿搭的潮玩角色风。
---

# Hand Drawn 15｜大鼻软偶

独立拆分自 [threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles) 的第 15 号画风。此 Skill 用于依据描述构造原版画风提示词，图像由用户选定的生图工具生成。

## 使用方法

1. 按下方原版配方保留完整约束，不重写或混合另一套画风。
2. 把 `【主体】`、`【主色调】`、`【文字】` 等实际出现的输入项替换成用户需求；配方本身的强调标签不是输入项。
3. 用户明确给出画幅比例时遵循用户指定；未指定时不要硬注入比例。若本画风是分镜信息图，保留原配方所需的多格结构。
4. 输出完整可直接复制的 Prompt；需要锚点的特殊画风，按后文提示使用原项目的结构化正式流程。不要将文本预览当成正式验收。

## 原版配方（完整收录）

## 15. 大鼻软偶(softnose-vinyl)

> 纯风格。比例:不传则不注入。占位符 `【主体】【构图】【眼型】【穿搭】【胡茬】【肤色】【背景底色】` 自动推断:【构图】默认 "full-body standing, front view, centered, symmetrical, square composition"(半身像写 "bust portrait, head and shoulders only, front view, centered, character fills most of the frame, square composition");【眼型】默认困倦眯眼 "tiny half-lidded bored sleepy eyes (small white ovals, small black pupils, a heavy flat upper eyelid line)"(可换圆点眼 "tiny round white eyes with small black dot pupils, a mildly startled neutral gaze");【穿搭】用色板内颜色配街头穿搭(hoodie/卫衣/条纹T/毛线帽/棒球帽/耳机/大头板鞋);【胡茬】成年男性角色填 "Tiny 2D hand-drawn stubble ticks (short thin black line strokes) scattered only on the chin and jaw of the smooth 3D face.",女性/儿童删空;【肤色】默认 "blush pink"(可换 "warm tan");【背景底色】默认 "warm blush-peach"(可换 pale butter-yellow / warm beige,同组图统一一种)。
>
> 出身:Midjourney --sref 533812435 的 gpt-image 复刻(2026-07-16 三形态对照定稿:全身站姿圆点眼镜男/半身毛帽眯眼男/坐姿耳机暖棕肤男,均与参考图并排盲测通过):现代柔和 3D 潮玩美学——简单几何形体、夸张比例、极简人物;超大垂管鼻+眯缝小眼+一字嘴给角色一种俏皮的呆萌气质。适合角色立绘、潮玩头像、街头人物系列。
> 角色一致性 SOP:本配方保证的是**风格**一致,不保证**同一角色**跨图长得一样(gpt-image 没有 MJ --sref 的锚定机制)。要出同一角色的系列图(表情包/连载配图):先用本配方抽一张满意的**锚图**,之后全部走图生图("保持这个角色不变,改为……"),不要每张都从文字重新生成。
> 命门(四条都必须写死):**①材质措辞**——必须写 "smooth matte soft-vinyl … NOT fuzzy, NOT felt, NOT wool",首测写 "felt-coated" 直接出毛毡绒公仔(翻车点),参考是光滑磨砂软胶;**②脸=身份**:超大垂管鼻盖过嘴 + 高位小眼 + **无眉毛** + 一字短嘴 + 长脸长脖,任何一项被"正常化"就串味(参考图人物一律无眉,长出眉毛立刻减分);**③2.5D 混维细节**:胡茬是 2D 短线手绘在光滑 3D 脸上,是本风格辨识度来源之一;**④背景与人同色板**:同色系纯色棚拍底 + 全暖限定色板,背景色必须从人物色板里取,脚下只留一小片软接触影。
> 和 [#13 北欧纸雕](https://github.com/threerocks/hand-drawn-styles/blob/main/STYLES.md#13-北欧纸雕paper-folk)同属"软 3D 渲染",区别:#13 是纸材质+民俗图案+大投影强立体;#15 是软胶潮玩+街头穿搭+柔光平底,气质一冷静手工一呆萌潮流。
> 模板为已验证英文原文,占位符也填英文,不要转译。

```
Soft matte 3D character render in the style of a modern designer collectible vinyl toy, built from simple rounded geometric shapes with playfully exaggerated proportions.
Subject: 【主体】, 【构图】.
CHARACTER ANATOMY (identity traits, most important): an extremely elongated tall face on a long cylindrical neck; an enormously oversized long drooping tubular nose hanging down over the mouth; 【眼型】 set high on the face and close together, with NO eyebrows at all; a single short thin black dash for the mouth, deadpan subtle expression; small simple rounded ears sticking out; a massive inflated capsule-shaped torso with huge rounded sloping shoulders; smooth sausage-like arms tapering to small simple mitt hands with barely-defined chubby fingers; sturdy simple legs; enormous chunky cartoon sneakers with fat flat white laces.
OUTFIT (streetwear): 【穿搭】.
MATERIAL & TEXTURE: smooth matte soft-vinyl surfaces like a high-end art toy — soft-touch rubber coating with only a barely-visible ultra-fine grain, NOT fuzzy, NOT felt, NOT wool; no gloss, no metallic, no plastic shine. 【胡茬】
COLOR PALETTE (strictly limited, warm): blush pink, salmon coral, butter yellow, cream white, warm peach, plus at most one dark accent (chocolate brown or black); 【肤色】 skin tone.
BACKGROUND & LIGHT: seamless solid 【背景底色】 studio backdrop, completely empty, drawn from the same warm palette as the character; soft even diffuse studio lighting, gentle ambient occlusion in crevices, one small soft contact shadow under the feet; no floor line, no horizon, no props.
RENDER: high-end CGI quality, clean, minimalist, playful deadpan charm.
```

## 来源与许可

- 原作者项目：[threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles)；原始条目：[STYLES.md · 15](https://github.com/threerocks/hand-drawn-styles/blob/b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b/STYLES.md)。
- 来源版本：`b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b`；源文件按 MIT 许可使用，详见随包附带的 `LICENSE`。
- 效果图：[官方样例](https://hand-drawn-images.pages.dev/hand-drawn/examples/15-softnose-vinyl.png)，仅链接展示，不复制第三方图片到本仓库。
- 如需完整脚本、参考图下载、校验和正式生产调用包，请使用 [上游完整版 Skill](https://github.com/threerocks/hand-drawn-styles)。
