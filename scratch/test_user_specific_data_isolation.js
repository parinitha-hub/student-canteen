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
  'login-student-username', 'login-student-password', 'login-student-name',
  'login-student-year', 'login-student-phone', 'login-worker-password',
  'register-student-name', 'register-student-username', 'register-student-year',
  'register-student-phone', 'register-student-password',
  'subtab-auth-signin', 'subtab-auth-register', 'student-signin-form', 'student-register-form',
  'order-customer-name', 'order-customer-year', 'order-customer-phone',
  'cart-modal', 'token-modal', 'token-order-message', 'token-number', 'token-total-paid',
  'token-items-list', 'bill-subtotal', 'bill-total', 'cart-modal-total', 'cart-subtotal-val',
  'cart-discount-row', 'cart-discount-label', 'cart-discount-val', 'cart-coupon-input',
  'cart-coupon-msg', 'cart-active-coupon-badge', 'stamp-track', 'stamp-progress-fill',
  'stamp-progress-text', 'stamp-reward-hint', 'loyalty-badge-text', 'my-orders-modal',
  'my-orders-list-container', 'menu-my-orders-count', 'my-orders-count',
  'cart-bar-items-val', 'cart-bar-total-val', 'floating-cart-count', 'floating-cart-total',
  'hero-cart-count', 'btn-hero-order-now', 'about-hero-primary-btn', 'about-hero-secondary-btn',
  'about-bottom-primary-btn', 'about-bottom-secondary-btn', 'btn-top-login',
  'profile-modal', 'profile-modal-body', 'cancel-order-modal', 'cancel-modal-content',
  'subtab-orders-btn', 'subtab-inventory-btn', 'subtab-calc-btn', 'subtab-pnl-btn', 'subtab-pwd-btn',
  'manager-pane-orders', 'manager-pane-inventory', 'manager-pane-calc', 'manager-pane-pnl', 'manager-pane-pwd',
  'inventory-table-body', 'inv-stat-total', 'inv-stat-instock', 'inv-stat-lowstock', 'inv-stat-soldout',
  'inv-warning-banner', 'inv-warning-text', 'inv-low-stock-badge', 'inv-search-input'
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

console.log('====================================================================');
console.log('TESTING USER-SPECIFIC LOGIN, CREDENTIALS & STRICT DATA ISOLATION');
console.log('====================================================================\n');

// -----------------------------------------------------------------------------
// TEST 1: Credentials Verification (Sign In)
// -----------------------------------------------------------------------------
console.log('[TEST 1] Credential Verification on Sign In');
// Invalid password attempt
elements['login-student-username'].value = 'SAV101';
elements['login-student-password'].value = 'wrongpassword';
let loginRes = window.handleStudentSignIn();
if (window.currentUser) {
  throw new Error('User should NOT be logged in with wrong password!');
}
console.log('  ✓ Incorrect password rejected cleanly.');

// Correct credentials attempt for Srinath (SAV101)
elements['login-student-password'].value = 'pass123';
window.handleStudentSignIn();
if (!window.currentUser || window.currentUser.username !== 'SAV101') {
  throw new Error('Valid login failed for SAV101!');
}
console.log(`  ✓ Successfully signed in as ${window.currentUser.name} (${window.currentUser.username}) - ${window.currentUser.year}`);
console.log('✓ TEST 1 PASSED: Credentials authentication verified!\n');

// -----------------------------------------------------------------------------
// TEST 2: Account Registration for a New Student
// -----------------------------------------------------------------------------
console.log('[TEST 2] New Student Account Registration');
elements['register-student-name'].value = 'Kavya S';
elements['register-student-username'].value = 'SAV105';
elements['register-student-year'].value = '2nd Year AI & DS';
elements['register-student-phone'].value = '9876543299';
elements['register-student-password'].value = 'kavyaPass';

window.handleStudentRegister();
if (!window.currentUser || window.currentUser.username !== 'SAV105') {
  throw new Error('Registration failed for new account SAV105!');
}
console.log(`  ✓ Successfully registered and logged in as ${window.currentUser.name} (${window.currentUser.username})`);

// Verify account is stored in account database
const accounts = window.getAccounts();
const found = accounts.find(a => a.username === 'SAV105');
if (!found || found.name !== 'Kavya S') {
  throw new Error('New account was not persisted to account database!');
}
console.log('  ✓ Account persisted in accounts store.');
console.log('✓ TEST 2 PASSED: Student account registration works perfectly!\n');

// -----------------------------------------------------------------------------
// TEST 3: User Data Isolation Between Student A and Student B
// -----------------------------------------------------------------------------
console.log('[TEST 3] Strict Data Isolation (Orders, Cart, Streak, Profile)');

// Step A: Login as Student A (Srinath - SAV101)
console.log('  Logging in as Student A (Srinath - SAV101)...');
window.fillDemoStudent('SAV101', 'pass123');
window.handleStudentSignIn();
console.log('  Active User:', window.currentUser.name);

// Srinath adds Veg Biryani to cart
window.updateDishQty('veg_biryani', 2);
console.log('  Srinath cart:', window.cart);
if (window.cart['veg_biryani'] !== 2) throw new Error('Srinath cart addition failed');

