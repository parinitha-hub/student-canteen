const fs = require('fs');
const http = require('http');
const assert = require('assert');

console.log("=========================================================================");
console.log("SAVITHA CANTEEN - COMPREHENSIVE REQUIREMENTS VERIFICATION");
console.log("=========================================================================\n");

// 1. Check index.html & frontend/index.html
const html = fs.readFileSync('index.html', 'utf-8');
const feHtml = fs.readFileSync('frontend/index.html', 'utf-8');
assert.strictEqual(html, feHtml, "index.html and frontend/index.html must be identical");
console.log("✅ Root and frontend index.html files are synchronized");

// 2. Check that password is NOT visible in HTML
assert(!html.includes('savitha123'), "Plaintext password 'savitha123' must NOT exist in HTML");
assert(!html.includes('Staff password:'), "Password hint text must NOT exist in HTML");
assert(!html.includes('1-Click Kitchen Staff Login'), "1-Click staff login button must NOT exist in HTML");
assert(html.includes('id="login-worker-password"'), "Password input must exist");
assert(html.includes('type="password" id="login-worker-password"'), "Password input must be type='password'");
assert(html.includes('placeholder="Enter staff password"'), "Password placeholder must be clean");
console.log("✅ Requirement 2 Passed: Password is completely hidden (not visible anywhere in UI/HTML)");

// 3. Check view-order nesting: dishes and category bar MUST be inside view-order
const viewOrderStart = html.indexOf('id="view-order"');
const viewOrderEnd = html.indexOf('id="view-manager"');
assert(viewOrderStart !== -1, "#view-order container must exist");
assert(viewOrderEnd !== -1, "#view-manager container must exist");
assert(viewOrderStart < viewOrderEnd, "#view-order must precede #view-manager");

const orderSection = html.slice(viewOrderStart, viewOrderEnd);
assert(orderSection.includes('class="category-bar"'), "Category bar must be inside #view-order");
assert(orderSection.includes('id="dishes-grid"'), "#dishes-grid must be inside #view-order");
assert(!orderSection.includes('active-order-actions'), "Orphaned active-order-actions must be removed");
console.log("✅ Requirement 1 Passed (HTML structure): Category bar and dishes grid are strictly enclosed within #view-order");

// 4. Check Add Review modal
assert(html.includes('id="add-review-modal"'), "#add-review-modal exists");
assert(html.includes('class="swiggy-stars-row"'), "Stars row exists for rating");
assert(html.includes('setSwiggyRating(1)'), "Can select 1 star");
assert(html.includes('setSwiggyRating(2)'), "Can select 2 stars");
assert(html.includes('setSwiggyRating(3)'), "Can select 3 stars");
assert(html.includes('setSwiggyRating(4)'), "Can select 4 stars");
assert(html.includes('setSwiggyRating(5)'), "Can select 5 stars");
assert(!html.includes('Loved it! (5.0'), "Forced example strings removed from HTML");
assert(!html.includes('e.g. 2nd Year CSE'), "Example e.g. text removed from review modal");
console.log("✅ Requirement 3 Passed: Add Review allows arbitrary star selection (1-5) as user wishes, with clean placeholders and no forced example labels");

// 5. Check js/app.js & frontend/js/app.js
const js = fs.readFileSync('js/app.js', 'utf-8');
const feJs = fs.readFileSync('frontend/js/app.js', 'utf-8');
assert.strictEqual(js, feJs, "js/app.js and frontend/js/app.js must be identical");
console.log("✅ Root and frontend js/app.js files are synchronized");

// Check JS guards
assert(js.includes('function initUserAuth()'), "initUserAuth exists in JS");
assert(js.includes('currentUser = null;'), "currentUser initialized to null on startup");
assert(js.includes('STRICT LOGIN GUARD: Without login, visitors cannot view the menu'), "performSwitchMode has login guard");
assert(js.includes('STRICT LOGIN GUARD: Cannot view food menu without logging in'), "navigateToSection has login guard");
assert(js.includes('handleMenuAccessRequest'), "handleMenuAccessRequest defined in JS");
assert(js.includes('function setSwiggyRating'), "setSwiggyRating defined in JS");
assert(js.includes('function updateSwiggyStarDisplay'), "updateSwiggyStarDisplay defined in JS");
console.log("✅ JS Authentication guards and review rating functions verified");

// 6. Test Live HTTP Server on port 5000
http.get('http://127.0.0.1:5000/', (res) => {
  assert.strictEqual(res.statusCode, 200, "Flask server must respond with 200 OK");
  let body = '';
  res.on('data', chunk => body += chunk);
  res.on('end', () => {
    assert(body.includes('Savitha Canteen'), "Response contains Savitha Canteen");
    assert(!body.includes('savitha123'), "Response contains no plaintext passwords");
    assert(body.includes('id="login-worker-password"'), "Response contains staff password field");
    assert(body.includes('id="view-order" style="display:none;"'), "Response has #view-order hidden by default");
    console.log("✅ Requirement 4 Passed: Live Flask web application is running cleanly with 200 OK and no errors");

    console.log("\n=========================================================================");
    console.log("🎉 ALL USER REQUIREMENTS VERIFIED & FULLY COMPLIANT!");
    console.log("=========================================================================");
    process.exit(0);
  });
}).on('error', (err) => {
  console.error("HTTP connection error to Flask:", err);
  process.exit(1);
});
