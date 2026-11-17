/* Static responsive Prompt and Skill gallery. No API keys or third-party JS. */
(() => {
  "use strict";
  const $ = id => document.getElementById(id);
  const state = { items: [], catalog: null, search: "", kind: "all", category: "all", sort: "new", view: "large", favorites: new Set(), selected: null, text: "", manage: null };

  // 大分类可交叉归属；旧素材的 category 和 tags 保留用于详情和搜索。
  const browseGroups = [
    ["poster","海报类"],["person","人物生图类"],["retouch","人像优化类"],
    ["photo","摄影风格类"],["art","插画艺术类"],["scene","场景建筑类"],
    ["brand","品牌产品类"],["other","其他"]
  ];
  // 已收录素材人工归类；添加新素材时由下方关键词规则兜底。
  const browseSlugs = {
    poster: `double-layer-fashion-portrait-poster haidayu-infrared-camera-epic-silhouette haidayu-person-epic-silhouette haiwei-xinjie-fashion-magazine-cover hangzhou-watercolor-travel-postcard mid-autumn-west-lake-paper-collage-poster photo-mogu-boneless-diptych photo-shadow-puppet-diptych urban-street-botanical-stipple-diptych vintage-color-lithograph-poster black-white-mens-fashion-nine-grid heytea-doodle-poster mono-color oriental-editorial-poster photo-abstract-editorial photo-relic-editorial xxd-panel-115`,
    person: `autumn-1970s-cinematic-fashion-portrait basketball-stands-broadcast-candid black-and-white-editorial-portrait black-white-four-pose-fine-art-portrait black-white-mens-fashion-nine-grid blue-hour-ferry-film-still blue-sky-archery-fashion-editorial crimson-low-angle-cinematic-portrait cyan-veil-bamboo-hat-hanfu-portrait double-layer-fashion-portrait-poster haidayu-person-epic-silhouette haiwei-xinjie-fashion-magazine-cover luxury-commercial-fashion-studio-portrait ming-phoenix-crown-bridal-portrait night-train-neon-cinematic-portrait peach-coral-floral-ballroom-fashion-portrait pink-purple-geometric-fashion-portrait professional-business-studio-portrait rainy-city-overpass-cinematic-film-still republic-era-night-alley-portrait silver-haired-wandering-swordswoman-film-portrait stone-bridge-parasol-hanfu-portrait studio-pose-transfer-shh summer-sunlit-cinematic-fine-art-portrait water-margin-heroes-selfie`,
    retouch: `autumn-1970s-cinematic-fashion-portrait basketball-stands-broadcast-candid black-and-white-editorial-portrait black-white-four-pose-fine-art-portrait black-white-mens-fashion-nine-grid double-layer-fashion-portrait-poster luxury-commercial-fashion-studio-portrait night-train-neon-cinematic-portrait professional-business-studio-portrait rainy-city-overpass-cinematic-film-still studio-pose-transfer-shh photo-abstract-editorial photo-relic-editorial`,
    photo: `autumn-1970s-cinematic-fashion-portrait basketball-stands-broadcast-candid black-and-white-editorial-portrait black-white-four-pose-fine-art-portrait black-white-mens-fashion-nine-grid blue-hour-ferry-film-still blue-sky-archery-fashion-editorial crimson-low-angle-cinematic-portrait cyan-veil-bamboo-hat-hanfu-portrait luxury-commercial-fashion-studio-portrait ming-phoenix-crown-bridal-portrait night-train-neon-cinematic-portrait peach-coral-floral-ballroom-fashion-portrait pink-purple-geometric-fashion-portrait professional-business-studio-portrait rainy-city-overpass-cinematic-film-still raw-black-and-white-street-snapshot republic-era-night-alley-portrait silver-haired-wandering-swordswoman-film-portrait stone-bridge-parasol-hanfu-portrait summer-sunlit-cinematic-fine-art-portrait water-margin-heroes-selfie haiwei-xinjie-perfume-product-photo`,
    art: `battlefield-assault-pencil-storyboard hangzhou-watercolor-travel-postcard mid-autumn-west-lake-paper-collage-poster photo-mogu-boneless-diptych photo-shadow-puppet-diptych photo-to-expressive-charcoal-sketch photo-to-hand-drawn-isometric-map science-encyclopedia-infographic urban-street-botanical-stipple-diptych vintage-color-lithograph-poster vintage-travel-watercolor-photo water-margin-heroes-selfie hand-drawn-styles heytea-doodle-poster mono-color oriental-editorial-poster photo-abstract-editorial photo-relic-editorial xxd-panel-115`,
    scene: `blue-hour-ferry-film-still map-arrow-to-real-world-view photo-to-hand-drawn-isometric-map rainy-city-overpass-cinematic-film-still panorama-generation yingzao`,
    brand: `haidayu-infrared-camera-epic-silhouette haidayu-person-epic-silhouette haiwei-xinjie-fashion-magazine-cover haiwei-xinjie-perfume-product-photo rainbow-bread-bakery-logo heytea-doodle-poster`
  };
  const browseIndex = new Map();
  for (const [group, list] of Object.entries(browseSlugs)) {
    for (const slug of list.split(" ")) {
      if (!browseIndex.has(slug)) browseIndex.set(slug, []);
      browseIndex.get(slug).push(group);
    }
  }
  function browseOf(item) {
    if (Array.isArray(item.browse_categories) && item.browse_categories.length) {
      const valid = item.browse_categories.filter(id => browseGroups.some(group => group[0] === id));
      if (valid.length) return [...new Set(valid)];
    }
    if (browseIndex.has(item.slug)) return browseIndex.get(item.slug);
    const words = [item.title, item.category, ...(item.tags || [])].join(" ");
    const ids = [];
    if (/海报|封面|画报|拼贴|明信片|poster/i.test(words)) ids.push("poster");
    if (/人物|人像|肖像|写真|汉服|古风|角色|模特|portrait|骑士|剑士/i.test(words)) ids.push("person");
    if (/人像优化|换装|姿态迁移|证件照|修图|形象照|照片转绘/i.test(words)) ids.push("retouch");
    if (/摄影|照片|胶片|电影|街拍|film|photo/i.test(words)) ids.push("photo");
    if (/插画|手绘|水彩|线稿|草图|拼贴|绘画|艺术|风格迁移|科普|图鉴/i.test(words)) ids.push("art");
    if (/全景|建筑|地图|空间|场景|城市|景观|三维|3D/i.test(words)) ids.push("scene");
    if (/品牌|产品|商品|电商|广告|包装|logo/i.test(words)) ids.push("brand");
    return ids.length ? [...new Set(ids)] : ["other"];
  }
  const favoriteKey = "prompt-gallery-favorites-v2";
  const viewKey = "prompt-gallery-view-v1";
  const promptUrlLimit = 6000; // GitHub errors on very long issue-prefill URLs
  const escapeHtml = text => String(text ?? "").replace(/[&<>"']/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" })[c]);
  const address = path => String(path || "").startsWith("https://") ? path : "./" + String(path || "").split("/").map(encodeURIComponent).join("/");
  const typeName = item => item.kind === "skill" ? "SKILL" : "PROMPT";
  const ellipsis = "…";
  function galleryCardWidth() {
    const first = $("gallery").querySelector(".gallery-card");
    if (first) return first.getBoundingClientRect().width;
    return ($("gallery").clientWidth - 60) / 4;
  }
  /* 按真实行高截断卡片里的标题/描述：让文字本身只占允许的行数，
     不靠 -webkit-line-clamp 硬裁（裁掉的内容仍占排版空间，会被判成文字重叠）。 */
  function trimToLines(el, maxLines) {
    const full = el.dataset.full != null ? el.dataset.full : el.textContent;
    el.dataset.full = full;
    el.textContent = full;
    const cs = getComputedStyle(el);
    const size = parseFloat(cs.fontSize) || 16;
    const lineHeight = parseFloat(cs.lineHeight) || size * 1.4;
    const limit = Math.ceil(lineHeight * maxLines) + 1;
    if (el.scrollHeight <= limit) return;
    const charsPerLine = Math.max(4, Math.floor(el.clientWidth / size));
    let text = full.slice(0, charsPerLine * maxLines + Math.ceil(charsPerLine * 0.4));
    el.textContent = text + ellipsis;
    for (let i = 0; i < 40 && text.length > 1 && el.scrollHeight > limit; i++) {
      text = text.slice(0, -1);
      el.textContent = text + ellipsis;
    }
    el.textContent = text.replace(/[，、：；,.:;\s]+$/, "") + ellipsis;
  }
  function fitCardText() {
    document.querySelectorAll("#gallery .card-details h3").forEach(el => trimToLines(el, 1));
    if (state.view === "small") return;
    document.querySelectorAll("#gallery .card-details p").forEach(el => trimToLines(el, 2));
  }
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
    document.body.style.overflow = (!$("detail-modal").hidden || !$("skill-import-modal").hidden ||
      !$("prompt-import-modal").hidden || !$("skill-manage-modal").hidden) ? "hidden" : "";
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
      if (state.category !== "all" && !browseOf(item).includes(state.category)) return false;
      if (q && ![item.title, item.description, item.category, item.model, ...(item.tags || []), item.search_text].join(" ").toLocaleLowerCase().includes(q)) return false;
      return true;
    }).sort((a, b) => state.sort === "az"
      ? a.title.localeCompare(b.title, "zh-CN")
      : String(b.updated_at).localeCompare(String(a.updated_at)) || a.title.localeCompare(b.title, "zh-CN"));
  }
  function renderBrowseCategories() {
    const counts = new Map(browseGroups.map(([id]) => [id, 0]));
    for (const item of state.items) for (const id of browseOf(item)) counts.set(id, counts.get(id) + 1);
    $("browse-tabs").innerHTML = browseGroups.filter(([id]) => counts.get(id)).map(([id, label]) => {
      const active = state.category === id;
      return '<button type="button" data-category="' + id + '" aria-pressed="' + active +
        '" class="' + (active ? "active" : "") + '">' + label + ' <span>' + counts.get(id) + '</span></button>';
    }).join("");
  }
  function render() {
    const results = listFiltered();
    $("count-all").textContent = state.items.length;
    $("hero-count").textContent = state.items.length;
    $("count-skill").textContent = state.items.filter(x => x.kind === "skill").length;
    $("count-prompt").textContent = state.items.filter(x => x.kind === "prompt").length;
    $("count-favorites").textContent = state.favorites.size;
    $("result-count").textContent = "共 " + results.length + " 个结果";
    document.querySelectorAll("#nav-tabs [data-type]").forEach(node => {
      const active = state.category === "all" && state.kind === node.dataset.type;
      node.classList.toggle("active", active);
      node.setAttribute("aria-pressed", String(active));
    });
    renderBrowseCategories();
    if (!results.length) {
      $("gallery").innerHTML = '<div class="empty">暂无匹配的素材<p>试试其他关键词，或清除筛选条件。</p></div>';
      return;
    }
    $("gallery").innerHTML = results.map((item, index) => {
      const coverSources = [...new Set([item.cover, ...(item.images || [])].filter(Boolean))];
      /* 首屏 4 张优先加载，其余懒加载 */
      const eager = index < 4;
      const image = coverSources.length
        ? '<img' + (eager ? ' loading="eager" fetchpriority="high"' : ' loading="lazy"') +
          ' src="' + escapeHtml(address(coverSources[0])) + '" alt="' + escapeHtml(item.title) + ' 效果图">'
        : '<span class="image-fallback">✳</span>';
      const coverDots = coverSources.length > 1
        ? '<div class="card-carousel-dots" role="group" aria-label="切换封面">' +
          coverSources.map((src, index) =>
            '<button type="button" data-slide-to="' + index + '" aria-label="切换到第 ' + (index + 1) + ' 张封面"' +
            (index === 0 ? ' aria-current="true"' : "") + '></button>').join("") +
          '</div>'
        : '';
      const cardWidth = galleryCardWidth();
      const chipMax = Math.max(1, Math.floor((cardWidth - 158) / (13 + 8)));
      const visibleTags = (item.tags || []).filter(tag => [...tag].reduce((s, c) => s + (c.charCodeAt(0) > 255 ? 2 : 1), 0) <= chipMax).slice(0, 2);
      const chips = '<span class="chip chip-kind">' + typeName(item) + "</span>" +
        visibleTags.map(tag => '<span class="chip">' + escapeHtml(tag) + "</span>").join("");
      const fav = state.favorites.has(item.id);
      return '<article class="gallery-card" data-item-id="' + escapeHtml(item.id) + '" data-cover-index="0"><button class="gallery-card-open" type="button" data-open="' + escapeHtml(item.id) +
        '"><div class="image-wrap">' + image +
        '</div><div class="card-details"><h3>' + escapeHtml(item.title) + '</h3><p>' + escapeHtml(item.description) +
        '</p></div></button>' + coverDots + '<div class="card-foot"><div class="chips">' + chips + '</div>' +
        '<div class="card-actions"><button class="favorite-button ' + (fav ? "active" : "") + '" data-fav="' + escapeHtml(item.id) +
        '" aria-label="' + (fav ? "取消收藏" : "收藏") + '">' + (fav ? "♥" : "♡") + '</button></div></div></article>';
    }).join("");
    fitCardText();
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
  async function writeClipboard(text) {
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
        return true;
      }
    } catch { /* fall back to the textarea method */ }
    try {
      const node = document.createElement("textarea");
      node.value = text;
      node.style.cssText = "position:fixed;left:-9999px;top:0";
      document.body.append(node);
      node.select();
      const ok = document.execCommand("copy");
      node.remove();
      return ok;
    } catch { return false; }
  }
  async function copyText(text) {
    if (!text) return showToast("内容尚未加载");
    if (await writeClipboard(text)) showToast("已复制到剪贴板");
    else showToast("复制受限，请选择下方文本手动复制");
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
    if (!$("prompt-import-modal").hidden) $("prompt-import-modal").hidden = true;
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
  function promptValue(id) {
    return $(id).value.trim();
  }
  function renderPromptSuggestions() {
    const unique = values => [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b, "zh-CN"));
    const options = values => values.map(value => '<option value="' + escapeHtml(value) + '"></option>').join("");
    $("prompt-category-options").innerHTML = options(unique(state.items.map(item => item.category)));
    $("prompt-model-options").innerHTML = options(unique(state.items.map(item => item.model)));
  }
  function openPromptImport() {
    if (!$("detail-modal").hidden) closeItem();
    if (!$("skill-import-modal").hidden) closeSkillImport();
    clearPromptImport();
    renderPromptSuggestions();
    $("prompt-body-count").textContent = $("prompt-body").value.length + " 字";
    $("prompt-import-modal").hidden = false;
    syncScrollLock();
    $("prompt-title").focus();
    $("prompt-title").select();
  }
  function closePromptImport() {
    if ($("prompt-import-modal").hidden) return;
    $("prompt-import-modal").hidden = true;
    syncScrollLock();
    $("open-prompt-import").focus();
  }
  function clearPromptImport() {
    document.querySelectorAll("#prompt-import-form [aria-invalid]").forEach(node => node.removeAttribute("aria-invalid"));
    $("prompt-import-error").hidden = true;
    $("prompt-import-status").hidden = true;
  }
  function showPromptError(message, field) {
    $("prompt-import-error").textContent = message;
    $("prompt-import-error").hidden = false;
    if (!field) return;
    $(field).setAttribute("aria-invalid", "true");
    $(field).focus();
  }
  function promptIssueUrl(params) {
    const base = (state.catalog?.repository_url || "https://github.com/yuqiangdede/ai-image-prompt-library") + "/issues/new";
    return base + "?" + params.toString();
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
      const preview = address(image.src);
      return '<figure class="manage-image' + (kept ? "" : " is-dropped") + '">' +
        '<div class="manage-image-frame">' +
        '<img loading="lazy" src="' + escapeHtml(preview) + '" alt="' +
        escapeHtml((image.isNew ? "新增图片 " : "图片 ") + (index + 1)) + '">' +
        (image.isNew ? '<span class="manage-image-badge">新增链接</span>' : "") +
        (kept ? "" : '<span class="manage-image-dropped">已移除</span>') +
        '</div>' +
        '<figcaption>' +
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
    const coverOptions =
      '<label class="manage-auto-cover"><input type="radio" name="manage-cover" data-manage-cover="auto"' +
      (manage.cover ? "" : " checked") + '> 自动选择封面（优先新增图片）</label>' +
      '<label class="manage-auto-cover"><input type="radio" name="manage-cover" data-manage-cover="upload-first"' +
      (manage.cover === "upload:1" ? " checked" : "") +
      '> 将 GitHub 表单上传的第 1 张图片设为封面（上传必填）</label>';
    $("manage-images").innerHTML =
      (images.length ? tiles : '<p class="manage-empty">当前没有图片，可添加图片链接或在 GitHub 表单中直接上传。</p>') +
      coverOptions;
    const kept = images.filter(image => image.kept);
    const newCount = kept.filter(image => image.isNew).length;
    const coverLabel = manage.cover === "upload:1" ? "GitHub 本次上传第 1 张图片" :
      manage.cover
        ? (images.find(image => image.src === manage.cover)?.isNew ? "新增链接图片" : "现有图片")
        : "自动（优先新增图片）";
    $("manage-summary").textContent =
      "已选保留 " + kept.length + " 张图片" +
      (newCount ? "（其中新增链接 " + newCount + " 张）" : "") +
      "；封面：" + coverLabel + "。GitHub 上传的图片提交后才会出现在图库中。";
  }
  function openManage(item = state.selected) {
    if (!item) return;
    const returnFocus = document.activeElement;
    const seen = new Set();
    const images = [];
    const add = src => {
      if (!src || seen.has(src)) return;
      seen.add(src);
      images.push({ src, kept: true, isNew: false });
    };
    (item.images || []).forEach(add);
    if (item.cover) add(item.cover);
    state.manage = { item, images, cover: item.cover || (images[0] && images[0].src) || "", returnFocus };
    $("manage-title").textContent = "管理「" + item.title + "」";
    $("manage-desc").textContent = "修改标题、简介、分类、标签和多张封面。提交后在 GitHub Issue 中核对确认，由 Actions 更新图库。";
    $("manage-item-title").value = item.title || "";
    $("manage-item-description").value = item.description || "";
    $("manage-item-category").value = item.category || "";
    $("manage-item-tags").value = (item.tags || []).join(", ");
    $("manage-danger-section").hidden = item.kind !== "skill";
    $("manage-new-image").value = "";
    $("manage-add-error").hidden = true;
    $("manage-status").hidden = true;
    $("manage-confirm").hidden = true;
    $("manage-delete").hidden = false;
    $("manage-edit-meta").href = state.catalog.repository_url + "/edit/main/library/" +
      (item.kind === "skill" ? "skills" : "prompts") + "/" +
      encodeURIComponent(item.slug) + "/meta.json";
    renderManage();
    $("skill-manage-modal").hidden = false;
    syncScrollLock();
    $("close-skill-manage").focus();
  }
  function closeManage() {
    if ($("skill-manage-modal").hidden) return;
    const focusTarget = state.manage?.returnFocus;
    $("skill-manage-modal").hidden = true;
    state.manage = null;
    syncScrollLock();
    if (focusTarget?.isConnected) focusTarget.focus();
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
    if (manage.cover && manage.cover !== "upload:1" && !kept.some(image => image.src === manage.cover)) {
      showToast("封面必须在保留的图片中");
      return;
    }
    const title = $("manage-item-title").value.trim();
    const description = $("manage-item-description").value.trim();
    const category = $("manage-item-category").value.trim();
    const tags = $("manage-item-tags").value.split(/[,，、\n]+/).map(x => x.trim().replace(/^#/, "")).filter(Boolean);
    if (!title || !description || !category) return showToast("标题、简介和分类不能为空");
    if (title.length > 80 || description.length > 300 || category.length > 40) return showToast("基础信息超过长度限制");
    if (tags.length > 24 || tags.some(tag => tag.length > 30)) return showToast("标签最多 24 个，每个不超过 30 字");
    const existing = kept.filter(image => !image.isNew).map(image => image.src);
    const added = kept.filter(image => image.isNew).map(image => image.src);
    const params = new URLSearchParams();
    params.set("template", manage.cover === "upload:1" ? "edit-item-upload.yml" : "edit-item.yml");
    params.set("item_kind", manage.item.kind);
    params.set("item_slug", manage.item.slug);
    params.set("item_title", title);
    params.set("item_description", description);
    params.set("item_category", category);
    params.set("item_tags", [...new Set(tags)].join(", "));
    params.set("keep_images", existing.length ? existing.join("\n") : "无");
    params.set("cover_url", manage.cover);
    params.set("new_image_urls", added.join("\n"));
    const url = state.catalog.repository_url + "/issues/new?" + params.toString();
    const message = manage.cover === "upload:1"
      ? "已打开 GitHub 确认页，请在「上传新图片」中选择本地图片一次。上传为必填，第一张上传的图片将成为封面；确认附件显示后再提交 Issue。"
      : "已打开 GitHub 确认页：需要上传本地图片时，直接在「上传新图片」选择一次即可；也可只修改已有图片或链接，确认后提交 Issue。";
    showManageStatus(message, url);
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
    /* 卡片列数/宽度变化时（窗口缩放、小图视图、调节滑块改排法）重新截断文字 */
    let lastGalleryWidth = 0;
    const refit = () => {
      const width = Math.round($("gallery").getBoundingClientRect().width);
      if (width === lastGalleryWidth) return;
      lastGalleryWidth = width;
      fitCardText();
    };
    if (window.ResizeObserver) {
      new ResizeObserver(refit).observe($("gallery"));
    } else {
      window.addEventListener("resize", refit);
    }
    /* 调节滑块改的是 <html> 上的 CSS 变量 / data-layout，不会触发 resize，
       这里跟着重新截断一次，标题字号或列数变化后文字才不会硬裁。 */
    let refitTimer;
    const scheduleRefit = () => {
      clearTimeout(refitTimer);
      refitTimer = setTimeout(fitCardText, 80);
    };
    new MutationObserver(scheduleRefit).observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["style", "class", "data-layout"]
    });
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
    $("open-prompt-import").addEventListener("click", openPromptImport);
    $("close-prompt-import").addEventListener("click", closePromptImport);
    $("prompt-import-modal").addEventListener("click", event => {
      if (event.target.dataset.promptDismiss) closePromptImport();
    });
    $("prompt-import-form").addEventListener("input", event => {
      if (event.target.matches("input, textarea")) event.target.removeAttribute("aria-invalid");
      $("prompt-import-error").hidden = true;
      if (event.target.id === "prompt-body") {
        $("prompt-body-count").textContent = event.target.value.length + " 字";
      }
    });
    $("prompt-import-form").addEventListener("submit", async event => {
      event.preventDefault();
      clearPromptImport();
      const title = promptValue("prompt-title");
      const description = promptValue("prompt-description");
      const category = promptValue("prompt-category");
      const tags = promptValue("prompt-tags");
      const model = promptValue("prompt-model");
      const prompt = $("prompt-body").value.trim();
      const slug = promptValue("prompt-slug");
      const coverRaw = promptValue("prompt-cover");
      if (!title) return showPromptError("请填写标题。", "prompt-title");
      if (title.length > 80) return showPromptError("标题不能超过 80 个字符。", "prompt-title");
      if (!description) return showPromptError("请填写简介。", "prompt-description");
      if (description.length > 300) return showPromptError("简介不能超过 300 个字符。", "prompt-description");
      if (!category) return showPromptError("请填写分类。", "prompt-category");
      if (category.length > 40) return showPromptError("分类不能超过 40 个字符。", "prompt-category");
      if (model.length > 40) return showPromptError("适用模型不能超过 40 个字符。", "prompt-model");
      if (!prompt) return showPromptError("请填写提示词正文。", "prompt-body");
      if (prompt.length > 20000) return showPromptError("提示词正文不能超过 20000 个字符。", "prompt-body");
      if (slug && slug.length > 60) return showPromptError("目录标识不能超过 60 个字符。", "prompt-slug");
      if (slug && !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) {
        return showPromptError("目录标识只允许小写字母、数字和连字符。", "prompt-slug");
      }
      let cover = "";
      if (coverRaw) {
        cover = manageImageUrl(coverRaw);
        if (!cover) {
          return showPromptError("封面图地址请填写 GitHub 图片链接（raw.githubusercontent.com，或 github.com 的 raw/blob 链接）。", "prompt-cover");
        }
      }
      const params = new URLSearchParams();
      params.set("template", "add-prompt.yml");
      params.set("title", "[添加提示词] " + title);
      params.set("prompt_title", title);
      params.set("prompt_description", description);
      params.set("prompt_category", category);
      if (tags) params.set("prompt_tags", tags);
      if (model) params.set("prompt_model", model);
      params.set("prompt_body", prompt);
      if (cover) params.set("cover_url", cover);
      if (slug) params.set("prompt_slug", slug);
      let url = promptIssueUrl(params);
      let message = "已打开 GitHub 确认页。请核对内容；封面还没填地址时，请在页面里上传封面图，然后提交 Issue。";
      let copyPromise = null;
      if (url.length > promptUrlLimit) {
        params.delete("prompt_body");
        url = promptIssueUrl(params);
        copyPromise = writeClipboard(prompt);
        message = "提示词正文较长，正在复制到剪贴板；打开 GitHub 页面后请粘贴到「提示词正文」再提交。";
      }
      $("prompt-import-fallback").href = url;
      $("prompt-import-status-text").textContent = message;
      $("prompt-import-status").hidden = false;
      window.open(url, "_blank", "noopener,noreferrer");
      if (copyPromise) {
        const copied = await copyPromise;
        $("prompt-import-status-text").textContent = copied
          ? "提示词正文较长，已复制到剪贴板。请在打开的 GitHub 页面「提示词正文」中粘贴后再提交。"
          : "提示词正文较长，未能自动复制。请从上面的输入框复制正文，粘贴到 GitHub 页面的「提示词正文」后再提交。";
      }
    });
    $("detail-edit").addEventListener("click", () => openManage());
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
      manage.cover = value === "auto" ? "" :
        value === "upload-first" ? "upload:1" : manage.images[Number(value)].src;
      renderManage();
      manageFocus('[data-manage-cover="' + value + '"]');
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
      state.kind = node.dataset.type; state.category = "all"; render();
    });
    document.querySelectorAll(".view-switch").forEach(group => {
      group.addEventListener("click", event => {
        const node = event.target.closest("[data-view]");
        if (!node || node.dataset.view === state.view) return;
        state.view = node.dataset.view;
        applyView(true);
      });
    });
    $("browse-tabs").addEventListener("click", event => {
      const node = event.target.closest("[data-category]");
      if (!node) return;
      state.kind = "all"; state.category = node.dataset.category; render();
    });
    $("search").addEventListener("input", event => { state.search = event.target.value; render(); });
    $("sort").addEventListener("change", event => { state.sort = event.target.value; render(); });
    /* 封面地址失效时退回品牌占位，避免相机/网络问题留下空白灰块 */
    $("gallery").addEventListener("error", event => {
      const img = event.target;
      const wrap = img instanceof HTMLImageElement ? img.closest(".image-wrap") : null;
      if (!wrap || !wrap.contains(img)) return;
      const fallback = document.createElement("span");
      fallback.className = "image-fallback";
      fallback.textContent = "✳";
      img.replaceWith(fallback);
    }, true);
    $("gallery").addEventListener("click", event => {
      const dot = event.target.closest("[data-slide-to]");
      if (dot) {
        const card = dot.closest(".gallery-card");
        const item = state.items.find(x => x.id === card?.dataset.itemId);
        if (!card || !item) return;
        const images = [...new Set([item.cover, ...(item.images || [])].filter(Boolean))];
        if (images.length < 2) return;
        const next = Math.min(images.length - 1, Math.max(0, Number(dot.dataset.slideTo) || 0));
        card.dataset.coverIndex = String(next);
        const preview = card.querySelector(".image-wrap img");
        if (preview) preview.src = address(images[next]);
        card.querySelectorAll(".card-carousel-dots button").forEach((el, index) => {
          if (index === next) el.setAttribute("aria-current", "true");
          else el.removeAttribute("aria-current");
        });
        return;
      }
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
        if (!$("prompt-import-modal").hidden) { closePromptImport(); return; }
        if (!$("skill-import-modal").hidden) { closeSkillImport(); return; }
        if (!$("detail-modal").hidden) closeItem();
      }
      if (event.key === "/" && $("detail-modal").hidden && $("skill-import-modal").hidden &&
          $("prompt-import-modal").hidden && $("skill-manage-modal").hidden &&
          !["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement.tagName)) {
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
