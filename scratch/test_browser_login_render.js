const fs = require('fs');

// Create Mock DOM
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
  'cart-modal', 'token-modal', 'token-order-message', 'token-number-display',
  'bill-subtotal', 'bill-total', 'cart-bar-items-val', 'cart-bar-total-val',
  'active-kitchen-pwd-badge', 'btn-toggle-badge-pwd'
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
  scrollTo: () => {}
};

global.document = {
  getElementById: (id) => elements[id] || createMockElement(id),
  querySelectorAll: (selector) => [],
  documentElement: {
    setAttribute: () => {},
    removeAttribute: () => {}
  },
  createElement: (tag) => createMockElement('dyn_' + Math.random(), tag),
  addEventListener: (evt, cb) => {
    if (evt === 'DOMContentLoaded') {
      global._domLoaded = cb;
    }
  }
};

global.fetch = async () => ({ ok: true, json: async () => ({ status: 'healthy' }) });

// Load app.js
const appCode = fs.readFileSync('js/app.js', 'utf8');
eval(appCode);
global._domLoaded();

console.log('=== TEST 1: Initial State ===');
console.log('Login view display:', elements['view-login'].style.display);
if (elements['view-login'].style.display !== 'flex') throw new Error('view-login not flex on start!');
console.log('PASSED: Login view is active on start.');

console.log('\n=== TEST 2: Student Login with Year & Phone ===');
elements['login-student-name'].value = 'Priya Patel';
elements['login-student-year'].value = '2nd Year';
elements['login-student-phone'].value = '9876543210';

window.handlePortalStudentLogin();

console.log('Order view display:', elements['view-order'].style.display);
console.log('Dishes grid length:', elements['dishes-grid'].innerHTML.length);
if (elements['view-order'].style.display !== 'block') throw new Error('view-order not visible after login!');
if (elements['dishes-grid'].innerHTML.length === 0) throw new Error('dishes-grid is empty after login!');
console.log('PASSED: Food menu is fully rendered and visible after login!');

console.log('\n=== TEST 3: Add to Cart and Check Pre-filled Data ===');
window.updateDishQty('veg_biryani', 2);
console.log('Cart counter:', elements['cart-counter'].textContent);
if (String(elements['cart-counter'].textContent) !== '2') throw new Error('Cart counter did not update!');

window.openCartModal();
console.log('Cart customer name:', elements['order-customer-name'].value);
console.log('Cart customer year:', elements['order-customer-year'].value);
console.log('Cart customer phone:', elements['order-customer-phone'].value);

if (elements['order-customer-name'].value !== 'Priya Patel') throw new Error('Name not pre-filled in cart!');
if (elements['order-customer-year'].value !== '2nd Year') throw new Error('Year not pre-filled in cart!');
if (elements['order-customer-phone'].value !== '9876543210') throw new Error('Phone not pre-filled in cart!');
console.log('PASSED: Student details accurately populated in checkout cart.');

console.log('\n=== TEST 4: Confirm Order & Check Kitchen Dashboard ===');
window.placeOrderAndGenerateToken();
console.log('Order token modal show:', elements['token-modal'].classList.contains('show'));
if (!elements['token-modal'].classList.contains('show')) throw new Error('Token modal was not displayed!');
console.log('PASSED: Order placed successfully and token generated!');

console.log('\n=== TEST 5: Kitchen Staff Login & Incoming Order Details ===');
elements['login-worker-password'].value = 'savitha123';
window.handlePortalWorkerLogin();
console.log('Kitchen manager view display:', elements['view-manager'].style.display);
if (elements['view-manager'].style.display !== 'block') throw new Error('Kitchen view not displayed!');

console.log('Live orders container:', elements['live-orders-container'].innerHTML);
const hasStudentName = elements['live-orders-container'].innerHTML.includes('Priya Patel');
const hasYear = elements['live-orders-container'].innerHTML.includes('2nd Year');
const hasPhone = elements['live-orders-container'].innerHTML.includes('9876543210');
const hasCallBtn = elements['live-orders-container'].innerHTML.includes('tel:9876543210');
const hasWaBtn = elements['live-orders-container'].innerHTML.includes('wa.me/919876543210');

console.log('Order card contains student name:', hasStudentName);
console.log('Order card contains year/class:', hasYear);
console.log('Order card contains phone:', hasPhone);
console.log('Order card contains call button:', hasCallBtn);
console.log('Order card contains WhatsApp button:', hasWaBtn);

if (!hasStudentName || !hasYear || !hasPhone || !hasCallBtn || !hasWaBtn) {
  throw new Error('Kitchen order card missing student contact information!');
}

console.log('\nALL 5 END-TO-END FLOW TESTS COMPLETED WITH 100% SUCCESS! 🚀');
process.exit(0);
