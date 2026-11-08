import json, re

# Load products catalog
with open('products_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Sort catalog so the top 6 featured products appear first:
# Netflix Premium, ChatGPT Plus, YouTube Premium, Locket Gold, Spotify Premium, Capcut Pro
top_names = ['netflix', 'chatgpt', 'youtube', 'locket', 'spotify', 'capcut']

def sort_key(p):
    pname = p['name'].lower()
    for idx, top in enumerate(top_names):
        if top in pname:
            return (0, idx)
    return (1, p['category'], p['name'])

catalog.sort(key=sort_key)

print(f"Catalog contains {len(catalog)} products.")
for p in catalog[:10]:
    print(" -", p['name'], f"({p['category']}) - {p['priceLabel']}")
