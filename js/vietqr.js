/**
 * Creamlan Store - VietQR & Bank Payment Module
 * Eximbank (BIN: 970431)
 * STK: 0327620117
 * Chủ TK: Cao Thanh Hải (CAO THANH HAI)
 * Zalo: 0327620117
 */

const PAYMENT_CONFIG = {
  bankId: "970431", // Eximbank BIN code verified from VietQR API
  bankName: "Eximbank",
  bankFullName: "Ngân hàng TMCP Xuất Nhập khẩu Việt Nam (Eximbank)",
  accountNo: "0327620117",
  accountName: "CAO THANH HAI",
  zaloPhone: "0327620117",
  zaloUrl: "https://zalo.me/0327620117",
  facebookUrl: "https://www.facebook.com/creamlan.1409/"
};

class VietQRManager {
  constructor() {
    this.config = PAYMENT_CONFIG;
  }

  // Generate order reference code: CRL-YYMMDD-XXXX
  generateOrderCode(phone = "") {
    const now = new Date();
    const yy = String(now.getFullYear()).slice(-2);
    const mm = String(now.getMonth() + 1).padStart(2, "0");
    const dd = String(now.getDate()).padStart(2, "0");
    const suffix = phone && phone.length >= 4 
      ? phone.slice(-4) 
      : String(Math.floor(1000 + Math.random() * 9000));
    return `CRL-${yy}${mm}${dd}-${suffix}`;
  }

  // Generate transfer content for bank: CRL [ORDER_CODE] [PHONE]
  createTransferContent(orderCode, phone = "") {
    // Keep it concise and within VietQR character limits (standard max 50 chars, no diacritics)
    const cleanPhone = phone ? phone.replace(/\D/g, "").slice(-4) : "";
    return `${orderCode}${cleanPhone ? " " + cleanPhone : ""}`;
  }

  // Generate VietQR Image URL
  getVietQrUrl(amount, content) {
    const accName = encodeURIComponent(this.config.accountName);
    const addInfo = encodeURIComponent(content);
    return `https://img.vietqr.io/image/${this.config.bankId}-${this.config.accountNo}-compact2.png?amount=${amount}&addInfo=${addInfo}&accountName=${accName}`;
  }

  // Generate Zalo pre-filled message text
  createZaloMessageText(order) {
    const lines = [
      "Xin chào Creamlan, tôi vừa thực hiện thanh toán đơn hàng.",
      "",
      `Mã đơn: ${order.orderCode}`,
      `Sản phẩm: ${order.productName} (${order.planVariant})`,
      `Thời hạn: ${order.duration || "Theo gói"}`,
      `Số lượng: ${order.quantity}`,
      `Số tiền: ${order.totalAmount.toLocaleString("vi-VN")} đ`,
      `Khách hàng: ${order.customerName || "Khách mua lẻ"} - SĐT: ${order.customerPhone || "N/A"}`,
      "",
      "Tôi sẽ gửi ảnh chụp giao dịch chuyển khoản để cửa hàng kiểm tra."
    ];
    return lines.join("\n");
  }

  // Generate Zalo chat link
  createZaloLink(order) {
    const text = this.createZaloMessageText(order);
    return `${this.config.zaloUrl}?text=${encodeURIComponent(text)}`;
  }
}

window.vietQR = new VietQRManager();
