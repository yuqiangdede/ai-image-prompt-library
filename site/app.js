/* Static responsive Prompt and Skill gallery. No API keys or third-party JS. */
(() => {
  "use strict";
  const $ = id => document.getElementById(id);
  const state = { items: [], catalog: null, search: "", kind: "all", category: "all", sort: "new", favorites: new Set(), selected: null, text: "" };
  const favoriteKey = "prompt-gallery-favorites-v2";
  const escapeHtml = text => String(text ?? "").replace(/[&<>"']/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" })[c]);
  const address = path => String(path || "").startsWith("https://") ? path : "./" + String(path || "").split("/").map(encodeURIComponent).join("/");
  const typeName = item => item.kind === "skill" ? "SKILL" : "PROMPT";
  let timer;

  try { state.favorites = new Set(JSON.parse(localStorage.getItem(favoriteKey) || "[]")); } catch { state.favorites = new Set(); }
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
    $("content-heading").textContent = item.kind === "skill" ? "SKILL.md 完整文本" : "完整 Prompt";
    $("detail-content").textContent = "正在读取内容…";
    $("copy-primary").textContent = item.kind === "skill" ? "复制给 ChatGPT 的 Skill 指令" : "复制完整 Prompt";
    $("download-file").textContent = item.kind === "skill" ? "下载 Skill ZIP" : "下载 Prompt";
    $("detail-note").textContent = item.kind === "skill"
      ? "ZIP 保留 Skill 配套文本、设计配置与脚本；上游有版权限制的参考图片不在 ZIP 内。复制文本不会自动安装 Skill。"
      : "复制后可以直接粘贴到 ChatGPT 图片生成对话。";
    $("open-source").href = state.catalog.repository_url + "/blob/main/" + item.content_path.split("/").map(encodeURIComponent).join("/");
    $("detail-modal").hidden = false;
    document.body.style.overflow = "hidden";
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
    document.body.style.overflow = "";
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
  function bind() {
    $("nav-tabs").addEventListener("click", event => {
      const node = event.target.closest("[data-type]");
      if (!node) return;
      state.kind = node.dataset.type; render();
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
      if (state.selected?.kind !== "skill") return copyText(state.text);
      copyText("请把以下 SKILL.md 当作这次生图任务的指令使用。需要额外的文件或设计配置时请明确提出，不能假装已经读取缺失附件。上游原始 Skill：" +
        (state.selected?.source_url || "") + "\n\n" + state.text);
    });
    $("download-file").addEventListener("click", download);
    window.addEventListener("keydown", event => {
      if (event.key === "Escape" && !$("detail-modal").hidden) closeItem();
      if (event.key === "/" && $("detail-modal").hidden && document.activeElement.tagName !== "INPUT") {
        event.preventDefault(); $("search").focus();
      }
    });
  }
  async function init() {
    bind();
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
