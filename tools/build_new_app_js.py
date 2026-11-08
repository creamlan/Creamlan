import json

with open('products_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

print(f"Total catalog products: {len(catalog)}")
total_plans = sum(len(p.get('plans', [])) for p in catalog)
print(f"Total plans: {total_plans}")

js_catalog_str = json.dumps(catalog, ensure_ascii=False, indent=2)

# 1. Generate js/app.js
js_code = f"""(function(){{
  "use strict";

  // ===== THÔNG TIN CREAMLAN STORE & TÀI KHOẢN EXIMBANK =====
  const zaloPhone = "0327620117";
  const zaloLink = "https://zalo.me/" + zaloPhone;
  const bankId = "970431"; // Eximbank BIN
  const bankName = "Eximbank";
  const bankAccountNo = "0327620117";
  const bankAccountName = "CAO THANH HAI";

  // ===== 22 SẢN PHẨM CHÍNH THỨC TỪ GOOGLE SHEETS =====
  const DEFAULT_PRODUCT_GROUPS = {js_catalog_str};

  let productGroupsData = DEFAULT_PRODUCT_GROUPS;
  let categories = ["all"];
  let selectedCategory = "all";
  let selectedStock = "all";
  let searchKeyword = "";
  let selectedGroup = null;
  let selectedPlan = null;
  let lastPaymentContent = "";
  let lastPaymentAmount = 0;
  let lastOrderCode = "";

  const $ = id => document.getElementById(id);
  const els = {{}};

  function safe(val){{
    return String(val == null ? "" : val)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }}

  function removeVietnameseTones(str){{
    str = String(str || "");
    str = str.replace(/[àáạảãâầấậẩẫăằắặẳẵ]/g, "a");
    str = str.replace(/[èéẹẻẽêềếệểễ]/g, "e");
    str = str.replace(/[ìíịỉĩ]/g, "i");
    str = str.replace(/[òóọỏõôồốộổỗơờớợởỡ]/g, "o");
    str = str.replace(/[ùúụủũưừứựửữ]/g, "u");
    str = str.replace(/[ỳýỵỷỹ]/g, "y");
    str = str.replace(/đ/g, "d");
    str = str.replace(/[ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴ]/g, "A");
    str = str.replace(/[ÈÉẸẺẼÊỀẾỆỂỄ]/g, "E");
    str = str.replace(/[ÌÍỊỈĨ]/g, "I");
    str = str.replace(/[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]/g, "O");
    str = str.replace(/[ÙÚỤỦŨƯỪỨỰỬỮ]/g, "U");
    str = str.replace(/[ỲÝỴỶỸ]/g, "Y");
    str = str.replace(/Đ/g, "D");
    return str;
  }}

  function imgHtml(group){{
    if(!group || !group.image) return `<span class="icon-fallback">${{safe(initials(group?.name))}}</span>`;
    const raw = String(group.image || "").trim();
    const isDirectImage = /^(https?:\\/\\/|data:image\\/|assets\\/|\\.\\/|\\/)/i.test(raw) && /\\.(png|jpe?g|webp|gif|svg)(\\?.*)?$/i.test(raw);
    const domain = raw.replace(/^https?:\\/\\//i, "").replace(/\\/.*$/, "");
    const url = isDirectImage 
      ? raw 
      : `https://www.google.com/s2/favicons?domain=${{domain}}&sz=256`;
    return `<img src="${{safe(url)}}" onerror="this.outerHTML='<span class=\\'icon-fallback\\'>${{safe(initials(group?.name))}}</span>';" alt="${{safe(group.name)}}" loading="lazy" decoding="async">`;
  }}

  function initials(name){{
    const words = String(name || "").trim().split(/\\s+/);
    if(!words.length || !words[0]) return "CL";
    if(words.length === 1) return words[0].slice(0, 2).toUpperCase();
    return (words[0][0] + words[1][0]).toUpperCase();
  }}

  function isPlanOut(plan){{
    return Boolean(plan && (plan.isOutOfStock || /hết hàng|out of stock/i.test(String(plan.price || ""))));
  }}

  function extractAmount(priceStr){{
    const s = String(priceStr || "").trim();
    if(isPlanOut({{price: s}})) return 0;
    const digits = s.replace(/[^0-9]/g, "");
    return digits ? parseInt(digits, 10) : 0;
  }}

  function isGroupOut(group){{
    if(!group.plans || !group.plans.length) return false;
    return group.plans.every(p => isPlanOut(p));
  }}

  function planLabel(plan){{
    if(isPlanOut(plan)) return "Hết hàng";
    const amt = extractAmount(plan.price);
    return amt ? amt.toLocaleString("vi-VN") + " đ" : (plan.price || "Liên hệ");
  }}

  function recomputeCategories(){{
    const set = new Set();
    productGroupsData.forEach(g => {{ if(g.category) set.add(g.category); }});
    categories = ["all", ...Array.from(set)];
  }}

  function shortCategory(cat){{
    if(!cat || cat === "all") return "Tất cả danh mục";
    if(/ai|công nghệ/i.test(cat)) return "AI";
    if(/giải trí/i.test(cat)) return "Giải trí";
    if(/thiết kế|đồ họa/i.test(cat)) return "Thiết kế";
    if(/học tập|khóa học/i.test(cat)) return "Học tập";
    return cat;
  }}

  function renderStats(){{
    if(els.totalProducts) els.totalProducts.textContent = productGroupsData.length;
    const totalPlans = productGroupsData.reduce((acc, g) => acc + (g.plans ? g.plans.length : 0), 0);
    if(els.totalPlans) els.totalPlans.textContent = totalPlans;
  }}

  function renderFilters(){{
    if(els.chips){{
      els.chips.innerHTML = categories.map(cat => {{
        const label = shortCategory(cat);
        const active = cat === selectedCategory ? " active" : "";
        return `<button class="chip${{active}}" data-cat="${{safe(cat)}}" type="button">${{safe(label)}}</button>`;
      }}).join("");
    }}
    if(els.categoryFilter){{
      els.categoryFilter.innerHTML = categories.map(cat => {{
        const label = cat === "all" ? "Tất cả danh mục" : cat;
        const selected = cat === selectedCategory ? " selected" : "";
        return `<option value="${{safe(cat)}}"${{selected}}>${{safe(label)}}</option>`;
      }}).join("");
    }}
  }}

  function renderFeatured(){{
    if(!els.featuredGrid) return;
    const top6 = productGroupsData.slice(0, 6);
    els.featuredGrid.innerHTML = top6.map(g => `
      <div class="featured-card" data-group-id="${{safe(g.id)}}" style="--card-glow:${{safe(g.glow)}}">
        <div class="featured-icon">${{imgHtml(g)}}</div>
        <div class="featured-name">${{safe(g.name)}}</div>
      </div>
    `).join("");
  }}

  function renderRail(items){{
    if(!els.quickRail) return;
    // Remove any duplicate images/brands in the rail
    const seen = new Set();
    const uniqueRailItems = [];
    items.forEach(it => {{
      const key = (it.image || it.brand || it.name).toLowerCase();
      if(!seen.has(key)){{
        seen.add(key);
        uniqueRailItems.push(it);
      }}
    }});

    els.quickRail.innerHTML = uniqueRailItems.map(g => `
      <div class="rail-item" data-group-id="${{safe(g.id)}}" title="${{safe(g.name)}}" style="--glow:${{safe(g.glow)}}">
        ${{imgHtml(g)}}
      </div>
    `).join("");

    updateRailButtons();
  }}

  function updateRailButtons(){{
    if(!els.quickRail) return;
    const sl = els.quickRail.scrollLeft;
    const maxScroll = els.quickRail.scrollWidth - els.quickRail.clientWidth;
    if(els.railPrev){{
      els.railPrev.style.display = sl > 12 ? "flex" : "none";
    }}
    if(els.railNext){{
      els.railNext.style.display = (maxScroll > 10 && sl < maxScroll - 12) ? "flex" : "none";
    }}
  }}

  function filteredGroups(){{
    const kw = removeVietnameseTones(searchKeyword.toLowerCase().trim());
    return productGroupsData.filter(g => {{
      if(selectedCategory !== "all" && g.category !== selectedCategory) return false;
      const isOut = isGroupOut(g);
      if(selectedStock === "available" && isOut) return false;
      if(selectedStock === "out" && !isOut) return false;
      if(kw){{
        const hay = removeVietnameseTones([
          g.name, g.brand, g.category, g.description,
          ...(g.plans || []).map(p => [p.variant, p.duration, p.note, p.warranty].join(" "))
        ].join(" ").toLowerCase());
        if(!hay.includes(kw)) return false;
      }}
      return true;
    }});
  }}

  function productCard(group){{
    const isOut = isGroupOut(group);
    const priceClass = isOut ? " out" : (!extractAmount(group.priceLabel) ? " contact" : "");
    return `
      <article class="product-card" data-group-id="${{safe(group.id)}}" style="--photo-glow:${{safe(group.glow)}}">
        <div class="product-icon">${{imgHtml(group)}}</div>
        <div>
          <div class="product-name">${{safe(group.name)}}</div>
          <div class="product-meta">${{safe(group.planCount)}} gói · ${{safe(group.brand || "Creamlan")}}</div>
        </div>
        <div class="product-price${{priceClass}}">${{safe(group.priceLabel || "Liên hệ")}}</div>
      </article>
    `;
  }}

  function renderProducts(){{
    const items = filteredGroups();
    if(els.resultCount) els.resultCount.textContent = items.length;
    if(els.productGroups){{
      els.productGroups.innerHTML = items.map(productCard).join("");
    }}
    if(els.empty){{
      els.empty.style.display = items.length ? "none" : "block";
    }}
    renderRail(items);
  }}

  // ===== MODAL & CHECKOUT LOGIC =====
  function openProductModal(groupId){{
    const g = productGroupsData.find(x => x.id === groupId);
    if(!g) return;
    selectedGroup = g;
    selectedPlan = null;
    clearPaymentResult();

    if(els.modalLogo) els.modalLogo.innerHTML = imgHtml(g);
    if(els.modalProductImage) els.modalProductImage.innerHTML = imgHtml(g);
    if(els.modalTitle) els.modalTitle.textContent = g.name;
    if(els.modalSub) els.modalSub.textContent = [g.brand, g.category].filter(Boolean).join(" · ");
    if(els.modalDesc) els.modalDesc.textContent = g.description || "";
    if(els.modalPlanCount) els.modalPlanCount.textContent = (g.plans ? g.plans.length : 0) + " gói";

    if(els.modalPlans){{
      els.modalPlans.innerHTML = (g.plans || []).map(planOption).join("");
    }}

    // Preselect first in-stock plan
    const firstInStock = (g.plans || []).find(p => !isPlanOut(p));
    if(firstInStock){{
      selectPlan(firstInStock.id);
    }} else if(g.plans && g.plans[0]){{
      selectPlan(g.plans[0].id);
    }}

    if(els.productModal){{
      els.productModal.classList.add("active");
      els.productModal.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
    }}
  }}

  function closeProductModal(){{
    if(els.productModal){{
      els.productModal.classList.remove("active");
      els.productModal.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    }}
  }}

  function planOption(plan){{
    const out = isPlanOut(plan);
    const outClass = out ? " out-of-stock" : "";
    const badges = [
      plan.duration ? `⏱️ ${{safe(plan.duration)}}` : "",
      plan.warranty ? `🛡️ ${{safe(plan.warranty)}}` : "",
      plan.accountType ? safe(plan.accountType) : ""
    ].filter(Boolean).map(b => `<span class="plan-badge${{b.includes('🛡️') ? ' warranty' : ''}}">${{b}}</span>`).join("");

    return `
      <div class="plan-option${{outClass}}" data-plan-id="${{safe(plan.id)}}">
        <div class="plan-meta">
          <div class="plan-name">${{safe(plan.variant || "Gói dịch vụ")}}</div>
          ${{plan.note ? `<div class="plan-sub">${{safe(plan.note)}}</div>` : ""}}
          <div class="plan-badges">${{badges}}</div>
        </div>
        <div class="plan-price">${{safe(planLabel(plan))}}</div>
      </div>
    `;
  }}

  function selectPlan(planId){{
    if(!selectedGroup) return;
    const plan = (selectedGroup.plans || []).find(p => p.id === planId);
    if(!plan) return;
    selectedPlan = plan;

    if(els.modalPlans){{
      els.modalPlans.querySelectorAll(".plan-option").forEach(el => {{
        el.classList.toggle("selected", el.getAttribute("data-plan-id") === planId);
      }});
    }}

    if(els.selectedPlanBox){{
      els.selectedPlanBox.innerHTML = `
        <b>Đã chọn:</b> ${{safe(selectedGroup.name)}}<br>
        <b>Gói:</b> ${{safe(plan.variant || plan.duration || "Mặc định")}}<br>
        <b>Thời hạn:</b> ${{safe(plan.duration || "Liên hệ")}} · <b>Giá:</b> ${{safe(planLabel(plan))}}
      `;
    }}

    clearPaymentResult();
  }}

  function showPaymentError(msg){{
    if(els.paymentError){{
      els.paymentError.textContent = msg;
      els.paymentError.style.display = "block";
    }}
  }}

  function clearPaymentResult(){{
    if(els.paymentError) els.paymentError.style.display = "none";
    if(els.paymentResult) els.paymentResult.classList.remove("active");
    lastPaymentContent = "";
    lastPaymentAmount = 0;
    lastOrderCode = "";
  }}

  function normalizeCustomerName(name){{
    return String(name || "").trim().replace(/\\s+/g, " ");
  }}

  function normalizePhone(phone){{
    return String(phone || "").replace(/[^0-9]/g, "");
  }}

  function productCode(group, plan){{
    const base = removeVietnameseTones((group.brand || group.name || "sp").toLowerCase()).replace(/[^a-z0-9]/g, "").slice(0, 16) || "sp";
    const duration = removeVietnameseTones([plan.duration, plan.variant].join(" ").toLowerCase());
    let d = "";
    const m = duration.match(/(\\d+)\\s*thang/); if(m) d = m[1] + "m";
    const y = duration.match(/(\\d+)\\s*nam/); if(y) d = y[1] + "y";
    return (base + (d ? " " + d : "")).slice(0, 24);
  }}

  function pad2(n){{ return String(n).padStart(2, "0"); }}

  function createOrderCode(phone){{
    const now = new Date();
    const date = String(now.getFullYear()).slice(2) + pad2(now.getMonth() + 1) + pad2(now.getDate());
    const time = pad2(now.getHours()) + pad2(now.getMinutes()) + pad2(now.getSeconds());
    const suffix = String(phone || "").slice(-4) || String(Math.floor(1000 + Math.random() * 9000));
    return `CRL-${{date}}-${{time}}-${{suffix}}`;
  }}

  function createTransferContent(group, plan, name){{
    const cleanName = removeVietnameseTones(normalizeCustomerName(name)).toUpperCase().replace(/[^A-Z0-9 ]/g, "").replace(/\\s+/g, " ").trim();
    return (cleanName + " " + productCode(group, plan)).trim().slice(0, 60);
  }}

  function createVietQrUrl(amount, content){{
    const accountName = bankAccountName ? "&accountName=" + encodeURIComponent(bankAccountName) : "";
    return `https://img.vietqr.io/image/${{bankId}}-${{bankAccountNo}}-compact2.png?amount=${{encodeURIComponent(amount)}}&addInfo=${{encodeURIComponent(content)}}${{accountName}}`;
  }}

  function getOrderText(confirmed = false){{
    const name = normalizeCustomerName(els.customerName ? els.customerName.value : "");
    const phone = normalizePhone(els.customerPhone ? els.customerPhone.value : "");
    const lines = [];
    lines.push(confirmed ? "Xin chào Creamlan Store, tôi đã chuyển khoản đơn hàng. Shop kiểm tra và xử lý đơn giúp mình." : "Xin chào Creamlan Store, tôi muốn đặt đơn hàng này.");
    if(lastOrderCode) lines.push("Mã đơn hàng: " + lastOrderCode);
    if(selectedGroup) lines.push("Sản phẩm: " + selectedGroup.name);
    if(selectedPlan){{
      lines.push("Gói: " + (selectedPlan.variant || selectedPlan.duration || ""));
      lines.push("Thời hạn: " + (selectedPlan.duration || "Liên hệ"));
      lines.push("Giá: " + planLabel(selectedPlan));
    }}
    lines.push("Họ tên: " + (name || ""));
    lines.push("SĐT: " + (phone || ""));
    if(lastPaymentAmount) lines.push("Số tiền chuyển khoản: " + Number(lastPaymentAmount).toLocaleString("vi-VN") + " đ");
    if(lastPaymentContent) lines.push("Nội dung chuyển khoản: " + lastPaymentContent);
    lines.push("Tài khoản nhận: Eximbank " + bankAccountNo + " - " + bankAccountName);
    lines.push("Ghi chú: " + (confirmed ? "Khách đã bấm xác nhận đã chuyển khoản trên website. Shop vui lòng kiểm tra giao dịch theo mã đơn và nội dung chuyển khoản." : "Khách đang tạo đơn từ website Creamlan Store."));
    return lines.filter(Boolean).join("\\n");
  }}

  function createZaloOrderLink(hasPayment, confirmed = false){{
    const text = getOrderText(confirmed && hasPayment);
    return zaloLink + "?text=" + encodeURIComponent(text);
  }}

  function generatePaymentQr(){{
    if(!selectedGroup || !selectedPlan) return showPaymentError("Bạn cần chọn một gói sản phẩm trước khi tạo QR.");
    const name = normalizeCustomerName(els.customerName.value);
    const phone = normalizePhone(els.customerPhone.value);
    if(!name){{
      els.customerName.focus();
      return showPaymentError("Vui lòng nhập họ tên khách hàng.");
    }}
    if(!phone || phone.length < 9 || phone.length > 11){{
      els.customerPhone.focus();
      return showPaymentError("Vui lòng nhập số điện thoại hợp lệ, chỉ gồm 9-11 chữ số.");
    }}
    const amount = extractAmount(selectedPlan.price);
    if(!amount){{
      if(els.zaloGeneral) els.zaloGeneral.href = createZaloOrderLink(false);
      return showPaymentError("Gói này đang hết hàng/chưa có giá cố định. Hãy bấm “Gửi đơn Zalo” để shop tư vấn tình trạng mới nhất.");
    }}

    const content = createTransferContent(selectedGroup, selectedPlan, name);
    lastPaymentContent = content;
    lastPaymentAmount = amount;
    lastOrderCode = createOrderCode(phone);

    if(els.qrImage) els.qrImage.src = createVietQrUrl(amount, content);
    if(els.paymentAmount) els.paymentAmount.textContent = Number(amount).toLocaleString("vi-VN") + " đ";
    if(els.paymentContent) els.paymentContent.textContent = content;
    if(els.paymentPhone) els.paymentPhone.textContent = phone;
    if(els.paymentOrderCode) els.paymentOrderCode.textContent = lastOrderCode;

    if(els.zaloGeneral) els.zaloGeneral.href = createZaloOrderLink(true);
    if(els.paymentResult) els.paymentResult.classList.add("active");
    if(els.paymentResult) els.paymentResult.scrollIntoView({{behavior: "smooth", block: "center"}});
    toast("Đã tạo QR thanh toán");
  }}

  async function copyText(text, message){{
    try {{
      await navigator.clipboard.writeText(text);
      toast(message || "Đã copy");
    }} catch(err){{
      window.prompt("Copy nội dung này:", text);
    }}
  }}

  function copyPaymentContent(){{
    if(!lastPaymentContent) return showPaymentError("Bạn cần tạo QR trước khi copy nội dung chuyển khoản.");
    copyText(lastPaymentContent, "Đã copy nội dung CK");
  }}

  function copyOrder(){{
    if(!selectedGroup) return;
    copyText(getOrderText(false), "Đã copy đơn hàng");
  }}

  async function confirmPayment(){{
    if(!lastPaymentContent || !lastPaymentAmount || !lastOrderCode){{
      return showPaymentError("Bạn cần tạo QR thanh toán trước, sau đó mới bấm xác nhận đã chuyển khoản.");
    }}
    const orderText = getOrderText(true);
    try {{
      await navigator.clipboard.writeText(orderText);
      toast("Đã copy đơn hàng, đang mở Zalo");
    }} catch(err){{
      window.prompt("Copy đơn hàng này:", orderText);
    }}
    if(els.confirmPaymentBtn) els.confirmPaymentBtn.textContent = "Đã copy đơn hàng ✓";
    if(els.paymentStatusBadge) els.paymentStatusBadge.innerHTML = '<span class="pulse-dot"></span> Đã bấm xác nhận chuyển khoản';
    if(els.paymentNote) els.paymentNote.textContent = "Đơn hàng đã được copy. Zalo sẽ mở kèm ghi chú: khách đã chuyển khoản, shop vui lòng kiểm tra giao dịch và xử lý đơn.";

    const url = createZaloOrderLink(true, true);
    const opened = window.open(url, "_blank", "noopener");
    if(!opened) window.location.href = url;
  }}

  function toast(message){{
    if(!els.toast) return;
    els.toast.textContent = message;
    els.toast.classList.add("active");
    clearTimeout(els.toast._timer);
    els.toast._timer = setTimeout(() => els.toast.classList.remove("active"), 2500);
  }}

  // ===== BIND EVENTS & BOOT =====
  function bindEvents(){{
    if(els.searchInput){{
      els.searchInput.addEventListener("input", e => {{
        searchKeyword = e.target.value;
        renderProducts();
      }});
    }}
    if(els.chips){{
      els.chips.addEventListener("click", e => {{
        const btn = e.target.closest(".chip");
        if(!btn) return;
        selectedCategory = btn.getAttribute("data-cat");
        renderFilters();
        renderProducts();
      }});
    }}
    if(els.categoryFilter){{
      els.categoryFilter.addEventListener("change", e => {{
        selectedCategory = e.target.value;
        renderFilters();
        renderProducts();
      }});
    }}
    if(els.stockFilter){{
      els.stockFilter.addEventListener("change", e => {{
        selectedStock = e.target.value;
        renderProducts();
      }});
    }}

    // Rail Prev & Next Scroll
    if(els.railPrev && els.quickRail){{
      els.railPrev.addEventListener("click", () => {{
        els.quickRail.scrollBy({{left: -240, behavior: "smooth"}});
      }});
    }}
    if(els.railNext && els.quickRail){{
      els.railNext.addEventListener("click", () => {{
        els.quickRail.scrollBy({{left: 240, behavior: "smooth"}});
      }});
    }}
    if(els.quickRail){{
      els.quickRail.addEventListener("scroll", updateRailButtons);
      els.quickRail.addEventListener("click", e => {{
        const item = e.target.closest(".rail-item");
        if(item) openProductModal(item.getAttribute("data-group-id"));
      }});
    }}

    if(els.featuredGrid){{
      els.featuredGrid.addEventListener("click", e => {{
        const card = e.target.closest(".featured-card");
        if(card) openProductModal(card.getAttribute("data-group-id"));
      }});
    }}
    if(els.productGroups){{
      els.productGroups.addEventListener("click", e => {{
        const card = e.target.closest(".product-card");
        if(card) openProductModal(card.getAttribute("data-group-id"));
      }});
    }}
    if(els.productModal){{
      els.productModal.addEventListener("click", e => {{
        if(e.target === els.productModal || e.target.hasAttribute("data-close")) closeProductModal();
      }});
    }}
    document.addEventListener("keydown", e => {{
      if(e.key === "Escape") closeProductModal();
    }});
    if(els.modalPlans){{
      els.modalPlans.addEventListener("click", e => {{
        const opt = e.target.closest(".plan-option");
        if(opt) selectPlan(opt.getAttribute("data-plan-id"));
      }});
    }}

    if(els.createQrBtn) els.createQrBtn.addEventListener("click", generatePaymentQr);
    if(els.copyPaymentBtn) els.copyPaymentBtn.addEventListener("click", copyPaymentContent);
    if(els.copyOrderBtn) els.copyOrderBtn.addEventListener("click", copyOrder);
    if(els.confirmPaymentBtn) els.confirmPaymentBtn.addEventListener("click", confirmPayment);

    // Bottom nav category tab
    if(els.categoryTab){{
      els.categoryTab.addEventListener("click", e => {{
        e.preventDefault();
        if(els.categoryFilter){{
          els.categoryFilter.focus();
          els.categoryFilter.scrollIntoView({{behavior: "smooth", block: "center"}});
        }}
      }});
    }}
  }}

  function boot(){{
    const ids = [
      "totalProducts", "totalPlans", "featuredGrid",
      "searchInput", "chips", "categoryFilter", "stockFilter", "resultCount",
      "quickRail", "railPrev", "railNext", "productGroups", "empty",
      "categoryTab", "productModal", "modalSheet", "modalLogo", "modalTitle",
      "modalSub", "modalProductImage", "modalDesc", "modalPlanCount", "modalPlans",
      "checkoutForm", "selectedPlanBox", "customerName", "customerPhone",
      "createQrBtn", "zaloGeneral", "paymentError", "paymentResult",
      "qrImage", "paymentStatusBadge", "paymentNote", "paymentAmount",
      "paymentContent", "paymentPhone", "paymentOrderCode", "copyPaymentBtn",
      "copyOrderBtn", "confirmPaymentBtn", "toast"
    ];
    ids.forEach(id => els[id] = $(id));

    recomputeCategories();
    renderStats();
    renderFilters();
    renderFeatured();
    renderProducts();
    bindEvents();
  }}

  if(document.readyState === "loading"){{
    document.addEventListener("DOMContentLoaded", boot);
  }} else {{
    boot();
  }}
}})();
"""

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("Generated js/app.js successfully!")
