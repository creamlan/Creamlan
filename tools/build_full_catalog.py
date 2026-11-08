import json, csv, re

# Read Google Sheets
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

# Read original HTML groups
with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

m = re.search(r'const DEFAULT_PRODUCT_GROUPS\s*=\s*(\[.*?\]);\s*const', html, re.DOTALL)
html_groups = json.loads(m.group(1))
html_group_by_name = {g['name'].lower().strip(): g for g in html_groups}
html_group_by_id = {g['id']: g for g in html_groups}

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

# Let's map sheet items into groups
# Key = canonical group identifier
sheet_groups = {
    "crl-chatgpt": {
        "id": "crl-chatgpt",
        "name": "ChatGPT Plus & OpenAI",
        "brand": "OpenAI",
        "category": "Công nghệ & AI",
        "image": "openai.com",
        "glow": "linear-gradient(135deg,#10a37f,#14b8a6,#064e3b)",
        "description": "Tài khoản ChatGPT Plus, GPT Edu, GPT Business hỗ trợ mô hình GPT-4o, o1, Canvas, tạo hình ảnh DALL-E, tốc độ phản hồi nhanh vượt trội.",
        "sheet_item_indices": [0, 1, 2, 3, 4, 5] # GPT EDU, GPT PLUS 1T, GPT PLUS cấp acc, GPT PLUS 6T, GPT PLUS 3T, GPT BUSSINESS
    },
    "crl-perplexity": {
        "id": "crl-perplexity",
        "name": "Perplexity AI Pro",
        "brand": "Perplexity",
        "category": "Công nghệ & AI",
        "image": "perplexity.ai",
        "glow": "linear-gradient(135deg,#20b2aa,#008080,#042f2e)",
        "description": "Công cụ tìm kiếm thông minh và nghiên cứu học thuật bằng AI thế hệ mới, hỗ trợ tra cứu thông tin chính xác kèm nguồn trích dẫn.",
        "sheet_item_indices": [6, 7] # 1T, 12T
    },
    "crl-canva": {
        "id": "crl-canva",
        "name": "Canva Pro & Edu",
        "brand": "Canva",
        "category": "Thiết kế & Đồ họa",
        "image": "canva.com",
        "glow": "linear-gradient(135deg,#00c4cc,#7d2ae8,#4c1d95)",
        "description": "Nâng cấp Canva Pro / Edu chính chủ từ email cá nhân. Mở khóa kho mẫu thiết kế cao cấp, công cụ xóa phông một chạm và tính năng Magic Studio.",
        "sheet_item_indices": [8, 9, 10, 11, 12] # Canva Edu 1N, 3N, Canva Pro 12T, 6T, 1T
    },
    "crl-capcut": {
        "id": "crl-capcut",
        "name": "CapCut Pro",
        "brand": "CapCut",
        "category": "Thiết kế & Đồ họa",
        "image": "capcut.com",
        "glow": "linear-gradient(135deg,#000000,#2563eb,#1e1b4b)",
        "description": "Tài khoản CapCut Pro chuyên nghiệp hỗ trợ 2 thiết bị. Mở khóa toàn bộ hiệu ứng VIP, âm thanh độc quyền và xuất video 4K sắc nét.",
        "sheet_item_indices": [13, 14, 15, 16, 17, 18, 19] # CapCut 7 ngày, 1T, 3T, 6T, 1N lẻ, 1N full, 6T full
    },
    "crl-adobe": {
        "id": "crl-adobe",
        "name": "Adobe Creative Cloud",
        "brand": "Adobe",
        "category": "Thiết kế & Đồ họa",
        "image": "adobe.com",
        "glow": "linear-gradient(135deg,#fa0f00,#ff6b6b,#881337)",
        "description": "Bộ công cụ sáng tạo đỉnh cao gồm Photoshop, Illustrator, Premiere Pro, After Effects và hơn 20 ứng dụng chuyên nghiệp của Adobe.",
        "sheet_item_indices": [20] # ADOBE 2 tháng
    },
    "crl-leonardo": {
        "id": "crl-leonardo",
        "name": "Leonardo.ai Premium",
        "brand": "Leonardo",
        "category": "Công nghệ & AI",
        "image": "leonardo.ai",
        "glow": "linear-gradient(135deg,#a855f7,#ec4899,#581c87)",
        "description": "Nền tảng tạo hình ảnh AI nghệ thuật chuyên sâu, hỗ trợ tạo ảnh độ phân giải cực cao, phong cách đa dạng cho designer và content creator.",
        "sheet_item_indices": [21, 22] # Artisan Ultimate, Gói Meatro
    },
    "crl-kling": {
        "id": "crl-kling",
        "name": "Kling AI Video Generator",
        "brand": "Kling",
        "category": "Công nghệ & AI",
        "image": "klingai.com",
        "glow": "linear-gradient(135deg,#6366f1,#8b5cf6,#312e81)",
        "description": "Công cụ tạo video AI chân thực hàng đầu từ văn bản hoặc hình ảnh, chuyển động mượt mà và vật lý chân thực.",
        "sheet_item_indices": [23] # KLING AI 1100 CREDIT
    },
    "crl-youtube": {
        "id": "crl-youtube",
        "name": "YouTube Premium",
        "brand": "YouTube",
        "category": "Giải trí Premium",
        "image": "youtube.com",
        "glow": "linear-gradient(135deg,#FF0000,#ff4b4b,#7f1d1d)",
        "description": "Trải nghiệm YouTube không quảng cáo, phát trong nền trên điện thoại, tải video xem ngoại tuyến và đi kèm YouTube Music Premium.",
        "sheet_item_indices": [24, 25, 26] # YT FAMILY 1T, 6T, 12T
    },
    "crl-netflix": {
        "id": "crl-netflix",
        "name": "Netflix Premium 4K",
        "brand": "Netflix",
        "category": "Giải trí Premium",
        "image": "netflix.com",
        "glow": "linear-gradient(135deg,#E50914,#ff3b30,#450a0a)",
        "description": "Tài khoản xem phim Netflix chuẩn Ultra HD 4K, âm thanh vòm Spatial Audio, đa dạng gói từ xem riêng chính chủ đến tiết kiệm.",
        "sheet_item_indices": [27, 28, 29, 30] # NEXFLIX standard, premium, giá rẻ, chính chủ riêng 4k
    },
    "crl-gemini": {
        "id": "crl-gemini",
        "name": "Google Gemini & Drive 5TB",
        "brand": "Google",
        "category": "Công nghệ & AI",
        "image": "google.com",
        "glow": "linear-gradient(135deg,#4285F4,#34A853,#1e3a8a)",
        "description": "Gói Google One mở rộng 5TB dung lượng lưu trữ Drive kèm quyền truy cập Gemini Pro / Ultra, NotebookLM và họp Google Meet không giới hạn.",
        "sheet_item_indices": [31, 32, 33, 34, 35] # Ultra x20, Ultra x5, Gemini Pro 12T, 12T 1 ngày, 1 năm add fam
    },
    "crl-locket": {
        "id": "crl-locket",
        "name": "Locket Gold Vĩnh Viễn",
        "brand": "Locket",
        "category": "Tiện ích & Khác",
        "image": "locket.camera",
        "glow": "linear-gradient(135deg,#f59e0b,#eab308,#78350f)",
        "description": "Nâng cấp Locket Gold chính chủ vĩnh viễn cho iOS. Đăng ảnh video dài, biểu tượng cảm xúc độc quyền, cam kết không dính iCloud, chỉ cần gửi username.",
        "sheet_item_indices": [36] # LOCKET GOLD VĨNH VIỄN
    },
    "crl-grok": {
        "id": "crl-grok",
        "name": "Grok AI Super (xAI)",
        "brand": "xAI",
        "category": "Công nghệ & AI",
        "image": "x.ai",
        "glow": "linear-gradient(135deg,#000000,#52525b,#18181b)",
        "description": "Mô hình trí tuệ nhân tạo Grok của Elon Musk, truy cập thời gian thực dữ liệu mạng xã hội X, tư duy sắc bén và phân tích trực tiếp.",
        "sheet_item_indices": [37, 38, 39] # Grok 12T, 6T, 1T
    },
    "crl-office": {
        "id": "crl-office",
        "name": "Microsoft 365 Full Bộ Office + 1TB OneDrive",
        "brand": "Microsoft",
        "category": "Học tập & Ngoại ngữ",
        "image": "microsoft.com",
        "glow": "linear-gradient(135deg,#0078d4,#0284c7,#0c4a6e)",
        "description": "Bản quyền Office 365 gồm Word, Excel, PowerPoint, Outlook cài đặt trực tiếp trên 5 thiết bị (PC, Mac, iPad, điện thoại) kèm 1TB OneDrive tốc độ cao.",
        "sheet_item_indices": [40] # MICROSOFT FULL BỘ OFFICE 1TB
    },
    "crl-quizlet": {
        "id": "crl-quizlet",
        "name": "Quizlet Plus",
        "brand": "Quizlet",
        "category": "Học tập & Ngoại ngữ",
        "image": "quizlet.com",
        "glow": "linear-gradient(135deg,#4257b2,#6366f1,#1e1b4b)",
        "description": "Học tập và ghi nhớ flashcard thông minh với chế độ Học bằng AI, làm bài kiểm tra thử không giới hạn, quét văn bản tự động và học ngoại tuyến.",
        "sheet_item_indices": [41, 42] # QUIZLET 1T, 12T
    },
    "crl-spotify": {
        "id": "crl-spotify",
        "name": "Spotify Premium",
        "brand": "Spotify",
        "category": "Giải trí Premium",
        "image": "spotify.com",
        "glow": "linear-gradient(135deg,#1DB954,#22c55e,#064e3b)",
        "description": "Tài khoản nghe nhạc Spotify Premium nâng cấp chính chủ từ email. Nghe nhạc chất lượng cao lossless, chuyển bài không giới hạn và tải offline.",
        "sheet_item_indices": [43, 44] # SPOTIFY 12T, 6T
    },
    "crl-duolingo": {
        "id": "crl-duolingo",
        "name": "Duolingo Super",
        "brand": "Duolingo",
        "category": "Học tập & Ngoại ngữ",
        "image": "duolingo.com",
        "glow": "linear-gradient(135deg,#58cc02,#22c55e,#14532d)",
        "description": "Học ngoại ngữ không giới hạn trái tim với Duolingo Super, làm bài ôn luyện cá nhân hóa, xóa bỏ hoàn toàn quảng cáo gây gián đoạn.",
        "sheet_item_indices": [45] # DOULINGO SUPER 12T
    },
    "crl-grammarly": {
        "id": "crl-grammarly",
        "name": "Grammarly Premium AI",
        "brand": "Grammarly",
        "category": "Học tập & Ngoại ngữ",
        "image": "grammarly.com",
        "glow": "linear-gradient(135deg,#15c39a,#10b981,#064e3b)",
        "description": "Trợ lý viết tiếng Anh chuyên nghiệp, sửa lỗi ngữ pháp, nâng cao giọng điệu văn bản và gợi ý từ vựng chuẩn xác cho học tập, công việc.",
        "sheet_item_indices": [46] # GRAMMALY 1T
    },
    "crl-meitu": {
        "id": "crl-meitu",
        "name": "Meitu SVIP",
        "brand": "Meitu",
        "category": "Thiết kế & Đồ họa",
        "image": "meitu.com",
        "glow": "linear-gradient(135deg,#f43f5e,#ec4899,#881337)",
        "description": "Ứng dụng chỉnh sửa ảnh và làm đẹp chân dung đỉnh cao với đầy đủ tính năng trang điểm AI, xóa khuyết điểm, phục chế ảnh cũ và bộ lọc SVIP.",
        "sheet_item_indices": [47] # MEITU SVIP 1T
    },
    "crl-hma": {
        "id": "crl-hma",
        "name": "HMA VPN (HideMyAss)",
        "brand": "HMA",
        "category": "Tiện ích & Khác",
        "image": "hidemyass.com",
        "glow": "linear-gradient(135deg,#f59e0b,#d97706,#78350f)",
        "description": "Dịch vụ VPN bảo mật danh tính trực tuyến hàng đầu với hơn 290 địa điểm máy chủ toàn cầu, bảo vệ kết nối mạng an toàn trên 5 thiết bị.",
        "sheet_item_indices": [48, 49] # HMA IOS 1T, HMA ANDROID 1T
    },
    "crl-picsart": {
        "id": "crl-picsart",
        "name": "Picsart Pro",
        "brand": "Picsart",
        "category": "Thiết kế & Đồ họa",
        "image": "picsart.com",
        "glow": "linear-gradient(135deg,#ec4899,#f43f5e,#831843)",
        "description": "Bộ công cụ sáng tạo hình ảnh toàn năng trên điện thoại và máy tính, mở khóa kho sticker, phông chữ và công cụ chỉnh sửa độc quyền.",
        "sheet_item_indices": [50] # PISCART PRO 12T
    },
    "crl-claude": {
        "id": "crl-claude",
        "name": "Claude AI Pro & Team (Anthropic)",
        "brand": "Anthropic",
        "category": "Công nghệ & AI",
        "image": "claude.ai",
        "glow": "linear-gradient(135deg,#cc785c,#ea580c,#7c2d12)",
        "description": "Mô hình Claude 3.5 Sonnet và Claude 3.7 đỉnh cao về lập trình, tư duy logic, phân tích dữ liệu lớn với ngữ cảnh dài 200K token.",
        "sheet_item_indices": [51] # CLAUDE PRO 1T
    },
    "crl-vieon": {
        "id": "crl-vieon",
        "name": "VieON VIP & VIP Pro",
        "brand": "VieON",
        "category": "Giải trí Premium",
        "image": "vieon.vn",
        "glow": "linear-gradient(135deg,#22c55e,#16a34a,#14532d)",
        "description": "Xem trực tiếp phim truyền hình, show giải trí đặc sắc, kênh truyền hình trong nước & quốc tế, gói VIP Pro kèm kho phim Galaxy Play.",
        "sheet_item_indices": [52, 53] # VIEON VIP 1T, VIEON VIP Pro 12T
    }
}

