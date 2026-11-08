import csv, json, re

with open('google_sheets.csv', 'r', encoding='utf-8', errors='replace') as f:
    rows = list(csv.reader(f))

sheet_items = []
for idx, r in enumerate(rows[2:], start=2):
    if len(r) > 3 and (r[1].strip() or r[3].strip()):
        sheet_items.append({
            'row': idx,
            'name': r[1].strip().replace('\n', ' '),
            'duration': r[2].strip().replace('\n', ' '),
            'price_raw': r[3].strip(),
            'upgrade_type': r[4].strip().replace('\n', ' ') if len(r) > 4 else '',
            'shared_private': r[5].strip().replace('\n', ' ') if len(r) > 5 else '',
            'warranty': r[6].strip().replace('\n', ' ') if len(r) > 6 else '',
            'note': r[8].strip().replace('\n', ' ') if len(r) > 8 else ''
        })

print(f"Total sheet items: {len(sheet_items)}")

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
        return "Liên hệ"
    return f"{amt:,.0f} đ".replace(',', '.')

# 22 Canonical Services strictly from Google Sheets:
# In preferred display order:
# 1. Netflix Premium
# 2. ChatGPT Plus & OpenAI
# 3. YouTube Premium
# 4. Locket Gold
# 5. Spotify Premium
# 6. CapCut Pro
# 7. Canva Pro & Edu
# 8. Google Gemini & Drive 5TB
# 9. Claude AI Pro
# 10. Grok AI Super
# 11. Leonardo.ai
# 12. Kling AI
# 13. Perplexity AI Pro
# 14. Adobe Creative Cloud
# 15. Microsoft 365 + 1TB OneDrive
# 16. Duolingo Super
# 17. Quizlet Plus
# 18. Grammarly Premium AI
# 19. Meitu SVIP
# 20. Picsart Pro
# 21. VieON VIP & VIP Pro
# 22. HMA VPN (HideMyAss)

