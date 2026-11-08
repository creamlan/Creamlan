import re, json

with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

# Extract the script
script_match = re.search(r'<script\b[^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
if script_match:
    js_content = script_match.group(1)
    
    # Let's extract DEFAULT_PRODUCT_GROUPS
    groups_match = re.search(r'const DEFAULT_PRODUCT_GROUPS\s*=\s*(\[.*?\]);\s*(?:const|let|var|function)', js_content, re.DOTALL)
    if groups_match:
        try:
            groups_json = groups_match.group(1)
            # Some JS might have trailing commas or slight syntax issues, let's parse with json or eval
            groups = json.loads(groups_json)
            print(f"Total product groups: {len(groups)}")
            for g in groups:
                print(f"- Group: {g.get('id')} | {g.get('name')} | {g.get('category')} | items: {len(g.get('items', []))}")
                for it in g.get('items', []):
                    print(f"    * {it.get('name')} | price: {it.get('price')} | originalPrice: {it.get('originalPrice')} | warranty: {it.get('warranty')} | note: {it.get('note', '')}")
        except Exception as e:
            print("Error parsing DEFAULT_PRODUCT_GROUPS as JSON:", e)
            print("Snippet:", groups_match.group(1)[:500])
    else:
        print("Could not find end of DEFAULT_PRODUCT_GROUPS, trying broader regex")

    # Let's check SHEET_API_URL
    api_match = re.search(r'const SHEET_API_URL\s*=\s*["\']([^"\']*)["\']', js_content)
    if api_match:
        print("SHEET_API_URL:", api_match.group(1))

    # Let's check other functions in JS
    funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', js_content)
    print("Functions defined in JS:", funcs)