# Now let's assemble each group with its plans
built_groups = []
used_sheet_indices = set()

for gid, gdef in sheet_groups.items():
    plans = []
    for s_idx in gdef['sheet_item_indices']:
        if s_idx < len(sheet_items):
            s = sheet_items[s_idx]
            used_sheet_indices.add(s_idx)
            amt, is_out = parse_price(s['price_raw'])
            adj_amt = adjust_price(amt) if (not is_out and amt > 0) else 0
            
            # Format variant label
            variant = s['name']
            # If variant contains duration or generic name, make it descriptive
            dur = s['duration']
            acc_type = s['upgrade_type']
            shared_pvt = s['shared_private']
            
            plans.append({
                "id": f"pln-{gid}-{len(plans)+1}",
                "variant": variant,
                "duration": dur,
                "accountType": acc_type,
                "sharedPrivate": shared_pvt,
                "warranty": s['warranty'] if s['warranty'] else "Chưa có thông tin bảo hành",
                "price": fmt_vnd(adj_amt) if adj_amt > 0 else ("Hết hàng" if is_out else "Liên hệ"),
                "priceAmount": adj_amt,
                "originalPrice": fmt_vnd(amt) if (amt > 0 and amt != adj_amt) else "",
                "originalPriceAmount": amt,
                "isOutOfStock": is_out,
                "note": s['note'],
                "sheetRow": s['row_idx']
            })
    
    # Calculate priceLabel and summary
    in_stock_prices = [p['priceAmount'] for p in plans if not p['isOutOfStock'] and p['priceAmount'] > 0]
    if in_stock_prices:
        min_p = min(in_stock_prices)
        price_label = f"Từ {fmt_vnd(min_p)}"
    elif any(p['isOutOfStock'] for p in plans):
        price_label = "Tạm hết hàng"
    else:
        price_label = "Liên hệ"
        
    dur_summary = " / ".join(list(dict.fromkeys(p['duration'] for p in plans if p['duration'] and p['duration'] != 'hết hàng')))
    
    built_groups.append({
        "id": gid,
        "name": gdef['name'],
        "brand": gdef['brand'],
        "category": gdef['category'],
        "image": gdef['image'],
        "glow": gdef['glow'],
        "description": gdef['description'],
        "priceLabel": price_label,
        "durationSummary": dur_summary or "Gói linh hoạt",
        "planCount": len(plans),
        "inStock": len(in_stock_prices) > 0,
        "plans": plans
    })

