import csv

with open('google_sheets.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

for i, r in enumerate(rows):
    if i == 0:
        print(f"Header: {r}")
        continue
    # Check if empty row or summary row
    content = " | ".join(c.strip() for c in r if c.strip())
    if content:
        print(f"Row {i:2d}: {content}")
