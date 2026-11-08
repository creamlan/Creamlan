import re, json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check scripts in index.html
scripts = re.findall(r'<script\s+src=["\']([^"\']+)["\']', html)
print("Scripts loaded:", scripts)
assert 'js/products-data.js' in scripts
assert 'js/sheets-sync.js' in scripts
assert 'js/vietqr.js' in scripts
assert 'js/app.js' in scripts

# Check css in index.html
css = re.findall(r'<link\s+rel=["\']stylesheet["\']\s+href=["\']([^"\']+)["\']', html)
print("CSS loaded:", css)
assert 'css/style.css' in css

# Check products data
with open('js/products-data.js', 'r', encoding='utf-8') as f:
    js_data = f.read()

m = re.search(r'const DEFAULT_PRODUCTS\s*=\s*(\[.*?\]);\s*if', js_data, re.DOTALL)
products = json.loads(m.group(1))
print(f"Products in js/products-data.js: {len(products)}")

# Check key products
keys = ['chatgpt', 'netflix', 'capcut', 'canva', 'youtube', 'locket', 'spotify', 'gemini']
for k in keys:
    found = any(k in p['name'].lower() or k in p['brand'].lower() for p in products)
    print(f"Product '{k}': {'FOUND' if found else 'MISSING'}")
    assert found

# Check VietQR config
with open('js/vietqr.js', 'r', encoding='utf-8') as f:
    vietqr_code = f.read()

assert '970431' in vietqr_code # Eximbank BIN
assert '0327620117' in vietqr_code # STK & Zalo
assert 'CAO THANH HAI' in vietqr_code # Account Name
assert 'https://zalo.me/0327620117' in vietqr_code # Zalo Link
print("VietQR configuration verified!")

print("ALL ASSETS & LOGIC VERIFIED SUCCESSFULLY!")
