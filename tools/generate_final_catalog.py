import json, csv, re

# 1. Load Google Sheets data
with open('google_sheets.csv', 'r', encoding='utf-8', errors='replace') as f:
    sheet_rows = list(csv.reader(f))

sheet_items = []
for idx, r in enumerate(sheet_rows[2:], start=2):
    if len(r) > 3 and (r[1].strip() or r[3].strip()):
        sheet_items.append({
            'row_idx': idx,
            'name': r[1].strip().replace('\n', ' '),
            'duration': r[2].strip().replace('\n', ' '),
            'price_raw': r[3].strip(),
            'upgrade_type': r[4].strip().replace('\n', ' ') if len(r) > 4 else '',
            'shared_private': r[5].strip().replace('\n', ' ') if len(r) > 5 else '',
            'warranty': r[6].strip().replace('\n', ' ') if len(r) > 6 else '',
            'commission': r[7].strip() if len(r) > 7 else '',
            'note': r[8].strip().replace('\n', ' ') if len(r) > 8 else ''
        })

# 2. Load original HTML groups
with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

m = re.search(r'const DEFAULT_PRODUCT_GROUPS\s*=\s*(\[.*?\]);\s*const', html, re.DOTALL)
html_groups = json.loads(m.group(1))

def parse_price(val):
    if not val:
        return 0, False
    s = str(val).lower().strip()
    if 'hết' in s or 'out' in s or 'tạm' in s or 'liên hệ' in s:
        return 0, True
    nums = re.findall(r'\d+', s.replace('.', '').replace(',', ''))
    if nums:
        return int(nums[0]), False
    return 0, False

def adjust_price(orig_amount):
    if orig_amount <= 0:
        return 0
    if orig_amount >= 200000:
        return orig_amount
    if orig_amount == 18000:
        return 20000
    if orig_amount == 28000:
        return 30000
    if orig_amount == 59000:
        return 60000
    if orig_amount == 88000:
        return 90000
    if orig_amount == 138000:
        return 140000
    if orig_amount == 199000:
        return 200000
    if orig_amount == 27000:
        return 30000
    if orig_amount == 43000:
        return 45000
    if orig_amount == 78000:
        return 80000
    return orig_amount

def fmt_vnd(amt):
    if amt <= 0:
        return ""
    return f"{amt:,.0f} đ".replace(',', '.')

