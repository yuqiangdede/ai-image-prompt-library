# ChatGPT 高清图片直传 GitHub：成功经验与后续操作手册

> 状态：accepted（已验证）  
> 日期：2026-11-18  
> 适用项目：`yuqiangdede/ai-image-prompt-library`  
> 目的：今后添加/替换生图素材时，默认**直接把真实高清图片提交到 GitHub main**，不再重复要求用户手工将图片上传到 Issue。  
> 权威分工：项目日常操作以 [README.md](../../../README.md) 为准；本文件记录本次成功路径、故障经验和验收要点；实际实现以仓库文件、Git 提交和 GitHub Actions 记录为准。

## 一、本次已确认的成功事实

- 素材：「薄荷绿蝶饰汉服少女｜低机位回眸·冷白日光·极浅景深写实摄影」。
- 生成图片：PNG 转成 **1086×1448 WebP，约 181 KB**。保留像素尺寸；WebP 是编码后的图片，并不意味着与 PNG 字节相同。
- 提交文件：`library/prompts/mint-butterfly-hanfu-portrait/images/cover.webp`、`meta.json`、`prompt.md`。
- 图片 Git Blob SHA：`5ef87aaf1a56a44416bd26fbdd268b3a4fe22a01`，提交后再次读取与本地 WebP 一致。
- main 提交：[`9982171bae78268b44c3fa10a2f8812c87ec715a`](https://github.com/yuqiangdede/ai-image-prompt-library/commit/9982171bae78268b44c3fa10a2f8812c87ec715a)。
- 部署：[`44186525628`](https://github.com/yuqiangdede/ai-image-prompt-library/actions/runs/44186525628)，`status=completed`、`conclusion=success`。
- 曾作为备用通道创建的 [Issue #22](https://github.com/yuqiangdede/ai-image-prompt-library/issues/22) 已在直传成功后关闭，**不再让 Issue 自动重复导入**。
- **限制说明**：本次 `prompt.md` 是从当时可恢复的提示词整理而成；不得据此声称已逐字恢复用户原始提示词。

## 二、以后默认执行的直传流程（优先）

1. **读取本项目规范及目标素材**：先看 [README.md](../../../README.md) 的素材目录规范，查 `library/prompts/<slug>/meta.json` 是否存在。新增则创建；替换封面则保留已有素材的其他数据。核对用户最终要保存的提示词全文，不能自行编造缺失段落还声称原样保存。
2. **准备高清图**：从本次会话拿到真正的生成图片文件（不能凭空编造 `/mnt/data` 路径）。PNG/JPEG 可转换为 WebP；保留原宽高比、分辨率与方向，按画质需要调压缩；不要默认生成仅供卡片使用的小缩略图代替高清封面。记录文件大小、分辨率、内容摘要。
3. **解决本地文件与 GitHub 连接不共享磁盘的问题**：先将 WebP 的二进制数据转为 **Base64 纯文本**，作为临时的受控文件，通过当前可用的文件连接器进行上传和读取。若连接器需要先列出新文件才能读取，则先列出；分段读取时按行号顺序拼接，去掉编码文本中的换行，不得截断、跳行、重排或把整个 Base64 输出到聊天窗口。
4. **在同一次工具编排中直接写 GitHub Blob**：拿到完整 Base64 后，调用 GitHub `create_blob`，`encoding="base64"`。校验 Base64 字符合法、长度以及解码后的文件内容；比对 GitHub 返回的 Blob SHA 与本地按 Git Blob 算法计算的 SHA。**Blob SHA 与普通 SHA-256 不是一回事**。
5. **一次性构造完整素材提交**：`meta.json`、`prompt.md` 使用 UTF-8 创建文本 Blob。实时读取 `main` 的最新 Commit SHA 及其 Tree SHA，用 `create_tree(base_tree_sha=...)` 添加 `images/cover.webp`、`meta.json`、`prompt.md`；再 `create_commit(parent_sha=最新 main)` 和 `update_ref(main, force=false)`。分支发生竞争冲突时重新获取最新 HEAD 并重建，不强推覆盖他人提交。
6. **三重验收**：
   - GitHub `main` 的 HEAD 指向新 Commit；
   - `fetch_file` 确认三个文件真实存在，且 `images/cover.webp` 的 Blob SHA 与本地一致；`meta.json` 的 `cover`、`images` 指向相对路径 `images/cover.webp`；
   - 查询该 Commit 对应的 GitHub Actions，直到 `status=completed` 且 `conclusion=success`；不能只凭工作流已触发就说“部署成功”。
7. **清理临时桥接数据**：移除临时 Base64 文本、测试文件和本地中转产物；如文件服务仅支持“移到回收站”，须如实记载，不宣称永久擦除。不要保存个人 Token、私人照片或其他敏感文件到公开仓库。

上传目标结构：

- `library/prompts/<slug>/meta.json`
- `library/prompts/<slug>/prompt.md`
- `library/prompts/<slug>/images/cover.webp`（多封面依照该素材自身 `meta.json` 管理）

GitHub Git Data API 的关键操作顺序：

`create_blob(image, base64)` → `create_blob(meta/prompt, utf-8)` → `GET refs/heads/main` → `GET git/commits/<HEAD>` → `create_tree(base_tree_sha)` → `create_commit(parent_sha=HEAD)` → `update_ref(main, force=false)` → `fetch_file / HEAD / Actions` 验证。

## 三、为什么前面失败，本次却成功

| 现象或误区 | 真实原因 | 正确做法 |
| --- | --- | --- |
| GitHub 只能传文字，不能直接上传图片 | 只看到了 `create_file`（UTF-8 文本接口），忽略 `create_blob` 支持 Base64 二进制 | 采用 Git Data Blob 接口，不用 `create_file` 承载二进制 |
| 本地生成的 WebP 路径不能给 GitHub | 图片位于会话文件环境，GitHub 连接不共享这块文件系统 | 通过临时 Base64 文本文件/可用文件连接器传递图片字节 |
| 文件连接器刚上传就提示文件不可见 | 文件可见性索引尚未出现在当前读取上下文 | 先使用文件列表获取可见文件 ID，再分段读出内容 |
| 长 Base64 读出不完整 | 文件读取可能被分段或截断，输出也有长度限制 | 工具内部循环分段读取，核对全部行数、编码长度和 Blob SHA |
| 图片已转成 WebP 就算上传成功 | 仅本地存在，与 GitHub 仓库无关 | GitHub 目录真实存在且 Blob SHA 一致才算入库 |
| `update_ref` 返回成功就算发布成功 | `main` 提交和 Pages 部署是两个阶段 | 必须检查对应 Actions 的最终 `success` |
| 用小预览图冒充高清封面 | 文件虽存在但损失用户要求的分辨率 | 保存原始像素尺寸的 WebP；缩略图只能做衍生图 |
| 无法直传就让用户下载 ZIP、到 Issue 再上传 | 这是兜底流程，增加人工操作 | **优先尝试已验证的直传链路，确认当前能力不可用时才提供 Issue 备用方案** |

## 四、备用方案：GitHub Issue + Actions

只有直传链路确实不可用时，再使用现存的 [Issue 表单与 Actions 机制](../../../README.md)。GitHub Issue 的附件需是真实 `user-attachments` 链接；只提交本地文件名、沙盒路径或 `upload:1` 但没有附件会失败。以前 Issue #19 经 Issue #21 复用真实附件后成功；Issue #13 因未实际附加文件而失败。

项目已经支持将**只含一张 WebP** 的 ZIP 上传到 `[待上传封面]` Issue 评论，由 Actions 解包并存储原 WebP。这是备用，不应代替默认直传。

## 五、面向以后会话的执行准则

- 用户说“加入项目 / 提交图片 / 用高清图作为封面”，优先按照第二节直传，无须先建议用户手动操作。
- 要继续使用已有仓库 `yuqiangdede/ai-image-prompt-library`，默认提交 `main`；不无故新建重复条目或替换已有其他封面。
- 保存的是**当前实际生成图**，不从网络搜索无关图片替代封面；若本次用户提供多张图，按要求逐张入库并维护 `images` / `cover`。
- 用户要求“不要发布”时，应区分“不要主动执行发布”与 `main` 推送自动触发 Pages 的仓库既有配置；必须事先说明这一客观机制，不能假称提交 `main` 却不会触发站点发布。
- 提交前校验真实路径和素材内容；提交后提供 Commit、封面 GitHub 路径、Actions 最终状态。**未完成就明确说明，不能把准备文件、创建 Issue、创建 Blob、成功提交和部署成功混为一谈。**
- 环境接口日后可能变化；此文记录的是 2026-11-18 已验证的可行流程。遇到失败先重新发现当前可用的连接器能力，不得未经排查就断言“无法上传图片”。

## 六、相关事实链接

- [本次 Git 提交](https://github.com/yuqiangdede/ai-image-prompt-library/commit/9982171bae78268b44c3fa10a2f8812c87ec715a)
- [仓库中的高清封面](https://github.com/yuqiangdede/ai-image-prompt-library/blob/main/library/prompts/mint-butterfly-hanfu-portrait/images/cover.webp)
- [成功的 GitHub Actions 运行](https://github.com/yuqiangdede/ai-image-prompt-library/actions/runs/44186525628)
- [本次中转 Issue #22（已关闭）](https://github.com/yuqiangdede/ai-image-prompt-library/issues/22)
- [Issue #19 的历史故障记录](https://github.com/yuqiangdede/ai-image-prompt-library/issues/19)
