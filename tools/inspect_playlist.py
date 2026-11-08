with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

import re
m = re.search(r'const PLAYLIST\s*=\s*\[(.*?)\];', html, re.DOTALL)
if m:
    print(m.group(0))
