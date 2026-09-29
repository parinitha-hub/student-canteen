const fs = require('fs');

console.log("=========================================================================");
console.log("TESTING: Today's Special Item (₹50) & Loyalty 10th-Order Free Coupon Card");
console.log("=========================================================================\n");

// 1. Static HTML Checks
const html = fs.readFileSync('index.html', 'utf-8');
const frontendHtml = fs.readFileSync('frontend/index.html', 'utf-8');

if (html !== frontendHtml) {
  console.error("✗ ERROR: root index.html and frontend/index.html are not in sync!");
  process.exit(1);
}
console.log("✓ Root index.html and frontend/index.html are synchronized.");

if (!html.includes('id="special-deal-banner"')) {
  console.error("✗ ERROR: special-deal-banner not found in index.html!");
  process.exit(1);
}
console.log("✓ Found Today's Special Deal banner (Flat ₹50) in index.html.");

if (!html.includes('id="loyalty-rewards-card"')) {
  console.error("✗ ERROR: loyalty-rewards-card not found in index.html!");
  process.exit(1);
}
console.log("✓ Found Loyalty Rewards Stamp Card in index.html.");

if (!html.includes('id="stamp-track"')) {
  console.error("✗ ERROR: stamp-track not found in index.html!");
  process.exit(1);
}
console.log("✓ Found 10-stamp track in index.html.");

if (!html.includes('id="cart-coupon-input"')) {
  console.error("✗ ERROR: cart-coupon-input not found in index.html!");
  process.exit(1);
}
console.log("✓ Found Cart Promo / Coupon code input in cart modal.");

// 2. DOM Mock for Dynamic Execution
const elements = {};
function createMockEl(id, tag = 'div') {
  return {
    id: id,
    tagName: tag.toUpperCase(),
    style: {},
    classList: {
      _c: new Set(),
      add: function(c) { this._c.add(c); },
      remove: function(c) { this._c.delete(c); },
      contains: function(c) { return this._c.has(c); }
    },
    value: '',
    textContent: '',
    innerHTML: '',
    children: [],
    placeholder: '',
    appendChild: function(c) { this.children.push(c); },
    removeChild: function(c) { this.children = this.children.filter(x => x !== c); },
    remove: function() {},
    focus: () => {}
  };
}

const mockIds = [
  "nav-btn-about", "nav-btn-home", "btn-top-my-orders-nav", "nav-btn-kitchen",
  "nav-btn-login", "user-auth-slot", "view-about", "view-login", "view-order",
  "view-manager", "main-view-toggle", "header-cart-btn", "btn-mode-order",
  "btn-mode-manager", "cart-floating-bar", "dishes-grid", "cart-items-container",
  "cart-modal", "my-orders-modal", "my-orders-list-container", "my-orders-count",
  "menu-my-orders-count", "hero-cart-count", "floating-cart-total", "floating-cart-count",
  "cart-modal-total", "cart-subtotal-val", "cart-discount-row", "cart-discount-label",
  "cart-discount-val", "cart-coupon-input", "cart-coupon-msg", "cart-active-coupon-badge",
  "stamp-track", "stamp-progress-fill", "stamp-progress-text", "stamp-reward-hint",
  "loyalty-badge-text", "special-deal-banner", "loyalty-rewards-card",
  "login-student-name", "login-student-year", "login-student-phone",
  "order-customer-name", "order-customer-year", "order-customer-phone",
  "live-order-badge", "live-orders-container", "toast-container", "about-hero-primary-btn"
];

mockIds.forEach(id => {
  elements[id] = createMockEl(id);
});

global.document = {
  getElementById: (id) => elements[id] || createMockEl(id),
  querySelectorAll: () => [],
  createElement: (tag) => createMockEl('dyn', tag),
  documentElement: { setAttribute: () => {}, removeAttribute: () => {} }
};

global.window = {
  scrollTo: () => {},
  location: { origin: "http://127.0.0.1:5000" },
  confirm: () => true
};

global.localStorage = {
  _store: {},
  getItem: function(k) { return this._store[k] || null; },
  setItem: function(k, v) { this._store[k] = String(v); },
  removeItem: function(k) { delete this._store[k]; }
};

global.sessionStorage = {
  getItem: () => null,
  setItem: () => {},
  removeItem: () => {}
};

// Evaluate app.js
const appJs = fs.readFileSync('js/app.js', 'utf-8');
eval(appJs);

// Login as student
window.currentUser = { role: "student", name: "Srinath", year: "3rd Year" };

// TEST 1: Today's Special Dish verification
console.log("\n[TEST 1] Today's Special Dish in Catalog (₹50)");
const specialDish = window.DISHES.find(d => d.id === "todays_special_combo");
console.log("  Special Dish Name:", specialDish.name);
console.log("  Special Dish Price: ₹" + specialDish.price, "(Expected: 50)");
console.log("  Special Dish Original Price: ₹" + specialDish.originalPrice, "(Expected: 120)");

