with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

import re

# Find sections
sections = re.findall(r'<section\b[^>]*id=["\']([^"\']+)["\']', html)
print("Sections with id:", sections)

# Find CSS variables and colors
css_vars = re.findall(r'(--[a-zA-Z0-9_-]+:\s*[^;]+;)', html)
print("CSS Vars (first 25):", css_vars[:25])

# Find JavaScript track list (for the music player)
tracks = re.search(r'const PLAYLIST\s*=\s*(\[.*?\]);', html, re.DOTALL)
if tracks:
    print("Playlist found:", tracks.group(1)[:300])
