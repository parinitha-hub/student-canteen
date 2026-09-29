const fs = require('fs');
const path = require('path');

// Simple DOM Mock to verify role-based visibility and transitions
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
  appendChild(child) { this.children.push(child); }
  removeChild(child) { this.children = this.children.filter(c => c !== child); }
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

global.window = {
  scrollTo: () => {},
  addEventListener: () => {}
};
global.document = {
  getElementById: (id) => getOrCreateElement(id),
  querySelectorAll: (selector) => [],
  createElement: (tag) => new ElementMock(tag),
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
eval(jsCode);

console.log("=== Running Role-Based Permission & Navigation Tests ===");

// 1. Startup Test (Unauthenticated Visitor)
initUserAuth();
const viewAbout = document.getElementById("view-about");
const viewLogin = document.getElementById("view-login");
const viewOrder = document.getElementById("view-order");
const viewMgr = document.getElementById("view-manager");
const userSlot = document.getElementById("user-auth-slot");

if (viewAbout.style.display !== "block") {
  console.error("FAIL: view-about should be block on startup");
  process.exit(1);
}
if (!userSlot.innerHTML.includes("btn-top-login")) {
  console.error("FAIL: Navbar should have ONLY login button");
  process.exit(1);
}
if (window.currentUser !== null) {
  console.error("FAIL: Unauthenticated visitor currentUser should be null");
  process.exit(1);
}
console.log("[PASS] 1. Initial load: displays About page with ONLY Login in navigation bar (currentUser = null)");

// 2. Gate Verification: Without login we should NOT get food menu items!
navigateToSection("home");
if (viewOrder.style.display === "block") {
  console.error("FAIL: Without login, food menu items must NOT be accessible!");
  process.exit(1);
}
if (viewLogin.style.display !== "flex") {
  console.error("FAIL: Attempting to access food menu without login should redirect to Login screen!");
  process.exit(1);
}
console.log("[PASS] 2. Without login, food menu items are strictly BLOCKED and redirected to Login screen!");

// 3. Verify Two Logos Exist in HTML for Student and Kitchen Staff
const indexHtml = fs.readFileSync(path.join(__dirname, '../index.html'), 'utf8');
if (!indexHtml.includes('id="login-tab-student"') || !indexHtml.includes('id="login-tab-worker"')) {
  console.error("FAIL: Login screen must contain two role tabs for Student and Kitchen Staff!");
  process.exit(1);
}
if (!indexHtml.includes('role-logo-student') || !indexHtml.includes('role-logo-worker')) {
  console.error("FAIL: Login screen must contain the two distinct role logos!");
  process.exit(1);
}
console.log("[PASS] 3. Login screen features two distinct logos: Student (🎓) and Kitchen Staff (👨‍🍳)!");

// 4. Student Login
document.getElementById("login-student-name").value = "Priya";
document.getElementById("login-student-year").value = "2nd Year";
handlePortalStudentLogin();

if (window.currentUser.role !== "student") {
  console.error("FAIL: Role should be student");
  process.exit(1);
}
if (viewOrder.style.display !== "block") {
  console.error("FAIL: Logged in Student should land on food menu (view-order)");
  process.exit(1);
}
if (userSlot.innerHTML.includes("👨‍🍳")) {
  console.error("FAIL: Student session chip should NOT have kitchen icon!");
  process.exit(1);
}
console.log("[PASS] 4. Student logged in: sees food menu, NO kitchen icon anywhere!");

// 5. Kitchen Staff Login
document.getElementById("login-worker-password").value = "savitha123";
handlePortalWorkerLogin();

if (window.currentUser.role !== "worker") {
  console.error("FAIL: Role should be worker");
  process.exit(1);
}
if (viewMgr.style.display !== "block") {
  console.error("FAIL: Kitchen staff should land on Kitchen Dashboard (view-manager)");
  process.exit(1);
}
// Try navigating to student menu as staff:
navigateToSection("home");
if (viewOrder.style.display === "block") {
  console.error("FAIL: Kitchen staff should NOT get student menu!");
  process.exit(1);
}
if (viewMgr.style.display !== "block") {
  console.error("FAIL: Kitchen staff should stay on Kitchen Dashboard!");
  process.exit(1);
}
console.log("[PASS] 5. Kitchen staff logged in: lands on Kitchen Dashboard and does NOT get food menu!");

// 6. Logout
logoutUser();
if (window.currentUser !== null) {
  console.error("FAIL: After logout currentUser should be null");
  process.exit(1);
}
if (!userSlot.innerHTML.includes("btn-top-login")) {
  console.error("FAIL: After logout navbar should contain ONLY login button");
  process.exit(1);
}
navigateToSection("home");
if (viewOrder.style.display === "block") {
  console.error("FAIL: After logout, food menu items must NOT be accessible!");
  process.exit(1);
}
console.log("[PASS] 6. Sign out cleanly resets to unauthenticated state with food menu items locked!");

console.log("\nALL DUAL-LOGO & MENU GATING TESTS PASSED WITH 100% ACCURACY!");
process.exit(0);