products_def = [
    {
        "id": "crl-netflix",
        "name": "Netflix Premium",
        "brand": "Netflix",
        "category": "Giải trí Premium",
        "image": "netflix.com",
        "glow": "linear-gradient(135deg,#E50914,#ff3b30,#450a0a)",
        "description": "Tài khoản xem phim Netflix chất lượng cao Ultra HD 4K, hỗ trợ đa dạng từ gói xem riêng chính chủ đến các gói tiết kiệm.",
        "sheet_indices": [27, 28, 29, 30] # Row 29, 30, 31, 32
    },
    {
        "id": "crl-chatgpt",
        "name": "ChatGPT Plus",
        "brand": "OpenAI",
        "category": "Công nghệ & AI",
        "image": "openai.com",
        "glow": "linear-gradient(135deg,#10a37f,#14b8a6,#064e3b)",
        "description": "Nâng cấp ChatGPT Plus, GPT Edu, GPT Business chính chủ hỗ trợ GPT-4o, o1, Canvas, tạo ảnh DALL-E không giới hạn.",
        "sheet_indices": [0, 1, 2, 3, 4, 5] # Row 2, 3, 4, 5, 6, 7
    },
    {
        "id": "crl-youtube",
        "name": "YouTube Premium",
        "brand": "YouTube",
        "category": "Giải trí Premium",
        "image": "youtube.com",
        "glow": "linear-gradient(135deg,#FF0000,#ff4b4b,#7f1d1d)",
        "description": "Xem YouTube không quảng cáo, phát trong nền khi tắt màn hình, tải video ngoại tuyến và đi kèm YouTube Music Premium.",
        "sheet_indices": [24, 25, 26] # Row 26, 27, 28
    },
    {
        "id": "crl-locket",
        "name": "Locket Gold",
        "brand": "Locket",
        "category": "Tiện ích & Khác",
        "image": "locket.camera",
        "glow": "linear-gradient(135deg,#f59e0b,#eab308,#78350f)",
        "description": "Nâng cấp Locket Gold chính chủ vĩnh viễn cho iOS. Đăng ảnh video dài, cam kết không dính iCloud, gửi username là hoàn thành.",
        "sheet_indices": [36] # Row 38
    },
    {
        "id": "crl-spotify",
        "name": "Spotify Premium",
        "brand": "Spotify",
        "category": "Giải trí Premium",
        "image": "spotify.com",
        "glow": "linear-gradient(135deg,#1DB954,#22c55e,#064e3b)",
        "description": "Tài khoản nghe nhạc Spotify Premium nâng cấp chính chủ từ email. Nghe nhạc chất lượng cao, chuyển bài không giới hạn.",
        "sheet_indices": [43, 44] # Row 45, 46
    },
    {
        "id": "crl-capcut",
        "name": "CapCut Pro",
        "brand": "CapCut",
        "category": "Thiết kế & Đồ họa",
        "image": "capcut.com",
        "glow": "linear-gradient(135deg,#000000,#2563eb,#1e1b4b)",
        "description": "Tài khoản CapCut Pro chuyên nghiệp dùng trên 2 thiết bị. Mở khóa toàn bộ hiệu ứng VIP và xuất video 4K sắc nét.",
        "sheet_indices": [13, 14, 15, 16, 17, 18, 19] # Row 15 - 21
    },
    {
        "id": "crl-canva",
        "name": "Canva Pro",
        "brand": "Canva",
        "category": "Thiết kế & Đồ họa",
        "image": "canva.com",
        "glow": "linear-gradient(135deg,#00c4cc,#7d2ae8,#4c1d95)",
        "description": "Nâng cấp Canva Pro & Edu chính chủ từ email cá nhân. Mở khóa kho mẫu thiết kế cao cấp và công cụ Magic Studio.",
        "sheet_indices": [8, 9, 10, 11, 12] # Row 10 - 14
    },
    {
        "id": "crl-gemini",
        "name": "Google Gemini & Drive",
        "brand": "Google",
        "category": "Công nghệ & AI",
        "image": "google.com",
        "glow": "linear-gradient(135deg,#4285F4,#34A853,#1e3a8a)",
        "description": "Gói Google One mở rộng 5TB dung lượng lưu trữ Drive kèm quyền truy cập Gemini Pro / Ultra và NotebookLM không giới hạn.",
        "sheet_indices": [31, 32, 33, 34, 35] # Row 33 - 37
    },
    {
        "id": "crl-claude",
        "name": "Claude AI Pro",
        "brand": "Anthropic",
        "category": "Công nghệ & AI",
        "image": "claude.ai",
        "glow": "linear-gradient(135deg,#cc785c,#ea580c,#7c2d12)",
        "description": "Mô hình Claude 3.5 Sonnet và Claude 3.7 đỉnh cao về lập trình, tư duy logic, phân tích dữ liệu lớn ngữ cảnh 200K token.",
        "sheet_indices": [51] # Row 53
    },
    {
        "id": "crl-grok",
        "name": "Grok AI Super",
        "brand": "xAI",
        "category": "Công nghệ & AI",
        "image": "x.ai",
        "glow": "linear-gradient(135deg,#000000,#52525b,#18181b)",
        "description": "Trí tuệ nhân tạo Grok của Elon Musk, truy cập thời gian thực mạng xã hội X, tư duy sắc bén và phân tích trực tiếp.",
        "sheet_indices": [37, 38, 39] # Row 39 - 41
    },
    {
        "id": "crl-leonardo",
        "name": "Leonardo.ai",
        "brand": "Leonardo",
        "category": "Công nghệ & AI",
        "image": "leonardo.ai",
        "glow": "linear-gradient(135deg,#a855f7,#ec4899,#581c87)",
        "description": "Nền tảng tạo hình ảnh AI nghệ thuật chuyên sâu, hỗ trợ tạo ảnh độ phân giải cao cho designer và sáng tạo nội dung.",
        "sheet_indices": [21, 22] # Row 23, 24
    },
    {
        "id": "crl-kling",
        "name": "Kling AI",
        "brand": "Kling",
        "category": "Công nghệ & AI",
        "image": "klingai.com",
        "glow": "linear-gradient(135deg,#6366f1,#8b5cf6,#312e81)",
        "description": "Công cụ tạo video AI chân thực hàng đầu thế giới từ văn bản và hình ảnh, chuyển động mượt mà và vật lý chân thực.",
        "sheet_indices": [23] # Row 25
    },
    {
        "id": "crl-perplexity",
        "name": "Perplexity AI Pro",
        "brand": "Perplexity",
        "category": "Công nghệ & AI",
        "image": "perplexity.ai",
        "glow": "linear-gradient(135deg,#20b2aa,#008080,#042f2e)",
        "description": "Công cụ tìm kiếm thông minh và nghiên cứu học thuật bằng AI thế hệ mới, trích dẫn nguồn tài liệu chính xác tuyệt đối.",
        "sheet_indices": [6, 7] # Row 8, 9
    },
    {
        "id": "crl-adobe",
        "name": "Adobe Creative Cloud",
        "brand": "Adobe",
        "category": "Thiết kế & Đồ họa",
        "image": "adobe.com",
        "glow": "linear-gradient(135deg,#fa0f00,#ff6b6b,#881337)",
        "description": "Bộ công cụ sáng tạo gồm Photoshop, Illustrator, Premiere Pro, After Effects và hơn 20 ứng dụng chuyên nghiệp của Adobe.",
        "sheet_indices": [20] # Row 22
    },
    {
        "id": "crl-office",
        "name": "Microsoft 365 Full Bộ Office",
        "brand": "Microsoft",
        "category": "Tiện ích & Khác",
        "image": "microsoft.com",
        "glow": "linear-gradient(135deg,#0078d4,#0284c7,#0c4a6e)",
        "description": "Bản quyền Office 365 gồm Word, Excel, PowerPoint, Outlook cài trên 5 thiết bị kèm 1TB OneDrive tốc độ cao.",
        "sheet_indices": [40] # Row 42
    },
    {
        "id": "crl-duolingo",
        "name": "Duolingo Super",
        "brand": "Duolingo",
        "category": "Học tập & Ngoại ngữ",
        "image": "duolingo.com",
        "glow": "linear-gradient(135deg,#58cc02,#22c55e,#14532d)",
        "description": "Học ngoại ngữ không giới hạn trái tim với Duolingo Super, làm bài luyện cá nhân hóa, xóa bỏ hoàn toàn quảng cáo.",
        "sheet_indices": [45] # Row 47
    },
    {
        "id": "crl-quizlet",
        "name": "Quizlet Plus",
        "brand": "Quizlet",
        "category": "Học tập & Ngoại ngữ",
        "image": "quizlet.com",
        "glow": "linear-gradient(135deg,#4257b2,#6366f1,#1e1b4b)",
        "description": "Học tập và ghi nhớ flashcard thông minh với chế độ Học AI, làm bài kiểm tra thử không giới hạn và học ngoại tuyến.",
        "sheet_indices": [41, 42] # Row 43, 44
    },
    {
        "id": "crl-grammarly",
        "name": "Grammarly Premium AI",
        "brand": "Grammarly",
        "category": "Học tập & Ngoại ngữ",
        "image": "grammarly.com",
        "glow": "linear-gradient(135deg,#15c39a,#10b981,#064e3b)",
        "description": "Trợ lý viết tiếng Anh chuyên nghiệp, sửa lỗi ngữ pháp, cải thiện câu từ và gợi ý từ vựng chuẩn xác cho công việc.",
        "sheet_indices": [46] # Row 48
    },
    {
        "id": "crl-meitu",
        "name": "Meitu SVIP",
        "brand": "Meitu",
        "category": "Thiết kế & Đồ họa",
        "image": "meitu.com",
        "glow": "linear-gradient(135deg,#f43f5e,#ec4899,#881337)",
        "description": "Ứng dụng chỉnh sửa ảnh chân dung đỉnh cao với tính năng trang điểm AI, xóa khuyết điểm, phục chế ảnh cũ và bộ lọc SVIP.",
        "sheet_indices": [47] # Row 49
    },
    {
        "id": "crl-picsart",
        "name": "Picsart Pro",
        "brand": "Picsart",
        "category": "Thiết kế & Đồ họa",
        "image": "picsart.com",
        "glow": "linear-gradient(135deg,#ec4899,#f43f5e,#831843)",
        "description": "Bộ công cụ sáng tạo hình ảnh toàn năng trên điện thoại và máy tính, mở khóa kho sticker, phông chữ và bộ lọc độc quyền.",
        "sheet_indices": [50] # Row 52
    },
    {
        "id": "crl-vieon",
        "name": "VieON VIP & VIP Pro",
        "brand": "VieON",
        "category": "Giải trí Premium",
        "image": "vieon.vn",
        "glow": "linear-gradient(135deg,#22c55e,#16a34a,#14532d)",
        "description": "Xem trực tiếp phim truyền hình, show giải trí đặc sắc, kênh truyền hình trong nước & quốc tế, gói VIP Pro kèm kho phim Galaxy Play.",
        "sheet_indices": [52, 53] # Row 54, 55
    },
    {
        "id": "crl-hma",
        "name": "HMA VPN (HideMyAss)",
        "brand": "HMA",
        "category": "Tiện ích & Khác",
        "image": "hidemyass.com",
        "glow": "linear-gradient(135deg,#f59e0b,#d97706,#78350f)",
        "description": "Dịch vụ VPN bảo mật danh tính trực tuyến hàng đầu với hơn 290 địa điểm máy chủ toàn cầu trên 5 thiết bị.",
        "sheet_indices": [48, 49] # Row 50, 51
    }
]

# Verify all 54 items in sheet are covered
covered = set()
for p in products_def:
    for idx in p['sheet_indices']:
        covered.add(idx)

print(f"Total sheet items covered: {len(covered)} / {len(sheet_items)}")
assert len(covered) == len(sheet_items), f"Missing: {set(range(len(sheet_items))) - covered}"
print("✓ Exactly 100% of Google Sheets items are mapped into these 22 products!")
