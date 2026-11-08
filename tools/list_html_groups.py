import json, re

with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

m = re.search(r'const DEFAULT_PRODUCT_GROUPS\s*=\s*(\[.*?\]);\s*const', html, re.DOTALL)
html_groups = json.loads(m.group(1))

print(f"Total HTML groups: {len(html_groups)}")
for i, g in enumerate(html_groups):
    print(f"{i+1:2d}. {g['id']}: {g['name']} ({g['category']}) - plans: {len(g.get('plans', []))}")
