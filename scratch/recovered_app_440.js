const http = require('http');
const fs = require('fs');
const assert = require('assert');

console.log("=== 1. Validating HTML Content ===");
const html = fs.readFileSync('index.html', 'utf-8');

// 1.1 Hero Button has handleMenuAccessRequest
assert(html.includes('handleMenuAccessRequest()'), "Missing handleMenuAccessRequest in index.html hero button");

// 1.2 Reviews Showcase Section
assert(html.includes('id="reviews-section"'), "Missing reviews-section in index.html");
assert(html.includes('id="reviews-cards-grid"'), "Missing reviews-cards-grid in index.html");
assert(html.includes('id="reviews-total-counter"'), "Missing reviews-total-counter in index.html");

// 1.3 Filter Chips (in different ways: 4 & 5 stars, categories)
assert(html.includes('id="chip-filter-all"'), "Missing chip-filter-all");
assert(html.includes('id="chip-filter-5"'), "Missing chip-filter-5 (5-star filter)");
assert(html.includes('id="chip-filter-4"'), "Missing chip-filter-4 (4-star filter)");
assert(html.includes('id="chip-filter-website"'), "Missing chip-filter-website");
assert(html.includes('id="chip-filter-speed"'), "Missing chip-filter-speed");
assert(html.includes('id="chip-filter-food"'), "Missing chip-filter-food");

// 1.4 Add Website Review Modal
assert(html.includes('id="add-review-modal"'), "Missing add-review-modal");
assert(html.includes('id="btn-rate-5"'), "Missing 5-star rating button in modal");
assert(html.includes('id="btn-rate-4"'), "Missing 4-star rating button in modal");
assert(html.includes('id="btn-submit-website-review"'), "Missing submit button in modal");

// 1.5 Developer Attribution preserved
assert(html.includes('Parinitha.S'), "Developer Parinitha.S attribution must be preserved");

console.log("✅ All HTML checks passed!");

console.log("\n=== 2. Validating JavaScript Logic ===");
const js = fs.readFileSync('js/app.js', 'utf-8');

// 2.1 Login Guard Check
assert(js.includes('STRICT LOGIN GUARD: Without login'), "Missing performSwitchMode login guard");
assert(js.includes('STRICT LOGIN GUARD: Cannot view food menu'), "Missing navigateToSection login guard");
assert(js.includes('function handleMenuAccessRequest'), "Missing handleMenuAccessRequest function");

// 2.2 Review System Functions
assert(js.includes('function filterReviews'), "Missing filterReviews function");
assert(js.includes('function renderFeedbackList'), "Missing renderFeedbackList function");
assert(js.includes('function openAddReviewModal'), "Missing openAddReviewModal function");
assert(js.includes('function closeAddReviewModal'), "Missing closeAddReviewModal function");
assert(js.includes('function selectReviewRating'), "Missing selectReviewRating function");
assert(js.includes('function handleWebsiteReviewSubmit'), "Missing handleWebsiteReviewSubmit function");

// 2.3 Window Exports
assert(js.includes('window.handleMenuAccessRequest = handleMenuAccessRequest;'), "Missing handleMenuAccessRequest export");
assert(js.includes('window.filterReviews = filterReviews;'), "Missing filterReviews export");
assert(js.includes('window.openAddReviewModal = openAddReviewModal;'), "Missing openAddReviewModal export");

console.log("✅ All JavaScript checks passed!");

console.log("\n=== 3. Testing Live HTTP Endpoints on Flask Server ===");

function testEndpoint(path, method = 'GET', body = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(`http://127.0.0.1:5000${path}`);
    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname + url.search,
      method: method,
      headers: body ? { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) } : {}
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve({ statusCode: res.statusCode, data });
      });
    });

    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

async function runApiTests() {
  const rootRes = await testEndpoint('/');
  assert.strictEqual(rootRes.statusCode, 200, "Root page should return 200");
  assert(rootRes.data.includes('reviews-section'), "Root page serves reviews-section");
  console.log("✅ Root GET /: 200 OK & rendered with reviews showcase");

  const fbRes = await testEndpoint('/api/feedback');
  assert.strictEqual(fbRes.statusCode, 200, "Feedback endpoint should return 200");
  const fbJson = JSON.parse(fbRes.data);
  assert(Array.isArray(fbJson.feedback), "Feedback array exists");
  
  const has5Star = fbJson.feedback.some(f => parseInt(f.rating) === 5);
  const has4Star = fbJson.feedback.some(f => parseInt(f.rating) === 4);
  assert(has5Star, "Should have 5-star reviews in feedback");
  assert(has4Star, "Should have 4-star reviews in feedback");
  console.log(`✅ API GET /api/feedback: 200 OK (Loaded ${fbJson.feedback.length} reviews including both 4-star and 5-star reviews)`);

  // Test submitting a 4-star review
  const test4StarReview = {
    name: "Campus Tester",
    year: "3rd Year CSE",
    rating: 4,
    category: "Website UI",
    comment: "Automated test: smooth UI and token system. 4 stars!",
    date: "2026-09-25",
    timestamp: Date.now()
  };

  const postRes = await testEndpoint('/api/feedback', 'POST', JSON.stringify(test4StarReview));
  assert(postRes.statusCode === 200 || postRes.statusCode === 201, "Feedback submission should succeed");
  console.log("✅ API POST /api/feedback: Successfully added 4-star review to database");
}

runApiTests().then(() => {
  console.log("\n=== ALL COMPREHENSIVE TESTS PASSED! ===");
  process.exit(0);
}).catch(err => {
  console.error("❌ Test failed:", err);
  process.exit(1);
});
