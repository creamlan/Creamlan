import re

with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

# Find all divs with id in original_site.html
ids = re.findall(r'<([a-zA-Z0-9]+)\s+[^>]*id=["\']([^"\']+)["\']', html)
print("Tags with IDs:", ids)

# Find modal
m = re.search(r'(<div\s+id=["\']productModal["\'].*?)(?=<script)', html, re.DOTALL)
if m:
    print("\n--- Modal HTML ---")
    print(m.group(1)[:2500])
