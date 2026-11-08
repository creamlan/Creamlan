import re, json, csv

with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

m = re.search(r'const DEFAULT_PRODUCT_GROUPS\s*=\s*(\[.*?\]);\s*const', html, re.DOTALL)
groups = json.loads(m.group(1))

print(f"Total groups in HTML: {len(groups)}")

with open('google_sheets.csv', 'r', encoding='utf-8', errors='replace') as f:
    sheet_rows = list(csv.reader(f))

# Header is row 1
header = sheet_rows[1]
print("Sheet Header:", header)

# Data rows from row 2
sheet_items = []
for idx, r in enumerate(sheet_rows[2:], start=2):
    if len(r) > 3 and (r[1].strip() or r[3].strip()):
        sheet_items.append({
            'row_idx': idx,
            'name': r[1].strip(),
            'duration': r[2].strip(),
            'price': r[3].strip(),
            'upgrade_type': r[4].strip() if len(r) > 4 else '',
            'shared_private': r[5].strip() if len(r) > 5 else '',
            'warranty': r[6].strip() if len(r) > 6 else '',
            'commission': r[7].strip() if len(r) > 7 else '',
            'note': r[8].strip() if len(r) > 8 else ''
        })

print(f"Total valid items in Sheet: {len(sheet_items)}")

# Let's inspect all sheet items
print("\n--- ALL SHEET ITEMS ---")
for it in sheet_items:
    print(f"Row {it['row_idx']:2d}: {it['name']} | Hạn: {it['duration']} | Giá: {it['price']} | Hình thức: {it['upgrade_type']} | Dùng: {it['shared_private']} | BH: {it['warranty']} | Note: {it['note']}")

# Let's inspect all groups in original HTML
print("\n--- ALL HTML GROUPS ---")
for g in groups:
    plans_info = [f"{p.get('variant', '')} ({p.get('duration', '')}) - {p.get('price', '')}" for p in g.get('plans', [])]
    print(f"{g['id']}: {g['name']} | Cat: {g['category']} | Brand: {g.get('brand')} | Plans: {plans_info}")
