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
    querySelectorAll: (sel) => [],
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

console.log('=== TEST: STUDENT NAME IN LIVE ORDERS ===');

// Check Initial Live Orders Feed (should have realistic student names, not generic 'Student')
sandbox.window.renderLiveOrders();
const initialFeed = elements['live-orders-container'].innerHTML;
console.log('Initial Live Orders Feed contains Karthik R.:', initialFeed.includes('Karthik R.'));
console.log('Initial Live Orders Feed contains Ananya Sharma:', initialFeed.includes('Ananya Sharma'));

if (!initialFeed.includes('Karthik R.') || !initialFeed.includes('Ananya Sharma')) {
  throw new Error('Initial orders missing authentic student names!');
}

// Student Login as 'Srinath'
elements['login-student-name'].value = 'Srinath';
elements['login-student-year'].value = '2nd Year';
elements['login-student-phone'].value = '9876543210';
sandbox.window.handlePortalStudentLogin();
console.log('Logged in student:', sandbox.window.currentUser);

// Add items to cart
sandbox.window.updateDishQty('veg_biryani', 1);
sandbox.window.updateDishQty('hakka_noodles', 1);

// Open cart modal
sandbox.window.openCartModal();
console.log('Cart modal customer name field prefilled:', elements['order-customer-name'].value);
if (elements['order-customer-name'].value !== 'Srinath') {
  throw new Error(`Cart modal customer name was not prefilled! Got: "${elements['order-customer-name'].value}"`);
}

// Place order
sandbox.window.placeOrderAndGenerateToken();
const newOrder = sandbox.window.lastPlacedOrder;
console.log('Generated Order Customer Name:', newOrder.customer);
console.log('Generated Order Customer Year:', newOrder.customerYear);

if (newOrder.customer !== 'Srinath' || newOrder.customerYear !== '2nd Year') {
  throw new Error('Placed order did not preserve student name or year!');
}

// Check Live Orders Render
sandbox.window.renderLiveOrders();
const liveFeed = elements['live-orders-container'].innerHTML;
console.log('Live Feed contains "👤 Srinath":', liveFeed.includes('👤 Srinath'));
console.log('Live Feed contains "(2nd Year)":', liveFeed.includes('2nd Year'));

if (!liveFeed.includes('👤 Srinath')) {
  throw new Error('Live Orders Feed failed to display the student name "Srinath"!');
}

console.log('\n🎉 SUCCESS: Live order displays the actual student name and year accurately with 0 errors!');
