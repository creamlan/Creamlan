/**
 * Creamlan Store - Google Sheets Synchronization Module
 * Real-time frontend sync with Google Sheets data source:
 * https://docs.google.com/spreadsheets/d/1MvsUV2Gxq3CXyUSEE8b-sAGkhuNoEaHs9HqlNAqaEg4/edit?gid=0
 */

const SHEET_CONFIG = {
  sheetId: "1MvsUV2Gxq3CXyUSEE8b-sAGkhuNoEaHs9HqlNAqaEg4",
  gid: "0",
  gvizUrl: "https://docs.google.com/spreadsheets/d/1MvsUV2Gxq3CXyUSEE8b-sAGkhuNoEaHs9HqlNAqaEg4/gviz/tq?tqx=out:json&tq=&gid=0",
  csvUrl: "https://docs.google.com/spreadsheets/d/1MvsUV2Gxq3CXyUSEE8b-sAGkhuNoEaHs9HqlNAqaEg4/export?format=csv&gid=0"
};

class SheetsSyncManager {
  constructor() {
    this.isSyncing = false;
    this.lastSyncedAt = null;
    this.listeners = [];
  }

  // Parse price string to integer and out-of-stock flag
  parsePrice(val) {
    if (!val && val !== 0) return { amount: 0, isOutOfStock: false };
    const s = String(val).toLowerCase().trim();
    if (s.includes("hết") || s.includes("out") || s.includes("tạm") || s.includes("liên hệ")) {
      return { amount: 0, isOutOfStock: true };
    }
    const nums = s.replace(/\./g, "").replace(/,/g, "").match(/\d+/);
    if (nums) {
      return { amount: parseInt(nums[0], 10), isOutOfStock: false };
    }
    return { amount: 0, isOutOfStock: false };
  }

  // Price adjustment rules as required by the prompt
  adjustPrice(origAmount) {
    if (origAmount <= 0) return 0;
    // High-value products (>= 200.000) keep exact price from Google Sheets
    if (origAmount >= 200000) return origAmount;

    // Specific low-value rounding to clean, beautiful numbers
    switch (origAmount) {
      case 18000: return 20000;
      case 28000: return 30000;
      case 59000: return 60000;
      case 88000: return 90000;
      case 138000: return 140000;
      case 199000: return 200000;
      case 27000: return 30000;
      case 43000: return 45000;
      case 78000: return 80000;
      default: return origAmount;
    }
  }

  formatVND(amt) {
    if (!amt || amt <= 0) return "";
    return amt.toLocaleString("vi-VN") + " đ";
  }

  // Parse Gviz JSON response
  parseGvizResponse(rawText) {
    try {
      // Matches google.visualization.Query.setResponse({...});
      const match = rawText.match(/google\.visualization\.Query\.setResponse\(([\s\S]*)\);?\s*$/);
      if (!match) return null;
      const json = JSON.parse(match[1]);
      const table = json.table;
      if (!table || !table.rows) return null;

      const items = [];
      table.rows.forEach((row, idx) => {
        const c = row.c;
        if (!c || c.length < 4) return;
        
        // Col B (idx 1): Name, Col C (idx 2): Duration, Col D (idx 3): Price, Col E (idx 4): Upgrade Type, Col F (idx 5): Shared/Private, Col G (idx 6): Warranty, Col I (idx 8): Note
        const name = c[1] && c[1].v != null ? String(c[1].v).trim() : "";
        const duration = c[2] && c[2].v != null ? String(c[2].v).trim() : "";
        const priceVal = c[3] ? (c[3].f || c[3].v) : "";
        const upgradeType = c[4] && c[4].v != null ? String(c[4].v).trim() : "";
        const sharedPrivate = c[5] && c[5].v != null ? String(c[5].v).trim() : "";
        const warranty = c[6] && c[6].v != null ? String(c[6].v).trim() : "";
        const note = c[8] && c[8].v != null ? String(c[8].v).trim() : "";

        if (name || priceVal) {
          items.push({
            rowIdx: idx + 2, // Account for header offset
            name,
            duration,
            priceRaw: String(priceVal),
            upgradeType,
            sharedPrivate,
            warranty,
            note
          });
        }
      });
      return items;
    } catch (e) {
      console.warn("Lỗi đọc dữ liệu Gviz:", e);
      return null;
    }
  }

  // Fetch via JSONP fallback if direct fetch fails (handles any CORS restrictions)
  fetchViaJsonp(url) {
    return new Promise((resolve, reject) => {
      const callbackName = "creamlan_gviz_cb_" + Date.now();
      const script = document.createElement("script");
      const timeout = setTimeout(() => {
        cleanup();
        reject(new Error("Timeout khi tải Google Sheets JSONP"));
      }, 10000);

      function cleanup() {
        clearTimeout(timeout);
        delete window[callbackName];
        if (script.parentNode) script.parentNode.removeChild(script);
      }

      window[callbackName] = (data) => {
        cleanup();
        resolve(data);
      };

      const sep = url.includes("?") ? "&" : "?";
      script.src = `${url}${sep}tqx=responseHandler:${callbackName}`;
      script.onerror = () => {
        cleanup();
        reject(new Error("Lỗi mạng khi tải script Google Sheets"));
      };

      document.head.appendChild(script);
    });
  }

