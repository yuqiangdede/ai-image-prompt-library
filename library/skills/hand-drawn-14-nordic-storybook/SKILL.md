---
name: hand-drawn-14-nordic-storybook
description: 斯堪的纳维亚绘本水粉，真实纸纹、低饱和蓝黄与简化人物。
---

# Hand Drawn 14｜北欧绘本水粉

独立拆分自 [threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles) 的第 14 号画风。此 Skill 用于依据描述构造原版画风提示词，图像由用户选定的生图工具生成。

## 使用方法

1. 按下方原版配方保留完整约束，不重写或混合另一套画风。
2. 把 `【主体】`、`【主色调】`、`【文字】` 等实际出现的输入项替换成用户需求；配方本身的强调标签不是输入项。
3. 用户明确给出画幅比例时遵循用户指定；未指定时不要硬注入比例。若本画风是分镜信息图，保留原配方所需的多格结构。
4. 输出完整可直接复制的 Prompt；需要锚点的特殊画风，按后文提示使用原项目的结构化正式流程。不要将文本预览当成正式验收。

## 原版配方（完整收录）

## 14. 北欧绘本水粉(nordic-storybook)

> 纯风格。比例:不传则不注入。占位符 `【主体】【构图】【纸底色】【光影】` 自动推断:【构图】默认 "standing full-body, centered"(半身像写 "bust portrait, head and shoulders, front facing, centered");【纸底色】默认 "warm off-white (≈#F8F7F2)"(可换 "pale ice-blue (≈#F3F7F9)" 或 "pale warm grey (≈#ECEEED)",同组图统一一种,务必带 ≈hex——不带色值模型会把底涂暗涂黄,已实测翻车);【光影】按构图自动选——全身立绘填 "One single soft pale-blue oval shadow under the feet, no other shading or shadows anywhere.",半身像填 "Behind the character floats one big soft warm cream-yellow oval halo of stippled gouache texture; no drop shadows anywhere."
>
> 出身:Midjourney --sref 1002025125 的 gpt-image 复刻(2026-07-16 三张同题对照定稿)——现代斯堪的纳维亚儿童绘本:柔和水粉纹理+温馨低饱和配色+富表现力的极简人物+微妙纸张纹理。适合角色立绘、绘本人物、温暖叙事场景。
> 命门(四条都必须写死):**①整画纸纹+大留白**——纸纹牙口必须盖住包括空背景在内的整张图,丢了立刻变普通数字插画;**②配色锁死**——丹宁蓝×芥末黄×奶油白+珊瑚腮红,头发限 auburn/深棕/银灰,多一种饱和色就串味;**③人物"设定稿味"**——细长脖子+瘦长四肢+明显鼻子(鼻头偏深珊瑚色)+小小 navy 椭圆眼+轮廓上飞出的单根发丝,不写死会出主流萌娃圆脸(首测即翻车点);**④光影系统是身份特征**——全画唯一投影是脚下一抹淡蓝椭圆(半身像换成身后奶黄椭圆光晕),别处零阴影、零外轮廓线,平涂哑光+衣料内干刷颗粒。
> 和 [#12 暖光童画](https://github.com/threerocks/hand-drawn-styles/blob/main/STYLES.md#12-暖光童画动画概念暖绘)的区别:#12 是 Pixar vis-dev 气质(大眼大虹膜、青橙互补、暖金辉光);#14 眼睛是小点、配色更冷静克制、零光效,是"安静的北欧绘本",两者气质相反。
> 模板为已验证英文原文,占位符也填英文,不要转译。

```
Soft gouache children's picture-book illustration in a modern Scandinavian storybook style, character-design sheet energy.
Subject: 【主体】, 【构图】, against a vast empty 【纸底色】 paper background with huge negative space around the single subject.
PAPER (identity trait): the paper is VERY light and airy, close to near-white — never dark, never heavily tinted; subtle fine paper grain tooth texture visible across the ENTIRE image including the empty background.
PALETTE (strict): cozy limited palette — denim cornflower blue and mustard butter yellow both clearly saturated enough to read cheerful, plus warm cream white and soft coral blush; hair only in auburn, dark umber, dark navy or silver grey; no other colors anywhere.
CHARACTER RECIPE: stylized quirky storybook proportions — long thin neck, slender elongated limbs, small hands; expressive minimalist face: two small navy oval eyes (for a glasses character: big round navy eyes behind round mustard wire glasses; for an angular adult: tiny navy dot eyes), an expressive prominent nose with a slightly darker coral tip, thin expressive slightly-worried eyebrows, faint subtle mouth, round rosy coral blush cheeks; hair painted as a few soft masses with a few thin flyaway hair-line strokes escaping the silhouette (an angular adult may instead get one GEOMETRIC sculpted hair mass with a pointed swoop, a squared jaw and exaggerated elongated legs); gentle, slightly awkward endearing posture, NOT cute mainstream cartoon.
TEXTURE: flat matte gouache color masses with granular dry-brush stippled texture inside the clothing and hair, NO hard outlines, no volumetric 3D rendering, no glossy digital shading.
LIGHT & SHADOW: 【光影】
Timeless heartwarming Scandinavian picture-book aesthetic. No text.
```

## 来源与许可

- 原作者项目：[threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles)；原始条目：[STYLES.md · 14](https://github.com/threerocks/hand-drawn-styles/blob/b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b/STYLES.md)。
- 来源版本：`b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b`；源文件按 MIT 许可使用，详见随包附带的 `LICENSE`。
- 效果图：[官方样例](https://hand-drawn-images.pages.dev/hand-drawn/examples/14-nordic-storybook.png)，仅链接展示，不复制第三方图片到本仓库。
- 如需完整脚本、参考图下载、校验和正式生产调用包，请使用 [上游完整版 Skill](https://github.com/threerocks/hand-drawn-styles)。
