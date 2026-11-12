/* Static responsive Prompt and Skill gallery. No API keys or third-party JS. */
(() => {
  "use strict";
  const $ = id => document.getElementById(id);
  const state = { items: [], catalog: null, search: "", kind: "all", category: "all", sort: "new", view: "large", favorites: new Set(), selected: null, text: "", manage: null };
  const favoriteKey = "prompt-gallery-favorites-v2";
  const viewKey = "prompt-gallery-view-v1";
  const escapeHtml = text => String(text ?? "").replace(/[&<>"']/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" })[c]);
  const address = path => String(path || "").startsWith("https://") ? path : "./" + String(path || "").split("/").map(encodeURIComponent).join("/");
  const typeName = item => item.kind === "skill" ? "SKILL" : "PROMPT";
  let timer;

  try { state.favorites = new Set(JSON.parse(localStorage.getItem(favoriteKey) || "[]")); } catch { state.favorites = new Set(); }
  try {
    const savedView = localStorage.getItem(viewKey);
    if (savedView === "large" || savedView === "small") state.view = savedView;
  } catch { state.view = "large"; }
  function showToast(message) {
    $("toast").textContent = message;
    $("toast").hidden = false;
    clearTimeout(timer);
    timer = setTimeout(() => $("toast").hidden = true, 2300);
  }
  function saveFavorites() {
    try { localStorage.setItem(favoriteKey, JSON.stringify([...state.favorites])); }
    catch { showToast("此浏览器暂时无法保存收藏"); }
  }
  function syncScrollLock() {
    document.body.style.overflow = (!$("detail-modal").hidden || !$("skill-import-modal").hidden || !$("skill-manage-modal").hidden) ? "hidden" : "";
  }
  function applyView(persist) {
    $("gallery").dataset.view = state.view;
    document.querySelectorAll(".view-switch [data-view]").forEach(node => {
      node.setAttribute("aria-pressed", String(node.dataset.view === state.view));
    });
    if (!persist) return;
    try { localStorage.setItem(viewKey, state.view); }
    catch { showToast("此浏览器暂时无法记住图标大小"); }
  }
  function listFiltered() {
    const q = state.search.trim().toLocaleLowerCase();
    return state.items.filter(item => {
      if (state.kind === "favorites" && !state.favorites.has(item.id)) return false;
      if (state.kind !== "all" && state.kind !== "favorites" && state.kind !== item.kind) return false;
      if (state.category !== "all" && state.category !== item.category) return false;
      if (q && ![item.title, item.description, item.category, item.model, ...(item.tags || []), item.search_text].join(" ").toLocaleLowerCase().includes(q)) return false;
      return true;
    }).sort((a, b) => state.sort === "az"
      ? a.title.localeCompare(b.title, "zh-CN")
      : String(b.updated_at).localeCompare(String(a.updated_at)) || a.title.localeCompare(b.title, "zh-CN"));
  }
  function renderCategories() {
    const counts = new Map();
    for (const item of state.items) counts.set(item.category, (counts.get(item.category) || 0) + 1);
    const categories = [["全部主题", "all", state.items.length], ...[...counts].sort((a,b) => a[0].localeCompare(b[0],"zh-CN")).map(([name,count]) => [name,name,count])];
    $("category-nav").innerHTML = categories.map(([label,value,count]) =>
      '<button type="button" data-category="' + escapeHtml(value) + '" class="' + (state.category === value ? "active" : "") + '">' + escapeHtml(label) + '<span class="count">' + count + "</span></button>"
    ).join("");
  }
  function render() {
    const results = listFiltered();
    $("count-all").textContent = state.items.length;
    $("hero-count").textContent = state.items.length;
    $("count-skill").textContent = state.items.filter(x => x.kind === "skill").length;
    $("count-prompt").textContent = state.items.filter(x => x.kind === "prompt").length;
    $("count-favorites").textContent = state.favorites.size;
    $("result-count").textContent = "共 " + results.length + " 个结果";
    $("reset-filter").hidden = state.kind === "all" && state.category === "all" && !state.search;
    document.querySelectorAll("#nav-tabs [data-type]").forEach(node => node.classList.toggle("active", state.kind === node.dataset.type));
    renderCategories();
    if (!results.length) {
      $("gallery").innerHTML = '<div class="empty">暂无匹配的素材<p>试试其他关键词，或清除筛选条件。</p></div>';
      return;
    }
    $("gallery").innerHTML = results.map(item => {
      const image = item.cover
        ? '<img loading="lazy" src="' + escapeHtml(address(item.cover)) + '" alt="' + escapeHtml(item.title) + ' 效果图">'
        : '<span class="image-fallback">✳</span>';
      const chips = (item.tags || []).slice(0, 2).map(tag => '<span class="chip">' + escapeHtml(tag) + "</span>").join("");
      const fav = state.favorites.has(item.id);
      return '<article class="gallery-card"><button class="gallery-card-open" type="button" data-open="' + escapeHtml(item.id) +
        '"><div class="image-wrap">' + image + '<span class="image-label">' + typeName(item) +
        '</span></div><div class="card-details"><h3>' + escapeHtml(item.title) + '</h3><p>' + escapeHtml(item.description) +
        '</p></div></button><div class="card-foot"><div class="chips">' + chips + '</div><button class="favorite-button ' +
        (fav ? "active" : "") + '" data-fav="' + escapeHtml(item.id) + '" aria-label="' + (fav ? "取消收藏" : "收藏") +
        '">' + (fav ? "♥" : "♡") + "</button></div></article>";
    }).join("");
  }
  function selectImage(path) {
    $("detail-hero").innerHTML = path
      ? '<img src="' + escapeHtml(address(path)) + '" alt="选中效果图的高清预览">'
      : "未上传效果图";
    document.querySelectorAll("#detail-thumbs button").forEach(el => el.classList.toggle("active", el.dataset.image === path));
  }
  function replaceItemQuery(id) {
    const url = new URL(location.href);
    if (id) url.searchParams.set("item", id);
    else url.searchParams.delete("item");
    history.replaceState({}, "", url);
  }
  async function openItem(id, updateQuery = true) {
    const item = state.items.find(x => x.id === id);
    if (!item) return showToast("找不到此条素材");
    state.selected = item;
    state.text = "";
    $("detail-kind").textContent = typeName(item) + " / " + item.category;
    $("detail-title").textContent = item.title;
    $("detail-description").textContent = item.description;
    $("detail-tags").innerHTML = (item.tags || []).map(t => "<span>" + escapeHtml(t) + "</span>").join("");
    $("detail-meta").innerHTML = "<div>适用模型<strong>" + escapeHtml(item.model) + "</strong></div><div>图库更新时间<strong>" + escapeHtml(item.updated_at) + "</strong></div>";
    $("detail-thumbs").innerHTML = (item.images || []).map(path =>
      '<button type="button" data-image="' + escapeHtml(path) + '" aria-label="切换预览图片"><img loading="lazy" src="' +
      escapeHtml(address(path)) + '" alt="效果图缩略图"></button>').join("");
    selectImage(item.cover || (item.images || [])[0] || "");
    $("source-box").hidden = !item.source_url;
    if (item.source_url) {
      $("upstream-link").href = item.source_url;
      $("upstream-link").textContent = item.source_url.replace("https://github.com/", "") + " ↗";
      $("upstream-sha").textContent = item.source_sha ? "上游 Commit: " + item.source_sha.slice(0, 12) + " / " + item.source_branch : "查看原始项目与授权说明";
    }
    const related = item.kind === "prompt"
      ? state.items.filter(x => x.kind === "skill" && (item.related_skills || []).includes(x.slug))
      : state.items.filter(x => x.kind === "prompt" && (x.related_skills || []).includes(item.slug));
    $("detail-related").innerHTML = related.map(x =>
      '<button type="button" data-related="' + escapeHtml(x.id) + '">关联' +
      (x.kind === "skill" ? " Skill" : " Prompt") + "：" + escapeHtml(x.title) + " ↗</button>"
    ).join("");
    const externalSkill = item.kind === "skill" && item.external_only === true;
    $("content-heading").textContent = externalSkill ? "使用说明（完整 Skill 位于上游仓库）" : item.kind === "skill" ? "SKILL.md 完整文本" : "完整 Prompt";
    $("detail-content").textContent = "正在读取内容…";
    $("copy-primary").textContent = externalSkill ? "复制安装命令" : item.kind === "skill" ? "复制给 ChatGPT 的 Skill 指令" : "复制完整 Prompt";
    $("copy-text").textContent = externalSkill ? "复制使用说明" : "仅复制原文";
    $("download-file").hidden = externalSkill;
    $("download-file").textContent = item.kind === "skill" ? "下载 Skill ZIP" : "下载 Prompt";
    $("detail-note").textContent = externalSkill
      ? "此条目只收藏作品图、项目入口与安装命令；未镜像上游 Skill 文件。请在支持 Skills 的 Agent 中运行安装命令，ChatGPT 网页对话中粘贴命令并不会自动安装。"
      : item.kind === "skill"
      ? "ZIP 保留 Skill 配套文本、设计配置与脚本；上游有版权限制的参考图片不在 ZIP 内。复制文本不会自动安装 Skill。"
      : "复制后可以直接粘贴到 ChatGPT 图片生成对话。";
    $("manage-box").hidden = !(item.kind === "skill" && (item.upstream_linked === true || item.source_url));
    $("open-source").href = externalSkill ? item.source_url : state.catalog.repository_url + "/blob/main/" + item.content_path.split("/").map(encodeURIComponent).join("/");
    $("open-source").textContent = externalSkill ? "到原项目查看完整 Skill ↗" : "在 GitHub 中打开 ↗";
    $("detail-modal").hidden = false;
    syncScrollLock();
    if (updateQuery) replaceItemQuery(id);
    try {
      const response = await fetch(address(item.content_path), { cache: "no-store" });
      if (!response.ok) throw new Error("HTTP " + response.status);
      const text = await response.text();
      if (state.selected?.id !== id) return;
      state.text = text;
      $("detail-content").textContent = text;
    } catch (error) {
      $("detail-content").textContent = "读取内容失败：" + error.message;
    }
  }
  function closeItem() {
    $("detail-modal").hidden = true;
    syncScrollLock();
    state.selected = null;
    state.text = "";
    replaceItemQuery("");
  }
  async function copyText(text) {
    if (!text) return showToast("内容尚未加载");
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        const node = document.createElement("textarea");
        node.value = text;
        node.style.cssText = "position:fixed;left:-9999px;top:0";
        document.body.append(node);
        node.select();
        const ok = document.execCommand("copy");
        node.remove();
        if (!ok) throw new Error("复制失败");
      }
      showToast("已复制到剪贴板");
    } catch { showToast("复制受限，请选择下方文本手动复制"); }
  }
  function download() {
    const item = state.selected;
    if (!item) return;
    const link = document.createElement("a");
    if (item.kind === "skill") {
      if (!item.skill_zip) return showToast("Skill ZIP 不可用");
      link.href = address(item.skill_zip);
      link.download = item.slug + ".zip";
    } else {
      if (!state.text) return showToast("Prompt 尚未加载");
      const blob = new Blob([state.text], { type: "text/markdown;charset=utf-8" });
      link.href = URL.createObjectURL(blob);
      link.download = item.slug + ".md";
      setTimeout(() => URL.revokeObjectURL(link.href), 3000);
    }
    document.body.append(link);
    link.click();
    link.remove();
  }
  function openSkillImport() {
    if (!$("detail-modal").hidden) closeItem();
    $("skill-repo-url").removeAttribute("aria-invalid");
    $("skill-import-error").hidden = true;
    $("skill-import-status").hidden = true;
    $("skill-import-modal").hidden = false;
    syncScrollLock();
    $("skill-repo-url").focus();
    $("skill-repo-url").select();
  }
  function closeSkillImport() {
    if ($("skill-import-modal").hidden) return;
    $("skill-import-modal").hidden = true;
    syncScrollLock();
    $("open-skill-import").focus();
  }
  function showImportError(message) {
    $("skill-repo-url").setAttribute("aria-invalid", "true");
    $("skill-import-error").textContent = message;
    $("skill-import-error").hidden = false;
    $("skill-repo-url").focus();
  }
  function manageImageUrl(raw) {
    let url;
    try { url = new URL(raw); } catch { return null; }
    if (url.protocol !== "https:" || url.username || url.password) return null;
    if (url.hostname === "raw.githubusercontent.com") return url.href;
    if (url.hostname !== "github.com") return null;
    const parts = url.pathname.split("/").filter(Boolean);
    if (parts[0] === "user-attachments" && (parts[1] === "assets" || parts[1] === "files")) return url.href;
    if (parts.length >= 5 && (parts[2] === "raw" || parts[2] === "blob")) {
      return "https://raw.githubusercontent.com/" + parts[0] + "/" + parts[1] + "/" + parts[3] +
        "/" + parts.slice(4).join("/") + url.search;
    }
    return null;
  }
  function manageFocus(selector) {
    const node = document.querySelector(selector);
    if (node) node.focus();
  }
  function renderManage() {
    const manage = state.manage;
    if (!manage) return;
    const images = manage.images;
    const tiles = images.map((image, index) => {
      const kept = image.kept;
      const cover = manage.cover === image.src;
      return '<figure class="manage-image' + (kept ? "" : " is-dropped") + '">' +
        '<div class="manage-image-frame">' +
        '<img loading="lazy" src="' + escapeHtml(address(image.src)) + '" alt="' +
        escapeHtml((image.isNew ? "新增图片 " : "图片 ") + (index + 1)) + '">' +
        (image.isNew ? '<span class="manage-image-badge">新增</span>' : "") +
        (kept ? "" : '<span class="manage-image-dropped">已移除</span>') +
        '</div><figcaption>' +
        '<label><input type="checkbox" data-manage-keep="' + index + '" aria-label="保留图片 ' +
        (index + 1) + '"' + (kept ? " checked" : "") + '> 保留</label>' +
        '<label><input type="radio" name="manage-cover" data-manage-cover="' + index +
        '" aria-label="将图片 ' + (index + 1) + ' 设为封面"' +
        (cover ? " checked" : "") + (kept ? "" : " disabled") + '> 封面</label>' +
        '</figcaption>' +
        (image.isNew ? '<button type="button" class="manage-image-remove" data-manage-remove="' + index +
          '" aria-label="移除这张新增图片">✕</button>' : "") +
        '</figure>';
    }).join("");
    const autoCover = images.length
      ? '<label class="manage-auto-cover"><input type="radio" name="manage-cover" data-manage-cover="auto"' +
        (manage.cover ? "" : " checked") + '> 新增图片优先作封面（含稍后上传）</label>'
      : "";
    $("manage-images").innerHTML = images.length
      ? tiles + autoCover
      : '<p class="manage-empty">当前没有图片。可以添加图片地址，或在 GitHub 表单中上传。</p>';
    const kept = images.filter(image => image.kept);
    const newCount = kept.filter(image => image.isNew).length;
    const coverLabel = manage.cover
      ? (images.find(image => image.src === manage.cover)?.isNew ? "新增图片" : "已选图片")
      : "自动（优先新增图片）";
    $("manage-summary").textContent = images.length
      ? "将保留 " + kept.length + " 张图片" + (newCount ? "（其中新增 " + newCount + " 张）" : "") +
        "；封面：" + coverLabel + "。"
      : "当前没有图片。";
  }
  function openManage() {
    const item = state.selected;
    if (!item) return;
    const seen = new Set();
    const images = [];
    const add = src => {
      if (!src || seen.has(src)) return;
      seen.add(src);
      images.push({ src, kept: true, isNew: false });
    };
    (item.images || []).forEach(add);
    if (item.cover) add(item.cover);
    state.manage = { item, images, cover: item.cover || (images[0] && images[0].src) || "" };
    $("manage-title").textContent = "管理「" + item.title + "」";
    $("manage-desc").textContent = "调整封面和效果图，或从图库移除这个 Skill。修改会先生成 GitHub Issue；只有仓库所有者提交的 Issue 会被 Actions 自动处理。";
    $("manage-new-image").value = "";
    $("manage-add-error").hidden = true;
    $("manage-status").hidden = true;
    $("manage-confirm").hidden = true;
    $("manage-delete").hidden = false;
    $("manage-edit-meta").href = state.catalog.repository_url + "/blob/main/library/skills/" +
      encodeURIComponent(item.slug) + "/meta.json";
    renderManage();
    $("skill-manage-modal").hidden = false;
    syncScrollLock();
    $("close-skill-manage").focus();
  }
  function closeManage() {
    if ($("skill-manage-modal").hidden) return;
    $("skill-manage-modal").hidden = true;
    state.manage = null;
    syncScrollLock();
    if (!$("detail-modal").hidden) $("manage-skill").focus();
  }
  function addManageImage() {
    const manage = state.manage;
    if (!manage) return;
    const input = $("manage-new-image");
    const raw = input.value.trim();
    $("manage-add-error").hidden = true;
    if (!raw) {
      input.focus();
      return;
    }
    const src = manageImageUrl(raw);
    if (!src) {
      $("manage-add-error").textContent = "请填写 GitHub 图片地址：raw.githubusercontent.com 链接，或 github.com 的 raw / blob 链接。";
      $("manage-add-error").hidden = false;
      input.focus();
      return;
    }
    if (manage.images.some(image => image.src === src)) {
      $("manage-add-error").textContent = "这张图片已经在列表里。";
      $("manage-add-error").hidden = false;
      input.focus();
      return;
    }
    if (manage.images.filter(image => image.isNew && image.kept).length >= 10) {
      $("manage-add-error").textContent = "每次最多新增 10 张图片。";
      $("manage-add-error").hidden = false;
      input.focus();
      return;
    }
    manage.images.push({ src, kept: true, isNew: true });
    manage.cover = src;
    input.value = "";
    renderManage();
    $("manage-add-image").focus();
  }
  function showManageStatus(message, url) {
    $("manage-status-text").textContent = message;
    $("manage-status-link").href = url;
    $("manage-status").hidden = false;
  }
  function submitManage() {
    const manage = state.manage;
    if (!manage) return;
    const kept = manage.images.filter(image => image.kept);
    if (manage.cover && !kept.some(image => image.src === manage.cover)) {
      showToast("封面必须在保留的图片中");
      return;
    }
    const existing = kept.filter(image => !image.isNew).map(image => image.src);
    const added = kept.filter(image => image.isNew).map(image => image.src);
    const params = new URLSearchParams();
    params.set("template", "edit-skill.yml");
    params.set("skill_slug", manage.item.slug);
    params.set("keep_images", existing.length ? existing.join("\n") : "无");
    params.set("cover_url", manage.cover);
    params.set("new_image_urls", added.join("\n"));
    const url = state.catalog.repository_url + "/issues/new?" + params.toString();
    showManageStatus("已尝试打开 GitHub 确认页。请检查图片列表，必要时在页面上传新图片，然后提交 Issue。", url);
    window.open(url, "_blank", "noopener,noreferrer");
  }
  function askDelete() {
    const manage = state.manage;
    if (!manage) return;
    $("manage-confirm-title").textContent = manage.item.title;
    $("manage-confirm").hidden = false;
    $("manage-delete").hidden = true;
    $("manage-confirm").scrollIntoView({ block: "nearest" });
    $("manage-delete-open").focus();
  }
  function cancelDelete() {
    $("manage-confirm").hidden = true;
    $("manage-delete").hidden = false;
    $("manage-delete").focus();
  }
  function openDeleteIssue() {
    const manage = state.manage;
    if (!manage) return;
    const params = new URLSearchParams();
    params.set("template", "delete-skill.yml");
    params.set("skill_slug", manage.item.slug);
    params.set("skill_title", manage.item.title);
    const url = state.catalog.repository_url + "/issues/new?" + params.toString();
    showManageStatus("已尝试打开删除确认页。请在 GitHub 勾选确认并提交，Actions 执行后才会真正删除。", url);
    window.open(url, "_blank", "noopener,noreferrer");
  }
  function bind() {
    $("open-skill-import").addEventListener("click", openSkillImport);
    $("close-skill-import").addEventListener("click", closeSkillImport);
    $("skill-import-modal").addEventListener("click", event => {
      if (event.target.dataset.importDismiss) closeSkillImport();
    });
    $("skill-repo-url").addEventListener("input", () => {
      $("skill-repo-url").removeAttribute("aria-invalid");
      $("skill-import-error").hidden = true;
    });
    $("skill-import-form").addEventListener("submit", event => {
      event.preventDefault();
      const raw = $("skill-repo-url").value.trim();
      try {
        const parsed = new URL(raw);
        const parts = parsed.pathname.split("/").filter(Boolean);
        if (parsed.protocol !== "https:" || parsed.hostname !== "github.com" || parts.length < 2 ||
            !parts.slice(0, 2).every(part => /^[a-zA-Z0-9_.-]+$/.test(part))) throw new Error("invalid");
      } catch {
        showImportError("请填写有效的 GitHub 仓库或 SKILL.md 链接");
        return;
      }
      $("skill-repo-url").removeAttribute("aria-invalid");
      $("skill-import-error").hidden = true;
      const base = "https://github.com/yuqiangdede/ai-image-prompt-library/issues/new";
      const url = base + "?template=add-skill.yml&skill_url=" + encodeURIComponent(raw);
      $("skill-import-fallback").href = url;
      $("skill-import-status-text").textContent = "已尝试打开 GitHub 确认页；如果没有自动打开，请用下面的链接继续。";
      $("skill-import-status").hidden = false;
      window.open(url, "_blank", "noopener,noreferrer");
    });
    $("manage-skill").addEventListener("click", openManage);
    $("close-skill-manage").addEventListener("click", closeManage);
    $("skill-manage-modal").addEventListener("click", event => {
      if (event.target.dataset.manageDismiss) closeManage();
    });
    $("manage-images").addEventListener("change", event => {
      const manage = state.manage;
      if (!manage) return;
      const keep = event.target.closest("[data-manage-keep]");
      if (keep) {
        const index = Number(keep.dataset.manageKeep);
        manage.images[index].kept = keep.checked;
        if (!keep.checked && manage.cover === manage.images[index].src) manage.cover = "";
        renderManage();
        manageFocus('[data-manage-keep="' + index + '"]');
        return;
      }
      const cover = event.target.closest("[data-manage-cover]");
      if (!cover) return;
      const value = cover.dataset.manageCover;
      manage.cover = value === "auto" ? "" : manage.images[Number(value)].src;
      renderManage();
      manageFocus(value === "auto" ? '[data-manage-cover="auto"]' : '[data-manage-cover="' + value + '"]');
    });
    $("manage-images").addEventListener("click", event => {
      const button = event.target.closest("[data-manage-remove]");
      if (!button || !state.manage) return;
      const removed = state.manage.images.splice(Number(button.dataset.manageRemove), 1)[0];
      if (removed && state.manage.cover === removed.src) state.manage.cover = "";
      renderManage();
      $("manage-add-image").focus();
    });
    $("manage-new-image").addEventListener("input", () => {
      $("manage-add-error").hidden = true;
    });
    $("manage-new-image").addEventListener("keydown", event => {
      if (event.key !== "Enter") return;
      event.preventDefault();
      addManageImage();
    });
    $("manage-add-image").addEventListener("click", addManageImage);
    $("manage-submit").addEventListener("click", submitManage);
    $("manage-delete").addEventListener("click", askDelete);
    $("manage-delete-cancel").addEventListener("click", cancelDelete);
    $("manage-delete-open").addEventListener("click", openDeleteIssue);
    $("nav-tabs").addEventListener("click", event => {
      const node = event.target.closest("[data-type]");
      if (!node) return;
      state.kind = node.dataset.type; render();
    });
    document.querySelectorAll(".view-switch").forEach(group => {
      group.addEventListener("click", event => {
        const node = event.target.closest("[data-view]");
        if (!node || node.dataset.view === state.view) return;
        state.view = node.dataset.view;
        applyView(true);
      });
    });
    $("category-nav").addEventListener("click", event => {
      const node = event.target.closest("[data-category]");
      if (!node) return;
      state.category = node.dataset.category; render();
    });
    $("search").addEventListener("input", event => { state.search = event.target.value; render(); });
    $("sort").addEventListener("change", event => { state.sort = event.target.value; render(); });
    $("reset-filter").addEventListener("click", () => {
      state.kind = "all"; state.category = "all"; state.search = ""; $("search").value = ""; render();
    });
    $("gallery").addEventListener("click", event => {
      const fav = event.target.closest("[data-fav]");
      if (fav) {
        if (state.favorites.has(fav.dataset.fav)) state.favorites.delete(fav.dataset.fav);
        else state.favorites.add(fav.dataset.fav);
        saveFavorites(); render(); return;
      }
      const open = event.target.closest("[data-open]");
      if (open) openItem(open.dataset.open);
    });
    $("detail-thumbs").addEventListener("click", event => {
      const button = event.target.closest("[data-image]");
      if (button) selectImage(button.dataset.image);
    });
    $("detail-related").addEventListener("click", event => {
      const button = event.target.closest("[data-related]");
      if (button) openItem(button.dataset.related);
    });
    $("close-modal").addEventListener("click", closeItem);
    $("detail-modal").addEventListener("click", event => { if (event.target.dataset.dismiss) closeItem(); });
    $("copy-text").addEventListener("click", () => copyText(state.text));
    $("copy-primary").addEventListener("click", () => {
      if (state.selected?.external_only) return copyText(state.selected.install_command || state.selected.source_url);
      if (state.selected?.kind !== "skill") return copyText(state.text);
      copyText("请把以下 SKILL.md 当作这次生图任务的指令使用。需要额外的文件或设计配置时请明确提出，不能假装已经读取缺失附件。上游原始 Skill：" +
        (state.selected?.source_url || "") + "\n\n" + state.text);
    });
    $("download-file").addEventListener("click", download);
    window.addEventListener("keydown", event => {
      if (event.key === "Escape") {
        if (!$("skill-manage-modal").hidden) { closeManage(); return; }
        if (!$("skill-import-modal").hidden) { closeSkillImport(); return; }
        if (!$("detail-modal").hidden) closeItem();
      }
      if (event.key === "/" && $("detail-modal").hidden && $("skill-import-modal").hidden &&
          $("skill-manage-modal").hidden && document.activeElement.tagName !== "INPUT") {
        event.preventDefault(); $("search").focus();
      }
    });
  }
  async function init() {
    bind();
    applyView();
    try {
      const response = await fetch("./data/catalog.json", { cache: "no-store" });
      if (!response.ok) throw new Error("HTTP " + response.status);
      state.catalog = await response.json();
      state.items = state.catalog.items || [];
      render();
      const linked = new URL(location.href).searchParams.get("item");
      if (linked) openItem(linked, false);
    } catch (error) {
      $("gallery").innerHTML = '<div class="empty">加载图库失败：' + escapeHtml(error.message) + "<p>请检查 GitHub Actions 构建与 Pages 部署。</p></div>";
      $("result-count").textContent = "加载失败";
    }
  }
  init();
})();
