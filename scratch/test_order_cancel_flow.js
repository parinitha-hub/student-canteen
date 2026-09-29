const fs = require('fs');

// Mock DOM
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
  'main-view-toggle', 'header-cart-btn', 'btn-mode-order', 'btn-mode-manager',
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
  'active-order-banner', 'banner-token-pill', 'banner-status-pill', 'banner-order-desc'
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

global.confirm = () => true; // Always confirm in automated test

const apiCalls = [];
global.fetch = async (url, opts) => {
  apiCalls.push({ url, opts });
  if (url.includes('/api/orders') && opts && opts.method === 'POST') {
    return { ok: true, json: async () => ({ status: 'success', order: JSON.parse(opts.body) }) };
  }
  return { ok: true, json: async () => ({ status: 'healthy', orders: [] }) };
};

// Load app.js
const appCode = fs.readFileSync('js/app.js', 'utf8');
eval(appCode);
global._domLoaded();

console.log('=== TEST 1: Student Login and Adding Items ===');
elements['login-student-name'].value = 'Srinath';
elements['login-student-year'].value = '3rd Year';
elements['login-student-phone'].value = '9876543210';
window.handlePortalStudentLogin();

// Add items to cart
window.updateDishQty('veg_biryani', 1);
window.updateDishQty('cold_coffee', 2);
window.openCartModal();

console.log('Cart subtotal:', elements['bill-subtotal'].textContent);
if (!elements['bill-subtotal'].textContent.includes('230')) {
  throw new Error('FAIL: Cart total mismatch (expected 110 + 2*60 = 230)');
}
console.log('PASSED: Cart contains ordered items accurately.');

console.log('\n=== TEST 2: Place Order & Verify Confirmation Modal ===');
window.placeOrderAndGenerateToken();

console.log('Token Modal show:', elements['token-modal'].classList.contains('show'));
const tokenNum = elements['token-number'].textContent;
console.log('Generated Token:', tokenNum);
console.log('Confirmation Items List:', elements['token-items-list'].innerHTML);
console.log('Total Paid in Confirmation:', elements['token-total-paid'].textContent);

if (!elements['token-modal'].classList.contains('show')) {
  throw new Error('FAIL: Confirmation modal was not displayed!');
}
if (!elements['token-items-list'].innerHTML.includes('Veg Biryani') || !elements['token-items-list'].innerHTML.includes('Cold Coffee')) {
  throw new Error('FAIL: Ordered items missing from confirmation modal!');
}
if (elements['token-total-paid'].textContent !== '₹230') {
  throw new Error('FAIL: Total in confirmation does not match order amount!');
}
console.log('PASSED: Ordered items and token are clearly visible in Confirmation Modal.');

console.log('\n=== TEST 3: Check Active Order Banner in Menu ===');
console.log('Active Order Banner display:', elements['active-order-banner'].style.display);
console.log('Banner Token:', elements['banner-token-pill'].textContent);
console.log('Banner Description:', elements['banner-order-desc'].textContent);

if (elements['active-order-banner'].style.display !== 'flex') {
  throw new Error('FAIL: Active order banner not visible on food menu!');
}
if (elements['banner-token-pill'].textContent !== tokenNum) {
  throw new Error('FAIL: Banner token does not match placed order token!');
}
console.log('PASSED: Active order banner keeps order visible in food menu.');

console.log('\n=== TEST 4: Kitchen Staff Sees Placed Order ===');
window.renderLiveOrders();
const kitchenHtml = elements['live-orders-container'].innerHTML;
console.log('Kitchen live orders contains token:', kitchenHtml.includes(tokenNum));
console.log('Kitchen live orders contains Veg Biryani:', kitchenHtml.includes('Veg Biryani'));
console.log('Kitchen live orders contains Cold Coffee:', kitchenHtml.includes('Cold Coffee'));
console.log('Kitchen order card has Cancel button:', kitchenHtml.includes('Cancel Order'));

if (!kitchenHtml.includes(tokenNum) || !kitchenHtml.includes('Veg Biryani') || !kitchenHtml.includes('Cold Coffee')) {
  throw new Error('FAIL: Kitchen staff cannot see the ordered items!');
}
if (!kitchenHtml.includes('Cancel Order')) {
  throw new Error('FAIL: Kitchen staff card missing Cancel Order button!');
}
console.log('PASSED: Kitchen staff immediately receives and displays the order with all items.');

console.log('\n=== TEST 5: Cancel Order ("if i cancle it should go") ===');
window.cancelCurrentTokenOrder();

console.log('After cancel:');
console.log('Token Modal show:', elements['token-modal'].classList.contains('show'));
console.log('Active Order Banner display:', elements['active-order-banner'].style.display);

window.renderLiveOrders();
const kitchenHtmlAfterCancel = elements['live-orders-container'].innerHTML;
console.log('Kitchen live orders contains cancelled token:', kitchenHtmlAfterCancel.includes(tokenNum));

if (elements['token-modal'].classList.contains('show')) {
  throw new Error('FAIL: Token modal still visible after cancel!');
}
if (elements['active-order-banner'].style.display !== 'none') {
  throw new Error('FAIL: Active order banner still visible after cancel!');
}
if (kitchenHtmlAfterCancel.includes(tokenNum)) {
  throw new Error('FAIL: Cancelled order did NOT go away from kitchen live orders!');
}
console.log('PASSED: Cancelled order went away cleanly from confirmation, banner, and kitchen staff!');

console.log('\n=== TEST 6: Kitchen Staff Direct Order Cancellation ===');
// Place another order
window.updateDishQty('chicken_biryani', 1);
window.placeOrderAndGenerateToken();
const token2 = elements['token-number'].textContent;
window.renderLiveOrders();
if (!elements['live-orders-container'].innerHTML.includes(token2)) {
  throw new Error('FAIL: Second order not in kitchen queue!');
}
console.log('Order 2 placed:', token2);

// Kitchen cancels it
window.cancelOrder(token2);
window.renderLiveOrders();
if (elements['live-orders-container'].innerHTML.includes(token2)) {
  throw new Error('FAIL: Kitchen direct cancellation failed to remove order!');
}
console.log('PASSED: Kitchen staff direct cancellation removes order instantly.');

console.log('\nALL TESTS PASSED WITH 100% SUCCESS! 🚀');
process.exit(0);
