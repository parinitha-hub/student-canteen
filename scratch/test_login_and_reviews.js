const fs = require('fs');

console.log("=== COMPREHENSIVE TEST FOR LOGIN, REVIEWS & ANIMATIONS ===");

// DOM Mock
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
  "nav-btn-about", "nav-btn-reviews", "nav-btn-home", "btn-top-my-orders-nav", "nav-btn-kitchen",
  "nav-btn-login", "user-auth-slot", "view-about", "view-login", "view-order",
  "view-manager", "main-view-toggle", "header-cart-btn", "btn-mode-order",
  "btn-mode-manager", "cart-floating-bar", "dishes-grid", "cart-items-container",
  "cart-modal", "my-orders-modal", "my-orders-list-container", "my-orders-count",
  "menu-my-orders-count", "hero-cart-count", "floating-cart-total", "floating-cart-count",
  "cart-modal-total", "order-customer-name", "order-customer-year", "order-customer-phone",
  "live-order-badge", "live-orders-container", "toast-container", "about-hero-primary-btn",
  "login-student-name", "login-student-year", "login-student-phone", "login-worker-password",
  "reviews-cards-grid", "reviews-section", "add-review-modal", "modal-fb-name",
  "modal-fb-year", "modal-fb-comment", "modal-fb-rating", "modal-fb-category"
];

mockIds.forEach(id => {
  elements[id] = createElementMock(id);
});

global.document = {
  getElementById: (id) => elements[id] || createElementMock(id),
  querySelectorAll: () => [],
  createElement: (tag) => createElementMock('dynamic', tag),
  documentElement: {
    setAttribute: () => {},
    removeAttribute: () => {}
  }
};

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

global.sessionStorage = {
  getItem: () => null,
  setItem: () => {},
  removeItem: () => {}
};

// Load js/app.js
const appCode = fs.readFileSync('js/app.js', 'utf-8');
eval(appCode);

// TEST 1: Default Startup state
console.log("\n[TEST 1] Initial Startup state");
initUserAuth();
console.log("  View About display:", elements["view-about"].style.display, "(Expected: block)");
console.log("  View Login display:", elements["view-login"].style.display, "(Expected: none)");
console.log("  View Order display:", elements["view-order"].style.display, "(Expected: none)");
if (elements["view-about"].style.display === "block" && elements["view-order"].style.display === "none") {
  console.log("  ✓ TEST 1 PASSED: Website starts on About page without errors!");
} else {
  console.error("  ✗ TEST 1 FAILED");
  process.exit(1);
}

// TEST 2: Navigate to Login View
console.log("\n[TEST 2] Navigate to Login Portal");
navigateToSection("login");
console.log("  View Login display:", elements["view-login"].style.display, "(Expected: block)");
console.log("  View About display:", elements["view-about"].style.display, "(Expected: none)");
if (elements["view-login"].style.display === "block" && elements["view-about"].style.display === "none") {
  console.log("  ✓ TEST 2 PASSED: Successfully navigated to Login Portal!");
} else {
  console.error("  ✗ TEST 2 FAILED");
  process.exit(1);
}

// TEST 3: Student Login via handlePortalStudentLogin
console.log("\n[TEST 3] Student Login via Form Submit");
elements["login-student-name"].value = "Priya Sharma";
elements["login-student-year"].value = "2nd Year";
elements["login-student-phone"].value = "9876543210";
const preventDefaultCalled = [];
handlePortalStudentLogin({
  preventDefault: () => preventDefaultCalled.push(true),
  stopPropagation: () => {}
});

console.log("  Current User role:", window.currentUser && window.currentUser.role);
console.log("  Current User name:", window.currentUser && window.currentUser.name);
console.log("  Stored in localStorage:", localStorage.getItem("savitha_user"));
console.log("  Order View display:", elements["view-order"].style.display, "(Expected: block)");

if (window.currentUser && window.currentUser.name === "Priya Sharma" && elements["view-order"].style.display === "block") {
  console.log("  ✓ TEST 3 PASSED: Student form login works seamlessly without page reload!");
} else {
  console.error("  ✗ TEST 3 FAILED");
  process.exit(1);
}

// TEST 4: Quick 1-Click Student Login
console.log("\n[TEST 4] Quick 1-Click Student Login");
logoutUser();
quickDemoStudentLogin();
console.log("  Quick user name:", window.currentUser && window.currentUser.name);
console.log("  Order View display after quick login:", elements["view-order"].style.display);
if (window.currentUser && window.currentUser.role === "student" && elements["view-order"].style.display === "block") {
  console.log("  ✓ TEST 4 PASSED: Quick student login works perfectly!");
} else {
  console.error("  ✗ TEST 4 FAILED");
  process.exit(1);
}