// Srinath places Order 1
window.placeOrderAndGenerateToken();
const srinathOrderToken = window.myOrders[0].token;
console.log(`  Srinath placed Order: ${srinathOrderToken}, My Orders count: ${window.myOrders.length}`);
if (window.myOrders.length !== 1) throw new Error('Srinath should have 1 order');

// Srinath adds a dessert to cart that remains unplaced
window.updateDishQty('samosa_chai', 1);
console.log('  Srinath cart currently has:', window.cart);

// Step B: Srinath logs out
console.log('  Srinath logs out...');
window.logoutUser();
if (window.currentUser !== null) throw new Error('currentUser should be null after logout');
if (Object.keys(window.cart).length !== 0) throw new Error('cart should be empty in memory after logout');
if (window.myOrders.length !== 0) throw new Error('myOrders should be empty in memory after logout');
console.log('  ✓ Memory session cleared after logout.');

// Step C: Student B (Divya - SAV102) logs in
console.log('\n  Logging in as Student B (Divya - SAV102)...');
window.fillDemoStudent('SAV102', 'pass123');
window.handleStudentSignIn();
console.log('  Active User:', window.currentUser.name);

// VERIFY: Divya MUST NOT see Srinath\'s cart!
console.log('  Divya cart contents:', window.cart);
if (window.cart['samosa_chai'] || window.cart['veg_biryani']) {
  throw new Error('SECURITY VIOLATION: Srinath\'s cart items leaked into Divya\'s cart!');
}
console.log('  ✓ Verified: Srinath\'s cart is NOT visible to Divya.');

// VERIFY: Divya MUST NOT see Srinath\'s orders!
window.renderMyOrdersList();
console.log('  Divya My Orders count:', window.myOrders.length);
if (window.myOrders.length !== 0) {
  throw new Error('SECURITY VIOLATION: Srinath\'s orders leaked into Divya\'s My Orders!');
}
if (elements['my-orders-list-container'].innerHTML.includes(srinathOrderToken)) {
  throw new Error('SECURITY VIOLATION: Srinath\'s order token rendered in Divya\'s orders list!');
}
console.log('  ✓ Verified: Srinath\'s orders are completely invisible to Divya.');

// Divya places her own order (Chicken Biryani)
window.updateDishQty('chicken_biryani', 1);
window.placeOrderAndGenerateToken();
const divyaOrderToken = window.myOrders[0].token;
console.log(`  Divya placed Order: ${divyaOrderToken}, My Orders count: ${window.myOrders.length}`);
if (window.myOrders.length !== 1 || window.myOrders[0].token !== divyaOrderToken) {
  throw new Error('Divya order placement failed');
}

// Step D: Divya logs out
console.log('  Divya logs out...');
window.logoutUser();

// Step E: Student A (Srinath) logs back in
console.log('\n  Logging back in as Student A (Srinath - SAV101)...');
window.fillDemoStudent('SAV101', 'pass123');
window.handleStudentSignIn();
console.log('  Active User:', window.currentUser.name);

// VERIFY: Srinath sees ONLY Srinath\'s order (#A-...) and DOES NOT see Divya\'s order!
console.log('  Srinath My Orders count:', window.myOrders.length);
console.log('  Srinath Order Token:', window.myOrders[0].token);
if (window.myOrders.length !== 1 || window.myOrders[0].token !== srinathOrderToken) {
  throw new Error('Srinath\'s order was not restored properly!');
}
if (window.myOrders.some(o => o.token === divyaOrderToken)) {
  throw new Error('SECURITY VIOLATION: Divya\'s order appeared in Srinath\'s account!');
}
console.log('  ✓ Verified: Srinath sees only his own order and NOT Divya\'s order.');

// VERIFY: Srinath\'s cart still has his Samosa & Chai!
console.log('  Srinath restored cart:', window.cart);
if (!window.cart['samosa_chai'] || window.cart['samosa_chai'] !== 1) {
  throw new Error('Srinath\'s private cart was not restored!');
}
console.log('  ✓ Verified: Srinath\'s private cart was restored cleanly.');
console.log('✓ TEST 3 PASSED: 100% data isolation between different user accounts confirmed!\n');

// -----------------------------------------------------------------------------
// TEST 4: User Profile Modal Display
// -----------------------------------------------------------------------------
console.log('[TEST 4] User Profile Display');
window.openProfileModal();
const profileHtml = elements['profile-modal-body'].innerHTML;
console.log('  Profile contains user name (Srinath):', profileHtml.includes('Srinath'));
console.log('  Profile contains Student ID (SAV101):', profileHtml.includes('SAV101'));
console.log('  Profile contains Department (3rd Year):', profileHtml.includes('3rd Year'));
if (!profileHtml.includes('Srinath') || !profileHtml.includes('SAV101')) {
  throw new Error('Profile modal does not display logged in user information!');
}
console.log('✓ TEST 4 PASSED: User profile modal displays accurate, user-specific data!\n');

console.log('====================================================================');
console.log('🎉 ALL USER-SPECIFIC LOGIN & DATA ISOLATION TESTS PASSED WITH 0 ERRORS! 🚀');
console.log('====================================================================');
process.exit(0);
