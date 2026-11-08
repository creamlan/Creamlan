import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('js/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

ids_in_js = re.findall(r'document\.getElementById\(["\']([^"\']+)["\']\)', app_js)
ids_in_html = set(re.findall(r'id=["\']([^"\']+)["\']', html))

missing = []
for i in set(ids_in_js):
    # Some IDs may be created dynamically like btnResetFilters
    if i not in ids_in_html and i != 'btnResetFilters':
        missing.append(i)

if not missing:
    print(f"✓ All {len(set(ids_in_js))} IDs in JS are present in HTML!")
else:
    print("Missing IDs:", missing)