  // Fetch Google Sheets data with auto fallback
  async fetchSheetData() {
    // 1. Try standard fetch with gviz
    try {
      const res = await fetch(SHEET_CONFIG.gvizUrl, { cache: "no-store" });
      if (res.ok) {
        const text = await res.text();
        const items = this.parseGvizResponse(text);
        if (items && items.length > 0) return items;
      }
    } catch (err) {
      console.warn("Direct fetch gviz không thành công, thử phương án JSONP...", err);
    }

    // 2. Try JSONP gviz
    try {
      const gvizData = await this.fetchViaJsonp(SHEET_CONFIG.gvizUrl);
      if (gvizData && gvizData.table && gvizData.table.rows) {
        const items = [];
        gvizData.table.rows.forEach((row, idx) => {
          const c = row.c;
          if (!c || c.length < 4) return;
          const name = c[1] && c[1].v != null ? String(c[1].v).trim() : "";
          const duration = c[2] && c[2].v != null ? String(c[2].v).trim() : "";
          const priceVal = c[3] ? (c[3].f || c[3].v) : "";
          const upgradeType = c[4] && c[4].v != null ? String(c[4].v).trim() : "";
          const sharedPrivate = c[5] && c[5].v != null ? String(c[5].v).trim() : "";
          const warranty = c[6] && c[6].v != null ? String(c[6].v).trim() : "";
          const note = c[8] && c[8].v != null ? String(c[8].v).trim() : "";

          if (name || priceVal) {
            items.push({
              rowIdx: idx + 2,
              name,
              duration,
              priceRaw: String(priceVal),
              upgradeType,
              sharedPrivate,
              warranty,
              note
            });
          }
        });
        if (items.length > 0) return items;
      }
    } catch (err) {
      console.warn("JSONP gviz cũng không thành công:", err);
    }

    return null;
  }

  // Match and apply sheet items into the active products catalog
  applySheetDataToCatalog(catalog, sheetItems) {
    if (!catalog || !sheetItems || !sheetItems.length) return catalog;

    let updatedCount = 0;

    catalog.forEach(product => {
      if (!product.plans || !product.plans.length) return;

      product.plans.forEach(plan => {
        // If this plan has a sheetRow reference or matches name + duration
        let matchedItem = null;
        if (plan.sheetRow) {
          matchedItem = sheetItems.find(it => it.rowIdx === plan.sheetRow);
        }
        
        if (!matchedItem) {
          // Match by name similarity and duration
          const planVarNorm = (plan.variant || "").toLowerCase();
          const planDurNorm = (plan.duration || "").toLowerCase();
          matchedItem = sheetItems.find(it => {
            const itNameNorm = it.name.toLowerCase();
            const itDurNorm = it.duration.toLowerCase();
            return (planVarNorm === itNameNorm || itNameNorm.includes(planVarNorm) || planVarNorm.includes(itNameNorm)) &&
                   (planDurNorm === itDurNorm || itDurNorm.includes(planDurNorm) || planDurNorm.includes(itDurNorm));
          });
        }

        if (matchedItem) {
          const { amount, isOutOfStock } = this.parsePrice(matchedItem.priceRaw);
          const adjAmount = this.adjustPrice(amount);

          plan.isOutOfStock = isOutOfStock;
          plan.priceAmount = adjAmount;
          plan.originalPriceAmount = amount;
          plan.price = adjAmount > 0 ? this.formatVND(adjAmount) : (isOutOfStock ? "Hết hàng" : "Liên hệ");
          plan.originalPrice = (amount > 0 && amount !== adjAmount) ? this.formatVND(amount) : "";
          
          if (matchedItem.warranty) {
            plan.warranty = matchedItem.warranty;
          }
          if (matchedItem.note) {
            plan.note = matchedItem.note;
          }
          if (matchedItem.upgradeType) {
            plan.accountType = matchedItem.upgradeType;
          }
          if (matchedItem.sharedPrivate) {
            plan.sharedPrivate = matchedItem.sharedPrivate;
          }
          updatedCount++;
        }
      });

      // Recompute price label & stock for product
      const availablePrices = product.plans
        .filter(p => !p.isOutOfStock && p.priceAmount > 0)
        .map(p => p.priceAmount);

      if (availablePrices.length > 0) {
        const minP = Math.min(...availablePrices);
        product.priceLabel = "Từ " + this.formatVND(minP);
        product.inStock = true;
      } else if (product.plans.some(p => p.isOutOfStock)) {
        product.priceLabel = "Tạm hết hàng";
        product.inStock = false;
      } else {
        product.priceLabel = "Liên hệ";
        product.inStock = true;
      }
    });

    console.log(`Đã cập nhật dữ liệu trực tiếp cho ${updatedCount} gói dịch vụ từ Google Sheets.`);
    return catalog;
  }

  // Trigger synchronization
  async sync(catalog, onStatusChange) {
    if (this.isSyncing) return;
    this.isSyncing = true;
    if (onStatusChange) onStatusChange({ status: "syncing", message: "Đang kết nối Google Sheets..." });

    try {
      const sheetItems = await this.fetchSheetData();
      if (sheetItems && sheetItems.length > 0) {
        this.applySheetDataToCatalog(catalog, sheetItems);
        this.lastSyncedAt = new Date();
        const timeStr = this.lastSyncedAt.toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" });
        if (onStatusChange) {
          onStatusChange({
            status: "success",
            message: `Đã đồng bộ Google Sheets (${timeStr})`,
            timestamp: this.lastSyncedAt
          });
        }
      } else {
        // Fallback: built-in data stays active
        if (onStatusChange) {
          onStatusChange({
            status: "fallback",
            message: "Dữ liệu ngoại tuyến sẵn sàng (Sheet không đổi)",
            timestamp: new Date()
          });
        }
      }
    } catch (err) {
      console.warn("Lỗi đồng bộ Google Sheets:", err);
      if (onStatusChange) {
        onStatusChange({
          status: "fallback",
          message: "Dữ liệu ngoại tuyến khả dụng",
          timestamp: new Date()
        });
      }
    } finally {
      this.isSyncing = false;
    }
  }
}

// Export singleton instance
window.sheetsSync = new SheetsSyncManager();
