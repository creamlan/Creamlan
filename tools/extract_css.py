with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

import re
style_match = re.search(r'<style\b[^>]*>(.*?)</style>', html, re.DOTALL)
if style_match:
    css_content = style_match.group(1)
    with open('css/style.css', 'w', encoding='utf-8') as out:
        out.write(css_content)
    print(f"Extracted {len(css_content)} bytes of original CSS to css/style.css")
