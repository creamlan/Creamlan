with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

import re
body_match = re.search(r'<body\b[^>]*>(.*?)<script', html, re.DOTALL)
if body_match:
    body_content = body_match.group(1)
    print("Body HTML length:", len(body_content))
    with open('tools/extracted_body.html', 'w', encoding='utf-8') as out:
        out.write(body_content)
    print("Saved tools/extracted_body.html")