# Canonical Sheet mappings
# Each product in Google Sheet gets assigned to a group:
sheet_group_defs = [
    {
        "id": "crl-gpt",
        "name": "ChatGPT Plus & OpenAI",
        "brand": "OpenAI",
        "category": "Công nghệ & AI",
        "image": "openai.com",
        "glow": "linear-gradient(135deg,#10a37f,#14b8a6,#064e3b)",
        "description": "Tài khoản ChatGPT Plus, GPT Edu, GPT Business hỗ trợ mô hình GPT-4o, o1, Canvas, tạo hình ảnh DALL-E, tốc độ phản hồi nhanh vượt trội.",
        "sheet_indices": [0, 1, 2, 3, 4, 5]
    },
    {
        "id": "crl-perplexity",
        "name": "Perplexity AI Pro",
        "brand": "Perplexity",
        "category": "Công nghệ & AI",
        "image": "perplexity.ai",
        "glow": "linear-gradient(135deg,#20b2aa,#008080,#042f2e)",
        "description": "Công cụ tìm kiếm thông minh và nghiên cứu học thuật bằng AI thế hệ mới, hỗ trợ tra cứu thông tin chính xác kèm nguồn trích dẫn.",
        "sheet_indices": [6, 7],
        "original_group_id": "grp-047"
    },
    {
        "id": "crl-canva",
        "name": "Canva Pro & Edu",
        "brand": "Canva",
        "category": "Thiết kế & Đồ họa",
        "image": "canva.com",
        "glow": "linear-gradient(135deg,#00c4cc,#7d2ae8,#4c1d95)",
        "description": "Nâng cấp Canva Pro / Edu chính chủ từ email cá nhân. Mở khóa kho mẫu thiết kế cao cấp, công cụ xóa phông một chạm và tính năng Magic Studio.",
        "sheet_indices": [8, 9, 10, 11, 12]
    },
    {
        "id": "grp-004", # Keep original id
        "name": "CapCut Pro",
        "brand": "CapCut",
        "category": "Thiết kế & Đồ họa",
        "image": "capcut.com",
        "glow": "linear-gradient(135deg,#000000,#2563eb,#1e1b4b)",
        "description": "Tài khoản CapCut Pro chuyên nghiệp hỗ trợ 2 thiết bị. Mở khóa toàn bộ hiệu ứng VIP, âm thanh độc quyền và xuất video 4K sắc nét.",
        "sheet_indices": [13, 14, 15, 16, 17, 18, 19],
        "original_group_id": "grp-004"
    },
    {
        "id": "crl-adobe",
        "name": "Adobe Creative Cloud",
        "brand": "Adobe",
        "category": "Thiết kế & Đồ họa",
        "image": "adobe.com",
        "glow": "linear-gradient(135deg,#fa0f00,#ff6b6b,#881337)",
        "description": "Bộ công cụ sáng tạo đỉnh cao gồm Photoshop, Illustrator, Premiere Pro, After Effects và hơn 20 ứng dụng chuyên nghiệp của Adobe.",
        "sheet_indices": [20]
    },
    {
        "id": "crl-leonardo",
        "name": "Leonardo.ai Premium",
        "brand": "Leonardo",
        "category": "Công nghệ & AI",
        "image": "leonardo.ai",
        "glow": "linear-gradient(135deg,#a855f7,#ec4899,#581c87)",
        "description": "Nền tảng tạo hình ảnh AI nghệ thuật chuyên sâu, hỗ trợ tạo ảnh độ phân giải cực cao, phong cách đa dạng cho designer và content creator.",
        "sheet_indices": [21, 22]
    },
    {
        "id": "crl-kling",
        "name": "Kling AI Video Generator",
        "brand": "Kling",
        "category": "Công nghệ & AI",
        "image": "klingai.com",
        "glow": "linear-gradient(135deg,#6366f1,#8b5cf6,#312e81)",
        "description": "Công cụ tạo video AI chân thực hàng đầu từ văn bản hoặc hình ảnh, chuyển động mượt mà và vật lý chân thực.",
        "sheet_indices": [23],
        "original_group_id": "grp-053"
    },
    {
        "id": "grp-002",
        "name": "YouTube Premium",
        "brand": "YouTube",
        "category": "Giải trí Premium",
        "image": "youtube.com",
        "glow": "linear-gradient(135deg,#FF0000,#ff4b4b,#7f1d1d)",
        "description": "Trải nghiệm YouTube không quảng cáo, phát trong nền trên điện thoại, tải video xem ngoại tuyến và đi kèm YouTube Music Premium.",
        "sheet_indices": [24, 25, 26],
        "original_group_id": "grp-002"
    },
    {
        "id": "grp-001",
        "name": "Netflix Premium 4K",
        "brand": "Netflix",
        "category": "Giải trí Premium",
        "image": "netflix.com",
        "glow": "linear-gradient(135deg,#E50914,#ff3b30,#450a0a)",
        "description": "Tài khoản xem phim Netflix chuẩn Ultra HD 4K, âm thanh vòm Spatial Audio, đa dạng gói từ xem riêng chính chủ đến tiết kiệm.",
        "sheet_indices": [27, 28, 29, 30],
        "original_group_id": "grp-001"
    },
    {
        "id": "crl-gemini",
        "name": "Google Gemini & Drive 5TB",
        "brand": "Google",
        "category": "Công nghệ & AI",
        "image": "google.com",
        "glow": "linear-gradient(135deg,#4285F4,#34A853,#1e3a8a)",
        "description": "Gói Google One mở rộng 5TB dung lượng lưu trữ Drive kèm quyền truy cập Gemini Pro / Ultra, NotebookLM và họp Google Meet không giới hạn.",
        "sheet_indices": [31, 32, 33, 34, 35]
    },
    {
        "id": "crl-locket",
        "name": "Locket Gold Vĩnh Viễn",
        "brand": "Locket",
        "category": "Tiện ích & Khác",
        "image": "locket.camera",
        "glow": "linear-gradient(135deg,#f59e0b,#eab308,#78350f)",
        "description": "Nâng cấp Locket Gold chính chủ vĩnh viễn cho iOS. Đăng ảnh video dài, biểu tượng cảm xúc độc quyền, cam kết không dính iCloud, chỉ cần gửi username.",
        "sheet_indices": [36]
    },
    {
        "id": "crl-grok",
        "name": "Grok AI Super (xAI)",
        "brand": "xAI",
        "category": "Công nghệ & AI",
        "image": "x.ai",
        "glow": "linear-gradient(135deg,#000000,#52525b,#18181b)",
        "description": "Mô hình trí tuệ nhân tạo Grok của Elon Musk, truy cập thời gian thực dữ liệu mạng xã hội X, tư duy sắc bén và phân tích trực tiếp.",
        "sheet_indices": [37, 38, 39]
    },
    {
        "id": "crl-office",
        "name": "Microsoft 365 Full Bộ Office + 1TB OneDrive",
        "brand": "Microsoft",
        "category": "Tiện ích & Khác",
        "image": "microsoft.com",
        "glow": "linear-gradient(135deg,#0078d4,#0284c7,#0c4a6e)",
        "description": "Bản quyền Office 365 gồm Word, Excel, PowerPoint, Outlook cài đặt trực tiếp trên 5 thiết bị (PC, Mac, iPad, điện thoại) kèm 1TB OneDrive tốc độ cao.",
        "sheet_indices": [40]
    },
    {
        "id": "grp-035",
        "name": "Quizlet Plus",
        "brand": "Quizlet",
        "category": "Học tập & Ngoại ngữ",
        "image": "quizlet.com",
        "glow": "linear-gradient(135deg,#4257b2,#6366f1,#1e1b4b)",
        "description": "Học tập và ghi nhớ flashcard thông minh với chế độ Học bằng AI, làm bài kiểm tra thử không giới hạn, quét văn bản tự động và học ngoại tuyến.",
        "sheet_indices": [41, 42],
        "original_group_id": "grp-035"
    },
    {
        "id": "grp-003",
        "name": "Spotify Premium",
        "brand": "Spotify",
        "category": "Giải trí Premium",
        "image": "spotify.com",
        "glow": "linear-gradient(135deg,#1DB954,#22c55e,#064e3b)",
        "description": "Tài khoản nghe nhạc Spotify Premium nâng cấp chính chủ từ email. Nghe nhạc chất lượng cao lossless, chuyển bài không giới hạn và tải offline.",
        "sheet_indices": [43, 44],
        "original_group_id": "grp-003"
    },
    {
        "id": "grp-009",
        "name": "Duolingo Super",
        "brand": "Duolingo",
        "category": "Học tập & Ngoại ngữ",
        "image": "duolingo.com",
        "glow": "linear-gradient(135deg,#58cc02,#22c55e,#14532d)",
        "description": "Học ngoại ngữ không giới hạn trái tim với Duolingo Super, làm bài ôn luyện cá nhân hóa, xóa bỏ hoàn toàn quảng cáo gây gián đoạn.",
        "sheet_indices": [45],
        "original_group_id": "grp-009"
    },
    {
        "id": "grp-016",
        "name": "Grammarly Premium AI",
        "brand": "Grammarly",
        "category": "Học tập & Ngoại ngữ",
        "image": "grammarly.com",
        "glow": "linear-gradient(135deg,#15c39a,#10b981,#064e3b)",
        "description": "Trợ lý viết tiếng Anh chuyên nghiệp, sửa lỗi ngữ pháp, nâng cao giọng điệu văn bản và gợi ý từ vựng chuẩn xác cho học tập, công việc.",
        "sheet_indices": [46],
        "original_group_id": "grp-016"
    },
    {
        "id": "grp-006",
        "name": "Meitu SVIP",
        "brand": "Meitu",
        "category": "Thiết kế & Đồ họa",
        "image": "meitu.com",
        "glow": "linear-gradient(135deg,#f43f5e,#ec4899,#881337)",
        "description": "Ứng dụng chỉnh sửa ảnh và làm đẹp chân dung đỉnh cao với đầy đủ tính năng trang điểm AI, xóa khuyết điểm, phục chế ảnh cũ và bộ lọc SVIP.",
        "sheet_indices": [47],
        "original_group_id": "grp-006"
    },
    {
        "id": "crl-hma",
        "name": "HMA VPN (HideMyAss)",
        "brand": "HMA",
        "category": "Tiện ích & Khác",
        "image": "hidemyass.com",
        "glow": "linear-gradient(135deg,#f59e0b,#d97706,#78350f)",
        "description": "Dịch vụ VPN bảo mật danh tính trực tuyến hàng đầu với hơn 290 địa điểm máy chủ toàn cầu, bảo vệ kết nối mạng an toàn trên 5 thiết bị.",
        "sheet_indices": [48, 49]
    },
    {
        "id": "crl-picsart",
        "name": "Picsart Pro",
        "brand": "Picsart",
        "category": "Thiết kế & Đồ họa",
        "image": "picsart.com",
        "glow": "linear-gradient(135deg,#ec4899,#f43f5e,#831843)",
        "description": "Bộ công cụ sáng tạo hình ảnh toàn năng trên điện thoại và máy tính, mở khóa kho sticker, phông chữ và công cụ chỉnh sửa độc quyền.",
        "sheet_indices": [50]
    },
    {
        "id": "grp-048",
        "name": "Claude AI Pro & Team (Anthropic)",
        "brand": "Anthropic",
        "category": "Công nghệ & AI",
        "image": "claude.ai",
        "glow": "linear-gradient(135deg,#cc785c,#ea580c,#7c2d12)",
        "description": "Mô hình Claude 3.5 Sonnet và Claude 3.7 đỉnh cao về lập trình, tư duy logic, phân tích dữ liệu lớn với ngữ cảnh dài 200K token.",
        "sheet_indices": [51],
        "original_group_id": "grp-048"
    },
    {
        "id": "crl-vieon",
        "name": "VieON VIP & VIP Pro",
        "brand": "VieON",
        "category": "Giải trí Premium",
        "image": "vieon.vn",
        "glow": "linear-gradient(135deg,#22c55e,#16a34a,#14532d)",
        "description": "Xem trực tiếp phim truyền hình, show giải trí đặc sắc, kênh truyền hình trong nước & quốc tế, gói VIP Pro kèm kho phim Galaxy Play.",
        "sheet_indices": [52, 53]
    }
]