print(f"Built {len(built_groups)} primary groups from Sheet. Sheet items used: {len(used_sheet_indices)} of {len(sheet_items)}")

# Now add products from original website that are not already covered:
# We preserve all original products!
for g in html_groups:
    # Check if this HTML group is already covered by one of our sheet groups
    # E.g. Netflix, YouTube, Spotify, CapCut, Meitu, Claude, Kling, Perplexity, Quizlet, Duolingo, Grammarly
    g_name_lower = g['name'].lower()
    
    already_covered = False
    for bg in built_groups:
        if bg['brand'].lower() in g_name_lower or g_name_lower in bg['name'].lower():
            # If the HTML group has extra plans not in Sheet, we can merge or skip duplicate
            already_covered = True
            break
            
    if not already_covered:
        # Convert plans
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
            
        # Map category cleanly
        cat = g.get('category', 'Khác')
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
            
        built_groups.append({
            "id": g['id'],
            "name": g['name'],
            "brand": g.get('brand', g['name'].split()[0]),
            "category": cat,
            "image": g.get('image', ''),
            "glow": g.get('glow', 'linear-gradient(135deg,#2563eb,#f59e0b)'),
            "description": g.get('description', f"Dịch vụ {g['name']} bản quyền chính hãng tại Creamlan Store."),
            "priceLabel": price_label,
            "durationSummary": g.get('durationSummary', '1 tháng / 1 năm'),
            "planCount": len(c_plans),
            "inStock": len(in_stock_prices) > 0 or not any(p['isOutOfStock'] for p in c_plans),
            "plans": c_plans
        })

print(f"Total catalog groups after merge: {len(built_groups)}")

# Output summary by category
cat_counts = {}
for bg in built_groups:
    cat_counts[bg['category']] = cat_counts.get(bg['category'], 0) + 1

for cat, count in cat_counts.items():
    print(f"  - {cat}: {count} products")

# Save to JSON
with open('products_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(built_groups, f, ensure_ascii=False, indent=2)

print("Saved to products_catalog.json!")
