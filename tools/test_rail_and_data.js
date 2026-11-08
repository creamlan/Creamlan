const fs = require('fs');

const jsCode = fs.readFileSync('js/app.js', 'utf8');

// Test that DEFAULT_PRODUCT_GROUPS can be extracted and parsed
const match = jsCode.match(/const DEFAULT_PRODUCT_GROUPS = (\[[\s\S]*?\]);\s*const ALL_SONGS/);
if (!match) {
  // Let's find const DEFAULT_PRODUCT_GROUPS = [...]
  const startIdx = jsCode.indexOf('const DEFAULT_PRODUCT_GROUPS = [');
  const endIdx = jsCode.indexOf('let productGroupsData =');
  const jsonStr = jsCode.slice(startIdx + 'const DEFAULT_PRODUCT_GROUPS = '.length, endIdx).trim().replace(/;$/, '');
  const data = JSON.parse(jsonStr);
  console.log(`Extracted products: ${data.length}`);
  
  // Test rail deduplication
  const seen = new Set();
  const uniqueRail = [];
  data.forEach(it => {
    const key = (it.image || it.brand || it.name).toLowerCase();
    if(!seen.has(key)){
      seen.add(key);
      uniqueRail.push(it);
    }
  });
  console.log(`Unique rail icons: ${uniqueRail.length}`);
  console.log('Rail brands:', uniqueRail.map(p => p.brand).join(', '));
  
  // Check if any brand is duplicated in the rail
  const brandCounts = {};
  uniqueRail.forEach(p => {
    brandCounts[p.brand] = (brandCounts[p.brand] || 0) + 1;
  });
  const dups = Object.entries(brandCounts).filter(([b, c]) => c > 1);
  console.log('Duplicate brands in rail:', dups.length === 0 ? 'NONE (Perfect!)' : dups);
}