if (!specialDish || specialDish.price !== 50) {
  throw new Error("Today's special dish is missing or not ₹50!");
}
console.log("✓ TEST 1 PASSED: Today's Special Dish exists at flat ₹50!");

// TEST 2: Add Today's Special to Cart
console.log("\n[TEST 2] Add Today's Special to Cart");
window.addTodaysSpecialToCart();
console.log("  Cart contents:", window.cart);
console.log("  Cart modal total:", elements["cart-modal-total"].textContent, "(Expected: ₹50)");

if (window.cart["todays_special_combo"] !== 1 || elements["cart-modal-total"].textContent !== "₹50") {
  throw new Error("Failed to add Today's Special to cart at ₹50!");
}
console.log("✓ TEST 2 PASSED: Successfully added Today's Special for ₹50 to cart!");

// TEST 3: Apply Coupon SAVITHA30 (Requires min ₹99 order)
console.log("\n[TEST 3] Coupon Validation (SAVITHA30 min order requirement)");
elements["cart-coupon-input"].value = "SAVITHA30";
window.applyCartCoupon();
console.log("  Coupon message for ₹50 order:", elements["cart-coupon-msg"].textContent);
if (!elements["cart-coupon-msg"].textContent.includes("minimum order value of ₹99")) {
  throw new Error("Coupon did not enforce minimum order value!");
}
console.log("✓ TEST 3 PASSED: Enforces minimum order requirement correctly!");

// Add another dish to exceed ₹99 (add veg_biryani @ ₹110 => total ₹160)
console.log("\n[TEST 4] Coupon SAVITHA30 on qualifying order (₹160 -> ₹130)");
window.updateDishQty("veg_biryani", 1);
elements["cart-coupon-input"].value = "SAVITHA30";
window.applyCartCoupon();

console.log("  Subtotal:", elements["cart-subtotal-val"].textContent, "(Expected: ₹160)");
console.log("  Discount:", elements["cart-discount-val"].textContent, "(Expected: -₹30)");
console.log("  Total to Pay:", elements["cart-modal-total"].textContent, "(Expected: ₹130)");

if (elements["cart-modal-total"].textContent !== "₹130" || elements["cart-discount-val"].textContent !== "-₹30") {
  throw new Error("Coupon SAVITHA30 did not calculate ₹30 discount properly!");
}
console.log("✓ TEST 4 PASSED: Coupon SAVITHA30 discounted ₹30 cleanly!");

// TEST 5: Loyalty 10th Order Free Food (FREE10)
console.log("\n[TEST 5] Loyalty 10th Order Free Food Stamp Card & Coupon (FREE10)");
window.simulateOrderStreak(); // Sets streak to 10
window.renderLoyaltyStampCard();

console.log("  Stamp track HTML contains 10th stamp:", elements["stamp-track"].innerHTML.includes("reward-tenth"));
console.log("  Loyalty badge text:", elements["loyalty-badge-text"].textContent);
console.log("  Reward hint:", elements["stamp-reward-hint"].textContent);

// Now apply FREE10
window.applyQuickCoupon("FREE10");
window.openCartModal();

console.log("  Subtotal:", elements["cart-subtotal-val"].textContent, "(Expected: ₹160)");
console.log("  Discount (FREE10 up to ₹150):", elements["cart-discount-val"].textContent, "(Expected: -₹150)");
console.log("  Total to Pay after 100% Free Food up to ₹150:", elements["cart-modal-total"].textContent, "(Expected: ₹10)");

if (elements["cart-discount-val"].textContent !== "-₹150" || elements["cart-modal-total"].textContent !== "₹10") {
  throw new Error("10th Order Free coupon calculation error!");
}
console.log("✓ TEST 5 PASSED: 10th Order Free coupon applies 100% discount up to ₹150!");

// TEST 6: Place order and verify streak progression
console.log("\n[TEST 6] Place Order with Loyalty Coupon");
elements["order-customer-name"].value = "Srinath";
window.placeOrderAndGenerateToken();

console.log("  My Orders count:", window.myOrders.length);
console.log("  Last order coupon used:", window.myOrders[0].coupon, "(Expected: FREE10)");
console.log("  Last order total charged: ₹" + window.myOrders[0].total, "(Expected: 10)");

if (window.myOrders[0].coupon !== "FREE10" || window.myOrders[0].total !== 10) {
  throw new Error("Order was not saved with coupon details!");
}
console.log("✓ TEST 6 PASSED: Order placed with 10th free meal coupon and recorded in My Orders!");

console.log("\n=========================================================================");
console.log("ALL 6 TESTS FOR TODAY'S SPECIAL & LOYALTY COUPON CARDS PASSED WITH 0 ERRORS!");
console.log("=========================================================================");
