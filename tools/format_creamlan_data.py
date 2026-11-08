import json

with open('products_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

print(f"Total products in catalog: {len(catalog)}")

# Ensure all items have valid fields for the dark theme UI
for p in catalog:
    # Ensure glow exists
    if not p.get('glow'):
        p['glow'] = "linear-gradient(135deg,#2563eb,#f59e0b)"
    
    # Ensure image exists
    if not p.get('image'):
        p['image'] = p['name'].split()[0].lower() + ".com"

    # Normalize category for the filters in UI:
    # Chips in UI: "AI", "Giải trí", "Thiết kế", "Học tập", "Khác"
    cat = p.get('category', 'Khác')
    if 'AI' in cat or 'Công nghệ' in cat:
        p['category'] = 'Công nghệ & AI'
        p['categoryShort'] = 'AI'
    elif 'Giải trí' in cat:
        p['category'] = 'Giải trí Premium'
        p['categoryShort'] = 'Giải trí'
    elif 'Thiết kế' in cat or 'Đồ họa' in cat:
        p['category'] = 'Thiết kế - chỉnh sửa ảnh/video'
        p['categoryShort'] = 'Thiết kế'
    elif 'Học tập' in cat or 'Ngoại ngữ' in cat:
        p['category'] = 'Học tập & khóa học'
        p['categoryShort'] = 'Học tập'
    else:
        p['category'] = 'Tiện ích & Khác'
        p['categoryShort'] = 'Khác'

    # Check plans
    for pln in p.get('plans', []):
        if not pln.get('accountType'):
            pln['accountType'] = 'Nâng từ email bạn' if 'email' in pln.get('variant', '').lower() else 'Cấp tài khoản'
        if not pln.get('warranty'):
            pln['warranty'] = 'Bảo hành Full'

with open('products_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

print("Updated products_catalog.json successfully!")
