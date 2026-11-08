import json, csv, re

# Let's inspect all products from Google Sheets and all groups from original_site.html

with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

m = re.search(r'const DEFAULT_PRODUCT_GROUPS\s*=\s*(\[.*?\]);\s*const', html, re.DOTALL)
html_groups = json.loads(m.group(1))

html_group_dict = {g['name'].lower().strip(): g for g in html_groups}

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

print(f"Total Sheet items: {len(sheet_items)}")
print(f"Total HTML groups: {len(html_groups)}")

# Let's see all unique product names in Sheet
unique_sheet_names = sorted(list(set(it['name'] for it in sheet_items)))
print(f"\nUnique Sheet product names ({len(unique_sheet_names)}):")
for name in unique_sheet_names:
    print(" -", repr(name))

# Let's check how HTML groups handle icons:
print("\nHTML groups image and icons:")
for g in html_groups:
    print(f"Group: {g['name']} | brand: {g.get('brand')} | image: {g.get('image')} | cat: {g.get('category')}")
