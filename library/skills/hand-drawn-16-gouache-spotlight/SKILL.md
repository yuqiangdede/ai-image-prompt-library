---
name: hand-drawn-16-gouache-spotlight
description: 满幅水粉刷底、角色背后聚光晕与夸张人物比例。
---

# Hand Drawn 16｜聚光水粉立绘

独立拆分自 [threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles) 的第 16 号画风。此 Skill 用于依据描述构造原版画风提示词，图像由用户选定的生图工具生成。

## 使用方法

1. 按下方原版配方保留完整约束，不重写或混合另一套画风。
2. 把 `【主体】`、`【主色调】`、`【文字】` 等实际出现的输入项替换成用户需求；配方本身的强调标签不是输入项。
3. 用户明确给出画幅比例时遵循用户指定；未指定时不要硬注入比例。若本画风是分镜信息图，保留原配方所需的多格结构。
4. 输出完整可直接复制的 Prompt；需要锚点的特殊画风，按后文提示使用原项目的结构化正式流程。不要将文本预览当成正式验收。

## 原版配方（完整收录）

## 16. 聚光水粉立绘(gouache-spotlight)

> 纯风格。比例:不传则不注入。占位符 `【主体】【背景色】【构图】【文字】` 自动推断:【背景色】按互补规则自动选——主体/服装偏蓝青就配 "warm amber-orange"(可用 "warm pale-amber" 减浓),主体偏暖橙就配 "soft sky-blue";同组图两种底色可混用(标杆组即两橙两蓝);【构图】默认 "waist-up centered portrait facing the viewer"(全身立绘/动物按需改写);【文字】默认 "No text anywhere."。
>
> 出身:Midjourney --sref 2344047981 的 gpt-image 复刻(2026-07-16 四张标杆图五轮逐张并排对照定稿:惊讶男孩/呆脸大叔/戴镜老爷爷/圆胖小鸟四种主体 × 橙/蓝两种底色全部验证,终版四张与标杆并排评分 94–96)。本质是"数码水粉动画概念立绘":满幅单色刷底 + 人物身后聚光晕 + 夸张比例大眼角色 + 软喷绘脸×干扫笔触,高级绘本 × 动画电影 vis-dev 气质。适合角色立绘、角色系列(跨张统一底色即成套)、i2v 动画锚图。
> 命门(五轮翻车教训,全部写死):**①背景笔触是三向走钢丝**——写重了(heavy mottling)出深色油画斑驳底(首轮翻车),写平了(mostly flat)出数字平涂(次轮小鸟翻车),不压饱和就出火焰橙底(四轮男孩偏差);唯一验证通过的表述是 "clearly visible loose scumbled dry-brush strokes + gentle tonal variation + matte and calm/muted + NOT fiery saturated";**②皮肤禁纹理**——脸和皮肤必须 airbrushed smooth 干净渐变,可见笔触只留在头发/皮毛/羽毛/衣服/背景;**③头发写羽化发簇**——"soft FEATHERED brush-stroke tufts, each tuft one wide soft feathered stroke",两个反向坑都要点名:写不够软出尖刺动漫发(首轮),只写 rounded masses 出卷花菜团(次轮),必须同时禁 "NOT razor-sharp anime spikes, NOT tight curly ringlets";**④眼睛要留眼白**——虹膜/瞳孔外必须写 visible white sclera,不写死成人角色会出无眼白的眯缝黑豆眼(三轮大叔翻车);**⑤身份特征=满幅涂满+聚光晕**——单色刷底涂满到边、人物身后一圈更亮的柔光,四边绝不露白纸;**⑥互补色排布**——全画只有一对互补色:蓝青主体×暖橙底,或暖橙主体×蓝底。
> 和 [#12 暖光童画](https://github.com/threerocks/hand-drawn-styles/blob/main/STYLES.md#12-暖光童画动画概念暖绘)同源(都是 MJ sref 动画 vis-dev 水粉的复刻),区别:#12 是"未画完的概念稿"(白纸留边+粉蓝奶黄碎笔背景+童画大虹膜),#16 是"画满的聚光立绘"(单色满幅底+聚光晕+虹膜正常留眼白,角色从萌娃到大叔小鸟全适配)。
> 模板为已验证英文原文,占位符也填英文,不要转译。

```
Character concept art in a modern animated-feature visual-development style, painterly digital GOUACHE illustration — matte, opaque, simplified shapes with clearly visible brushwork.
Subject: 【主体】, 【构图】.
STYLE RECIPE (follow exactly): the whole image is built from CLEARLY VISIBLE soft brush strokes — every area shows the direction of the brush, like a hand-painted gouache concept painting, yet the values stay soft and low-contrast; BACKGROUND (keep it CALM): one single soft MUTED 【背景色】 color field covering the whole canvas edge to edge, painted with clearly visible but GENTLE loose scumbled dry-brush strokes and subtle tonal variation (some patches slightly lighter, some slightly deeper), matte and calm — NOT fiery over-saturated color, NOT heavy dark oil mottling, NOT flat digital fill; a noticeably lighter soft glow right behind the character like a soft spotlight, fading calmly toward slightly deeper corners; fully abstract with no scenery, no white paper border; FACE & SKIN: soft smooth airbrushed volume with clean gradients, NO canvas texture on the skin, warm rosy flush on cheeks, nose and ears; EYES: oversized round expressive cartoon eyes with visible WHITE sclera around the irises and one bright white highlight dot each, bold painterly eyebrows; exaggerated caricature proportions; HAIR / FUR / FEATHERS: painted as soft FEATHERED brush-stroke tufts — each tuft is one wide soft feathered stroke, fluffy silhouette, warm rim light glowing on the edges, a few cool reflected-light strokes on the shadow side — NOT razor-sharp anime spikes, NOT tight curly ringlets; CLOTHING: big simplified color blocks with visible dry-brush strokes and slightly rough painterly edges, minimal detail; PALETTE: one complementary pair only — teal/denim blue against warm orange-amber — soft cinematic lighting, storybook charm, premium animated-film character concept art quality.
【文字】
```

## 来源与许可

- 原作者项目：[threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles)；原始条目：[STYLES.md · 16](https://github.com/threerocks/hand-drawn-styles/blob/b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b/STYLES.md)。
- 来源版本：`b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b`；源文件按 MIT 许可使用，详见随包附带的 `LICENSE`。
- 效果图：[官方样例](https://hand-drawn-images.pages.dev/hand-drawn/examples/16-gouache-spotlight.png)，仅链接展示，不复制第三方图片到本仓库。
- 如需完整脚本、参考图下载、校验和正式生产调用包，请使用 [上游完整版 Skill](https://github.com/threerocks/hand-drawn-styles)。