# Track which original group IDs are mapped by sheet groups
covered_orig_group_ids = set()
for sg in sheet_group_defs:
    if "original_group_id" in sg:
        covered_orig_group_ids.add(sg["original_group_id"])

# Also check groups covered by multiple items
# grp-010 (Duolingo Max), grp-011 (Family Duolingo) can be kept as individual products or sub-plans. Let's keep them as individual products so that NO product from original site is missing!
# grp-014, grp-015 (Grammarly EDU): keep as individual products.
# grp-049 (Claude AI Max 5x): keep as individual product.
# grp-051, grp-052 (Kling packages): keep as individual products.
# grp-036 (Quizlet Plus Unlimited): keep as individual product.

final_catalog = []

# Process sheet group definitions
for sg in sheet_group_defs:
    plans = []
    for idx in sg['sheet_indices']:
        s = sheet_items[idx]
        amt, is_out = parse_price(s['price_raw'])
        adj_amt = adjust_price(amt) if (not is_out and amt > 0) else 0
        
        # Build variant text
        variant = s['name']
        plans.append({
            "id": f"pln-{sg['id']}-{len(plans)+1}",
            "variant": variant,
            "duration": s['duration'],
            "accountType": s['upgrade_type'] or "Liên hệ",
            "sharedPrivate": s['shared_private'] or "RIÊNG",
            "warranty": s['warranty'] if s['warranty'] else "Chưa có thông tin bảo hành",
            "price": fmt_vnd(adj_amt) if adj_amt > 0 else ("Hết hàng" if is_out else "Liên hệ"),
            "priceAmount": adj_amt,
            "originalPrice": fmt_vnd(amt) if (amt > 0 and amt != adj_amt) else "",
            "originalPriceAmount": amt,
            "isOutOfStock": is_out,
            "note": s['note'],
            "sheetRow": s['row_idx']
        })
        
    in_stock_prices = [p['priceAmount'] for p in plans if not p['isOutOfStock'] and p['priceAmount'] > 0]
    if in_stock_prices:
        min_p = min(in_stock_prices)
        price_label = f"Từ {fmt_vnd(min_p)}"
    elif any(p['isOutOfStock'] for p in plans):
        price_label = "Tạm hết hàng"
    else:
        price_label = "Liên hệ"
        
    dur_summary = " / ".join(list(dict.fromkeys(p['duration'] for p in plans if p['duration'] and p['duration'] != 'hết hàng')))
    
    final_catalog.append({
        "id": sg['id'],
        "name": sg['name'],
        "brand": sg['brand'],
        "category": sg['category'],
        "image": sg['image'],
        "glow": sg['glow'],
        "description": sg['description'],
        "priceLabel": price_label,
        "durationSummary": dur_summary or "Gói linh hoạt",
        "planCount": len(plans),
        "inStock": len(in_stock_prices) > 0,
        "hasSheetData": True,
        "plans": plans
    })

