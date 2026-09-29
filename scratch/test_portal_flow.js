const fs = require('fs');

// Simple DOM Mock
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

// IDs needed by app.js
const neededIds = [
  'main-view-toggle', 'header-cart-btn', 'btn-mode-order', 'btn-mode-manager',
  'view-login', 'view-order', 'view-manager', 'cart-floating-bar',
  'user-auth-slot', 'theme-name', 'theme-icon', 'dishes-grid', 'backend-status',
  'toast-container', 'history-table-body', 'cart-counter', 'cart-total-pill',
  'cart-items-list', 'live-order-badge', 'live-orders-container',
  'login-tab-student', 'login-tab-worker', 'login-panel-student', 'login-panel-worker',
  'login-student-name', 'login-worker-password', 'curr-pwd-disp', 'selected-dish-display',
  'mgr_date', 'mgr_day', 'mgr_holiday'
];

neededIds.forEach(id => createMockElement(id));

// Set initial inputs
elements['login-student-name'].value = 'Rahul Sharma';
elements['login-worker-password'].value = 'savitha123';

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

// Trigger DOMContentLoaded
global._domLoaded();

console.log('--- Step 1: Initial Page Load ---');
console.log('view-login display:', elements['view-login'].style.display);
console.log('view-order display:', elements['view-order'].style.display);
console.log('view-manager display:', elements['view-manager'].style.display);
if (elements['view-login'].style.display !== 'flex') {
  throw new Error('FAIL: view-login was not displayed as flex on initial load!');
}
console.log('[OK] Initial page load displays Simple Login page directly');

console.log('\n--- Step 2: Tab Switching ---');
window.switchLoginTab('worker');
console.log('Staff panel display:', elements['login-panel-worker'].style.display);
console.log('Student panel display:', elements['login-panel-student'].style.display);
if (elements['login-panel-worker'].style.display !== 'block') {
  throw new Error('FAIL: Staff panel was not displayed!');
}
window.switchLoginTab('student');
console.log('Student panel display after switch back:', elements['login-panel-student'].style.display);
console.log('[OK] Tab switching between Student and Kitchen Staff works cleanly');

console.log('\n--- Step 3: 1-Click Student Login ---');
window.handlePortalStudentLogin();
console.log('After student login:');
console.log('view-login display:', elements['view-login'].style.display);
console.log('view-order display:', elements['view-order'].style.display);
if (elements['view-order'].style.display !== 'block') {
  throw new Error('FAIL: view-order was not displayed after Student login!');
}
console.log('[OK] Student login transitions smoothly to Food Menu view');

console.log('\n--- Step 4: Logout from Student View ---');
window.logoutUser();
console.log('After logout:');
console.log('view-login display:', elements['view-login'].style.display);
console.log('view-order display:', elements['view-order'].style.display);
if (elements['view-login'].style.display !== 'flex') {
  throw new Error('FAIL: Logout did not return to view-login!');
}
console.log('[OK] Logout returns directly to the Simple Login page');

console.log('\n--- Step 5: Kitchen Staff Login ---');
window.switchLoginTab('worker');
window.handlePortalWorkerLogin();
console.log('After staff login:');
console.log('view-login display:', elements['view-login'].style.display);
console.log('view-manager display:', elements['view-manager'].style.display);
if (elements['view-manager'].style.display !== 'block') {
  throw new Error('FAIL: view-manager was not displayed after Staff login!');
}
console.log('[OK] Kitchen Staff login opens Kitchen Dashboard with live incoming orders');

console.log('\n--- Step 6: Logout from Staff View ---');
window.logoutUser();
console.log('After staff logout:');
console.log('view-login display:', elements['view-login'].style.display);
if (elements['view-login'].style.display !== 'flex') {
  throw new Error('FAIL: Staff logout did not return to view-login!');
}
console.log('[OK] Staff logout returns directly to Simple Login page');

console.log('\n--- Step 7: Skip Login as Guest ---');
window.quickPortalStudentLogin();
console.log('After guest login:');
console.log('view-order display:', elements['view-order'].style.display);
if (elements['view-order'].style.display !== 'block') {
  throw new Error('FAIL: Guest login did not display food menu!');
}
console.log('[OK] Guest login works flawlessly');

console.log('\nALL APPLICATION FLOWS PASSED WITH ZERO ERRORS! 🚀');
process.exit(0);
