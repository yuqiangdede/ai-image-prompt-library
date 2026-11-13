# Hand Drawn Styles｜手绘画风 Skill（图库索引）

原项目：https://github.com/threerocks/hand-drawn-styles

完整 Skill：https://github.com/threerocks/hand-drawn-styles/blob/main/SKILL.md

此文件为图库原创简介，不是上游完整技能包。上游包含 23 套手绘、插画画风（编号 1–20、22、23，以及 3.1 变体），例如儿童蜡笔、吉卜力风、水墨写意、像素、纸雕、暖色绘本、朱墨水墨漫画与皮影彩染。该 Skill 负责根据画风编号生成完整提示词或引用参考图的 JSON 调用包，本身不生成图片。

## 安装完整 Skill

```bash
npx skills add https://github.com/threerocks/hand-drawn-styles --skill hand-drawn
```

## 使用示例

向支持 Skills 的 Agent 输入：“用 hand-drawn 的 8 号水墨写意画风，把我描述的江南小镇场景转换成完整生图提示词。”

画风的准确参数、参考图、特殊验收流程及运行脚本，以原项目 PROTOCOL.md、STYLES.md、SKILL.md 为准。某些画风需要参考图和额外检查；本图库的索引文件不能替代完整安装。

## 版权与同步

上游代码与指令标注 MIT 许可证；参考图素材未复制到本仓库。此条目通过 link-only 每日跟踪上游提交，不镜像复杂依赖文件；安装命令始终从上游获取完整版。
