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
  'view-about', 'view-login', 'view-order', 'view-manager', 'cart-floating-bar',
  'user-auth-slot', 'theme-name', 'theme-icon', 'dishes-grid', 'backend-status',
  'toast-container', 'history-table-body', 'cart-counter', 'cart-total-pill',
  'cart-items-container', 'cart-items-list', 'live-order-badge', 'live-orders-container',
  'login-tab-student', 'login-tab-worker', 'login-panel-student', 'login-panel-worker',
  'login-student-name', 'login-student-year', 'login-student-phone', 'login-worker-password',
  'order-customer-name', 'order-customer-year', 'order-customer-phone',
  'cart-modal', 'token-modal', 'token-order-message', 'token-number', 'token-total-paid',
  'token-items-list', 'bill-subtotal', 'bill-total', 'cart-modal-total',
  'cart-bar-items-val', 'cart-bar-total-val', 'floating-cart-count', 'floating-cart-total',
  'hero-cart-count', 'btn-hero-order-now', 'about-hero-primary-btn', 'about-hero-secondary-btn',
  'about-bottom-primary-btn', 'about-bottom-secondary-btn', 'btn-top-login',
  'active-kitchen-pwd-badge', 'btn-toggle-badge-pwd', 'about-website', 'feedback-section',
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

global.fetch = async () => ({ ok: true, json: async () => ({ status: 'healthy', orders: [] }) });

// Load app.js
const appCode = fs.readFileSync('js/app.js', 'utf8');
eval(appCode);
global._domLoaded();

console.log('=== TEST 1: Opening Website - Only ONE Login Way ===');
console.log('Active view:', elements['view-about'].style.display === 'block' ? 'view-about' : 'other');
if (elements['view-about'].style.display !== 'block') throw new Error('view-about should be active on startup');

// Verify that hero primary button goes to food menu & order, NOT a duplicate login button!
console.log('Hero primary button text:', elements['about-hero-primary-btn'].innerHTML);
if (elements['about-hero-primary-btn'].innerHTML.includes('Login')) {
  throw new Error('Hero button should not be a duplicate login button!');
}
if (!elements['about-hero-primary-btn'].innerHTML.includes('Menu')) {
  throw new Error('Hero button should invite viewing menu & ordering');
}

// Verify that bottom CTA goes to menu, NOT a duplicate login button!
console.log('Bottom CTA button text:', elements['about-bottom-primary-btn'].innerHTML);
if (elements['about-bottom-primary-btn'].innerHTML.includes('Login')) {
  throw new Error('Bottom CTA button should not be a duplicate login button!');
}
console.log('PASSED: Only ONE login way exists in top navigation bar!');

console.log('\n=== TEST 2: Login Screen - No Example Names or 10 Digits ===');
window.navigateToSection('login');
console.log('Login view display:', elements['view-login'].style.display);
if (elements['view-login'].style.display !== 'flex') throw new Error('view-login not flex on login navigation!');

// Perform student login with user-provided name
elements['login-student-name'].value = 'Srinath';
elements['login-student-year'].value = '3rd Year';
elements['login-student-phone'].value = ''; // No phone entered

window.handlePortalStudentLogin();

console.log('Current user after login:', window.currentUser);
if (window.currentUser.name !== 'Srinath') throw new Error('User name should be Srinath, not ' + window.currentUser.name);
if (window.currentUser.phone !== '') throw new Error('Phone should be empty, not ' + window.currentUser.phone);
console.log('PASSED: User logged in without fake example names or fake 10-digit numbers!');

console.log('\n=== TEST 3: Student Menu - Order Now Option on Selected Items ===');
console.log('Order view display:', elements['view-order'].style.display);
console.log('Dishes grid rendered:', elements['dishes-grid'].innerHTML.length > 0);
if (elements['view-order'].style.display !== 'block') throw new Error('view-order not visible');
if (!elements['dishes-grid'].innerHTML.includes('Veg Biryani')) throw new Error('Dishes not rendered in menu');

// Add item to cart
window.updateDishQty('veg_biryani', 1);

// Verify that the dish card now contains an "Order Now" button
console.log('Dish card contains Order Now when qty > 0:', elements['dishes-grid'].innerHTML.includes('btn-order-now-selected'));
if (!elements['dishes-grid'].innerHTML.includes('btn-order-now-selected')) {
  throw new Error('Dish card does NOT have an Order Now button when item is selected!');
}

// Verify that floating cart bar is shown with Order Now
console.log('Floating cart bar has show class:', elements['cart-floating-bar'].classList.contains('show'));
console.log('Floating cart total:', elements['floating-cart-total'].textContent);
console.log('Floating cart count:', elements['floating-cart-count'].textContent);
if (!elements['cart-floating-bar'].classList.contains('show')) {
  throw new Error('Floating Order Now bar should be visible when items are selected');
}
if (elements['floating-cart-total'].textContent !== '₹110') {
  throw new Error('Total price should be ₹110');
}
console.log('PASSED: Order Now option is prominently available when items are selected!');

console.log('\n=== TEST 4: Open Cart Modal & Confirm Order Without Dummy Data ===');
window.openCartModal();
console.log('Cart modal has show class:', elements['cart-modal'].classList.contains('show'));
if (!elements['cart-modal'].classList.contains('show')) throw new Error('Cart modal not opened');

console.log('Order customer name in modal:', elements['order-customer-name'].value);
console.log('Order customer phone in modal:', elements['order-customer-phone'].value);
if (elements['order-customer-name'].value !== 'Srinath') {
  throw new Error('Customer name should be Srinath, got: ' + elements['order-customer-name'].value);
}
if (elements['order-customer-phone'].value === '9876543210') {
  throw new Error('Fake phone number 9876543210 should NOT be present in cart modal!');
}

// Place order and generate token
window.placeOrderAndGenerateToken();

console.log('Token modal has show class:', elements['token-modal'].classList.contains('show'));
console.log('Generated token:', elements['token-number'].textContent);
console.log('Token message:', elements['token-order-message'].innerHTML);

if (!elements['token-modal'].classList.contains('show')) throw new Error('Token modal not shown');
if (elements['token-order-message'].innerHTML.includes('9876543210')) {
  throw new Error('Token order message must not contain fake phone 9876543210!');
}

console.log('PASSED: Order successfully placed and token generated without any dummy data!');

console.log('\n=== TEST 5: Live Orders Queue in Kitchen ===');
console.log('Live orders count:', window.liveOrders.length);
if (window.liveOrders.length !== 1) throw new Error('There should be exactly 1 live order (the one just placed)');
if (window.liveOrders[0].customerName !== 'Srinath') throw new Error('Live order customer name should be Srinath');
console.log('Live order detail:', window.liveOrders[0].customerName, window.liveOrders[0].token);

console.log('\nALL TESTS PASSED WITH 100% SUCCESS! 🚀');
process.exit(0);
