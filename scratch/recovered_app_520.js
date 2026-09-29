const fs = require('fs');
const http = require('http');
const assert = require('assert');

console.log("=== 1. Testing 'My Orders' Visibility ===");
const html = fs.readFileSync('index.html', 'utf-8');

// A. Navbar on Home Page must NOT have My Orders
const navStart = html.indexOf('<nav class="nav-links" id="main-nav-links"');
const navEnd = html.indexOf('</nav>', navStart);
const navContent = html.substring(navStart, navEnd);
assert(!navContent.includes('My Orders'), "Navbar on home page must NOT have My Orders");
assert(!navContent.includes('btn-top-orders'), "Navbar on home page must NOT have btn-top-orders");
console.log("✅ Top navbar on home page has NO 'My Orders' button");

// B. Home page hero (view-about) must NOT have My Orders
const aboutStart = html.indexOf('id="view-about"');
const aboutEnd = html.indexOf('id="view-login"');
const aboutContent = html.substring(aboutStart, aboutEnd);
assert(!aboutContent.includes('My Orders'), "Home page hero must NOT have My Orders");
console.log("✅ Home page (view-about) has NO 'My Orders' button");

// C. Student Menu (view-order) MUST have My Orders right at the top
const orderStart = html.indexOf('id="view-order"');
const orderEnd = html.indexOf('id="view-manager"');
const orderContent = html.substring(orderStart, orderEnd);
assert(orderContent.includes('id="btn-menu-top-my-orders"'), "Student menu must have btn-menu-top-my-orders");
assert(orderContent.includes('My Orders'), "Student menu must display My Orders at the top");
console.log("✅ Student Menu displays 'My Orders' right at the top bar");

console.log("\n=== 2. Testing 'Order Now' Not Everywhere on Food Items ===");
const js = fs.readFileSync('js/app.js', 'utf-8');
const dishesFnStart = js.indexOf('function renderDishes()');
const dishesFnEnd = js.indexOf('function filterCategory', dishesFnStart);
const dishesFnContent = js.substring(dishesFnStart, dishesFnEnd);

// Ensure individual dish cards don't have Order Now buttons
assert(!dishesFnContent.includes('Order Now'), "Individual dish cards must NOT contain 'Order Now' buttons");
assert(dishesFnContent.includes('add-btn'), "Individual dish cards must have ADD + button");
assert(dishesFnContent.includes('qty-pill'), "Individual dish cards must have qty-pill");
console.log("✅ Individual food cards do NOT have 'Order Now' buttons everywhere; only clean ADD + and qty controls");

console.log("\n=== 3. Testing Simple Reviews Section ===");
assert(html.includes('id="reviews-section"'), "reviews-section exists");
assert(html.includes('id="reviews-cards-grid"'), "reviews-cards-grid exists");
assert(html.includes('Leave a Review'), "Leave a Review button exists");
// Ensure complex chips/dashboards are removed
assert(!html.includes('id="chip-filter-5"'), "Complex filter chips removed for simplicity");
assert(!html.includes('Explore Reviews In Different Ways'), "Complex filter header removed for simplicity");
console.log("✅ Reviews section is clean, elegant, and simple like standard websites have");

console.log("\n=== 4. Testing Live HTTP Server ===");
http.get('http://127.0.0.1:5000/', (res) => {
  assert.strictEqual(res.statusCode, 200, "Server should return 200");
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    assert(data.includes('Savitha Canteen'), "Response includes Savitha Canteen");
    console.log("✅ Live Flask server returns 200 OK without errors");
    console.log("\n🎉 ALL TESTS PASSED SUCCESSFULLY!");
    process.exit(0);
  });
}).on('error', (err) => {
  console.error("HTTP error:", err);
  process.exit(1);
});
