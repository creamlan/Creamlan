import json, csv, re

with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

m = re.search(r'const DEFAULT_PRODUCT_GROUPS\s*=\s*(\[.*?\]);\s*const', html, re.DOTALL)
html_groups = json.loads(m.group(1))

with open('google_sheets.csv', 'r', encoding='utf-8', errors='replace') as f:
    sheet_rows = list(csv.reader(f))

sheet_items = []
for idx, r in enumerate(sheet_rows[2:], start=2):
    if len(r) > 3 and (r[1].strip() or r[3].strip()):
        sheet_items.append({
            'row_idx': idx,
            'name': r[1].strip().replace('\n', ' '),
            'duration': r[2].strip(),
            'price_raw': r[3].strip(),
            'upgrade_type': r[4].strip() if len(r) > 4 else '',
            'shared_private': r[5].strip() if len(r) > 5 else '',
            'warranty': r[6].strip() if len(r) > 6 else '',
            'commission': r[7].strip() if len(r) > 7 else '',
            'note': r[8].strip() if len(r) > 8 else ''
        })

print(f"Sheet items: {len(sheet_items)}, HTML groups: {len(html_groups)}")

# Let's see category list in original website
cats = set(g['category'] for g in html_groups)
print("Original categories:", cats)

# Let's inspect the pricing rules from user prompt:
# "Quy tắc điều chỉnh giá bán:
# Đối với sản phẩm có giá trị thấp:
# - Có thể tăng thêm từ 2.000đ đến 10.000đ.
# - Mục tiêu là giúp giá bán trở nên tròn và dễ nhìn hơn.
# - Chỉ áp dụng cho một số sản phẩm phù hợp.
# - Không bắt buộc tăng tất cả sản phẩm giá thấp.
# Đối với sản phẩm có giá trị cao:
# - Giữ nguyên giá bán từ Google Sheets.
# - Không tự ý tăng giá.
# Nguyên tắc chung:
# - Không áp dụng mức tăng giá đồng loạt.
# - Không tự ý giảm giá.
# - Không tự tạo chương trình khuyến mãi.
# - Không làm thay đổi giá gốc trong dữ liệu nguồn.
# - Luôn phân biệt rõ giá gốc và giá bán cuối cùng.
# Ví dụ minh họa:
# - Giá nguồn: 27.000đ -> Giá bán: 30.000đ.
# - Giá nguồn: 43.000đ -> Giá bán: 45.000đ.
# - Giá nguồn: 78.000đ -> Giá bán: 80.000đ.
# - Giá nguồn: 199.000đ -> Giá bán 200.000đ."
