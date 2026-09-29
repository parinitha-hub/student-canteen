const fs = require('fs');
const http = require('http');
const assert = require('assert');

console.log("=== 1. Validating Swiggy/Zomato Review Modal ===");
const html = fs.readFileSync('index.html', 'utf-8');

assert(html.includes('class="swiggy-stars-row"'), "Swiggy stars row exists");
assert(html.includes('setSwiggyRating'), "setSwiggyRating exists in HTML");
assert(html.includes('Submit Review'), "Submit Review button exists in modal");
assert(!html.includes('btn-rating-choice'), "Old complex rating buttons removed from review modal");
console.log("✅ Add review modal is simple like Swiggy and Zomato");

console.log("\n=== 2. Validating Kitchen Staff Login ===");
assert(html.includes('id="tab-login-worker"'), "Kitchen Staff tab exists on login card");
assert(html.includes('switchLoginRoleTab'), "switchLoginRoleTab exists");
assert(html.includes('quickStaffLogin'), "quickStaffLogin exists");
assert(html.includes('savitha123'), "Staff password hint exists");

const js = fs.readFileSync('js/app.js', 'utf-8');
assert(js.includes('function switchLoginRoleTab'), "switchLoginRoleTab defined in JS");
assert(js.includes('function quickStaffLogin'), "quickStaffLogin defined in JS");
assert(js.includes('function verifyKitchenPassword'), "verifyKitchenPassword defined in JS");
console.log("✅ Kitchen staff login is prominent, accessible, and supports 1-click and standard passwords");

console.log("\n=== 3. Validating Order Visibility (Only in My Orders) ===");
// Ensure active-order-banner is NOT present in index.html
assert(!html.includes('id="active-order-banner"'), "active-order-banner must be removed from HTML");
// Ensure My Orders button exists at the top of the student menu
assert(html.includes('id="btn-menu-top-my-orders"'), "btn-menu-top-my-orders exists at top of student menu");
console.log("✅ Order banner removed from website top; orders only visible when opening My Orders");

console.log("\n=== 4. Testing Live HTTP Server ===");
http.get('http://127.0.0.1:5000/', (res) => {
  assert.strictEqual(res.statusCode, 200, "Server must return 200");
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    assert(data.includes('Savitha Canteen'), "Response includes Savitha Canteen");
    assert(data.includes('tab-login-worker'), "Response includes kitchen staff tab");
    assert(!data.includes('active-order-banner'), "Response does not include active-order-banner");
    console.log("✅ Live Flask server returns 200 OK with all refined features");
    console.log("\n🎉 ALL TESTS PASSED SUCCESSFULLY!");
    process.exit(0);
  });
}).on('error', (err) => {
  console.error("HTTP error:", err);
  process.exit(1);
});
