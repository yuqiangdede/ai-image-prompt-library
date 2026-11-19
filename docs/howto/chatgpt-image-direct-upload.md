# ChatGPT 生图加入图库：高清图片直传 GitHub 的完整操作手册（SOP）

> **适用仓库**：[`yuqiangdede/ai-image-prompt-library`](https://github.com/yuqiangdede/ai-image-prompt-library)  
> **维护日期**：2026-11-19  
> **默认路径**：直接提交 `main`，使用真实高清图作为封面，不要求用户重复下载/上传。  
> **适用任务**：新增 Prompt、替换 Prompt/Skill 的封面、给已有条目追加多张效果图。  
> **历史经验**：[2026-11-18 高清图直传成功与故障复盘](../pocket/pitfalls/2026-11-18-chatgpt-image-direct-upload.md)。

## 1. 一页看懂：最终要完成什么

```
用户的提示词 + 当前会话真正生成的高清图片
  ↓
检查标题/slug/已有条目 → 图片转 WebP（不缩小像素） → 准备 meta.json、prompt.md
  ↓
图片字节 → Base64 文本中转 → GitHub create_blob(base64)
  ↓
验证本地 Git Blob SHA = GitHub Blob SHA
  ↓
create_tree(图片+元数据+提示词) → create_commit → update_ref(main)
  ↓
确认 main HEAD、三份文件、元数据引用、图片 SHA
  ↓
确认 GitHub Actions push 构建及 Pages 部署最终 success
  ↓
清理 Base64 中转文件 → 汇报成功/未完成项
```

**绝不能混淆四种状态**：①本地 WebP 已准备；②GitHub Blob 已建立；③`main` 已包含完整素材；④GitHub Pages 已部署成功。前一项完成，不等于后一项完成。

### 1.1 项目保存结构

```text
library/prompts/<slug>/
├── meta.json             # 标题、简介、分类、标签、封面路径、图片列表
├── prompt.md             # 用户确认的完整提示词，保留关键约束
└── images/
    ├── cover.webp        # 当前主封面，保存真实高清图
    └── ...               # 可选的其他效果图
```

Skill 采用 `library/skills/<slug>/`，正文为 `SKILL.md`，其余封面更新原则相同。`<slug>` 仅使用小写英文字母、数字与中划线。相对图片路径通常为 `images/cover.webp`。

## 2. 准备工作与前置核对

1. **以本次任务为准**：明确新增、替换封面，还是保留旧封面并追加图片；确认是否要求“不发布”。当前仓库 `main` 的 `push` 会触发 Pages 工作流，所以不能承诺“推到 main 但完全不触发发布”。
2. **确认原始图片**：只能使用本次会话中的实际生图结果或用户明确指定的参考/效果图片。先通过文件工具确认文件路径和字节真实存在。不能把示例路径当成实际附件，不能搜索一张不相关的网图替代。
3. **核对同名条目**：先查目标 `library/prompts/<slug>/meta.json`，避免新建重复条目。替换时先读取原 `meta.json`，保留无关字段、旧图及关联关系（除非用户要求删除）。
4. **核对提示词**：保存用户实际提供的最终版本；不改写成几句简略摘要。若内容不可完整恢复，应标注来源限制，不可声称“原文保存”。
5. **确认权限**：GitHub 连接器要有该仓库写权限。不要把 PAT、Cookie 或其他密钥写进公开仓库、聊天文字或 Issue。

## 3. 第一步：将真正的高清图准备为 WebP

### 3.1 使用仓库内辅助脚本（推荐）

脚本：[`scripts/prepare_chatgpt_cover.py`](../../scripts/prepare_chatgpt_cover.py)。它完成**不缩放像素的 WebP 转换、Base64 文本生成、SHA 与清单计算**，不调用 GitHub，也不发送文件。

需要 Python 3.10+，并在使用脚本的环境安装 Pillow（这是图片准备的可选依赖，图库构建本身仍使用原来的依赖）。

```bash
# 文件：命令行执行示例（不是仓库新增的 .sh 文件）
python -m pip install Pillow
python scripts/prepare_chatgpt_cover.py /真实路径/生成图片.png \
  --output /tmp/gallery-upload/cover.webp \
  --quality 93
```

示例输出：

```text
/tmp/gallery-upload/cover.webp                  高清封面（不缩小分辨率）
/tmp/gallery-upload/cover.webp.b64.txt          Base64 文件中转文本
/tmp/gallery-upload/cover.webp.manifest.json    尺寸/字节数/Blob SHA/文件 SHA-256
```

脚本会保留原图的宽高像素；没有开启“AI 放大”或二次缩放。`quality=93` 只是推荐参数，和历史上传使用的压缩参数可能不同，因此**相同 PNG 重新编码后的 WebP Blob SHA 可能不同**。原图是 WebP 时，脚本保留其文件字节。

### 3.2 必查项目

- 宽、高、纵横比：例如 9:16 竖图应保持纵幅，不旋转、不拉伸。
- 文件大小：本项目公开上传流程按单张不超过 8 MiB 控制；如超出，调整编码质量，而不是首先缩小分辨率。
- 质量：细叶片、毛发、渐变等细节不能变成明显涂抹或色块。必要时保留原 PNG 作为本地来源，不要把小缩略图作为高清封面上传。
- 哈希：清单里的 `git_blob_sha1` 是后续对照用的**Git Blob SHA**；`sha256` 是文件内容校验值，二者不相同。

Git Blob 的计算方法：

```python
# 文件：scripts/prepare_chatgpt_cover.py（核心计算逻辑节选）
import hashlib

def git_blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()
```

## 4. 第二步：准备素材数据（meta.json + prompt.md）

先选稳定、无冲突的 slug。例如本次素材：`autumn-canopy-blue-sky-upward-photography`。

`prompt.md` 必须包含完整提示词；新素材的 `meta.json` 至少应填写标题、简介、分类、标签、模型、封面和图片列表。

```json
// 文件：library/prompts/<slug>/meta.json（示意；写入时去掉本行注释）
{
  "title": "仰望秋日树冠 · 五彩秋叶与湛蓝天空｜极简仰拍自然风光摄影",
  "description": "9:16 仰拍秋日树冠与蓝天的真实风光摄影",
  "category": "风景摄影",
  "tags": ["秋叶", "蓝天", "仰拍", "风光摄影"],
  "model": "GPT 图像生成",
  "updated_at": "2026-11-19",
  "cover": "images/cover.webp",
  "images": ["images/cover.webp"],
  "related_skills": []
}
```

**注意**：这个 JSON 只作字段格式示例，不能拿它代替具体素材的完整提示词或现有元数据。图片放在条目目录的 `images/` 下；网站构建器会检查图片路径是否真实存在。

## 5. 第三步：跨过“图片文件与 GitHub 连接器磁盘不共享”这道坎

这是整个流程最容易失败的环节。ChatGPT 中生成的图片可能在 `/mnt/data/...`，但是 GitHub 连接器**不能直接读取这一条本地路径**。正确方法是把图片字节变成 Base64 文本，通过当前会话可用的文件连接器中转，再把完整 Base64 传给 GitHub 的二进制 Blob 接口。

### 5.1 使用文件库作为临时桥（本项目已实际跑通）

1. 本地生成 `cover.webp.b64.txt`（辅助脚本已完成），记录清单中的 `base64_chars`、`base64_lines`、`webp_bytes`、`git_blob_sha1`。
2. 使用文件连接器的 `files__manage_library`，对该**真实存在**的文本文件执行 `upload(container_path=..., destination_path=...)`。这是临时中转，不是把文件当成图库封面。
3. 从上传结果取得真实 `file_id` / `library_file_id`。如读取接口尚看不见文件，可先在 Library 执行 `files__list`，找到最新的中转文件。
4. 用 `files__read` 以 `start_line` + `max_lines` 分段读取。可每段读 50–100 行，必要时并行读取不同区间，再**严格按起始行排序**。
5. 每段检查 `start_line`、`end_line`、`total_lines`；所有区间必须连续，不得缺失或重叠。读取结果的 `content` 可能是含多行文本的一个字符串，不可误认为每个数组元素只有一行。
6. 拼接所有文本后只移除 Base64 的换行/空白字符，检查：长度等于清单的 `base64_chars`、长度可被 4 整除、字符集合法、解码后字节数等于 `webp_bytes`、解码内容的 Git Blob SHA 与清单一致。
7. **不要**把几十万字符的 Base64 直接打印进聊天窗口或普通模型回复；输出会被截断，污染对话，还不能保证再读取完整。应在同一次工具编排中读取、拼接、验证并传给 GitHub。

调用结构示意（实际工具参数以当前连接器定义为准）：

```json
// 文件：连接器请求示例（伪代码，不是可直接提交的 JSON 文件）
{
  "operations": [{
    "operation": "upload",
    "container_path": "/tmp/gallery-upload/cover.webp.b64.txt",
    "destination_path": "/tmp-gallery-cover-bridge.txt"
  }]
}
```

```json
// 文件：分段读取请求示例（替换为真实返回的 file_id）
{
  "read": [{
    "ref_id": "真实的_file_id",
    "start_line": 1,
    "max_lines": 70
  }]
}
```

### 5.2 不能使用的错误方式

- 把 `/mnt/data/cover.webp` 写进 `meta.json`：GitHub Pages 找不到这张图。
- 用 GitHub `create_file` 或 `update_file`（专为 UTF-8 文本）来写入 WebP 二进制：会失败或损坏。
- 将 Base64 字符串本身当作图片 URL 或将 `.b64.txt` 当作封面。
- 长字符串分段读出后，未核对总行数与 SHA 就直接提交。

## 6. 第四步：通过 GitHub Git Data API 提交真实图片和文本

### 6.1 创建 GitHub Blob

对图片调用 `create_blob`，**必须**传 `encoding="base64"`；`content` 是上一步完整拼接的 Base64 字符串。GitHub 返回图片 Blob SHA 后，立即与清单的 `git_blob_sha1` 比较。不一致则停止，不能继续提交。

`meta.json` 和 `prompt.md` 是 UTF-8 文本，应分别调用 `create_blob(encoding="utf-8")`，取得各自 SHA。

### 6.2 使用最新 main 构造 Tree

- 获取**此时最新** `refs/heads/main` HEAD commit SHA，以及该 commit 对应的基础 Tree SHA。
- 首选 `create_tree(base_tree_sha=<基础 Tree SHA>)`，将三条文件写入一个新树（图片、元数据、提示词）。不要建立空白根树覆盖现有素材。
- 如果当前 GitHub 连接器只提供 HEAD Commit 而不直接提供 Tree SHA，先核对当前接口的参数行为；**2026-11-19 的实际连接器曾接受 HEAD SHA 作为 `base_tree_sha` 并成功建立新树，但不保证所有 GitHub 客户端都这么支持**。能取 Tree SHA 时优先用 Tree SHA。
- Tree entry 固定包含 `path`、`mode="100644"`、`type="blob"`、`sha=<对应 Blob SHA>`。

三个路径示例：

```text
library/prompts/autumn-canopy-blue-sky-upward-photography/images/cover.webp
library/prompts/autumn-canopy-blue-sky-upward-photography/meta.json
library/prompts/autumn-canopy-blue-sky-upward-photography/prompt.md
```

### 6.3 创建 Commit，再更新 main

1. `create_commit(message=..., tree_sha=<新 Tree>, parent_sha=<最新 HEAD>)` 得到新的提交 SHA。
2. `update_ref(branch_name="main", sha=<新提交 SHA>, expected_sha=<旧 HEAD>, force=false)`，禁止强推覆盖别人的修改。
3. 如果主分支已被其他人/Actions 推进，按新 HEAD **重新取得基础 Tree、重新创建 Tree/Commit**，再安全更新，不能强制覆盖。
4. 用户要求新增多图时，可在同一次 Tree 中列出多张图片 Blob；`images` 数组存全部图片，`cover` 指向指定的主封面。
5. 替换已有封面时，除目标路径、相关元数据外，保留其他图片和关联信息；不要误删历史效果图。

**注意**：只创建 Blob 不会让文件出现在仓库里；只有 Tree/Commit/main 三个动作完成后，才算真正入库。

## 7. 第五步：三层验收，尤其不能漏掉 Pages

| 层级 | 必须检查 | 成功条件 |
| --- | --- | --- |
| ① Git | 重新读取 `main` HEAD、提交记录 | HEAD 确实指向新增提交（或之后包含该提交的更新） |
| ② 文件 | `fetch_file` 逐个读取 `cover.webp`、`meta.json`、`prompt.md` | 三份文件实际存在；WebP Blob SHA 与本地清单一致；`cover` / `images` 相对路径正确；提示词正文完整 |
| ③ 发布 | 检查该次 push 触发的 `.github/workflows/pages.yml` | 对应运行 `status=completed` 且 `conclusion=success`，必要时打开在线图库确认新素材可见 |

**重要陷阱：** 当前某些 GitHub 连接器的 `fetch_commit_workflow_runs` 只返回 PR 事件。我们是直接推送 `main`，所以返回 `workflow_runs=[]` **不代表没触发 Actions，也不代表部署成功或失败**。`get_commit_combined_status` 返回空列表也不能代替 Actions 验收。

如果连接器无法查询 push 类型运行记录，使用仓库的 [GitHub Actions 页面](https://github.com/yuqiangdede/ai-image-prompt-library/actions/workflows/pages.yml)，按 HEAD SHA 或最新 push 找到构建；具备 GitHub CLI 环境时也可以：

```bash
# 文件：终端验收命令（示例）
REPO=yuqiangdede/ai-image-prompt-library
SHA=替换为提交SHA
gh run list --repo "$REPO" --workflow pages.yml --commit "$SHA"
gh run view 运行ID --repo "$REPO" --json status,conclusion,headSha,event,url
```

**只在实际看到对应运行最终 `success` 后说“发布成功”**。无法查询时必须明确写“main 已提交，Pages 尚未验证”；不应补造运行编号。

## 8. 第六步：清理临时中转和汇报

- 完成提交后，在文件库删除临时 `.b64.txt` 中转记录，并按需要清理容器内临时文件。连接器可能只返回 `moved to trash`，只能说“已移到回收站”，不能说“彻底永久删除”。
- 本地 PNG 可以由用户自行保留；仓库默认仅存压缩后的高清 WebP，不添加随意来源的图片。
- 向用户提供：**素材名、slug、分类、图片尺寸、WebP 大小、封面地址、完整提示词地址、Commit 链接、Actions 状态**。三层验证未通过的部分要如实说明。
- 如果用户明确要求不发布，应先说明 `main` push 自动触发部署；按用户要求选择暂不推 `main` 或另行处理，不能误报。

## 9. 真实案例：2026-11-19 秋日树冠摄影

本案例是一次**确实完成图片直传、三文件入库和 main 提交**的实践，关键数值如下：

| 项目 | 本次实际值 |
| --- | --- |
| 素材标题 | 仰望秋日树冠 · 五彩秋叶与湛蓝天空｜极简仰拍自然风光摄影 |
| slug | `autumn-canopy-blue-sky-upward-photography` |
| 原始像素 | 941 × 1672（竖幅接近 9:16） |
| WebP 字节数 | **667,818 bytes**（约 652 KiB） |
| Base64 字符数 | **890,424** |
| 中转文本行数 | **928 行** |
| Git 图片 Blob SHA | `c8e0cca17893e617e4545a2c46526107ff59f59c` |
| main Commit SHA | `d2d1151557403bdbc5302b4cdd37c54ccb6a3e03` |
| 元数据 Blob SHA | `3abbd71c6445220898379ce5f749e130aeb0e713` |
| 提示词 Blob SHA | `c431dc5af5791d37bd4ee0e066b327eaf8e7d517` |

- [查看提交](https://github.com/yuqiangdede/ai-image-prompt-library/commit/d2d1151557403bdbc5302b4cdd37c54ccb6a3e03)
- [查看仓库真实高清封面](https://github.com/yuqiangdede/ai-image-prompt-library/blob/main/library/prompts/autumn-canopy-blue-sky-upward-photography/images/cover.webp)
- [查看仓库内完整中文提示词](https://github.com/yuqiangdede/ai-image-prompt-library/blob/main/library/prompts/autumn-canopy-blue-sky-upward-photography/prompt.md)
- [在线图库](https://yuqiangdede.github.io/ai-image-prompt-library/)

本次已重新读取 GitHub 三份文件，图片 SHA 与本地原始 WebP **完全一致**，`main` HEAD 指向提交。**截至当时的连接器验收，未拿到该次 push 对应的 Actions 最终记录，因此不能将“已提交”写成“已证实 Pages 发布成功”**。之后需要按第 7 节补查 Actions。

注意：辅助脚本是事后整理出来的**以后推荐流程**，默认质量参数与这次实际转换的设置未必相同；不要用新脚本重新编码后的 SHA 冒充这次的历史 SHA。

## 10. 故障定位顺序与备用通道

| 故障 | 优先检查与处理 |
| --- | --- |
| 图片路径交给 GitHub 报错 | 本地/连接器磁盘不共享；使用 Base64 文本桥，不能直接传 `/mnt/data/...` |
| `create_file` 上传图片失败 | 用 `create_blob`，明确 `encoding=base64` |
| 中转文件刚上传但读取不到 | 使用 `files__list` 找真实 `file_id`，再分段读取 |
| Base64 长度对不上 | 检查总行数、每段起止行、内嵌换行及读取截断；缺少一行就重读 |
| 图片 Blob SHA 不一致 | 停止提交，重新核算解码字节和 Git Blob 算法；不能忽略 |
| 只创建了 Blob，但图库没图 | 核对 Tree → Commit → main ref 三步，且相对路径正确 |
| `update_ref` 冲突 | 获取最新 main/Tree，重建 commit；绝不强推 |
| Actions 查询为空 | 确认是不是只筛 PR 的接口；改查 push workflow 运行及日志 |
| Actions 构建失败 | 查看日志（常见：缺 `meta.json`/`prompt.md`、图片路径错、slug 不合法） |
| 新图看不见 | 先核对 Pages 部署成功，再清缓存/刷新，核对 `dist/data/catalog.json` |

**备用通道仅限直传确实不可用时**：按仓库 README 的 `[待上传封面]` Issue + 单张 WebP ZIP 附件 + Actions 流程办理。Issue 必须含**真正上传后由 GitHub 产生的附件链接**；本地路径和单纯文字 `upload:1` 均无效。已有素材的修改应走相应管理 Issue，避免重复创建新条目。

## 11. 下次直接复制的请求口令

> 把当前生成图片及完整中文提示词加入 `yuqiangdede/ai-image-prompt-library`，默认直接提交 `main`，以当前原始高分辨率图转换为高清 WebP 主封面（不缩小像素），先查重。严格按 `docs/howto/chatgpt-image-direct-upload.md` 操作：生成 WebP、Base64 中转、校验 Git Blob SHA，提交图片 + `meta.json` + `prompt.md`，确认主分支及文件全部存在；再核对 Actions 的 push 部署结果。不要让我重新手工上传图片，不要把本地路径当图片地址，任何环节没完成就明确说明；最终给出 Commit、高清封面、完整提示词和部署状态。

**统一原则**：先实际尝试直传并完成 SHA 验收，再考虑备用方案。历史经验只能作为参考；本次仓库内容、连接器能力和 Actions 结果始终以实时检查为准。
