import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

match = re.search(r'const ids = \[([\s\S]*?)\];', js)
if not match:
    print("Could not find const ids in js/app.js")
    exit(1)

ids_raw = match.group(1)
ids = [x.strip().strip('"').strip("'") for x in ids_raw.split(',') if x.strip().strip('"').strip("'")]

print(f"Checking {len(ids)} IDs from js/app.js:")
missing = []
for el_id in ids:
    pattern = f'id="{el_id}"'
    if pattern in html:
        print(f"  [OK] id=\"{el_id}\"")
    else:
        print(f"  [MISSING] id=\"{el_id}\"")
        missing.append(el_id)

if missing:
    print(f"\nERROR: Missing {len(missing)} IDs in index.html: {missing}")
    exit(1)
else:
    print("\nSUCCESS: All element IDs are present in index.html!")