# Now add all original HTML groups that weren't in covered_orig_group_ids!
for g in html_groups:
    if g['id'] in covered_orig_group_ids:
        continue # Already mapped
        
    # Map plans
    c_plans = []
    for p in g.get('plans', []):
        amt, is_out = parse_price(p.get('price'))
        adj_amt = adjust_price(amt) if (not is_out and amt > 0) else 0
        c_plans.append({
            "id": p.get('id', f"pln-{g['id']}-{len(c_plans)+1}"),
            "variant": p.get('variant', 'Gói dịch vụ'),
            "duration": p.get('duration', '1 tháng'),
            "accountType": p.get('accountType', 'Liên hệ'),
            "sharedPrivate": "RIÊNG",
            "warranty": p.get('warranty') if p.get('warranty') else "Chưa có thông tin bảo hành",
            "price": fmt_vnd(adj_amt) if adj_amt > 0 else (p.get('price') or "Liên hệ"),
            "priceAmount": adj_amt,
            "originalPrice": fmt_vnd(amt) if (amt > 0 and amt != adj_amt) else "",
            "originalPriceAmount": amt,
            "isOutOfStock": is_out or "hết" in str(p.get('price')).lower(),
            "note": p.get('note', ''),
            "sheetRow": None
        })
        
    in_stock_prices = [p['priceAmount'] for p in c_plans if not p['isOutOfStock'] and p['priceAmount'] > 0]
    if in_stock_prices:
        min_p = min(in_stock_prices)
        price_label = f"Từ {fmt_vnd(min_p)}"
    else:
        price_label = g.get('priceLabel', 'Liên hệ')
        
    cat = g.get('category', 'Tiện ích & Khác')
    if 'Học tập' in cat:
        cat = 'Học tập & Ngoại ngữ'
    elif 'Thiết kế' in cat:
        cat = 'Thiết kế & Đồ họa'
    elif 'AI' in cat:
        cat = 'Công nghệ & AI'
    elif 'Giải trí' in cat:
        cat = 'Giải trí Premium'
    else:
        cat = 'Tiện ích & Khác'
        
    final_catalog.append({
        "id": g['id'],
        "name": g['name'],
        "brand": g.get('brand', g['name'].split()[0]),
        "category": cat,
        "image": g.get('image', ''),
        "glow": g.get('glow', 'linear-gradient(135deg,#2563eb,#f59e0b)'),
        "description": g.get('description', f"Dịch vụ {g['name']} chính hãng tại Creamlan Store."),
        "priceLabel": price_label,
        "durationSummary": g.get('durationSummary', '1 tháng / 1 năm'),
        "planCount": len(c_plans),
        "inStock": len(in_stock_prices) > 0 or not any(p['isOutOfStock'] for p in c_plans),
        "hasSheetData": False,
        "plans": c_plans
    })

print(f"Total products in final catalog: {len(final_catalog)}")

# Check that Twinkl and all other products are included:
all_names = [p['name'] for p in final_catalog]
print("Twinkl included?", any('twinkl' in n.lower() for n in all_names))
print("CapCut included?", any('capcut' in n.lower() for n in all_names))
print("Locket included?", any('locket' in n.lower() for n in all_names))
print("Gemini included?", any('gemini' in n.lower() for n in all_names))
print("ChatGPT included?", any('chatgpt' in n.lower() for n in all_names))

with open('products_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(final_catalog, f, ensure_ascii=False, indent=2)

print("Saved products_catalog.json successfully!")
