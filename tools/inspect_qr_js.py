with open('original_site.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

import re
# check functions around generatePaymentQr, createVietQrUrl, confirmPayment, etc.
m = re.search(r'(function generatePaymentQr.*?)(?=function updatePlayerUI)', html, re.DOTALL)
if m:
    print(m.group(1)[:3000])
