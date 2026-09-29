const fs = require('fs');
const assert = require('assert');

// 1. Mock DOM
const elements = {};
function createMockElement(id, tag = 'div') {
  const el = {
    id,
    tagName: tag.toUpperCase(),
    style: {},
    classList: {
      classes: new Set(),
      add: (c) => el.classList.classes.add(c),
      remove: (c) => el.classList.classes.delete(c),
      contains: (c) => el.classList.classes.has(c)
    },
    dataset: {},
    value: '',
    innerHTML: '',
    textContent: '',
    focus: () => {},
    appendChild: () => {},
    remove: () => {},
    addEventListener: () => {},
    setAttribute: () => {},
    removeAttribute: () => {}
  };
  elements[id] = el;
  return el;
}

const neededIds = [
  'main-view-toggle', 'header-cart-btn', 'header-token-btn', 'header-token-label',
  'btn-mode-order', 'btn-mode-manager',
  'view-login', 'view-order', 'view-manager', 'cart-floating-bar',
  'user-auth-slot', 'theme-name', 'theme-icon', 'dishes-grid', 'backend-status',
  'toast-container', 'history-table-body', 'cart-counter', 'cart-total-pill',
  'cart-items-list', 'live-order-badge', 'live-orders-container',
  'login-tab-student', 'login-tab-worker', 'login-panel-student', 'login-panel-worker',
  'login-student-name', 'login-student-year', 'login-student-phone', 'login-worker-password',
  'order-customer-name', 'order-customer-year', 'order-customer-phone',
  'cart-modal', 'token-modal', 'token-order-message', 'token-number',
  'token-student-name', 'token-student-year', 'token-student-phone', 'token-items-list', 'token-total-paid',
  'bill-subtotal', 'bill-total', 'cart-bar-items-val', 'cart-bar-total-val',
  'active-kitchen-pwd-badge', 'btn-toggle-badge-pwd', 'btn-cancel-token-order',
  'active-order-banner', 'banner-token-pill', 'banner-status-pill', 'banner-order-desc',
  'mgr-token-search-input', 'daily-plan-board', 'kitchen-result-card', 'res-mgr-sub',
  'res-mgr-cook', 'res-mgr-demand', 'res-mgr-buf', 'res-mgr-reason',
  'mgr_weather', 'mgr_event', 'mgr_day', 'mgr_food_item', 'mgr_prev_day', 'mgr_prev_week'
];

neededIds.forEach(id => createMockElement(id));

const storage = {};
global.localStorage = {
  getItem: (k) => storage[k] || null,
  setItem: (k, v) => { storage[k] = String(v); },
  removeItem: (k) => { delete storage[k]; }
};

global.window = {
  location: { origin: 'http://127.0.0.1:5000' },
  scrollTo: () => {},
  addEventListener: () => {}
};

global.document = {
  getElementById: (id) => elements[id] || createMockElement(id),
  querySelectorAll: (sel) => [],
  documentElement: { setAttribute: () => {}, removeAttribute: () => {} },
  createElement: (tag) => createMockElement('dyn_' + Math.random(), tag),
  addEventListener: (evt, cb) => {
    if (evt === 'DOMContentLoaded') global._domLoaded = cb;
  }
};

global.confirm = () => true;

const apiCalls = [];
global.fetch = async (url, opts) => {
  apiCalls.push({ url, opts });
  if (url.includes('/api/orders') && opts && opts.method === 'POST') {
    return { ok: true, json: async () => ({ status: 'success', order: JSON.parse(opts.body) }) };
  }
  return { ok: true, json: async () => ({ status: 'healthy', orders: [] }) };
};

// 2. Load model_engine.js
const modelEngineCode = fs.readFileSync('js/model_engine.js', 'utf8');
eval(modelEngineCode);

// 3. Load app.js
const appCode = fs.readFileSync('js/app.js', 'utf8');
eval(appCode);
global._domLoaded();

