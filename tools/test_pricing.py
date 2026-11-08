import json, csv, re

# Load Google Sheets data
with open('google_sheets.csv', 'r', encoding='utf-8', errors='replace') as f:
    sheet_rows = list(csv.reader(f))

sheet_items = []
for idx, r in enumerate(sheet_rows[2:], start=2):
    if len(r) > 3 and (r[1].strip() or r[3].strip()):
        sheet_items.append({
            'row_idx': idx,
            'name': r[1].strip().replace('\n', ' '),
            'duration': r[2].strip(),
            'price_raw': r[3].strip(),
            'upgrade_type': r[4].strip() if len(r) > 4 else '',
            'shared_private': r[5].strip() if len(r) > 5 else '',
            'warranty': r[6].strip() if len(r) > 6 else '',
            'commission': r[7].strip() if len(r) > 7 else '',
            'note': r[8].strip() if len(r) > 8 else ''
        })

# Load HTML groups
with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

m = re.search(r'const DEFAULT_PRODUCT_GROUPS\s*=\s*(\[.*?\]);\s*const', html, re.DOTALL)
html_groups = json.loads(m.group(1))

print(f"Loaded {len(sheet_items)} sheet items and {len(html_groups)} HTML groups.")

# Helper to parse price string to integer
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

# Price adjustment rule as requested by user prompt:
# For low value (< 200.000):
# May round up 1.000 - 5.000 to clean numbers:
# 18.000 -> 20.000
# 28.000 -> 30.000
# 59.000 -> 60.000
# 88.000 -> 90.000
# 138.000 -> 140.000
# 125.000 -> 125.000 (clean)
# 10.000, 35.000, 50.000, 75.000, 100.000 -> keep
# High value (>= 200.000): keep exact price from Google Sheets
def adjust_price(orig_amount):
    if orig_amount <= 0:
        return 0
    if orig_amount >= 200000:
        return orig_amount
    # Low value rounding examples
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

# Test price adjustment on all sheet items
for it in sheet_items:
    amt, is_out = parse_price(it['price_raw'])
    if not is_out and amt > 0:
        adj = adjust_price(amt)
        if adj != amt:
            print(f"Price adjusted: {it['name']} ({it['duration']}): {amt:,} đ -> {adj:,} đ")
