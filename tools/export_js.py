import json

with open('products_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

js_content = f"""/**
 * Creamlan Store - Product Catalog Data
 * Sourced from Google Sheets (https://docs.google.com/spreadsheets/d/1MvsUV2Gxq3CXyUSEE8b-sAGkhuNoEaHs9HqlNAqaEg4)
 * and original shoponline catalog.
 * Generated automatically.
 */

const DEFAULT_PRODUCTS = {json.dumps(catalog, ensure_ascii=False, indent=2)};

if (typeof window !== 'undefined') {{
  window.DEFAULT_PRODUCTS = DEFAULT_PRODUCTS;
}}

if (typeof module !== 'undefined' && module.exports) {{
  module.exports = {{ DEFAULT_PRODUCTS }};
}}
"""

with open('js/products-data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Wrote js/products-data.js with {len(catalog)} products!")
