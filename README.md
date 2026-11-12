# AI 生图 Prompt / Skill 图库

以图片为入口的 Prompt 与 Agent Skill 资料库。无需 VPS、数据库或生图 API。GitHub 保存文本与图片，GitHub Pages 提供手机和电脑都能访问的响应式图库。

- **图库**：搜索、分类、效果图查看、复制 Prompt / Skill 指令、下载完整 Skill ZIP、本地收藏。
- **上游关联**：Skill 可绑定原始 GitHub 仓库，展示作者、来源地址、同步 Commit。
- **自动同步**：GitHub Actions 每天检查并同步允许再分发的上游 Skill 文本、配置与脚本；保留本地 `meta.json` 和封面设置。
- **来源与版权**：上游图片许可可能不同于 Skill 文本许可；默认不镜像第三方参考图片。本站示例的斑马封面直接引用上游官方图片地址。

## 在线地址

https://yuqiangdede.github.io/ai-image-prompt-library/

如首次打开为 404，请在仓库的 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**，再从 Actions 页面运行“Deploy Prompt & Skill Gallery”。

## 素材结构

```text
site/                            网页代码
library/prompts/<slug>/          Prompt：meta.json、prompt.md、images/
library/skills/<slug>/           Skill：meta.json、SKILL.md、references/、scripts/等
library/skills/<slug>/upstream.json  上游仓库、分支和已同步 SHA
scripts/build_site.py            校验素材、生成索引和 ZIP
scripts/sync_upstream.py          检查并同步上游 Skill
.github/workflows/pages.yml      自动更新、构建和部署
```

## 日常操作

**添加提示词**：在 `library/prompts/` 新建目录，放入 `prompt.md`、`meta.json` 和 `images/` 下人工上传的效果图，提交 `main` 后自动发布。

**添加 Skill**：在 `library/skills/` 新建目录，放入完整 `SKILL.md`、配套资源和 `meta.json`。来自 GitHub 的 Skill 可增加 `upstream.json` 来启用定时同步。

**修改封面**：调整 `meta.json` 的 `cover` / `images`。上游同步不会修改本地 `meta.json`。

**手动同步上游**：仓库的 Actions → Deploy Prompt & Skill Gallery → Run workflow → 选择“同步上游”。

**本地预览**（Python 3.10+）：

```sh
python scripts/build_site.py
python -m http.server 8000 --directory dist
```

浏览器访问 http://localhost:8000。

## 版权与安全

`yanliudesign/mono-color-skill` 的 Skill 指令、代码和配置采用 MIT，须保留原作者许可。它的 `examples/` 艺术作品不包含在 MIT 授权范围内，**禁止未经授权复制到本站公开仓库**，本站仅链接原始资源 URL。

自动同步仅复制白名单中的文本、配置、SVG 色板和脚本，**不会在 CI 中执行上游脚本**。上游更新若更改许可证或违反白名单校验，同步应当失败以等待人工处理。公开仓库不应存储私人照片、私密提示词或访问密钥。

## 部署检查

- 提交到 `main` 触发部署。
- 每日按 UTC 定时检查上游更新；只有内容改变才提交 SHA/资源变更。
- 定时工作流部署是在**同一次工作流**完成的，因为 GITHUB_TOKEN 推送的提交不会自动再次触发工作流。
- 如果账户/仓库的 GitHub Actions 工作流写入权限被关闭，需要在 Settings → Actions → General 允许写入。

项目使用原生 HTML/CSS/JS 和 Python 标准库。
## 只填 GitHub 原 Skill 地址，自动生成并发布

首页新增“通过 GitHub 地址自动添加 Skill”入口。复制原作者仓库地址，点击“自动添加 Skill”；浏览器会打开 **GitHub Issue 表单**（自动填好地址），仓库所有者登录后点击提交，就会触发 GitHub Actions 自动添加并发布。

自动识别公开仓库中的 SKILL.md、README 与 frontmatter；生成标题、简介、分类、标签、封面链接（如原仓库没有合适图片则用默认占位图）、安装命令、meta.json、upstream.json 和独立编写的 SKILL.md 索引。**不复制上游完整源代码、参考图或不明授权文件**。上游 SHA 每日自动更新。

注意事项：
- **需要在 GitHub 页面确认提交一次**：GitHub Pages 是静态网站，不能直接向仓库写入，也不应该在网页里保存个人 Token。
- 为防止公开仓库被其他人恶意添加，只有所有者 `yuqiangdede` 提交且标题为 `[导入 Skill]` 的 Issue 能触发自动导入。
- 原仓库有多个 `SKILL.md` 时，提供单个 Skill 文件的链接，否则会明确拒绝以防误导入。
- 导入成功会在 Issue 中回复并自动关闭；失败则回复错误排查提示，可到 Actions 查看详细日志。
- Skill 没有明确授权时只做 `link-only` 索引；复制安装命令仅适用于支持 Skills 的 Agent 环境，不会自动安装到 ChatGPT 网页。

核心实现：`scripts/import_skill.py`、`.github/ISSUE_TEMPLATE/add-skill.yml`、`.github/workflows/pages.yml`。

## 手工添加 Skill（不用命令行）

以“营造 Yingzao”为例，所有操作都可在 GitHub 网页完成：

1. 打开仓库 `library/skills/`，选择 **Add file → Create new file**。先创建 `<slug>/meta.json`，提交时选择 `main`。GitHub 不能上传空目录，新建路径时用斜杠分隔。
2. 同目录创建 `SKILL.md`。**只有得到原作者许可且许可允许再分发时**，才复制完整 Skill 与配套文件；否则仅写原创介绍与原项目链接，并在 `meta.json` 设置 `"external_only": true`。
3. 有上游来源时，再创建 `upstream.json`。明确许可的 MIT 项目可使用已支持的 `allowlisted-mit-text`；许可不明确的项目用 `link-only`，每天只核对上游 Commit，不复制文件。
4. 封面可放在 `library/skills/<slug>/images/`：进入对应目录，点击 **Add file → Upload files** 上传图片，然后将 `meta.json` 中的 `cover` 和 `images` 设为 `images/cover.jpg` 等路径。也可使用原项目允许公开引用的 HTTPS GitHub 图片 URL。
5. 检查 Actions → **Deploy Prompt & Skill Gallery** 是否执行成功，然后刷新 [GitHub Pages 图库](https://yuqiangdede.github.io/ai-image-prompt-library/)。

`external_only` Skill 可填写 `install_command`，详情页会显示“复制安装命令”，不会提供内容不完整的 ZIP。不要误以为在 ChatGPT 网页中粘贴安装命令就完成 Skill 安装；应在支持 Skills 的 Agent/终端中运行。

### 营造 Yingzao 示例

完整文件目录：
- `library/skills/yingzao/meta.json`：名称、标签、封面、安装命令
- `library/skills/yingzao/SKILL.md`：原创索引和使用说明
- `library/skills/yingzao/upstream.json`：上游链接与每日 Commit 跟踪

该上游暂未发现明确的根目录 `LICENSE`，因此采用 `link-only`，而不是复制上游的参考图、Python 脚本或完整指令。
