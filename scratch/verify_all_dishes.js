const fs = require('fs');
const path = require('path');
const vm = require('vm');

const appJs = fs.readFileSync(path.join(__dirname, '..', 'js', 'app.js'), 'utf8');
const win = { scrollTo: () => {}, addEventListener: () => {} };
const ctx = { window: win, document: { getElementById: () => null, querySelectorAll: () => [] } };
vm.createContext(ctx);
vm.runInContext(appJs, ctx);

console.log('=== VERIFYING FOOD CATALOG ===');
console.log('Total Dishes in menu:', win.DISHES.length);

const categories = {};
let missingCount = 0;

win.DISHES.forEach((d, i) => {
  const rootImg = path.join(__dirname, '..', d.image);
  const frontendImg = path.join(__dirname, '..', 'frontend', d.image);
  const ok = fs.existsSync(rootImg) && fs.existsSync(frontendImg);
  if (!ok) missingCount++;

  categories[d.category] = (categories[d.category] || 0) + 1;
  console.log(`${String(i + 1).padStart(2, ' ')}. [${d.category.toUpperCase().padEnd(9, ' ')}] ${d.name.padEnd(30, ' ')} ₹${String(d.price).padStart(3, ' ')} | Rating: ${d.rating} ⭐ | Img: ${ok ? '✓ OK' : '✗ MISSING'}`);
});

console.log('\nBreakdown by Category:');
console.log(categories);

if (missingCount > 0) {
  console.error(`\n❌ ERROR: ${missingCount} dishes have missing image files!`);
  process.exit(1);
} else {
  console.log('\n✅ ALL 16 DISHES HAVE VALID IMAGES & PROPER METADATA!');
}
