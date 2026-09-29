const fs = require('fs');

console.log("==========================================================");
console.log("🔒 TESTING KITCHEN STAFF PASSWORD PRIVACY & 'savi123'");
console.log("==========================================================");

// TEST 1: Check index.html for password visibility
console.log("\n[TEST 1] Verifying Default Password is NOT Visible in HTML");
const html = fs.readFileSync('index.html', 'utf-8');
const frontendHtml = fs.readFileSync('frontend/index.html', 'utf-8');

if (html.includes("Default password:") || frontendHtml.includes("Default password:")) {
  throw new Error("FAIL: 'Default password:' text is still present in HTML!");
}
if (html.includes("canteen123") || frontendHtml.includes("canteen123")) {
  throw new Error("FAIL: 'canteen123' is still visible in index.html!");
}
if (html.includes("savi123") || frontendHtml.includes("savi123")) {
  throw new Error("FAIL: 'savi123' must not be written in plaintext in index.html!");
}

console.log("✓ TEST 1 PASSED: Default password is completely invisible in index.html and frontend/index.html!");

// Setup minimal DOM mock
const elements = {};
function createElementMock(id, tag = 'div') {
  return {
    id: id,
    tagName: tag.toUpperCase(),
    style: {},
    classList: {
      _classes: new Set(),
      add: function(c) { this._classes.add(c); },
      remove: function(c) { this._classes.delete(c); },
      contains: function(c) { return this._classes.has(c); }
    },
    value: '',
    textContent: '',
    innerHTML: '',
    children: [],
    appendChild: function(c) { this.children.push(c); },
    removeChild: function(c) { this.children = this.children.filter(x => x !== c); },
    remove: function() {},
    addEventListener: () => {},
    focus: () => {}
  };
}

const mockIds = [
  "nav-btn-kitchen", "view-manager", "view-about", "view-login", "view-order",
  "login-panel-worker", "login-worker-password", "worker-password-input",
  "user-auth-slot", "current-pwd-input", "new-pwd-input", "toast-container"
];

mockIds.forEach(id => {
  elements[id] = createElementMock(id);
});

global.document = {
  getElementById: (id) => elements[id] || createElementMock(id),
  querySelectorAll: () => [],
  createElement: (tag) => createElementMock('dynamic', tag),
  documentElement: { setAttribute: () => {}, removeAttribute: () => {} }
};

let lastToastMessage = "";
global.window = {
  scrollTo: () => {},
  location: { origin: "http://127.0.0.1:5000" },
  confirm: () => true
};

global.localStorage = {
  _store: {},
  getItem: function(k) { return this._store[k] || null; },
  setItem: function(k, v) { this._store[k] = String(v); },
  removeItem: function(k) { delete this._store[k]; }
};

global.sessionStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };

// Load app.js
const appCode = fs.readFileSync('js/app.js', 'utf-8');
eval(appCode);

// TEST 2: Wrong Password Attempt
console.log("\n[TEST 2] Testing Wrong Password Rejection");
elements["login-worker-password"].value = "wrong_pass_999";
handlePortalWorkerLogin({ preventDefault: () => {}, stopPropagation: () => {} });

if (window.currentUser && window.currentUser.role === "worker") {
  throw new Error("FAIL: Wrong password was incorrectly authenticated!");
}
console.log("✓ TEST 2 PASSED: Wrong password rejected cleanly!");

// TEST 3: Login with 'savi123'
console.log("\n[TEST 3] Testing Login with 'savi123'");
elements["login-worker-password"].value = "savi123";
handlePortalWorkerLogin({ preventDefault: () => {}, stopPropagation: () => {} });

if (!window.currentUser || window.currentUser.role !== "worker") {
  throw new Error("FAIL: 'savi123' failed to authenticate kitchen staff!");
}
if (elements["view-manager"].style.display !== "block") {
  throw new Error("FAIL: view-manager was not displayed upon login!");
}
console.log("  Current User:", window.currentUser);
console.log("  View Manager display:", elements["view-manager"].style.display);
console.log("✓ TEST 3 PASSED: 'savi123' successfully authenticates into Kitchen Staff Dashboard!");

// TEST 4: Password Update Feature
console.log("\n[TEST 4] Testing Staff Password Update Functionality");
elements["current-pwd-input"].value = "savi123";
elements["new-pwd-input"].value = "chef2026";
handleStaffPasswordChange({ preventDefault: () => {} });

console.log("  Updated password in storage:", global.localStorage.getItem("savitha_kitchen_pwd"));
if (global.localStorage.getItem("savitha_kitchen_pwd") !== "chef2026") {
  throw new Error("FAIL: New password was not updated in localStorage!");
}

// Test login with the newly updated password
logoutUser();
elements["login-worker-password"].value = "chef2026";
handlePortalWorkerLogin({ preventDefault: () => {}, stopPropagation: () => {} });
if (!window.currentUser || window.currentUser.role !== "worker") {
  throw new Error("FAIL: Newly updated password failed to authenticate!");
}
console.log("✓ TEST 4 PASSED: Password update workflow works seamlessly!");

console.log("\n==========================================================");
console.log("🎉 ALL PASSWORD PRIVACY & AUTHENTICATION TESTS PASSED 100%!");
console.log("==========================================================");
