(function(){
  "use strict";

  // ===== THÔNG TIN CREAMLAN STORE & TÀI KHOẢN EXIMBANK =====
  const zaloPhone = "0327620117";
  const zaloLink = "https://zalo.me/" + zaloPhone;
  const bankId = "970431"; // Eximbank BIN
  const bankName = "Eximbank";
  const bankAccountNo = "0327620117";
  const bankAccountName = "CAO THANH HAI";

  // ===== 22 SẢN PHẨM CHÍNH THỨC TỪ GOOGLE SHEETS =====
  const DEFAULT_PRODUCT_GROUPS = [
  {
    "id": "crl-netflix",
    "name": "Netflix Premium",
    "brand": "Netflix",
    "category": "Giải trí Premium",
    "image": "netflix.com",
    "glow": "linear-gradient(135deg,#E50914,#ff3b30,#450a0a)",
    "description": "Dịch vụ xem phim Netflix chất lượng cao Ultra HD 4K, hỗ trợ gói xem riêng chính chủ và các gói tiết kiệm.",
    "priceLabel": "Từ 35.000 đ",
    "durationSummary": "1 tháng",
    "planCount": 4,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-netflix-1",
        "variant": "NEXFLIX HÀNG FARM (standard)",
        "duration": "1 tháng",
        "accountType": "1 thiết bị",
        "sharedPrivate": "CHUNG",
        "warranty": "Bảo Hành Full",
        "price": "35.000 đ",
        "priceAmount": 35000,
        "originalPrice": "",
        "originalPriceAmount": 35000,
        "isOutOfStock": false,
        "note": "( XÀI ĐÔI KHI BỊ OUT )"
      },
      {
        "id": "pln-crl-netflix-2",
        "variant": "NETFLIX HÀNG FARM (premium)",
        "duration": "1 tháng",
        "accountType": "3-4 thiết bị",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "60.000 đ",
        "priceAmount": 60000,
        "originalPrice": "",
        "originalPriceAmount": 60000,
        "isOutOfStock": false,
        "note": "( XÀI ĐÔI KHI BỊ OUT )"
      },
      {
        "id": "pln-crl-netflix-3",
        "variant": "NETFLIX GIÁ RẺ",
        "duration": "1 tháng",
        "accountType": "3-4 thiết bị",
        "sharedPrivate": "CHUNG",
        "warranty": "Bảo Hành Full",
        "price": "35.000 đ",
        "priceAmount": 35000,
        "originalPrice": "",
        "originalPriceAmount": 35000,
        "isOutOfStock": false,
        "note": "dùng cho máy tính và TV, ios ( XÀI ĐÔI KHI BỊ OUT )"
      },
      {
        "id": "pln-crl-netflix-4",
        "variant": "NETFLIX CHÍNH CHỦ DÙNG RIÊNG 4K FULL HD",
        "duration": "1 tháng",
        "accountType": "1 thiết bị",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "90.000 đ",
        "priceAmount": 90000,
        "originalPrice": "88.000 đ",
        "originalPriceAmount": 88000,
        "isOutOfStock": false,
        "note": ""
      }
    ]
  },
  {
    "id": "crl-chatgpt",
    "name": "ChatGPT Plus",
    "brand": "OpenAI",
    "category": "Công nghệ & AI",
    "image": "openai.com",
    "glow": "linear-gradient(135deg,#10a37f,#14b8a6,#064e3b)",
    "description": "Nâng cấp ChatGPT Plus, GPT Edu, GPT Business chính chủ hỗ trợ GPT-4o, o1, Canvas, tạo ảnh DALL-E không giới hạn.",
    "priceLabel": "Từ 200.000 đ",
    "durationSummary": "2 năm / 1 tháng / 6 tháng / 3 tháng",
    "planCount": 6,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-chatgpt-1",
        "variant": "GPT EDU",
        "duration": "2 năm",
        "accountType": "ACC CẤP",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành 12 Tháng",
        "price": "800.000 đ",
        "priceAmount": 800000,
        "originalPrice": "",
        "originalPriceAmount": 800000,
        "isOutOfStock": false,
        "note": "loại này model ngang ngửa plus nha"
      },
      {
        "id": "pln-crl-chatgpt-2",
        "variant": "GPT PLUS",
        "duration": "1 tháng",
        "accountType": "NÂNG TỪ EMAIL BẠN",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành 1 Tháng",
        "price": "300.000 đ",
        "priceAmount": 300000,
        "originalPrice": "",
        "originalPriceAmount": 300000,
        "isOutOfStock": false,
        "note": ""
      },
      {
        "id": "pln-crl-chatgpt-3",
        "variant": "GPT PLUS cấp acc",
        "duration": "1 tháng",
        "accountType": "ACC CẤP",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành 24h",
        "price": "200.000 đ",
        "priceAmount": 200000,
        "originalPrice": "",
        "originalPriceAmount": 200000,
        "isOutOfStock": false,
        "note": ""
      },
      {
        "id": "pln-crl-chatgpt-4",
        "variant": "GPT PLUS",
        "duration": "6 tháng",
        "accountType": "NÂNG TỪ EMAIL BẠN",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "Hết hàng",
        "priceAmount": 0,
        "originalPrice": "",
        "originalPriceAmount": 0,
        "isOutOfStock": true,
        "note": "ACC RENEW HẰNG THÁNG"
      },
      {
        "id": "pln-crl-chatgpt-5",
        "variant": "GPT PLUS",
        "duration": "3 tháng",
        "accountType": "NÂNG TỪ EMAIL BẠN",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "Hết hàng",
        "priceAmount": 0,
        "originalPrice": "",
        "originalPriceAmount": 0,
        "isOutOfStock": true,
        "note": "ACC RENEW HẰNG THÁNG"
      },
      {
        "id": "pln-crl-chatgpt-6",
        "variant": "GPT BUSSINESS",
        "duration": "1 tháng",
        "accountType": "NÂNG TỪ EMAIL BẠN",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "Hết hàng",
        "priceAmount": 0,
        "originalPrice": "",
        "originalPriceAmount": 0,
        "isOutOfStock": true,
        "note": "GÓI NÀY RẤT ỔN ĐỊNH VÀ KHÔNG LO BAY ACC NẾU KHÁCH HÀNG KHÔNG CHAT VI PHẠM CHÍNH SÁCH ,"
      }
    ]
  },
  {
    "id": "crl-youtube",
    "name": "YouTube Premium",
    "brand": "YouTube",
    "category": "Giải trí Premium",
    "image": "youtube.com",
    "glow": "linear-gradient(135deg,#FF0000,#ff4b4b,#7f1d1d)",
    "description": "Xem YouTube không quảng cáo, phát trong nền khi tắt màn hình, tải video ngoại tuyến và đi kèm YouTube Music Premium.",
    "priceLabel": "Từ 30.000 đ",
    "durationSummary": "1 tháng / 6 tháng / 12 tháng",
    "planCount": 3,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-youtube-1",
        "variant": "YT PRENIUM ( FAMILY )",
        "duration": "1 tháng",
        "accountType": "NÂNG TỪ EMAIL BẠN",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "30.000 đ",
        "priceAmount": 30000,
        "originalPrice": "28.000 đ",
        "originalPriceAmount": 28000,
        "isOutOfStock": false,
        "note": "loại này sẽ đổi fam hằng tháng mình sẽ hỗ trợ đổi và gỡ lỗi 12 tháng cho các bạn"
      },
      {
        "id": "pln-crl-youtube-2",
        "variant": "YT PRENIUM ( FAMILY )",
        "duration": "6 tháng",
        "accountType": "NÂNG TỪ EMAIL BẠN",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "160.000 đ",
        "priceAmount": 160000,
        "originalPrice": "",
        "originalPriceAmount": 160000,
        "isOutOfStock": false,
        "note": "loại này sẽ đổi fam hằng tháng mình sẽ hỗ trợ đổi và gỡ lỗi 12 tháng cho các bạn"
      },
      {
        "id": "pln-crl-youtube-3",
        "variant": "YT PRENIUM ( FAMILY )",
        "duration": "12 tháng",
        "accountType": "NÂNG TỪ EMAIL BẠN",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "320.000 đ",
        "priceAmount": 320000,
        "originalPrice": "",
        "originalPriceAmount": 320000,
        "isOutOfStock": false,
        "note": "loại này sẽ đổi fam hằng tháng mình sẽ hỗ trợ đổi và gỡ lỗi 12 tháng cho các bạn"
      }
    ]
  },
  {
    "id": "crl-locket",
    "name": "Locket Gold",
    "brand": "Locket",
    "category": "Tiện ích & Khác",
    "image": "locket.camera",
    "glow": "linear-gradient(135deg,#f59e0b,#eab308,#78350f)",
    "description": "Nâng cấp Locket Gold chính chủ vĩnh viễn cho iOS. Đăng ảnh video dài, cam kết không dính iCloud, gửi username là hoàn thành.",
    "priceLabel": "Từ 125.000 đ",
    "durationSummary": "VĨNH VIỄN",
    "planCount": 1,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-locket-1",
        "variant": "LOCKET GOLD",
        "duration": "VĨNH VIỄN",
        "accountType": "1 thiết bị",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành 3 Năm",
        "price": "125.000 đ",
        "priceAmount": 125000,
        "originalPrice": "",
        "originalPriceAmount": 125000,
        "isOutOfStock": false,
        "note": "CAM KẾT KHÔNG DÍNH ICL, GỬI USER LÀ DONE"
      }
    ]
  },
  {
    "id": "crl-spotify",
    "name": "Spotify Premium",
    "brand": "Spotify",
    "category": "Giải trí Premium",
    "image": "spotify.com",
    "glow": "linear-gradient(135deg,#1DB954,#22c55e,#064e3b)",
    "description": "Tài khoản nghe nhạc Spotify Premium nâng cấp chính chủ từ email. Nghe nhạc chất lượng cao lossless, chuyển bài không giới hạn.",
    "priceLabel": "Từ 280.000 đ",
    "durationSummary": "12 tháng / 6 tháng",
    "planCount": 2,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-spotify-1",
        "variant": "SPOTIFY",
        "duration": "12 tháng",
        "accountType": "NÂNG CHÍNH CHỦ",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "380.000 đ",
        "priceAmount": 380000,
        "originalPrice": "",
        "originalPriceAmount": 380000,
        "isOutOfStock": false,
        "note": ""
      },
      {
        "id": "pln-crl-spotify-2",
        "variant": "SPOTIFY",
        "duration": "6 tháng",
        "accountType": "NÂNG CHÍNH CHỦ",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "280.000 đ",
        "priceAmount": 280000,
        "originalPrice": "",
        "originalPriceAmount": 280000,
        "isOutOfStock": false,
        "note": ""
      }
    ]
  },
  {
    "id": "crl-capcut",
    "name": "CapCut Pro",
    "brand": "CapCut",
    "category": "Thiết kế & Đồ họa",
    "image": "capcut.com",
    "glow": "linear-gradient(135deg,#000000,#2563eb,#1e1b4b)",
    "description": "Tài khoản CapCut Pro chuyên nghiệp dùng trên 2 thiết bị. Mở khóa toàn bộ hiệu ứng VIP và xuất video 4K sắc nét.",
    "priceLabel": "Từ 10.000 đ",
    "durationSummary": "7 ngày / 1 tháng / 6 tháng",
    "planCount": 7,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-capcut-1",
        "variant": "Tài khoản CapCut",
        "duration": "7 ngày",
        "accountType": "2 thiết bị",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "10.000 đ",
        "priceAmount": 10000,
        "originalPrice": "",
        "originalPriceAmount": 10000,
        "isOutOfStock": false,
        "note": "bán rất chạy"
      },
      {
        "id": "pln-crl-capcut-2",
        "variant": "Tài khoản CapCut",
        "duration": "1 tháng",
        "accountType": "2 thiết bị",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "60.000 đ",
        "priceAmount": 60000,
        "originalPrice": "59.000 đ",
        "originalPriceAmount": 59000,
        "isOutOfStock": false,
        "note": ""
      },
      {
        "id": "pln-crl-capcut-3",
        "variant": "Tài khoản Capcut (3 tháng)",
        "duration": "hết hàng",
        "accountType": "2 thiết bị",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "200.000 đ",
        "priceAmount": 200000,
        "originalPrice": "",
        "originalPriceAmount": 200000,
        "isOutOfStock": false,
        "note": ""
      },
      {
        "id": "pln-crl-capcut-4",
        "variant": "Tài khoản CapCut (6 tháng)",
        "duration": "hết hàng",
        "accountType": "2 thiết bị",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "400.000 đ",
        "priceAmount": 400000,
        "originalPrice": "",
        "originalPriceAmount": 400000,
        "isOutOfStock": false,
        "note": "hàng này ad cấp theo tháng nên khi đổi acc sẽ không bị mất các dự án"
      },
      {
        "id": "pln-crl-capcut-5",
        "variant": "Tài khoản CapCut (1 năm)",
        "duration": "hết hàng",
        "accountType": "2 thiết bị",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "680.000 đ",
        "priceAmount": 680000,
        "originalPrice": "",
        "originalPriceAmount": 680000,
        "isOutOfStock": false,
        "note": "cấp lẻ theo tháng"
      },
      {
        "id": "pln-crl-capcut-6",
        "variant": "Tài khoản CapCut (1 năm)",
        "duration": "hết hàng",
        "accountType": "2 thiết bị",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "600.000 đ",
        "priceAmount": 600000,
        "originalPrice": "",
        "originalPriceAmount": 600000,
        "isOutOfStock": false,
        "note": "full acc 12 tháng không cấp lẻ từng tháng"
      },
      {
        "id": "pln-crl-capcut-7",
        "variant": "Tài khoản CapCut ( 6 tháng )",
        "duration": "6 tháng",
        "accountType": "2 thiết bị",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "380.000 đ",
        "priceAmount": 380000,
        "originalPrice": "",
        "originalPriceAmount": 380000,
        "isOutOfStock": false,
        "note": "full acc 6 tháng không cấp lẻ từng tháng"
      }
    ]
  },
  {
    "id": "crl-canva",
    "name": "Canva Pro",
    "brand": "Canva",
    "category": "Thiết kế & Đồ họa",
    "image": "canva.com",
    "glow": "linear-gradient(135deg,#00c4cc,#7d2ae8,#4c1d95)",
    "description": "Nâng cấp Canva Pro & Edu chính chủ từ email cá nhân. Mở khóa kho mẫu thiết kế cao cấp và công cụ Magic Studio.",
    "priceLabel": "Từ 10.000 đ",
    "durationSummary": "1 năm / 3 năm / 12 tháng / 6 tháng / 1 tháng",
    "planCount": 5,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-canva-1",
        "variant": "Canva Edu",
        "duration": "1 năm",
        "accountType": "NÂNG TỪ EMAIL BẠN",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "50.000 đ",
        "priceAmount": 50000,
        "originalPrice": "",
        "originalPriceAmount": 50000,
        "isOutOfStock": false,
        "note": "tính năng tương tự pro thiếu 1 số cái thôi"
      },
      {
        "id": "pln-crl-canva-2",
        "variant": "Canva Edu",
        "duration": "3 năm",
        "accountType": "NÂNG TỪ EMAIL BẠN",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "75.000 đ",
        "priceAmount": 75000,
        "originalPrice": "",
        "originalPriceAmount": 75000,
        "isOutOfStock": false,
        "note": "tính năng tương tự pro thiếu 1 số cái thôi"
      },
      {
        "id": "pln-crl-canva-3",
        "variant": "Canva Pro",
        "duration": "12 tháng",
        "accountType": "NÂNG TỪ EMAIL BẠN",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "100.000 đ",
        "priceAmount": 100000,
        "originalPrice": "",
        "originalPriceAmount": 100000,
        "isOutOfStock": false,
        "note": "không phải edu"
      },
      {
        "id": "pln-crl-canva-4",
        "variant": "Canva Pro",
        "duration": "6 tháng",
        "accountType": "NÂNG TỪ EMAIL BẠN",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "50.000 đ",
        "priceAmount": 50000,
        "originalPrice": "",
        "originalPriceAmount": 50000,
        "isOutOfStock": false,
        "note": "không phải edu"
      },
      {
        "id": "pln-crl-canva-5",
        "variant": "Canva Pro",
        "duration": "1 tháng",
        "accountType": "NÂNG TỪ EMAIL BẠN",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "10.000 đ",
        "priceAmount": 10000,
        "originalPrice": "",
        "originalPriceAmount": 10000,
        "isOutOfStock": false,
        "note": "không phải edu"
      }
    ]
  },
  {
    "id": "crl-gemini",
    "name": "Google Gemini & Drive",
    "brand": "Google",
    "category": "Công nghệ & AI",
    "image": "google.com",
    "glow": "linear-gradient(135deg,#4285F4,#34A853,#1e3a8a)",
    "description": "Gói Google One mở rộng 5TB dung lượng lưu trữ Drive kèm quyền truy cập Gemini Pro / Ultra và NotebookLM không giới hạn.",
    "priceLabel": "Từ 35.000 đ",
    "durationSummary": "1 năm / 12 tháng",
    "planCount": 5,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-gemini-1",
        "variant": "GG GEMINI ULTRA x20 TẠO VIDEO  0 CREDIT",
        "duration": "1 năm",
        "accountType": "2-3 thiết bị",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "2.500.000 đ",
        "priceAmount": 2500000,
        "originalPrice": "",
        "originalPriceAmount": 2500000,
        "isOutOfStock": false,
        "note": ""
      },
      {
        "id": "pln-crl-gemini-2",
        "variant": "GG GEMINI ULTRA x5 TẠO VIDEO  0 credit",
        "duration": "12 tháng",
        "accountType": "2-3 thiết bị",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành full",
        "price": "900.000 đ",
        "priceAmount": 900000,
        "originalPrice": "",
        "originalPriceAmount": 900000,
        "isOutOfStock": false,
        "note": ""
      },
      {
        "id": "pln-crl-gemini-3",
        "variant": "GEMINI PRO + 5TB DRIVER + notebook lm + call meet không giới hạn",
        "duration": "12 tháng",
        "accountType": "NÂNG CẤP TỪ ACC  BẠN LOG BAO MÁY CŨNG OK",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "550.000 đ",
        "priceAmount": 550000,
        "originalPrice": "",
        "originalPriceAmount": 550000,
        "isOutOfStock": false,
        "note": "CHỦ FAM NÂNG CHÍNH CHỦ"
      },
      {
        "id": "pln-crl-gemini-4",
        "variant": "GEMINI PRO + 5TB DRIVER + notebook lm + call meet không giới hạn",
        "duration": "12 tháng",
        "accountType": "NÂNG CẤP TỪ ACC  BẠN LOG BAO MÁY CŨNG OK",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành 1 Ngày",
        "price": "35.000 đ",
        "priceAmount": 35000,
        "originalPrice": "",
        "originalPriceAmount": 35000,
        "isOutOfStock": false,
        "note": "CHỦ FAM NÂNG CHÍNH CHỦ"
      },
      {
        "id": "pln-crl-gemini-5",
        "variant": "GEMINI PRO + 5TB DRIVER + notebook lm + call meet không giới hạn",
        "duration": "1 năm",
        "accountType": "NÂNG CẤP TỪ ACC  BẠN LOG BAO MÁY CŨNG OK",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "160.000 đ",
        "priceAmount": 160000,
        "originalPrice": "",
        "originalPriceAmount": 160000,
        "isOutOfStock": false,
        "note": "ADD FAMILY"
      }
    ]
  },
  {
    "id": "crl-claude",
    "name": "Claude AI Pro",
    "brand": "Claude",
    "category": "Công nghệ & AI",
    "image": "claude.ai",
    "glow": "linear-gradient(135deg,#cc785c,#ea580c,#7c2d12)",
    "description": "Mô hình Claude 3.5 Sonnet và Claude 3.7 đỉnh cao về lập trình, tư duy logic, phân tích dữ liệu lớn ngữ cảnh 200K token.",
    "priceLabel": "Từ 380.000 đ",
    "durationSummary": "1 tháng",
    "planCount": 1,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-claude-1",
        "variant": "CLAUDE PRO",
        "duration": "1 tháng",
        "accountType": "NÂNG CẤP TỪ ACC",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "380.000 đ",
        "priceAmount": 380000,
        "originalPrice": "",
        "originalPriceAmount": 380000,
        "isOutOfStock": false,
        "note": ""
      }
    ]
  },
  {
    "id": "crl-grok",
    "name": "Grok AI Super",
    "brand": "Grok",
    "category": "Công nghệ & AI",
    "image": "x.ai",
    "glow": "linear-gradient(135deg,#000000,#52525b,#18181b)",
    "description": "Trí tuệ nhân tạo Grok của Elon Musk, truy cập thời gian thực mạng xã hội X, tư duy sắc bén và phân tích trực tiếp.",
    "priceLabel": "Từ 70.000 đ",
    "durationSummary": "7  ngày",
    "planCount": 3,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-grok-1",
        "variant": "GROK SUPER DÙNG RIÊNG 12 THÁNG",
        "duration": "hết hàng",
        "accountType": "2-3 thiết bị",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "690.000 đ",
        "priceAmount": 690000,
        "originalPrice": "",
        "originalPriceAmount": 690000,
        "isOutOfStock": false,
        "note": ""
      },
      {
        "id": "pln-crl-grok-2",
        "variant": "GROK SUPER DÙNG RIÊNG 6 THÁNG",
        "duration": "hết hàng",
        "accountType": "2-3 thiết bị",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "450.000 đ",
        "priceAmount": 450000,
        "originalPrice": "",
        "originalPriceAmount": 450000,
        "isOutOfStock": false,
        "note": ""
      },
      {
        "id": "pln-crl-grok-3",
        "variant": "GROK SUPER DÙNG RIÊNG 1 THÁNG",
        "duration": "7  ngày",
        "accountType": "ACC CẤP",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "70.000 đ",
        "priceAmount": 70000,
        "originalPrice": "",
        "originalPriceAmount": 70000,
        "isOutOfStock": false,
        "note": ""
      }
    ]
  },
  {
    "id": "crl-leonardo",
    "name": "Leonardo.ai",
    "brand": "Leonardo",
    "category": "Công nghệ & AI",
    "image": "leonardo.ai",
    "glow": "linear-gradient(135deg,#a855f7,#ec4899,#581c87)",
    "description": "Nền tảng tạo hình ảnh AI nghệ thuật chuyên sâu, hỗ trợ tạo ảnh độ phân giải cao cho designer và sáng tạo nội dung.",
    "priceLabel": "Từ 250.000 đ",
    "durationSummary": "1 tháng",
    "planCount": 2,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-leonardo-1",
        "variant": "LEONARDO (Artisan Ultimate)",
        "duration": "1 tháng",
        "accountType": "1 thiết bị",
        "sharedPrivate": "CHUNG",
        "warranty": "Bảo Hành Full",
        "price": "250.000 đ",
        "priceAmount": 250000,
        "originalPrice": "",
        "originalPriceAmount": 250000,
        "isOutOfStock": false,
        "note": ""
      },
      {
        "id": "pln-crl-leonardo-2",
        "variant": "LEONARDO (Gói Meatro)",
        "duration": "1 tháng",
        "accountType": "1 thiết bị",
        "sharedPrivate": "CHUNG",
        "warranty": "Bảo Hành Full",
        "price": "300.000 đ",
        "priceAmount": 300000,
        "originalPrice": "",
        "originalPriceAmount": 300000,
        "isOutOfStock": false,
        "note": ""
      }
    ]
  },
  {
    "id": "crl-kling",
    "name": "Kling AI",
    "brand": "Kling",
    "category": "Công nghệ & AI",
    "image": "klingai.com",
    "glow": "linear-gradient(135deg,#6366f1,#8b5cf6,#312e81)",
    "description": "Công cụ tạo video AI chân thực hàng đầu thế giới từ văn bản và hình ảnh, chuyển động mượt mà và vật lý chân thực.",
    "priceLabel": "Từ 160.000 đ",
    "durationSummary": "1 tháng",
    "planCount": 1,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-kling-1",
        "variant": "KLING AI 1100 CREDIT (STANDARD)",
        "duration": "1 tháng",
        "accountType": "ACC CẤP",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "160.000 đ",
        "priceAmount": 160000,
        "originalPrice": "",
        "originalPriceAmount": 160000,
        "isOutOfStock": false,
        "note": ""
      }
    ]
  },
  {
    "id": "crl-perplexity",
    "name": "Perplexity AI Pro",
    "brand": "Perplexity",
    "category": "Công nghệ & AI",
    "image": "perplexity.ai",
    "glow": "linear-gradient(135deg,#20b2aa,#008080,#042f2e)",
    "description": "Công cụ tìm kiếm thông minh và nghiên cứu học thuật bằng AI thế hệ mới, trích dẫn nguồn tài liệu chính xác tuyệt đối.",
    "priceLabel": "Hết hàng",
    "durationSummary": "1 tháng / 12 tháng",
    "planCount": 2,
    "inStock": false,
    "plans": [
      {
        "id": "pln-crl-perplexity-1",
        "variant": "PEPRPLEXITY",
        "duration": "1 tháng",
        "accountType": "cấp acc hoặc nâng từ email",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "Hết hàng",
        "priceAmount": 0,
        "originalPrice": "",
        "originalPriceAmount": 0,
        "isOutOfStock": true,
        "note": "GÓI NÀY HẰNG THÁNG SẼ MẤT DỮ LIỆU CỦA THÁNG TRƯỚC"
      },
      {
        "id": "pln-crl-perplexity-2",
        "variant": "PEPRPLEXITY",
        "duration": "12 tháng",
        "accountType": "cấp acc hoặc nâng từ email",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "Hết hàng",
        "priceAmount": 0,
        "originalPrice": "",
        "originalPriceAmount": 0,
        "isOutOfStock": true,
        "note": "khách không được tự ý thêm người khác vào workspace nếu không sẽ hủy không hoàn tiền"
      }
    ]
  },
  {
    "id": "crl-adobe",
    "name": "Adobe Creative Cloud",
    "brand": "Adobe",
    "category": "Thiết kế & Đồ họa",
    "image": "adobe.com",
    "glow": "linear-gradient(135deg,#fa0f00,#ff6b6b,#881337)",
    "description": "Bộ công cụ sáng tạo gồm Photoshop, Illustrator, Premiere Pro, After Effects và hơn 20 ứng dụng chuyên nghiệp của Adobe.",
    "priceLabel": "Từ 200.000 đ",
    "durationSummary": "2 tháng",
    "planCount": 1,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-adobe-1",
        "variant": "ADOBE",
        "duration": "2 tháng",
        "accountType": "ACC CẤP",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "200.000 đ",
        "priceAmount": 200000,
        "originalPrice": "",
        "originalPriceAmount": 200000,
        "isOutOfStock": false,
        "note": ""
      }
    ]
  },
  {
    "id": "crl-office",
    "name": "Microsoft 365 Full Bộ Office",
    "brand": "Microsoft",
    "category": "Tiện ích & Khác",
    "image": "microsoft.com",
    "glow": "linear-gradient(135deg,#0078d4,#0284c7,#0c4a6e)",
    "description": "Bản quyền Office 365 gồm Word, Excel, PowerPoint, Outlook cài trên 5 thiết bị kèm 1TB OneDrive tốc độ cao.",
    "priceLabel": "Từ 180.000 đ",
    "durationSummary": "1 năm",
    "planCount": 1,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-office-1",
        "variant": "MICROSOFT FULL BỘ OFFICE 1TB",
        "duration": "1 năm",
        "accountType": "NÂNG TỪ EMAIL BẠN",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "180.000 đ",
        "priceAmount": 180000,
        "originalPrice": "",
        "originalPriceAmount": 180000,
        "isOutOfStock": false,
        "note": ""
      }
    ]
  },
  {
    "id": "crl-duolingo",
    "name": "Duolingo Super",
    "brand": "Duolingo",
    "category": "Học tập & Ngoại ngữ",
    "image": "duolingo.com",
    "glow": "linear-gradient(135deg,#58cc02,#22c55e,#14532d)",
    "description": "Học ngoại ngữ không giới hạn trái tim với Duolingo Super, làm bài luyện cá nhân hóa, xóa bỏ hoàn toàn quảng cáo.",
    "priceLabel": "Từ 250.000 đ",
    "durationSummary": "12 tháng",
    "planCount": 1,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-duolingo-1",
        "variant": "DOULINGO SUPER",
        "duration": "12 tháng",
        "accountType": "NÂNG CHÍNH CHỦ",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "250.000 đ",
        "priceAmount": 250000,
        "originalPrice": "",
        "originalPriceAmount": 250000,
        "isOutOfStock": false,
        "note": ""
      }
    ]
  },
  {
    "id": "crl-quizlet",
    "name": "Quizlet Plus",
    "brand": "Quizlet",
    "category": "Học tập & Ngoại ngữ",
    "image": "quizlet.com",
    "glow": "linear-gradient(135deg,#4257b2,#6366f1,#1e1b4b)",
    "description": "Học tập và ghi nhớ flashcard thông minh với chế độ Học AI, làm bài kiểm tra thử không giới hạn và học ngoại tuyến.",
    "priceLabel": "Từ 30.000 đ",
    "durationSummary": "1 tháng / 12 tháng",
    "planCount": 2,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-quizlet-1",
        "variant": "QUIZLET",
        "duration": "1 tháng",
        "accountType": "ACC CẤP",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "30.000 đ",
        "priceAmount": 30000,
        "originalPrice": "28.000 đ",
        "originalPriceAmount": 28000,
        "isOutOfStock": false,
        "note": ""
      },
      {
        "id": "pln-crl-quizlet-2",
        "variant": "QUIZLET",
        "duration": "12 tháng",
        "accountType": "ACC CẤP",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "180.000 đ",
        "priceAmount": 180000,
        "originalPrice": "",
        "originalPriceAmount": 180000,
        "isOutOfStock": false,
        "note": ""
      }
    ]
  },
  {
    "id": "crl-grammarly",
    "name": "Grammarly Premium AI",
    "brand": "Grammarly",
    "category": "Học tập & Ngoại ngữ",
    "image": "grammarly.com",
    "glow": "linear-gradient(135deg,#15c39a,#10b981,#064e3b)",
    "description": "Trợ lý viết tiếng Anh chuyên nghiệp, sửa lỗi ngữ pháp, cải thiện câu từ và gợi ý từ vựng chuẩn xác cho công việc.",
    "priceLabel": "Từ 150.000 đ",
    "durationSummary": "1 tháng",
    "planCount": 1,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-grammarly-1",
        "variant": "GRAMMALY",
        "duration": "1 tháng",
        "accountType": "NÂNG CHÍNH CHỦ",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "150.000 đ",
        "priceAmount": 150000,
        "originalPrice": "",
        "originalPriceAmount": 150000,
        "isOutOfStock": false,
        "note": ""
      }
    ]
  },
  {
    "id": "crl-meitu",
    "name": "Meitu SVIP",
    "brand": "Meitu",
    "category": "Thiết kế & Đồ họa",
    "image": "meitu.com",
    "glow": "linear-gradient(135deg,#f43f5e,#ec4899,#881337)",
    "description": "Ứng dụng chỉnh sửa ảnh chân dung đỉnh cao với tính năng trang điểm AI, xóa khuyết điểm, phục chế ảnh cũ và bộ lọc SVIP.",
    "priceLabel": "Từ 140.000 đ",
    "durationSummary": "1 tháng",
    "planCount": 1,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-meitu-1",
        "variant": "MEITU SVIP",
        "duration": "1 tháng",
        "accountType": "ACC CẤP",
        "sharedPrivate": "RIÊNG ( 3 máy )",
        "warranty": "Bảo Hành Full",
        "price": "140.000 đ",
        "priceAmount": 140000,
        "originalPrice": "138.000 đ",
        "originalPriceAmount": 138000,
        "isOutOfStock": false,
        "note": ""
      }
    ]
  },
  {
    "id": "crl-picsart",
    "name": "Picsart Pro",
    "brand": "Picsart",
    "category": "Thiết kế & Đồ họa",
    "image": "picsart.com",
    "glow": "linear-gradient(135deg,#ec4899,#f43f5e,#831843)",
    "description": "Bộ công cụ sáng tạo hình ảnh toàn năng trên điện thoại và máy tính, mở khóa kho sticker, phông chữ và bộ lọc độc quyền.",
    "priceLabel": "Từ 240.000 đ",
    "durationSummary": "12 tháng",
    "planCount": 1,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-picsart-1",
        "variant": "PISCART PRO",
        "duration": "12 tháng",
        "accountType": "NÂNG CẤP TỪ ACC",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành 3 Tháng",
        "price": "240.000 đ",
        "priceAmount": 240000,
        "originalPrice": "",
        "originalPriceAmount": 240000,
        "isOutOfStock": false,
        "note": ""
      }
    ]
  },
  {
    "id": "crl-vieon",
    "name": "VieON VIP & VIP Pro",
    "brand": "VieON",
    "category": "Giải trí Premium",
    "image": "vieon.vn",
    "glow": "linear-gradient(135deg,#22c55e,#16a34a,#14532d)",
    "description": "Xem trực tiếp phim truyền hình, show giải trí đặc sắc, kênh truyền hình trong nước & quốc tế, gói VIP Pro kèm kho phim Galaxy Play.",
    "priceLabel": "Từ 35.000 đ",
    "durationSummary": "1 tháng / 12 tháng",
    "planCount": 2,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-vieon-1",
        "variant": "VIEON VIP",
        "duration": "1 tháng",
        "accountType": "NÂNG CẤP TỪ ACC",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "35.000 đ",
        "priceAmount": 35000,
        "originalPrice": "",
        "originalPriceAmount": 35000,
        "isOutOfStock": false,
        "note": ""
      },
      {
        "id": "pln-crl-vieon-2",
        "variant": "VIEON VIP Pro",
        "duration": "12 tháng",
        "accountType": "NÂNG CẤP TỪ ACC",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "680.000 đ",
        "priceAmount": 680000,
        "originalPrice": "",
        "originalPriceAmount": 680000,
        "isOutOfStock": false,
        "note": "12 tháng (xem được galaxay play)"
      }
    ]
  },
  {
    "id": "crl-hma",
    "name": "HMA VPN (HideMyAss)",
    "brand": "HMA",
    "category": "Tiện ích & Khác",
    "image": "hidemyass.com",
    "glow": "linear-gradient(135deg,#f59e0b,#d97706,#78350f)",
    "description": "Dịch vụ VPN bảo mật danh tính trực tuyến hàng đầu với hơn 290 địa điểm máy chủ toàn cầu trên 5 thiết bị.",
    "priceLabel": "Từ 20.000 đ",
    "durationSummary": "1 tháng",
    "planCount": 2,
    "inStock": true,
    "plans": [
      {
        "id": "pln-crl-hma-1",
        "variant": "HMA IOS",
        "duration": "1 tháng",
        "accountType": "CẤP DÙNG 5 MÁY",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "30.000 đ",
        "priceAmount": 30000,
        "originalPrice": "28.000 đ",
        "originalPriceAmount": 28000,
        "isOutOfStock": false,
        "note": ""
      },
      {
        "id": "pln-crl-hma-2",
        "variant": "HMA ANDROID",
        "duration": "1 tháng",
        "accountType": "CẤP DÙNG 5 MÁY",
        "sharedPrivate": "RIÊNG",
        "warranty": "Bảo Hành Full",
        "price": "20.000 đ",
        "priceAmount": 20000,
        "originalPrice": "18.000 đ",
        "originalPriceAmount": 18000,
        "isOutOfStock": false,
        "note": ""
      }
    ]
  }
];

  let productGroupsData = DEFAULT_PRODUCT_GROUPS;
  let categories = ["all"];
  let selectedCategory = "all";
  let selectedStock = "all";
  let searchKeyword = "";
  let selectedGroup = null;
  let selectedPlan = null;
  let lastPaymentContent = "";
  let lastPaymentAmount = 0;
  let lastOrderCode = "";

  const $ = id => document.getElementById(id);
  const els = {};

  function safe(val){
    return String(val == null ? "" : val)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function removeVietnameseTones(str){
    str = String(str || "");
    str = str.replace(/[àáạảãâầấậẩẫăằắặẳẵ]/g, "a");
    str = str.replace(/[èéẹẻẽêềếệểễ]/g, "e");
    str = str.replace(/[ìíịỉĩ]/g, "i");
    str = str.replace(/[òóọỏõôồốộổỗơờớợởỡ]/g, "o");
    str = str.replace(/[ùúụủũưừứựửữ]/g, "u");
    str = str.replace(/[ỳýỵỷỹ]/g, "y");
    str = str.replace(/đ/g, "d");
    str = str.replace(/[ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴ]/g, "A");
    str = str.replace(/[ÈÉẸẺẼÊỀẾỆỂỄ]/g, "E");
    str = str.replace(/[ÌÍỊỈĨ]/g, "I");
    str = str.replace(/[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]/g, "O");
    str = str.replace(/[ÙÚỤỦŨƯỪỨỰỬỮ]/g, "U");
    str = str.replace(/[ỲÝỴỶỸ]/g, "Y");
    str = str.replace(/Đ/g, "D");
    return str;
  }

  function imgHtml(group){
    if(!group || !group.image) return `<span class="icon-fallback">${safe(initials(group?.name))}</span>`;
    const raw = String(group.image || "").trim();
    const isDirectImage = /^(https?:\/\/|data:image\/|assets\/|\.\/|\/)/i.test(raw) && /\.(png|jpe?g|webp|gif|svg)(\?.*)?$/i.test(raw);
    const domain = raw.replace(/^https?:\/\//i, "").replace(/\/.*$/, "");
    const url = isDirectImage 
      ? raw 
      : `https://www.google.com/s2/favicons?domain=${domain}&sz=256`;
    return `<img src="${safe(url)}" onerror="this.outerHTML='<span class=\'icon-fallback\'>${safe(initials(group?.name))}</span>';" alt="${safe(group.name)}" loading="lazy" decoding="async">`;
  }

  function initials(name){
    const words = String(name || "").trim().split(/\s+/);
    if(!words.length || !words[0]) return "CL";
    if(words.length === 1) return words[0].slice(0, 2).toUpperCase();
    return (words[0][0] + words[1][0]).toUpperCase();
  }

  function isPlanOut(plan){
    return Boolean(plan && (plan.isOutOfStock || /hết hàng|out of stock/i.test(String(plan.price || ""))));
  }

  function extractAmount(priceStr){
    const s = String(priceStr || "").trim();
    if(isPlanOut({price: s})) return 0;
    const digits = s.replace(/[^0-9]/g, "");
    return digits ? parseInt(digits, 10) : 0;
  }

  function isGroupOut(group){
    if(!group.plans || !group.plans.length) return false;
    return group.plans.every(p => isPlanOut(p));
  }

  function planLabel(plan){
    if(isPlanOut(plan)) return "Hết hàng";
    const amt = extractAmount(plan.price);
    return amt ? amt.toLocaleString("vi-VN") + " đ" : (plan.price || "Liên hệ");
  }

  function recomputeCategories(){
    const set = new Set();
    productGroupsData.forEach(g => { if(g.category) set.add(g.category); });
    categories = ["all", ...Array.from(set)];
  }

  function shortCategory(cat){
    if(!cat || cat === "all") return "Tất cả danh mục";
    if(/ai|công nghệ/i.test(cat)) return "AI";
    if(/giải trí/i.test(cat)) return "Giải trí";
    if(/thiết kế|đồ họa/i.test(cat)) return "Thiết kế";
    if(/học tập|khóa học/i.test(cat)) return "Học tập";
    return cat;
  }

  function renderStats(){
    if(els.totalProducts) els.totalProducts.textContent = productGroupsData.length;
    const totalPlans = productGroupsData.reduce((acc, g) => acc + (g.plans ? g.plans.length : 0), 0);
    if(els.totalPlans) els.totalPlans.textContent = totalPlans;
  }

  function renderFilters(){
    if(els.chips){
      els.chips.innerHTML = categories.map(cat => {
        const label = shortCategory(cat);
        const active = cat === selectedCategory ? " active" : "";
        return `<button class="chip${active}" data-cat="${safe(cat)}" type="button">${safe(label)}</button>`;
      }).join("");
    }
    if(els.categoryFilter){
      els.categoryFilter.innerHTML = categories.map(cat => {
        const label = cat === "all" ? "Tất cả danh mục" : cat;
        const selected = cat === selectedCategory ? " selected" : "";
        return `<option value="${safe(cat)}"${selected}>${safe(label)}</option>`;
      }).join("");
    }
  }

  function renderFeatured(){
    if(!els.featuredGrid) return;
    const top6 = productGroupsData.slice(0, 6);
    els.featuredGrid.innerHTML = top6.map(g => `
      <div class="featured-card" data-group-id="${safe(g.id)}" style="--card-glow:${safe(g.glow)}">
        <div class="featured-icon">${imgHtml(g)}</div>
        <div class="featured-name">${safe(g.name)}</div>
      </div>
    `).join("");
  }

  function renderRail(items){
    if(!els.quickRail) return;
    // Remove any duplicate images/brands in the rail
    const seen = new Set();
    const uniqueRailItems = [];
    items.forEach(it => {
      const key = (it.image || it.brand || it.name).toLowerCase();
      if(!seen.has(key)){
        seen.add(key);
        uniqueRailItems.push(it);
      }
    });

    els.quickRail.innerHTML = uniqueRailItems.map(g => `
      <div class="rail-item" data-group-id="${safe(g.id)}" title="${safe(g.name)}" style="--glow:${safe(g.glow)}">
        ${imgHtml(g)}
      </div>
    `).join("");

    updateRailButtons();
  }

  function updateRailButtons(){
    if(!els.quickRail) return;
    const sl = els.quickRail.scrollLeft;
    const maxScroll = els.quickRail.scrollWidth - els.quickRail.clientWidth;
    if(els.railPrev){
      els.railPrev.style.display = sl > 12 ? "flex" : "none";
    }
    if(els.railNext){
      els.railNext.style.display = (maxScroll > 10 && sl < maxScroll - 12) ? "flex" : "none";
    }
  }

  function filteredGroups(){
    const kw = removeVietnameseTones(searchKeyword.toLowerCase().trim());
    return productGroupsData.filter(g => {
      if(selectedCategory !== "all" && g.category !== selectedCategory) return false;
      const isOut = isGroupOut(g);
      if(selectedStock === "available" && isOut) return false;
      if(selectedStock === "out" && !isOut) return false;
      if(kw){
        const hay = removeVietnameseTones([
          g.name, g.brand, g.category, g.description,
          ...(g.plans || []).map(p => [p.variant, p.duration, p.note, p.warranty].join(" "))
        ].join(" ").toLowerCase());
        if(!hay.includes(kw)) return false;
      }
      return true;
    });
  }

  function productCard(group){
    const isOut = isGroupOut(group);
    const priceClass = isOut ? " out" : (!extractAmount(group.priceLabel) ? " contact" : "");
    return `
      <article class="product-card" data-group-id="${safe(group.id)}" style="--photo-glow:${safe(group.glow)}">
        <div class="product-icon">${imgHtml(group)}</div>
        <div>
          <div class="product-name">${safe(group.name)}</div>
          <div class="product-meta">${safe(group.planCount)} gói · ${safe(group.brand || "Creamlan")}</div>
        </div>
        <div class="product-price${priceClass}">${safe(group.priceLabel || "Liên hệ")}</div>
      </article>
    `;
  }

  function renderProducts(){
    const items = filteredGroups();
    if(els.resultCount) els.resultCount.textContent = items.length;
    if(els.productGroups){
      els.productGroups.innerHTML = items.map(productCard).join("");
    }
    if(els.empty){
      els.empty.style.display = items.length ? "none" : "block";
    }
    renderRail(items);
  }

  // ===== MODAL & CHECKOUT LOGIC =====
  function openProductModal(groupId){
    const g = productGroupsData.find(x => x.id === groupId);
    if(!g) return;
    selectedGroup = g;
    selectedPlan = null;
    clearPaymentResult();

    if(els.modalLogo) els.modalLogo.innerHTML = imgHtml(g);
    if(els.modalProductImage) els.modalProductImage.innerHTML = imgHtml(g);
    if(els.modalTitle) els.modalTitle.textContent = g.name;
    if(els.modalSub) els.modalSub.textContent = [g.brand, g.category].filter(Boolean).join(" · ");
    if(els.modalDesc) els.modalDesc.textContent = g.description || "";
    if(els.modalPlanCount) els.modalPlanCount.textContent = (g.plans ? g.plans.length : 0) + " gói";

    if(els.modalPlans){
      els.modalPlans.innerHTML = (g.plans || []).map(planOption).join("");
    }

    // Preselect first in-stock plan
    const firstInStock = (g.plans || []).find(p => !isPlanOut(p));
    if(firstInStock){
      selectPlan(firstInStock.id);
    } else if(g.plans && g.plans[0]){
      selectPlan(g.plans[0].id);
    }

    if(els.productModal){
      els.productModal.classList.add("active");
      els.productModal.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
    }
  }

  function closeProductModal(){
    if(els.productModal){
      els.productModal.classList.remove("active");
      els.productModal.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    }
  }

  function planOption(plan){
    const out = isPlanOut(plan);
    const outClass = out ? " out-of-stock" : "";
    const badges = [
      plan.duration ? `⏱️ ${safe(plan.duration)}` : "",
      plan.warranty ? `🛡️ ${safe(plan.warranty)}` : "",
      plan.accountType ? safe(plan.accountType) : ""
    ].filter(Boolean).map(b => `<span class="plan-badge${b.includes('🛡️') ? ' warranty' : ''}">${b}</span>`).join("");

    return `
      <div class="plan-option${outClass}" data-plan-id="${safe(plan.id)}">
        <div class="plan-meta">
          <div class="plan-name">${safe(plan.variant || "Gói dịch vụ")}</div>
          ${plan.note ? `<div class="plan-sub">${safe(plan.note)}</div>` : ""}
          <div class="plan-badges">${badges}</div>
        </div>
        <div class="plan-price">${safe(planLabel(plan))}</div>
      </div>
    `;
  }

  function selectPlan(planId){
    if(!selectedGroup) return;
    const plan = (selectedGroup.plans || []).find(p => p.id === planId);
    if(!plan) return;
    selectedPlan = plan;

    if(els.modalPlans){
      els.modalPlans.querySelectorAll(".plan-option").forEach(el => {
        el.classList.toggle("selected", el.getAttribute("data-plan-id") === planId);
      });
    }

    if(els.selectedPlanBox){
      els.selectedPlanBox.innerHTML = `
        <b>Đã chọn:</b> ${safe(selectedGroup.name)}<br>
        <b>Gói:</b> ${safe(plan.variant || plan.duration || "Mặc định")}<br>
        <b>Thời hạn:</b> ${safe(plan.duration || "Liên hệ")} · <b>Giá:</b> ${safe(planLabel(plan))}
      `;
    }

    clearPaymentResult();
  }

  function showPaymentError(msg){
    if(els.paymentError){
      els.paymentError.textContent = msg;
      els.paymentError.style.display = "block";
    }
  }

  function clearPaymentResult(){
    if(els.paymentError) els.paymentError.style.display = "none";
    if(els.paymentResult) els.paymentResult.classList.remove("active");
    lastPaymentContent = "";
    lastPaymentAmount = 0;
    lastOrderCode = "";
  }

  function normalizeCustomerName(name){
    return String(name || "").trim().replace(/\s+/g, " ");
  }

  function normalizePhone(phone){
    return String(phone || "").replace(/[^0-9]/g, "");
  }

  function productCode(group, plan){
    const base = removeVietnameseTones((group.brand || group.name || "sp").toLowerCase()).replace(/[^a-z0-9]/g, "").slice(0, 16) || "sp";
    const duration = removeVietnameseTones([plan.duration, plan.variant].join(" ").toLowerCase());
    let d = "";
    const m = duration.match(/(\d+)\s*thang/); if(m) d = m[1] + "m";
    const y = duration.match(/(\d+)\s*nam/); if(y) d = y[1] + "y";
    return (base + (d ? " " + d : "")).slice(0, 24);
  }

  function pad2(n){ return String(n).padStart(2, "0"); }

  function createOrderCode(phone){
    const now = new Date();
    const date = String(now.getFullYear()).slice(2) + pad2(now.getMonth() + 1) + pad2(now.getDate());
    const time = pad2(now.getHours()) + pad2(now.getMinutes()) + pad2(now.getSeconds());
    const suffix = String(phone || "").slice(-4) || String(Math.floor(1000 + Math.random() * 9000));
    return `CRL-${date}-${time}-${suffix}`;
  }

  function createTransferContent(group, plan, name){
    const cleanName = removeVietnameseTones(normalizeCustomerName(name)).toUpperCase().replace(/[^A-Z0-9 ]/g, "").replace(/\s+/g, " ").trim();
    return (cleanName + " " + productCode(group, plan)).trim().slice(0, 60);
  }

  function createVietQrUrl(amount, content){
    const accountName = bankAccountName ? "&accountName=" + encodeURIComponent(bankAccountName) : "";
    return `https://img.vietqr.io/image/${bankId}-${bankAccountNo}-compact2.png?amount=${encodeURIComponent(amount)}&addInfo=${encodeURIComponent(content)}${accountName}`;
  }

  function getOrderText(confirmed = false){
    const name = normalizeCustomerName(els.customerName ? els.customerName.value : "");
    const phone = normalizePhone(els.customerPhone ? els.customerPhone.value : "");
    const lines = [];
    lines.push(confirmed ? "Xin chào Creamlan Store, tôi đã chuyển khoản đơn hàng. Shop kiểm tra và xử lý đơn giúp mình." : "Xin chào Creamlan Store, tôi muốn đặt đơn hàng này.");
    if(lastOrderCode) lines.push("Mã đơn hàng: " + lastOrderCode);
    if(selectedGroup) lines.push("Sản phẩm: " + selectedGroup.name);
    if(selectedPlan){
      lines.push("Gói: " + (selectedPlan.variant || selectedPlan.duration || ""));
      lines.push("Thời hạn: " + (selectedPlan.duration || "Liên hệ"));
      lines.push("Giá: " + planLabel(selectedPlan));
    }
    lines.push("Họ tên: " + (name || ""));
    lines.push("SĐT: " + (phone || ""));
    if(lastPaymentAmount) lines.push("Số tiền chuyển khoản: " + Number(lastPaymentAmount).toLocaleString("vi-VN") + " đ");
    if(lastPaymentContent) lines.push("Nội dung chuyển khoản: " + lastPaymentContent);
    lines.push("Tài khoản nhận: Eximbank " + bankAccountNo + " - " + bankAccountName);
    lines.push("Ghi chú: " + (confirmed ? "Khách đã bấm xác nhận đã chuyển khoản trên website. Shop vui lòng kiểm tra giao dịch theo mã đơn và nội dung chuyển khoản." : "Khách đang tạo đơn từ website Creamlan Store."));
    return lines.filter(Boolean).join("\n");
  }

  function createZaloOrderLink(hasPayment, confirmed = false){
    const text = getOrderText(confirmed && hasPayment);
    return zaloLink + "?text=" + encodeURIComponent(text);
  }

  function generatePaymentQr(){
    if(!selectedGroup || !selectedPlan) return showPaymentError("Bạn cần chọn một gói sản phẩm trước khi tạo QR.");
    const name = normalizeCustomerName(els.customerName.value);
    const phone = normalizePhone(els.customerPhone.value);
    if(!name){
      els.customerName.focus();
      return showPaymentError("Vui lòng nhập họ tên khách hàng.");
    }
    if(!phone || phone.length < 9 || phone.length > 11){
      els.customerPhone.focus();
      return showPaymentError("Vui lòng nhập số điện thoại hợp lệ, chỉ gồm 9-11 chữ số.");
    }
    const amount = extractAmount(selectedPlan.price);
    if(!amount){
      if(els.zaloGeneral) els.zaloGeneral.href = createZaloOrderLink(false);
      return showPaymentError("Gói này đang hết hàng/chưa có giá cố định. Hãy bấm “Gửi đơn Zalo” để shop tư vấn tình trạng mới nhất.");
    }

    const content = createTransferContent(selectedGroup, selectedPlan, name);
    lastPaymentContent = content;
    lastPaymentAmount = amount;
    lastOrderCode = createOrderCode(phone);

    if(els.qrImage) els.qrImage.src = createVietQrUrl(amount, content);
    if(els.paymentAmount) els.paymentAmount.textContent = Number(amount).toLocaleString("vi-VN") + " đ";
    if(els.paymentContent) els.paymentContent.textContent = content;
    if(els.paymentPhone) els.paymentPhone.textContent = phone;
    if(els.paymentOrderCode) els.paymentOrderCode.textContent = lastOrderCode;

    if(els.zaloGeneral) els.zaloGeneral.href = createZaloOrderLink(true);
    if(els.paymentResult) els.paymentResult.classList.add("active");
    if(els.paymentResult) els.paymentResult.scrollIntoView({behavior: "smooth", block: "center"});
    toast("Đã tạo QR thanh toán");
  }

  async function copyText(text, message){
    try {
      await navigator.clipboard.writeText(text);
      toast(message || "Đã copy");
    } catch(err){
      window.prompt("Copy nội dung này:", text);
    }
  }

  function copyPaymentContent(){
    if(!lastPaymentContent) return showPaymentError("Bạn cần tạo QR trước khi copy nội dung chuyển khoản.");
    copyText(lastPaymentContent, "Đã copy nội dung CK");
  }

  function copyOrder(){
    if(!selectedGroup) return;
    copyText(getOrderText(false), "Đã copy đơn hàng");
  }

  async function confirmPayment(){
    if(!lastPaymentContent || !lastPaymentAmount || !lastOrderCode){
      return showPaymentError("Bạn cần tạo QR thanh toán trước, sau đó mới bấm xác nhận đã chuyển khoản.");
    }
    const orderText = getOrderText(true);
    try {
      await navigator.clipboard.writeText(orderText);
      toast("Đã copy đơn hàng, đang mở Zalo");
    } catch(err){
      window.prompt("Copy đơn hàng này:", orderText);
    }
    if(els.confirmPaymentBtn) els.confirmPaymentBtn.textContent = "Đã copy đơn hàng ✓";
    if(els.paymentStatusBadge) els.paymentStatusBadge.innerHTML = '<span class="pulse-dot"></span> Đã bấm xác nhận chuyển khoản';
    if(els.paymentNote) els.paymentNote.textContent = "Đơn hàng đã được copy. Zalo sẽ mở kèm ghi chú: khách đã chuyển khoản, shop vui lòng kiểm tra giao dịch và xử lý đơn.";

    const url = createZaloOrderLink(true, true);
    const opened = window.open(url, "_blank", "noopener");
    if(!opened) window.location.href = url;
  }

  function toast(message){
    if(!els.toast) return;
    els.toast.textContent = message;
    els.toast.classList.add("active");
    clearTimeout(els.toast._timer);
    els.toast._timer = setTimeout(() => els.toast.classList.remove("active"), 2500);
  }

  // ===== BIND EVENTS & BOOT =====
  function bindEvents(){
    if(els.searchInput){
      els.searchInput.addEventListener("input", e => {
        searchKeyword = e.target.value;
        renderProducts();
      });
    }
    if(els.chips){
      els.chips.addEventListener("click", e => {
        const btn = e.target.closest(".chip");
        if(!btn) return;
        selectedCategory = btn.getAttribute("data-cat");
        renderFilters();
        renderProducts();
      });
    }
    if(els.categoryFilter){
      els.categoryFilter.addEventListener("change", e => {
        selectedCategory = e.target.value;
        renderFilters();
        renderProducts();
      });
    }
    if(els.stockFilter){
      els.stockFilter.addEventListener("change", e => {
        selectedStock = e.target.value;
        renderProducts();
      });
    }

    // Rail Prev & Next Scroll
    if(els.railPrev && els.quickRail){
      els.railPrev.addEventListener("click", () => {
        els.quickRail.scrollBy({left: -240, behavior: "smooth"});
      });
    }
    if(els.railNext && els.quickRail){
      els.railNext.addEventListener("click", () => {
        els.quickRail.scrollBy({left: 240, behavior: "smooth"});
      });
    }
    if(els.quickRail){
      els.quickRail.addEventListener("scroll", updateRailButtons);
      els.quickRail.addEventListener("click", e => {
        const item = e.target.closest(".rail-item");
        if(item) openProductModal(item.getAttribute("data-group-id"));
      });
    }

    if(els.featuredGrid){
      els.featuredGrid.addEventListener("click", e => {
        const card = e.target.closest(".featured-card");
        if(card) openProductModal(card.getAttribute("data-group-id"));
      });
    }
    if(els.productGroups){
      els.productGroups.addEventListener("click", e => {
        const card = e.target.closest(".product-card");
        if(card) openProductModal(card.getAttribute("data-group-id"));
      });
    }
    if(els.productModal){
      els.productModal.addEventListener("click", e => {
        if(e.target === els.productModal || e.target.hasAttribute("data-close")) closeProductModal();
      });
    }
    document.addEventListener("keydown", e => {
      if(e.key === "Escape") closeProductModal();
    });
    if(els.modalPlans){
      els.modalPlans.addEventListener("click", e => {
        const opt = e.target.closest(".plan-option");
        if(opt) selectPlan(opt.getAttribute("data-plan-id"));
      });
    }

    if(els.createQrBtn) els.createQrBtn.addEventListener("click", generatePaymentQr);
    if(els.copyPaymentBtn) els.copyPaymentBtn.addEventListener("click", copyPaymentContent);
    if(els.copyOrderBtn) els.copyOrderBtn.addEventListener("click", copyOrder);
    if(els.confirmPaymentBtn) els.confirmPaymentBtn.addEventListener("click", confirmPayment);

    // Bottom nav category tab
    if(els.categoryTab){
      els.categoryTab.addEventListener("click", e => {
        e.preventDefault();
        if(els.categoryFilter){
          els.categoryFilter.focus();
          els.categoryFilter.scrollIntoView({behavior: "smooth", block: "center"});
        }
      });
    }
  }

  function boot(){
    const ids = [
      "totalProducts", "totalPlans", "featuredGrid",
      "searchInput", "chips", "categoryFilter", "stockFilter", "resultCount",
      "quickRail", "railPrev", "railNext", "productGroups", "empty",
      "categoryTab", "productModal", "modalSheet", "modalLogo", "modalTitle",
      "modalSub", "modalProductImage", "modalDesc", "modalPlanCount", "modalPlans",
      "checkoutForm", "selectedPlanBox", "customerName", "customerPhone",
      "createQrBtn", "zaloGeneral", "paymentError", "paymentResult",
      "qrImage", "paymentStatusBadge", "paymentNote", "paymentAmount",
      "paymentContent", "paymentPhone", "paymentOrderCode", "copyPaymentBtn",
      "copyOrderBtn", "confirmPaymentBtn", "toast"
    ];
    ids.forEach(id => els[id] = $(id));

    recomputeCategories();
    renderStats();
    renderFilters();
    renderFeatured();
    renderProducts();
    bindEvents();
  }

  if(document.readyState === "loading"){
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
