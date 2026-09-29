const fs = require('fs');
const path = require('path');

// Simple DOM Mock to verify app.js transition logic in pure Node
const html = fs.readFileSync(path.join(__dirname, '../index.html'), 'utf8');

// Minimal DOM simulation
class ElementMock {
  constructor(id, tag = 'div') {
    this.id = id;
    this.tagName = tag.toUpperCase();
    this.style = {};
    this.classList = {
      classes: new Set(),
      add: (c) => this.classList.classes.add(c),
      remove: (c) => this.classList.classes.delete(c),
      contains: (c) => this.classList.classes.has(c)
    };
    this.innerHTML = '';
    this.value = '';
    this.children = [];
  }
  appendChild(c) { this.children.push(c); }
  removeChild(c) {}
  remove() {}
  focus() {}
  scrollIntoView() {}
}

const elements = {};
function getOrCreateElement(id) {
  if (!elements[id]) {
    elements[id] = new ElementMock(id);
  }
  return elements[id];
}

// Setup basic global window & document mocks
global.window = {
  scrollTo: () => {},
  addEventListener: () => {}
};
global.document = {
  getElementById: (id) => getOrCreateElement(id),
  querySelectorAll: (selector) => [],
  createElement: (tag) => new ElementMock('toast', tag),
  addEventListener: () => {}
};
global.localStorage = {
  getItem: () => null,
  setItem: () => {},
  removeItem: () => {}
};
global.fetch = async () => ({
  ok: true,
  json: async () => ({ status: 'success', feedback: [] })
});

// Load app.js code
const jsCode = fs.readFileSync(path.join(__dirname, '../js/app.js'), 'utf8');

// Evaluate in sandbox
eval(jsCode);

console.log("=== Testing UI View Transitions & Startup ===");

// 1. Startup Test
initUserAuth();

const viewAbout = document.getElementById("view-about");
const viewLogin = document.getElementById("view-login");
const viewOrder = document.getElementById("view-order");
const viewMgr = document.getElementById("view-manager");

if (viewAbout.style.display !== "block") {
  console.error("FAIL: view-about should be block on startup, got:", viewAbout.style.display);
  process.exit(1);
}
if (viewLogin.style.display !== "none") {
  console.error("FAIL: view-login should be none on startup, got:", viewLogin.style.display);
  process.exit(1);
}
console.log("[PASS] Startup test: About Website page is displayed first (#view-about)");

// 2. Click Login Test
navigateToSection("login");
if (viewLogin.style.display !== "flex") {
  console.error("FAIL: view-login should be flex after clicking login, got:", viewLogin.style.display);
  process.exit(1);
}
if (viewAbout.style.display !== "none") {
  console.error("FAIL: view-about should be none when on login page, got:", viewAbout.style.display);
  process.exit(1);
}
console.log("[PASS] Navigating to 'login' displays the Login Page (#view-login)");

// 3. Click Back to About
navigateToSection("about");
if (viewAbout.style.display !== "block") {
  console.error("FAIL: view-about should be block after clicking about, got:", viewAbout.style.display);
  process.exit(1);
}
if (viewLogin.style.display !== "none") {
  console.error("FAIL: view-login should be none after navigating to about, got:", viewLogin.style.display);
  process.exit(1);
}
console.log("[PASS] Navigating back to 'about' displays the About Website page (#view-about)");

// 4. "Again I should get login page"
navigateToSection("login");
if (viewLogin.style.display !== "flex") {
  console.error("FAIL: view-login should be flex again, got:", viewLogin.style.display);
  process.exit(1);
}
if (viewAbout.style.display !== "none") {
  console.error("FAIL: view-about should be none on login again, got:", viewAbout.style.display);
  process.exit(1);
}
console.log("[PASS] Repeatedly navigating to 'login' displays the Login Page again without errors!");

// 5. Navigate to Menu without login -> blocked!
navigateToSection("home");
if (viewOrder.style.display === "block") {
  console.error("FAIL: view-order should NOT be block without login!");
  process.exit(1);
}
if (viewLogin.style.display !== "flex") {
  console.error("FAIL: unauthenticated home navigation must redirect to login!");
  process.exit(1);
}
console.log("[PASS] Gating verified: Navigating to menu without login is blocked and redirected to Login");

// 6. Login as Student and navigate to Menu -> success!
handlePortalStudentLogin();
if (viewOrder.style.display !== "block") {
  console.error("FAIL: view-order should be block after student login, got:", viewOrder.style.display);
  process.exit(1);
}
console.log("[PASS] Logged in Student accesses the Food Menu seamlessly");

console.log("\nALL UI TRANSITIONS VERIFIED COMPLETELY ERROR-FREE!");
process.exit(0);
