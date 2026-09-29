const fs = require('fs');

console.log("=================================================================");
console.log("FINAL VERIFICATION: Clean Login (No Visible Name) & Menu Privacy");
console.log("=================================================================\n");

// 1. Static HTML Checks
const html = fs.readFileSync('index.html', 'utf-8');
const frontendHtml = fs.readFileSync('frontend/index.html', 'utf-8');

// Ensure root and frontend are 100% in sync
if (html !== frontendHtml) {
  console.error("✗ ERROR: root index.html and frontend/index.html are not in sync!");
  process.exit(1);
}
console.log("✓ Root index.html and frontend/index.html are synchronized.");

// Check: No demo login button in login panel
if (html.includes("Quick 1-Click Login") || html.includes("Karthik Raj - 3rd Year")) {
  console.error("✗ ERROR: Demo button or Karthik Raj still found in index.html!");
  process.exit(1);
}
console.log("✓ No demo login buttons or hardcoded names in login panel.");

// Check: login student name input has clean placeholder and autocomplete="off"
if (!html.includes('placeholder="Enter your full name"') || !html.includes('autocomplete="off"')) {
  console.error("✗ ERROR: login-student-name input placeholder or autocomplete is incorrect!");
  process.exit(1);
}
console.log("✓ Student login input has clean placeholder and autocomplete='off'.");

// 2. Dynamic JS DOM Simulation
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
  "cart-modal-total", "login-student-name", "login-student-year", "login-student-phone",
  "login-worker-password", "order-customer-name", "order-customer-year", "order-customer-phone",
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
  _store: {
    // Simulate leftover session from prior usage
    "savitha_user": JSON.stringify({ role: "student", name: "Previous User", year: "3rd Year" })
  },
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
const appJs = fs.readFileSync('js/app.js', 'utf-8');
eval(appJs);

// STEP 1: Startup Check (Even if previous session was in localStorage)
console.log("\n[TEST 1] Initial Startup Behavior");
initUserAuth();

console.log("  View About display:", elements["view-about"].style.display, "(Expected: block)");
console.log("  View Order display:", elements["view-order"].style.display, "(Expected: none)");
console.log("  Nav Menu display:", elements["nav-btn-home"].style.display, "(Expected: none)");
console.log("  Nav My Orders display:", elements["btn-top-my-orders-nav"].style.display, "(Expected: none)");

if (elements["view-about"].style.display !== "block") throw new Error("About view is not active on startup!");
if (elements["view-order"].style.display === "block") throw new Error("Food menu is prematurely visible without entering menu!");
if (elements["nav-btn-home"].style.display === "inline-flex") throw new Error("Menu nav is prematurely visible on About page!");
if (elements["btn-top-my-orders-nav"].style.display === "inline-flex") throw new Error("My Orders nav is prematurely visible on About page!");
console.log("✓ TEST 1 PASSED: Without entering the menu, food menu is completely hidden!");

// STEP 2: Navigate to Login Screen
console.log("\n[TEST 2] Login Screen State (No Name Visible)");
navigateToSection("login");

console.log("  View Login display:", elements["view-login"].style.display, "(Expected: block)");
console.log("  login-student-name value:", JSON.stringify(elements["login-student-name"].value), "(Expected: '')");
console.log("  user-auth-slot HTML contains user name:", elements["user-auth-slot"].innerHTML.includes("Previous User"));

if (elements["view-login"].style.display !== "block") throw new Error("Login view is not visible!");
if (elements["login-student-name"].value !== "") throw new Error("Student name input has a prefilled name!");
if (elements["user-auth-slot"].innerHTML.includes("Previous User")) throw new Error("Top header shows user session name on login screen!");
console.log("✓ TEST 2 PASSED: Login page has no visible names (completely clean & blank)!");

// STEP 3: Student Login & Entering Menu
console.log("\n[TEST 3] Entering Menu via Login Form");
elements["login-student-name"].value = "Srinath";
elements["login-student-year"].value = "2nd Year";
handlePortalStudentLogin();

console.log("  Current User:", window.currentUser);
console.log("  View Order display after login:", elements["view-order"].style.display, "(Expected: block)");
console.log("  Nav Menu display after login:", elements["nav-btn-home"].style.display, "(Expected: inline-flex)");
console.log("  Nav My Orders display after login:", elements["btn-top-my-orders-nav"].style.display, "(Expected: inline-flex)");

if (elements["view-order"].style.display !== "block") throw new Error("Food menu is not visible after entering menu!");
if (elements["nav-btn-home"].style.display !== "inline-flex") throw new Error("Menu nav button is missing on order page!");
if (elements["btn-top-my-orders-nav"].style.display !== "inline-flex") throw new Error("My Orders nav button is missing on order page!");
console.log("✓ TEST 3 PASSED: Food menu is visible ONLY after entering the menu!");

// STEP 4: Return to About Page
console.log("\n[TEST 4] Returning to About Page");
navigateToSection("about");

console.log("  View About display:", elements["view-about"].style.display, "(Expected: block)");
console.log("  View Order display:", elements["view-order"].style.display, "(Expected: none)");
console.log("  Nav Menu display:", elements["nav-btn-home"].style.display, "(Expected: none)");
console.log("  Nav My Orders display:", elements["btn-top-my-orders-nav"].style.display, "(Expected: none)");

if (elements["view-about"].style.display !== "block") throw new Error("About view is not displayed!");
if (elements["view-order"].style.display === "block") throw new Error("Food menu is visible on About page!");
if (elements["nav-btn-home"].style.display === "inline-flex") throw new Error("Menu nav is visible on About page!");
if (elements["btn-top-my-orders-nav"].style.display === "inline-flex") throw new Error("My Orders nav is visible on About page!");
console.log("✓ TEST 4 PASSED: Menu and My Orders cleanly hidden on About page!");

console.log("\n=================================================================");
console.log("ALL TESTS COMPLETED SUCCESSFULLY WITH 0 ERRORS!");
console.log("=================================================================");
