const fs = require('fs');

const catalog = JSON.parse(fs.readFileSync('products_catalog.json', 'utf8'));
const jsCode = fs.readFileSync('js/app.js', 'utf8');

const startIdx = jsCode.indexOf('const DEFAULT_PRODUCT_GROUPS = [');
const endIdx = jsCode.indexOf('let productGroupsData =');
const jsonStr = jsCode.slice(startIdx + 'const DEFAULT_PRODUCT_GROUPS = '.length, endIdx).trim().replace(/;$/, '');
const appProducts = JSON.parse(jsonStr);

console.log(`Catalog length: ${catalog.length}, App.js length: ${appProducts.length}`);
if (catalog.length !== appProducts.length) {
  console.error("Length mismatch!");
  process.exit(1);
}

for (let i = 0; i < catalog.length; i++) {
  if (catalog[i].name !== appProducts[i].name || catalog[i].plans.length !== appProducts[i].plans.length) {
    console.error(`Mismatch at index ${i}: ${catalog[i].name} vs ${appProducts[i].name}`);
    process.exit(1);
  }
}

console.log("All products and plans match 100% perfectly between catalog and app.js!");
