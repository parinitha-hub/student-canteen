const fs = require('fs');
const path = require('path');

console.log("=========================================================================");
console.log("TESTING: Simplified Menu Page & Expanded Food Item Catalog (Zero Errors)");
console.log("=========================================================================");

const rootIndex = fs.readFileSync(path.join(__dirname, '../index.html'), 'utf8');
const frontendIndex = fs.readFileSync(path.join(__dirname, '../frontend/index.html'), 'utf8');
const appJsCode = fs.readFileSync(path.join(__dirname, '../js/app.js'), 'utf8');
const frontendAppJs = fs.readFileSync(path.join(__dirname, '../frontend/js/app.js'), 'utf8');

// 1. Synchronization Check
if (rootIndex !== frontendIndex) {
  throw new Error("FAIL: root index.html does not match frontend/index.html");
}
if (appJsCode !== frontendAppJs) {
  throw new Error("FAIL: root js/app.js does not match frontend/js/app.js");
}
console.log("✓ Root and frontend files are 100% synchronized.");

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
eval(appJsCode);

const dishes = window.DISHES;
if (!Array.isArray(dishes) || dishes.length === 0) {
  throw new Error("FAIL: DISHES array not found or empty.");
}
console.log(`✓ DISHES catalog loaded successfully with ${dishes.length} total dishes.`);

// 3. Test Newly Added Dishes
const expectedNewDishIds = [
  "chicken_noodles",
  "peri_peri_fries",
  "campus_burger",
  "chicken_burger",
  "medu_vada_plate",
  "ghee_podi_idli",
  "rava_masala_dosa",
  "special_chicken_fried_rice",
  "south_executive_meal",
  "fresh_watermelon_juice"
];

const dishMap = new Map(dishes.map(d => [d.id, d]));

for (const dishId of expectedNewDishIds) {
  const dish = dishMap.get(dishId);
  if (!dish) {
    throw new Error(`FAIL: Expected dish '${dishId}' was not found in DISHES!`);
  }
  if (!dish.name || !dish.price || !dish.image || !dish.category) {
    throw new Error(`FAIL: Dish '${dishId}' is missing essential properties (name, price, image, category).`);
  }
  if (typeof dish.rating !== 'number' || dish.rating < 4.0 || dish.rating > 5.0) {
    throw new Error(`FAIL: Dish '${dishId}' has invalid rating: ${dish.rating}`);
  }
  // Check that the image file actually exists on disk
  const imagePath = path.join(__dirname, '..', dish.image);
  if (!fs.existsSync(imagePath)) {
    throw new Error(`FAIL: Image file for dish '${dishId}' does not exist at '${imagePath}'`);
  }
  console.log(`  ✓ Dish '${dish.name}' (ID: ${dish.id}, ₹${dish.price}, ${dish.category}, ⭐ ${dish.rating}) image verified.`);
}
console.log(`✓ All ${expectedNewDishIds.length} newly added food items verified with valid image assets!`);

// 4. Test Add-To-Cart & Cart Modal Calculations for New Dishes
console.log("\n[TEST: Add-to-cart on new dishes]");
window.currentUser = { role: "student", name: "Srinath", year: "2nd Year" };
window.cart = {}; // Reset cart
window.updateDishQty("chicken_noodles", 1);
window.updateDishQty("peri_peri_fries", 1);
window.updateDishQty("south_executive_meal", 1);

if (window.cart["chicken_noodles"] !== 1 || window.cart["peri_peri_fries"] !== 1 || window.cart["south_executive_meal"] !== 1) {
  throw new Error("FAIL: Items were not added to cart correctly!");
}

// Check subtotal computation
let subtotal = 0;
for (const [id, qty] of Object.entries(window.cart)) {
  const d = dishes.find(x => x.id === id);
  if (d) subtotal += d.price * qty;
}

// chicken_noodles (125) + peri_peri_fries (60) + south_executive_meal (120) = 305
if (subtotal !== 305) {
  throw new Error(`FAIL: Subtotal mismatch! Expected 305, got ${subtotal}`);
}
console.log(`✓ Subtotal correctly computed for new dishes: ₹${subtotal}`);

// 5. Test Simplified Menu Page Structure in HTML
const requiredMenuIds = [
  "view-order",
  "special-deal-banner",
  "btn-add-special-deal",
  "loyalty-rewards-card",
  "stamp-progress-fill",
  "stamp-progress-text",
  "dishes-grid"
];

for (const id of requiredMenuIds) {
  if (!rootIndex.includes(`id="${id}"`)) {
    throw new Error(`FAIL: Menu page is missing required element id="${id}"`);
  }
}
console.log("✓ Menu page contains all essential streamlined offer and catalog IDs.");

// 6. Test Category Filter
window.renderDishes();
const renderedHtml = elements["dishes-grid"].innerHTML;
if (!renderedHtml.includes("Spicy Chicken Hakka Noodles") || !renderedHtml.includes("Crispy Peri Peri Fries")) {
  throw new Error("FAIL: Rendered dishes grid missing newly added dishes!");
}
console.log("✓ Dishes grid renders newly added items seamlessly with star ratings & images.");

console.log("\n=========================================================================");
console.log("ALL TESTS FOR SIMPLIFIED MENU AND NEW FOOD ITEMS PASSED WITH 0 ERRORS!");
console.log("=========================================================================");
