import json, csv, re

with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

m = re.search(r'const DEFAULT_PRODUCT_GROUPS\s*=\s*(\[.*?\]);\s*const', html, re.DOTALL)
html_groups = json.loads(m.group(1))

with open('google_sheets.csv', 'r', encoding='utf-8', errors='replace') as f:
    sheet_rows = list(csv.reader(f))

sheet_items = []
for idx, r in enumerate(sheet_rows[2:], start=2):
    if len(r) > 3 and (r[1].strip() or r[3].strip()):
        sheet_items.append({
            'row_idx': idx,
            'name': r[1].strip().replace('\n', ' '),
            'duration': r[2].strip(),
            'price': r[3].strip(),
            'upgrade_type': r[4].strip() if len(r) > 4 else '',
            'shared_private': r[5].strip() if len(r) > 5 else '',
            'warranty': r[6].strip() if len(r) > 6 else '',
            'commission': r[7].strip() if len(r) > 7 else '',
            'note': r[8].strip() if len(r) > 8 else ''
        })

print("--- MATCHING INVESTIGATION ---")

# Let's see how sheet products match HTML groups
# For each sheet item, find matching HTML group
sheet_to_html = {}
for s in sheet_items:
    s_name_lower = s['name'].lower()
    matched = None
    for g in html_groups:
        g_name_lower = g['name'].lower()
        # Direct contains or equivalence
        if (s_name_lower in g_name_lower or g_name_lower in s_name_lower or
            any(w in g_name_lower for w in s_name_lower.split() if len(w) > 3)):
            matched = g
            break
    sheet_to_html[s['name']] = matched['name'] if matched else 'NO MATCH'

for s_name, g_match in sheet_to_html.items():
    print(f"Sheet: {s_name:<40} -> HTML: {g_match}")

print("\n--- HTML GROUPS NOT MATCHED BY SHEET ---")
matched_html_names = set(sheet_to_html.values())
for g in html_groups:
    if g['name'] not in matched_html_names:
        print(f"HTML only: {g['id']} | {g['name']} | Plans: {[p['variant'] for p in g['plans']]}")
