---
name: hand-drawn-19-roundhead-redline
description: 大圆头、细石墨四肢及红色重点；正式生产需原始锚点与质量验收。
---

# Hand Drawn 19｜圆头红线极简童画

独立拆分自 [threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles) 的第 19 号画风。此 Skill 用于依据描述构造原版画风提示词，图像由用户选定的生图工具生成。

## 使用方法

1. 按下方原版配方保留完整约束，不重写或混合另一套画风。
2. 把 `【主体】`、`【主色调】`、`【文字】` 等实际出现的输入项替换成用户需求；配方本身的强调标签不是输入项。
3. 用户明确给出画幅比例时遵循用户指定；未指定时不要硬注入比例。若本画风是分镜信息图，保留原配方所需的多格结构。
4. 输出完整可直接复制的 Prompt；需要锚点的特殊画风，按后文提示使用原项目的结构化正式流程。不要将文本预览当成正式验收。

> **正式生产注意**：本风格有强制的参考图、结构化调用或验收合同。单独复制下方文本只能作为预览，不能替代上游的正式 JSON 调用包和验证。请安装原始完整仓库，按 [PROTOCOL.md](https://github.com/threerocks/hand-drawn-styles/blob/main/PROTOCOL.md) 执行该风格的正式流程（包括固定画风锚点、参考图顺序和验收）；缺少条件时不得标记生产级通过。

**上游正式调用示例**：

```bash
python3 scripts/render_prompt.py --style 19 --subject '描述要画的内容' --format json
```

## 原版配方（完整收录）

## 19. 圆头红线极简童画(roundhead-redline)

> 别名:`roundhead-redline`、`redline-roundhead`、`graphite-redline`、`圆头红线`、`黑红白圆头童画`。纯风格。比例:不传则不注入。占位符 `【主体】【文字】` 自动推断。正式生产必须附带 [assets/style-19/anchor-roundhead-redline.png](https://hand-drawn-images.pages.dev/hand-drawn/assets/style-19/anchor-roundhead-redline.png)，默认无字。
>
> 研发边界:本配方从五张外部动画设定参考中抽取平面结构、铅笔压力、干性颜料、限色色板和负空间机制；锚点、样图、默认人物、服装、道具和动作均为原创，不保存或分发外部参考，不复现片名、标识、固定角色、固定红白横条服装或海报排版。
>
> 命门:①**锚点是主视觉真源**——正式生产每张都必须传入原创三主体锚点，锚点按 1024×1536 解码像素 SHA-256 固定；缺失、换图、像素变化或调用端不能传高保真参考图时停止生产；②**平面大头小身，但不是 Q 版**——头是轻微不规则的大圆/椭圆，躯干明显更小，四肢是极细弹性单线，动作靠长弧线、倾斜和失衡支点表达，禁止三维体积和标准化萌系骨架；③**脸只留两道竖眼**——两道粗重、不等长、不完全平行的炭黑竖痕，无眼白、虹膜、高光、写实鼻唇；情绪来自头部与全身姿态；④**线必须像真实铅笔**——细石墨轮廓在同一条曲线里有压力深浅、纸纹断续、少量试探性重描，不能是干净矢量线，也不能整画套统一抖动滤镜；⑤**黑红白限色**——暖白纸、石墨灰、炭黑和单一珊瑚红；红色每个动作只承担一个明确焦点，低压腮红除外；⑥**白底是构图的一部分**——只画一个主动作和最多两件必要道具，禁止完整房间、风景、透视地面和投影系统。
>
> 正式生产合同:基础生成必须使用固定锚点和锁定的模型快照，输出先标记为 `candidate-only`；调用端按机读硬失败条件检查后才能标记为 final。后期“统一加粗/抖线/蜡笔滤镜”不能补救偏离，失败图应拒收并从同一锚点重新生成。当前验证发现，只改线条的编辑阶段改善有限，因此不把编辑阶段设为强制步骤。
>
> `【文字】` 正式生产固定填 `No text anywhere.`。需要标题或海报文字时先生成无字底图，再走独立排版流程；不要让文字生成风险污染画风回归。
>
> 模板为已验证的英文原文，占位符中的主体也建议使用具体英文动作描述；不要转译或缩写配方。

```
Image 1 is the only approved style-only anchor. Transfer its visual grammar, not its people, animal, clothes, objects, positions or actions.

SUBJECT: 【主体】.

VISUAL CONTRACT:
A radically minimal, flat, handmade children's-animation drawing on bright near-white paper. No 3D volume. Build each subject from one dominant large, slightly irregular round or oval head, a much smaller simple torso, extremely thin elastic single-line limbs, three- or four-stroke twig hands and tiny bent-hook feet. The gesture must read through long action arcs, asymmetry, body lean and an intentionally unstable point of balance. Do not reuse one standardized skeleton across subjects.

Faces use exactly two thick near-vertical charcoal eye marks, slightly unequal and not perfectly parallel; no eye whites, pupils, irises, highlights, eyelashes, modeled nose or realistic lips. Emotion comes from head tilt, eye-mark tilt and whole-body gesture. Optional cheeks are two faint uneven low-pressure coral rubs.

Outer contours are thin real graphite pencil lines, not clean vector paths: pressure visibly breathes from faint gray to darker graphite within a curve; paper tooth causes microscopic breaks; selected contours include one short offset searching stroke or a brief retraced dark patch. Keep this sparse and accidental, not an all-over sketch effect. Charcoal-black and coral-red filled areas show dry colored-pencil or wax-pastel rubbing with uneven pressure, starts, stops and crossing passes; never a repeated digital texture.

STRICT PALETTE: bright near-white paper, graphite gray, charcoal black and one coral-red hue only. Coral red is one rhythmic focal accent on the explicitly named prop or garment detail, plus optional faint cheeks. Do not invent another coral garment or object.

COMPOSITION: the unpainted white field occupies most of the canvas. One main action, at most two necessary props, no room, landscape, decorative background, horizon, perspective floor or cast-shadow system. Under a subject, at most one short loose gray pencil smudge.

AVOID: any title, logo, watermark or poster layout; red-and-white striped shirt with black shorts; commercial vector art; stock icon; generic cute storybook; chibi; anime; 3D; realistic anatomy; smooth digital line; uniform thick outline; smooth gradient; airbrushed blush; repeated procedural crayon texture; photographic paper scene.

【文字】
```

## 来源与许可

- 原作者项目：[threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles)；原始条目：[STYLES.md · 19](https://github.com/threerocks/hand-drawn-styles/blob/b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b/STYLES.md)。
- 来源版本：`b3727de45a2a40f3f3e2ce93f19d4a3c7a0c5f4b`；源文件按 MIT 许可使用，详见随包附带的 `LICENSE`。
- 效果图：[官方样例](https://hand-drawn-images.pages.dev/hand-drawn/assets/style-19/anchor-roundhead-redline.png)，仅链接展示，不复制第三方图片到本仓库。
- 如需完整脚本、参考图下载、校验和正式生产调用包，请使用 [上游完整版 Skill](https://github.com/threerocks/hand-drawn-styles)。
