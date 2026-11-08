import json

with open('products_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

import re
m = re.search(r'const DEFAULT_PRODUCT_GROUPS\s*=\s*(\[.*?\]);\s*const', html, re.DOTALL)
html_groups = json.loads(m.group(1))

catalog_names = set(c['name'].lower() for c in catalog)
catalog_ids = set(c['id'] for c in catalog)

print("Original groups not directly in catalog by name:")
for g in html_groups:
    found = False
    for c in catalog:
        if g['name'].lower() in c['name'].lower() or g['id'] == c['id'] or g['brand'].lower() in c['name'].lower():
            found = True
            break
    if not found:
        print(f"NOT FOUND: {g['id']} - {g['name']}")
    else:
        # Check if matched by exact or brand
        pass