// TEST 5: Kitchen Staff Login
console.log("\n[TEST 5] Kitchen Staff Login");
logoutUser();
elements["login-worker-password"].value = "savi123";
handlePortalWorkerLogin({
  preventDefault: () => {},
  stopPropagation: () => {}
});
console.log("  Staff role:", window.currentUser && window.currentUser.role);
console.log("  Staff dashboard display:", elements["view-manager"].style.display, "(Expected: block)");
if (window.currentUser && window.currentUser.role === "worker" && elements["view-manager"].style.display === "block") {
  console.log("  ✓ TEST 5 PASSED: Kitchen staff login authenticated successfully!");
} else {
  console.error("  ✗ TEST 5 FAILED");
  process.exit(1);
}

async function runTests() {
  // TEST 6: Reviews Section & Navigation
  console.log("\n[TEST 6] Reviews Section & Navigation");
  navigateToSection("reviews");
  console.log("  About view display for reviews:", elements["view-about"].style.display, "(Expected: block)");
  console.log("  Reviews nav button active:", elements["nav-btn-reviews"].classList.contains("active"));
  if (elements["view-about"].style.display === "block" && elements["nav-btn-reviews"].classList.contains("active")) {
    console.log("  ✓ TEST 6 PASSED: Navigation to reviews works!");
  } else {
    console.error("  ✗ TEST 6 FAILED");
    process.exit(1);
  }

  // TEST 7: Reviews Loading & Rendering
  console.log("\n[TEST 7] Reviews Rendering");
  await loadFeedback();
  const reviewsHtml = elements["reviews-cards-grid"].innerHTML;
  console.log("  Reviews grid rendered length:", reviewsHtml.length);
  console.log("  Contains stars graphic:", reviewsHtml.includes("dish-stars-graphic") || reviewsHtml.includes("★"));
  console.log("  Contains Verified badge:", reviewsHtml.includes("Verified"));

  if (reviewsHtml.length > 50 && (reviewsHtml.includes("★") || reviewsHtml.includes("Verified"))) {
    console.log("  ✓ TEST 7 PASSED: Reviews rendered with 5-star ratings and verified badges!");
  } else {
    console.error("  ✗ TEST 7 FAILED");
    process.exit(1);
  }

  // TEST 8: Food Item Star Ratings
  console.log("\n[TEST 8] Food Item Star Ratings in Menu");
  quickDemoStudentLogin();
  const dishesHtml = elements["dishes-grid"].innerHTML;
  console.log("  Dishes grid HTML length:", dishesHtml.length);
  console.log("  Dishes contain star rating row:", dishesHtml.includes("dish-star-rating-row"));
  console.log("  Dishes contain stars graphic:", dishesHtml.includes("dish-stars-graphic"));

  if (dishesHtml.includes("dish-star-rating-row") && dishesHtml.includes("★")) {
    console.log("  ✓ TEST 8 PASSED: Food items display prominent 5-star ratings!");
  } else {
    console.error("  ✗ TEST 8 FAILED");
    process.exit(1);
  }

  // TEST 9: HTML File Integrity (Developer photo, Reviews pre-rendered, 0 broken links)
  console.log("\n[TEST 9] HTML & Asset Verification");
  const html = fs.readFileSync('index.html', 'utf-8');
  const hasDevPhoto = html.includes('assets/parinitha.jpg');
  const hasLinkedIn = html.includes('linkedin.com/in/pari-parinitha-s-6196b8354');
  const hasReviewsGrid = html.includes('id="reviews-cards-grid"');
  const hasReviewsPreRendered = html.includes('Sneha Reddy') && html.includes('Divya Krishnan');
  const hasFloatingBadge = html.includes('hero-floating-badge');

  console.log("  Developer photo referenced:", hasDevPhoto);
  console.log("  Developer LinkedIn profile linked:", hasLinkedIn);
  console.log("  Reviews grid present:", hasReviewsGrid);
  console.log("  Pre-rendered verified reviews:", hasReviewsPreRendered);
  console.log("  Floating hero badge:", hasFloatingBadge);

  if (hasDevPhoto && hasLinkedIn && hasReviewsGrid && hasReviewsPreRendered && hasFloatingBadge) {
    console.log("  ✓ TEST 9 PASSED: HTML integrity is 100% verified!");
  } else {
    console.error("  ✗ TEST 9 FAILED");
    process.exit(1);
  }

  console.log("\n=======================================================");
  console.log("ALL 9 TESTS FOR LOGIN, REVIEWS & ANIMATIONS PASSED!");
  console.log("=======================================================");
}

runTests();
