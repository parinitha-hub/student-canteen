/**
 * Comprehensive Order Now End-to-End Simulation Test
 * Validates all logic and DOM manipulations in js/app.js
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

// 1. Read index.html to extract all element IDs
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');

// Lightweight DOM element mock
class MockElement {
  constructor(id, tagName = 'div') {
    this.id = id;
    this.tagName = tagName.toUpperCase();
    const set = new Set();
    this.classList = {
      add: (c) => set.add(c),
      remove: (c) => set.delete(c),
      contains: (c) => set.has(c),
      toggle: (c) => set.has(c) ? set.delete(c) : set.add(c)
    };
    this.style = {};
    this.children = [];
    this.innerHTML = '';
    this._textContent = '';
    this.value = '';
  }
  get textContent() { return this._textContent; }
  set textContent(v) { this._textContent = String(v); }
  appendChild(child) {
    this.children.push(child);
  }
  remove() {
    this.children = [];
  }
  focus() {}
  scrollIntoView() {}
}

const elements = {};
// Extract all IDs from index.html
const idRegex = /id=["']([^"']+)["']/g;
let match;
while ((match = idRegex.exec(html)) !== null) {
  const id = match[1];
  elements[id] = new MockElement(id);
}

const mockWindow = {
  scrollTo: () => {},
  addEventListener: () => {},
  localStorage: {
    _data: {},
    getItem(k) { return this._data[k] || null; },
    setItem(k, v) { this._data[k] = String(v); },
    removeItem(k) { delete this._data[k]; },
    clear() { this._data = {}; }
  },
  sessionStorage: {
    _data: {},
    getItem(k) { return this._data[k] || null; },
    setItem(k, v) { this._data[k] = String(v); },
    removeItem(k) { delete this._data[k]; },
    clear() { this._data = {}; }
  }
};

const sandbox = {
  window: mockWindow,
  localStorage: mockWindow.localStorage,
  sessionStorage: mockWindow.sessionStorage,
  document: {
    getElementById: (id) => elements[id] || null,
    querySelector: (sel) => null,
    querySelectorAll: (sel) => [],
    documentElement: {
      setAttribute: () => {},
      removeAttribute: () => {}
    },
    createElement: (tag) => new MockElement('', tag)
  },
  fetch: () => Promise.resolve({ ok: true, json: () => Promise.resolve({}) }),
  console: console,
  setTimeout: (fn) => { try { fn(); } catch(e){} },
  clearTimeout: () => {},
  setInterval: () => {},
  clearInterval: () => {},
  Date: Date,
  Math: Math,
  JSON: JSON
};

vm.createContext(sandbox);

// Load app.js into sandbox
const appJsCode = fs.readFileSync(path.join(__dirname, '..', 'js', 'app.js'), 'utf8');
vm.runInContext(appJsCode, sandbox);

console.log("=== STARTING ORDER NOW VERIFICATION ===");

// Step 1: Initial state without login
console.log("\n[Test 1] Verify strict login protection:");
console.log("Current user:", sandbox.window.currentUser);
sandbox.window.openCartModal(); // Should prompt login and NOT open cart modal
if (!elements['cart-modal'].classList.contains('show')) {
  console.log("✓ PASS: Cart modal not shown when unauthenticated.");
} else {
  throw new Error("FAIL: Cart modal was shown without login!");
}

// Step 2: Login as Student
console.log("\n[Test 2] Student Login:");
elements['login-student-name'].value = 'Srinath';
elements['login-student-year'].value = '2nd Year';
elements['login-student-phone'].value = '9876543210';
sandbox.window.handlePortalStudentLogin();
console.log("Logged in user:", sandbox.window.currentUser);
if (sandbox.window.currentUser && sandbox.window.currentUser.name === 'Srinath' && sandbox.window.currentUser.role === 'student') {
  console.log("✓ PASS: Student successfully logged in.");
} else {
  throw new Error("FAIL: Student login failed!");
}

// Step 3: Open empty cart
console.log("\n[Test 3] Empty cart behavior when clicking 'Order Now':");
sandbox.window.openCartModal();
const listContainer = elements['cart-items-container'];
const modalTotal = elements['cart-modal-total'];
console.log("Modal show class present:", elements['cart-modal'].classList.contains('show'));
console.log("Cart items container snippet:", listContainer.innerHTML.replace(/\s+/g, ' ').substring(0, 100));
console.log("Modal total displayed:", modalTotal.textContent);

if (elements['cart-modal'].classList.contains('show') && listContainer.innerHTML.includes('Your Cart is Empty')) {
  console.log("✓ PASS: Cart modal opened and displayed clear empty state message.");
} else {
  throw new Error("FAIL: Empty cart state did not render properly!");
}

// Close empty cart
sandbox.window.closeCartModal();
if (!elements['cart-modal'].classList.contains('show')) {
  console.log("✓ PASS: Cart modal closed cleanly.");
} else {
  throw new Error("FAIL: Cart modal did not close!");
}

// Step 4: Add items to cart
console.log("\n[Test 4] Adding dishes to cart:");
sandbox.window.updateDishQty('veg_biryani', 2); // ₹110 * 2 = 220
sandbox.window.updateDishQty('paneer_thali', 1); // ₹130 * 1 = 130
console.log("Current cart:", sandbox.window.cart);
console.log("Hero cart counter:", elements['hero-cart-count'].textContent);
console.log("Floating cart total:", elements['floating-cart-total'].textContent);
console.log("Floating cart items count:", elements['floating-cart-count'].textContent);
console.log("Floating cart bar visible:", elements['cart-floating-bar'].classList.contains('show'));

if (sandbox.window.cart['veg_biryani'] === 2 && sandbox.window.cart['paneer_thali'] === 1 &&
    elements['hero-cart-count'].textContent === '3' &&
    elements['floating-cart-total'].textContent === '₹350' &&
    elements['cart-floating-bar'].classList.contains('show')) {
  console.log("✓ PASS: Cart quantities and floating bar totals calculated accurately.");
} else {
  throw new Error("FAIL: Cart updating failed!");
}

// Step 5: Open cart with items
console.log("\n[Test 5] Opening cart with items:");
sandbox.window.openCartModal();
console.log("Cart modal show class:", elements['cart-modal'].classList.contains('show'));
console.log("Prepopulated customer name:", elements['order-customer-name'].value);
console.log("Cart total displayed:", elements['cart-modal-total'].textContent);

if (elements['cart-modal'].classList.contains('show') &&
    elements['cart-modal-total'].textContent === '₹350' &&
    listContainer.innerHTML.includes('Veg Biryani') &&
    listContainer.innerHTML.includes('Paneer Thali') &&
    elements['order-customer-name'].value === 'Srinath') {
  console.log("✓ PASS: Cart modal shows all selected items, correct total ₹350, and student name.");
} else {
  throw new Error("FAIL: Cart items did not render properly!");
}

// Step 6: Click "Order Now & Get Token"
console.log("\n[Test 6] Placing order & generating pickup token:");
sandbox.window.placeOrderAndGenerateToken();

console.log("Cart modal closed:", !elements['cart-modal'].classList.contains('show'));
console.log("Cart empty after order:", Object.keys(sandbox.window.cart).length === 0);
console.log("Last placed order:", sandbox.window.lastPlacedOrder);
console.log("Token modal show class:", elements['token-modal'].classList.contains('show'));
console.log("Token number displayed:", elements['token-number'].textContent);
console.log("Token total paid displayed:", elements['token-total-paid'].textContent);
console.log("Token items summary snippet:", elements['token-items-list'].innerHTML.replace(/\s+/g, ' ').substring(0, 100));

if (elements['token-modal'].classList.contains('show') &&
    sandbox.window.lastPlacedOrder &&
    sandbox.window.lastPlacedOrder.token.startsWith('#') &&
    sandbox.window.lastPlacedOrder.total === 350 &&
    elements['token-number'].textContent === sandbox.window.lastPlacedOrder.token &&
    elements['token-total-paid'].textContent === '₹350') {
  console.log("✓ PASS: Order placed, pickup token generated, and token confirmation modal displayed!");
} else {
  throw new Error("FAIL: Token generation or token modal display failed!");
}

// Step 7: Check My Orders
console.log("\n[Test 7] Verify My Orders modal:");
sandbox.window.closeTokenModal();
sandbox.window.openMyOrdersModal();
console.log("My orders modal show class:", elements['my-orders-modal'].classList.contains('show'));
const myOrdersList = elements['my-orders-list-container'];
console.log("My orders list content snippet:", myOrdersList.innerHTML.replace(/\s+/g, ' ').substring(0, 160));

if (elements['my-orders-modal'].classList.contains('show') &&
    myOrdersList.innerHTML.includes(sandbox.window.lastPlacedOrder.token)) {
  console.log("✓ PASS: Order appears properly in My Orders with token and items!");
} else {
  throw new Error("FAIL: Order not found in My Orders!");
}

console.log("\n=======================================================");
console.log("🎉 ALL TESTS PASSED: ORDER NOW WORKS 100% WITHOUT ERRORS!");
console.log("=======================================================\n");
