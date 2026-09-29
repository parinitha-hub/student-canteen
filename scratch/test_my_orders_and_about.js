const http = require('http');
const fs = require('fs');
const assert = require('assert');

console.log("=== 1. Testing HTML Structure ===");
const html = fs.readFileSync('index.html', 'utf-8');

// 1. Check My Orders button in top navbar
assert(html.includes('id="btn-top-orders"'), "Missing btn-top-orders in navbar");
assert(html.includes('id="my-orders-count"'), "Missing my-orders-count badge");

// 2. Check My Orders button in Menu Header
assert(html.includes('id="btn-menu-my-orders"'), "Missing btn-menu-my-orders in menu header");

// 3. Check Token Modal has 'View in My Orders' button
assert(html.includes('View in My Orders'), "Missing View in My Orders button in Token Modal");

// 4. Check My Orders Modal exists
assert(html.includes('id="my-orders-modal"'), "Missing my-orders-modal in HTML");
assert(html.includes('id="my-orders-list-container"'), "Missing my-orders-list-container in HTML");

// 5. Check Simplified About Website section
assert(html.includes('id="view-about"'), "Missing view-about in HTML");
assert(html.includes('How Savitha Canteen Works'), "Missing clean How Savitha Canteen Works heading");
assert(html.includes('1. Select Your Dishes'), "Missing step 1");
assert(html.includes('2. Get Instant Token'), "Missing step 2");
assert(html.includes('3. Zero-Wait Pickup'), "Missing step 3");
assert(html.includes('Parinitha.S'), "Preserved developer Parinitha.S attribution");
// Ensure heavy feedback form was removed from About section
assert(!html.includes('id="feedback-form"'), "Heavy feedback-form should be removed from simplified about section");

console.log("✅ HTML structure assertions passed!");

console.log("\n=== 2. Testing HTTP Endpoints from Flask Server ===");

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

async function runHttpTests() {
  const rootRes = await testEndpoint('/');
  assert.strictEqual(rootRes.statusCode, 200, "Root / should return 200");
  assert(rootRes.data.includes('Savitha Canteen'), "Root page contains Savitha Canteen");
  assert(rootRes.data.includes('btn-top-orders'), "Root served contains btn-top-orders");
  console.log("✅ Root GET /: 200 OK & rendered successfully with My Orders navigation");

  const healthRes = await testEndpoint('/api/health');
  assert.strictEqual(healthRes.statusCode, 200, "Health should return 200");
  const healthJson = JSON.parse(healthRes.data);
  assert.strictEqual(healthJson.status, 'healthy');
  console.log("✅ API GET /api/health: 200 OK & healthy");

  const ordersRes = await testEndpoint('/api/orders');
  assert.strictEqual(ordersRes.statusCode, 200, "Orders should return 200");
  const ordersJson = JSON.parse(ordersRes.data);
  assert(Array.isArray(ordersJson.orders), "Orders array exists");
  console.log(`✅ API GET /api/orders: 200 OK (current live orders: ${ordersJson.orders.length})`);

  // Test placing a test order and cancelling it
  const testOrder = {
    id: "test_" + Date.now(),
    token: "#TEST-99",
    items: [{ id: 1, name: "Veg Biryani", price: 90, qty: 1, subtotal: 90 }],
    total: 90,
    time: "18:50",
    status: "Preparing in Kitchen ⏳",
    timestamp: Date.now()
  };

  const createRes = await testEndpoint('/api/orders', 'POST', JSON.stringify(testOrder));
  assert.strictEqual(createRes.statusCode, 201, "Order creation should return 201");
  console.log("✅ API POST /api/orders: 201 Created successfully");

  const cancelRes = await testEndpoint(`/api/orders/${testOrder.id}/cancel`, 'POST');
  assert.strictEqual(cancelRes.statusCode, 200, "Order cancellation should return 200");
  console.log("✅ API POST /api/orders/:id/cancel: 200 Cancelled & removed cleanly");
}

runHttpTests().then(() => {
  console.log("\n=== ALL TESTS PASSED SUCCESSFULLY! ===");
  process.exit(0);
}).catch(err => {
  console.error("❌ Test failed:", err);
  process.exit(1);
});
