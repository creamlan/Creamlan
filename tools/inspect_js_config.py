with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

import re
# check playlist in JS
m = re.search(r'const PLAYLIST\s*=\s*(\[.*?\]);\s*const', html, re.DOTALL)
if m:
    print("Playlist snippet:")
    print(m.group(1))

# check bank config in JS
m2 = re.search(r'(const zaloPhone.*?(?=const DEFAULT_PRODUCT_GROUPS))', html, re.DOTALL)
if m2:
    print("\nBank and Zalo config snippet:")
    print(m2.group(1))
