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
            'upgrade_type': r[4].strip() if len(r) > 4 else '',
            'shared_private': r[5].strip() if len(r) > 5 else '',
            'warranty': r[6].strip() if len(r) > 6 else '',
            'commission': r[7].strip() if len(r) > 7 else '',
            'note': r[8].strip() if len(r) > 8 else ''
        })

# Read original HTML groups
with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

m = re.search(r'const DEFAULT_PRODUCT_GROUPS\s*=\s*(\[.*?\]);\s*const', html, re.DOTALL)
html_groups = json.loads(m.group(1))
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

def fmt_price(amt, is_out=False):
    if is_out:
        return "Hết hàng"
    if amt <= 0:
        return "Liên hệ"
    return f"{amt:,.0f} đ".replace(',', '.')

# We will build product items grouped logically.
# Let's inspect how Google Sheet items group into products:
# 1. ChatGPT (GPT Plus, GPT Edu, GPT Business)
# 2. Perplexity AI
# 3. Canva (Canva Edu, Canva Pro)
# 4. CapCut Pro
# 5. Adobe
# 6. Leonardo AI
# 7. Kling AI
# 8. YouTube Premium
# 9. Netflix Premium
# 10. Google Gemini & Drive
# 11. Locket Gold
# 12. Grok Super AI
# 13. Microsoft Office 365 1TB
# 14. Quizlet Plus
# 15. Spotify Premium
# 16. Duolingo Super
# 17. Grammarly
# 18. Meitu SVIP
# 19. HMA VPN
# 20. Picsart Pro
# 21. Claude AI
# 22. VieON VIP

print("Sheet grouping analysis...")