console.log('Testing Menu Catalog Size...');
assert.strictEqual(window.DISHES.length, 32, `Expected 32 dishes, found ${window.DISHES.length}`);
console.log(`✅ DISHES count is exactly ${window.DISHES.length}`);

console.log('Testing Categories...');
const cats = new Set(window.DISHES.map(d => d.category));
assert.ok(cats.has('breakfast'), 'Has breakfast');
assert.ok(cats.has('lunch'), 'Has lunch');
assert.ok(cats.has('snacks'), 'Has snacks');
assert.ok(cats.has('quick'), 'Has quick');
console.log(`✅ All 4 food categories present: ${Array.from(cats).join(', ')}`);

console.log('Testing 1-Click Instant Order Now & Token Generation...');
window.quickOrderDish('masala_dosa');

const placedToken = elements['token-number'].textContent;
assert.ok(placedToken.startsWith('#'), 'Token generated with #');
assert.strictEqual(elements['token-modal'].classList.contains('show'), true, 'Token modal is open');
assert.strictEqual(elements['active-order-banner'].style.display, 'flex', 'Active order banner is visible');
assert.strictEqual(elements['header-token-btn'].style.display, 'inline-flex', 'Header token button is visible');
console.log(`✅ 1-Click Order confirmed! Token generated: ${placedToken}`);

console.log('Testing Live Orders in Kitchen...');
assert.ok(window.liveOrders.length >= 1, 'Order registered in kitchen queue');
const kitchenOrder = window.liveOrders[0];
assert.strictEqual(kitchenOrder.token, placedToken, 'Kitchen queue matches token');
console.log(`✅ Kitchen Staff received Order ${kitchenOrder.token} with ${kitchenOrder.items[0].name}`);

console.log('Testing Kitchen Staff Token Search & Confirmation...');
elements['mgr-token-search-input'].value = placedToken;
window.confirmTokenInKitchen();

const orderAfterDeliver = window.liveOrders.find(o => o.token === placedToken);
assert.strictEqual(orderAfterDeliver, undefined, 'Order marked handed over/completed');
console.log(`✅ Token ${placedToken} successfully confirmed & handed over in kitchen staff!`);

console.log('Testing 1-Click Order & Cancellation Flow...');
window.quickOrderDish('chicken_biryani');
const secondToken = elements['token-number'].textContent;
console.log(`Placed second order: ${secondToken}`);
assert.ok(window.liveOrders.some(o => o.token === secondToken), 'Second order in queue');

// Now cancel it
window.cancelCurrentTokenOrder();
assert.ok(!window.liveOrders.some(o => o.token === secondToken), 'Second order cancelled and removed from queue');
assert.strictEqual(elements['active-order-banner'].style.display, 'none', 'Banner hidden after cancellation');
assert.strictEqual(elements['header-token-btn'].style.display, 'none', 'Header token button hidden after cancellation');
console.log(`✅ Order ${secondToken} successfully cancelled and completely cleared!`);

console.log('Testing Client ML Predictions across all dishes...');
const allItems = window.FoodMLClientEngine.getAllItems();
assert.ok(allItems.length >= 24, `Expected full metadata items, found ${allItems.length}`);
allItems.forEach(item => {
  const defaults = window.FoodMLClientEngine.getItemDefaults(item);
  const pred = window.FoodMLClientEngine.predict({
    food_item: item,
    day_of_week: 'Tuesday',
    weather: 'Sunny',
    special_event: 'None'
  });
  assert.ok(pred.predicted_quantity > 0, `Prediction positive for ${item}`);
  assert.ok(pred.recommended_portions >= pred.predicted_quantity, `Recommended portions >= demand for ${item}`);
});
console.log(`✅ Client ML Prediction tested and verified for all ${allItems.length} menu items!`);

console.log('\n========================================');
console.log('ALL COMPLETE SUITE TESTS PASSED 100%! 🎉');
console.log('========================================');
