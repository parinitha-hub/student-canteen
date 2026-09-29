const fs = require('fs');
const path = require('path');
const vm = require('vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');

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
  appendChild(child) { this.children.push(child); }
  remove() { this.children = []; }
  focus() {}
  scrollIntoView() {}
}

const elements = {};
const idRegex = /id=["']([^"']+)["']/g;
let match;
while ((match = idRegex.exec(html)) !== null) {
  elements[match[1]] = new MockElement(match[1]);
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
    querySelector: () => null,
    querySelectorAll: () => [],
    documentElement: { setAttribute: () => {}, removeAttribute: () => {} },
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
const appJsCode = fs.readFileSync(path.join(__dirname, '..', 'js', 'app.js'), 'utf8');
vm.runInContext(appJsCode, sandbox);

console.log('=== TESTING NEW DISHES ORDERING FLOW ===');

// 1. Login as Student
elements['login-student-name'].value = 'Priya';
elements['login-student-year'].value = '3rd Year';
sandbox.window.handlePortalStudentLogin();
console.log('Logged in as:', sandbox.window.currentUser.name);

// 2. Add New Food Items:
// Idli Vada (₹65), Mumbai Pav Bhaji (₹90), Cold Coffee (₹50), Gulab Jamun (₹45)
sandbox.window.updateDishQty('idli_vada', 1);
sandbox.window.updateDishQty('pav_bhaji', 2);
sandbox.window.updateDishQty('cold_coffee', 2);
sandbox.window.updateDishQty('gulab_jamun', 1);

// Total expected: 65 + (90*2) + (50*2) + 45 = 65 + 180 + 100 + 45 = ₹390
console.log('Cart entries:', sandbox.window.cart);
console.log('Floating Cart Total:', elements['floating-cart-total'].textContent);
console.log('Floating Cart Items Count:', elements['floating-cart-count'].textContent);

if (elements['floating-cart-total'].textContent !== '₹390') {
  throw new Error(`Total mismatch! Expected ₹390, got ${elements['floating-cart-total'].textContent}`);
}

// 3. Open Cart Modal
sandbox.window.openCartModal();
if (!elements['cart-modal'].classList.contains('show')) {
  throw new Error('Cart modal failed to open');
}
console.log('Cart items HTML contains all dishes:', 
  elements['cart-items-container'].innerHTML.includes('Idli Vada') &&
  elements['cart-items-container'].innerHTML.includes('Mumbai Pav Bhaji') &&
  elements['cart-items-container'].innerHTML.includes('Thick Cold Coffee') &&
  elements['cart-items-container'].innerHTML.includes('Hot Gulab Jamun')
);

// 4. Place Order & Generate Token
sandbox.window.placeOrderAndGenerateToken();
const order = sandbox.window.lastPlacedOrder;
console.log('Placed Order Token:', order.token);
console.log('Order Total:', order.total);
console.log('Order Items count:', order.items.length);
console.log('Token modal visible:', elements['token-modal'].classList.contains('show'));
console.log('Token displayed in modal:', elements['token-number'].textContent);

if (order.total !== 390 || order.items.length !== 4) {
  throw new Error('Order verification failed!');
}

console.log('\n✅ NEW DISHES ORDER FLOW VERIFIED SUCCESSFULLY!');
