/**
 * CanteenAI — All-in-One Swiggy/Zomato Food Order & AI Demand Prediction Controller
 */

// Food Menu Catalog with Authentic Photography
const DISHES = [
  {
    id: "veg_biryani",
    name: "Veg Biryani",
    category: "lunch",
    price: 110,
    rating: 4.8,
    reviews: 142,
    isVeg: true,
    image: "assets/veg_biryani.jpg",
    desc: "Aromatic basmati rice layered with fresh vegetables, mint, and secret royal biryani masala. Served with cooling raita.",
    demandStatus: "🔥 High Demand Today (~195 portions cooking)"
  },
  {
    id: "chicken_biryani",
    name: "Chicken Biryani",
    category: "lunch",
    price: 150,
    rating: 4.9,
    reviews: 218,
    isVeg: false,
    image: "assets/chicken_biryani.jpg",
    desc: "Dum-cooked tender chicken pieces with fragrant saffron rice, fried onions and boiled egg. Served with mirchi ka salan.",
    demandStatus: "⚡ Campus Bestseller"
  },
  {
    id: "masala_dosa",
    name: "Masala Dosa",
    category: "breakfast",
    price: 80,
    rating: 4.7,
    reviews: 164,
    isVeg: true,
    image: "assets/masala_dosa.jpg",
    desc: "Crispy golden fermented crepe roasted in pure ghee, stuffed with seasoned potato filling. Served with piping hot sambar.",
    demandStatus: "🥞 Morning Rush Favorite"
  },
  {
    id: "paneer_thali",
    name: "Paneer Thali",
    category: "lunch",
    price: 130,
    rating: 4.8,
    reviews: 98,
    isVeg: true,
    image: "assets/paneer_thali.jpg",
    desc: "Wholesome lunch plate: Rich paneer butter masala, dal tadka, jeera rice, 2 soft butter rotis, salad and gulab jamun.",
    demandStatus: "🍱 Full Meal Favorite"
  },
  {
    id: "chole_bhature",
    name: "Chole Bhature",
    category: "lunch",
    price: 95,
    rating: 4.6,
    reviews: 112,
    isVeg: true,
    image: "assets/chole_bhature.jpg",
    desc: "Two fluffy puffed bhaturas served with spicy Punjabi chickpea masala, pickled carrots, and green chili salad.",
    demandStatus: "🫓 Brunch Special"
  },
  {
    id: "samosa_chai",
    name: "Samosa & Cutting Chai",
    category: "snacks",
    price: 40,
    rating: 4.9,
    reviews: 310,
    isVeg: true,
    image: "assets/samosa_chai.jpg",
    desc: "Two crispy hand-rolled potato & green pea samosas paired with steaming fragrant cardamom-infused cutting chai.",
    demandStatus: "☕ All-Time Snack Favorite"
  },
  {
    id: "fried_rice",
    name: "Veg Fried Rice",
    category: "quick",
    price: 90,
    rating: 4.6,
    reviews: 84,
    isVeg: true,
    image: "assets/fried_rice.jpg",
    desc: "Wok-tossed long-grain rice with crunchy capsicum, carrots, spring onions, and garlic-soy chili seasoning.",
    demandStatus: "🍚 Quick Hot Meal"
  },
  {
    id: "sandwich",
    name: "Grilled Cheese Sandwich",
    category: "quick",
    price: 65,
    rating: 4.7,
    reviews: 130,
    isVeg: true,
    image: "assets/sandwich.jpg",
    desc: "Tri-layer toasted jumbo bread packed with mozzarella cheese, sweet corn, sliced tomatoes and spicy mint chutney.",
    demandStatus: "🥪 Exam Week Quick Bite"
  }
];

// Global State
let cart = {}; // { dishId: quantity }
let currentCategory = "all";
let isBackendConnected = false;
let historyRecords = [];
let currentUser = null; // { role: 'student' | 'worker' | 'guest', name: string }

// Live Orders Queue (Students order -> Kitchen gets notified in real time)
let liveOrders = [];
try {
  const savedOrders = localStorage.getItem("savitha_live_orders");
  liveOrders = savedOrders ? JSON.parse(savedOrders) : [
    {
      id: "ORD-101",
      token: "#A-14",
      customerName: "Priya Sharma",
      items: [{ name: "Chicken Biryani", qty: 1, price: 160, subtotal: 160 }],
      total: 160,
      time: "12:15 PM",
      status: "Ready at Counter! ✅",
      timestamp: Date.now() - 600000
    },
    {
      id: "ORD-102",
      token: "#B-28",
      customerName: "Arjun Verma",
      items: [{ name: "Samosa & Chai", qty: 2, price: 50, subtotal: 100 }],
      total: 100,
      time: "12:28 PM",
      status: "Preparing in Kitchen ⏳",
      timestamp: Date.now() - 120000
    }
  ];
} catch (e) {
  liveOrders = [];
}

const API_BASE = (window.location && window.location.origin && window.location.origin.startsWith("http")) 
  ? window.location.origin 
  : "http://127.0.0.1:5000";

document.addEventListener("DOMContentLoaded", () => {
  initUserAuth();
  updateKitchenPasswordDisplay();
  renderDishes();
  initManagerDefaults();
  updateLiveOrderBadge();
  loadHistory();
  checkServerHealth();
  setInterval(checkServerHealth, 12000);
});

// Color Themes & Dynamic Palette Manager
const THEMES = [
  { id: "teal-coral", name: "Teal & Coral", icon: "🌊" },
  { id: "royal-violet", name: "Royal Violet", icon: "🌌" },
  { id: "midnight", name: "Midnight Dark", icon: "🌙" },
  { id: "ruby", name: "Ruby & Gold", icon: "🍷" }
];

let currentThemeIndex = 0;

function initTheme() {
  try {
    const savedTheme = localStorage.getItem("savitha_theme") || "teal-coral";
    const foundIdx = THEMES.findIndex(t => t.id === savedTheme);
    currentThemeIndex = foundIdx >= 0 ? foundIdx : 0;
  } catch (e) {
    currentThemeIndex = 0;
  }
  applyTheme(THEMES[currentThemeIndex]);
}

window.cycleTheme = function() {
  currentThemeIndex = (currentThemeIndex + 1) % THEMES.length;
  const nextTheme = THEMES[currentThemeIndex];
  applyTheme(nextTheme);
  try {
    localStorage.setItem("savitha_theme", nextTheme.id);
  } catch (e) {}
  showToast(`Palette switched to ${nextTheme.name} ${nextTheme.icon}`, "info");
};

function applyTheme(theme) {
  if (theme.id === "teal-coral") {
    document.documentElement.removeAttribute("data-theme");
  } else {
    document.documentElement.setAttribute("data-theme", theme.id);
  }
  const nameEl = document.getElementById("theme-name");
  if (nameEl) nameEl.textContent = theme.name;
  const iconEl = document.getElementById("theme-icon");
  if (iconEl) iconEl.textContent = theme.icon;
}


/* =========================================================================
   1. FOOD MENU & CART CONTROLLER
   ========================================================================= */

function renderDishes() {
  const container = document.getElementById("dishes-grid");
  if (!container) return;

  const filtered = currentCategory === "all" 
    ? DISHES 
    : DISHES.filter(d => d.category === currentCategory);

  let html = "";
  filtered.forEach(dish => {
    const qty = cart[dish.id] || 0;
    const typeClass = dish.isVeg ? "veg" : "non-veg";
    let buttonHtml = "";

    if (qty > 0) {
      buttonHtml = `
        <div class="qty-pill">
          <button type="button" onclick="updateDishQty('${dish.id}', -1)">-</button>
          <span>${qty}</span>
          <button type="button" onclick="updateDishQty('${dish.id}', 1)">+</button>
        </div>
      `;
    } else {
      buttonHtml = `
        <button type="button" class="add-btn" onclick="updateDishQty('${dish.id}', 1)">
          ADD +
        </button>
      `;
    }

    html += `
      <div class="dish-card">
        <div class="dish-img-wrap">
          <img src="${dish.image}" alt="${dish.name}" class="dish-img" onerror="this.src='assets/hero_banner.jpg'">
          <div class="food-type-icon ${typeClass}"></div>
          <span class="rating-badge">⭐ ${dish.rating}</span>
          <div class="dish-img-overlay"></div>
        </div>
        <div class="dish-body">
          <div class="dish-title-row">
            <h3 class="dish-name">${dish.name}</h3>
          </div>
          <p class="dish-desc">${dish.desc}</p>
          <div class="demand-tag">${dish.demandStatus}</div>
          <div class="dish-footer">
            <div class="dish-price">₹${dish.price}</div>
            <div id="btn-wrap-${dish.id}">
              ${buttonHtml}
            </div>
          </div>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

window.filterCategory = function(cat, btn) {
  currentCategory = cat;
  document.querySelectorAll(".category-pill").forEach(p => p.classList.remove("active"));
  if (btn) btn.classList.add("active");
  renderDishes();
};

window.updateDishQty = function(dishId, delta) {
  if (!currentUser) {
    currentUser = { role: "student", name: "Student" };
    try { localStorage.setItem("savitha_user", JSON.stringify(currentUser)); } catch (e) {}
    renderUserAuthSlot();
  }

  const current = cart[dishId] || 0;
  const next = current + delta;
  if (next <= 0) {
    delete cart[dishId];
  } else {
    cart[dishId] = next;
  }

  renderDishes();
  updateCartBar();
};

function updateCartBar() {
  const bar = document.getElementById("cart-floating-bar");
  const counter = document.getElementById("cart-counter");
  const totalVal = document.getElementById("cart-bar-total-val");
  const itemsVal = document.getElementById("cart-bar-items-val");

  let totalQty = 0;
  let totalPrice = 0;

  for (const [id, qty] of Object.entries(cart)) {
    const dish = DISHES.find(d => d.id === id);
    if (dish) {
      totalQty += qty;
      totalPrice += (dish.price * qty);
    }
  }

  if (counter) counter.textContent = totalQty;

  if (totalQty > 0) {
    if (bar) bar.classList.add("show");
    if (totalVal) totalVal.textContent = `₹${totalPrice}`;
    if (itemsVal) itemsVal.textContent = `${totalQty} item${totalQty > 1 ? 's' : ''} in your order`;
  } else {
    if (bar) bar.classList.remove("show");
  }
}

// Cart Modal
window.openCartModal = function() {
  if (!currentUser) {
    currentUser = { role: "student", name: "Student" };
    try { localStorage.setItem("savitha_user", JSON.stringify(currentUser)); } catch (e) {}
    renderUserAuthSlot();
  }

  const modal = document.getElementById("cart-modal");
  const list = document.getElementById("cart-items-list");
  const subtotal = document.getElementById("bill-subtotal");
  const total = document.getElementById("bill-total");
  const nameInput = document.getElementById("order-customer-name");
  if (nameInput && currentUser && currentUser.name) {
    nameInput.value = currentUser.name;
  }

  if (!modal || !list) return;

  const entries = Object.entries(cart);
  if (entries.length === 0) {
    showToast("Your cart is empty. Add a delicious dish first!", "info");
    return;
  }

  let html = "";
  let sum = 0;

  entries.forEach(([id, qty]) => {
    const dish = DISHES.find(d => d.id === id);
    if (dish) {
      const itemCost = dish.price * qty;
      sum += itemCost;
      html += `
        <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid var(--border);">
          <div style="display:flex; align-items:center; gap:10px;">
            <img src="${dish.image}" alt="${dish.name}" style="width:40px; height:40px; border-radius:8px; object-fit:cover;" onerror="this.src='assets/hero_banner.jpg'">
            <div>
              <strong style="color:var(--text-main); font-size:0.95rem;">${dish.name}</strong>
              <div style="font-size:0.8rem; color:var(--text-muted);">₹${dish.price} x ${qty}</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:12px;">
            <strong style="color:var(--text-main);">₹${itemCost}</strong>
            <button type="button" onclick="updateDishQty('${dish.id}', -1)" style="background:transparent; border:none; color:#ef4444; font-size:1.1rem; cursor:pointer;" aria-label="Remove item">✕</button>
          </div>
        </div>
      `;
    }
  });

  list.innerHTML = html;
  if (subtotal) subtotal.textContent = `₹${sum}`;
  if (total) total.textContent = `₹${sum}`;

  modal.classList.add("show");
};

window.closeCartModal = function() {
  const modal = document.getElementById("cart-modal");
  if (modal) modal.classList.remove("show");
};

// Place Order & Token Generation ("You Got the Order!")
window.placeOrderAndGenerateToken = function() {
  closeCartModal();

  const nameInput = document.getElementById("order-customer-name");
  const custName = (nameInput && nameInput.value.trim())
    ? nameInput.value.trim()
    : (currentUser && currentUser.name ? currentUser.name : "Student");

  if (currentUser) {
    currentUser.name = custName;
    try { localStorage.setItem("savitha_user", JSON.stringify(currentUser)); } catch (e) {}
    renderUserAuthSlot();
  }

  // Extract ordered items
  const orderedItems = [];
  let orderTotal = 0;
  for (const [id, qty] of Object.entries(cart)) {
    const dish = DISHES.find(d => d.id === id);
    if (dish && qty > 0) {
      orderedItems.push({
        id: dish.id,
        name: dish.name,
        qty: qty,
        price: dish.price,
        subtotal: dish.price * qty
      });
      orderTotal += dish.price * qty;
    }
  }

  if (orderedItems.length === 0) {
    showToast("Please add dishes to your cart first!", "warning");
    return;
  }

  // Generate random digital token e.g. #A-42
  const letter = String.fromCharCode(65 + Math.floor(Math.random() * 6));
  const num = Math.floor(10 + Math.random() * 89);
  const token = `#${letter}-${num}`;

  // Save to live orders queue for Kitchen AI
  const newOrder = {
    id: "ORD-" + Date.now(),
    token: token,
    customerName: custName,
    items: orderedItems,
    total: orderTotal,
    time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    status: "Preparing in Kitchen ⏳",
    timestamp: Date.now()
  };
  liveOrders.unshift(newOrder);
  try {
    localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders));
  } catch (e) {}
  updateLiveOrderBadge();

  // Populate Token Modal with 'You Got the Order!' details
  const tokenEl = document.getElementById("token-number");
  if (tokenEl) tokenEl.textContent = token;

  const msgEl = document.getElementById("token-order-message");
  if (msgEl) {
    msgEl.innerHTML = `We got your order, <strong>${custName}</strong>! The kitchen is preparing your meal hot and fresh.`;
  }

  const itemsListEl = document.getElementById("token-items-list");
  if (itemsListEl) {
    itemsListEl.innerHTML = orderedItems.map(item => `
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span>${item.qty}x ${item.name}</span>
        <span style="font-weight:700;">₹${item.subtotal}</span>
      </div>
    `).join("");
  }

  const totalPaidEl = document.getElementById("token-total-paid");
  if (totalPaidEl) totalPaidEl.textContent = `₹${orderTotal}`;

  const tokenModal = document.getElementById("token-modal");
  if (tokenModal) tokenModal.classList.add("show");

  // Reset cart
  cart = {};
  renderDishes();
  updateCartBar();

  // Joyful student confirmation toast
  showToast(`🎉 You got the order! Token ${token} is confirmed and sent to kitchen.`, "success");
};

window.closeTokenModal = function() {
  const tokenModal = document.getElementById("token-modal");
  if (tokenModal) tokenModal.classList.remove("show");
};

/* =========================================================================
   2. AUTHENTICATION & PORTAL GATEWAYS
   ========================================================================= */

function getKitchenStaffPassword() {
  try {
    return localStorage.getItem("savitha_kitchen_pwd") || "savitha123";
  } catch (e) {
    return "savitha123";
  }
}

function setKitchenStaffPassword(newPwd) {
  try {
    localStorage.setItem("savitha_kitchen_pwd", newPwd);
  } catch (e) {}
}

function verifyKitchenPassword(inputPwd) {
  const current = getKitchenStaffPassword();
  return inputPwd.trim() === current.trim();
}

function updateKitchenPasswordDisplay() {
  const current = getKitchenStaffPassword();
  document.querySelectorAll(".staff-pwd-hint").forEach(el => {
    el.textContent = current;
  });
  const curDisp = document.getElementById("curr-pwd-disp");
  if (curDisp) curDisp.textContent = current;
}

window.togglePasswordVisibility = function(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  if (input.type === "password") {
    input.type = "text";
    if (btn) btn.textContent = "🙈";
  } else {
    input.type = "password";
    if (btn) btn.textContent = "👁️";
  }
};

function renderUserAuthSlot() {
  const slot = document.getElementById("user-auth-slot");
  if (!slot) return;

  if (currentUser && currentUser.role) {
    const isWorker = currentUser.role === "worker";
    const icon = isWorker ? "👨‍🍳" : "🎓";
    const displayName = currentUser.name || (isWorker ? "Staff" : "Student");
    slot.innerHTML = `
      <div class="user-session-chip">
        <span>${icon} ${displayName}</span>
        <button type="button" class="btn-logout-tiny" onclick="logoutUser()" title="Sign Out">Sign Out</button>
      </div>
    `;
  } else {
    slot.innerHTML = `
      <button type="button" class="theme-switch-pill" onclick="openAuthModal()" style="font-weight:700;">
        <span>👤</span> <span>Sign In</span>
      </button>
    `;
  }
}

function initUserAuth() {
  try {
    const saved = localStorage.getItem("savitha_user");
    if (saved) {
      currentUser = JSON.parse(saved);
    }
  } catch (e) {}

  renderUserAuthSlot();

  if (currentUser && currentUser.role === "worker") {
    performSwitchMode("manager");
  } else if (currentUser && currentUser.role === "student") {
    performSwitchMode("order");
  } else {
    // Open in order mode with guest access
    currentUser = { role: "student", name: "Student" };
    renderUserAuthSlot();
    performSwitchMode("order");
  }
}

window.switchLoginTab = function(tab) {
  const tabStudent = document.getElementById("login-tab-student");
  const tabWorker = document.getElementById("login-tab-worker");
  const panelStudent = document.getElementById("login-panel-student");
  const panelWorker = document.getElementById("login-panel-worker");

  if (tab === "worker") {
    if (tabStudent) tabStudent.classList.remove("active");
    if (tabWorker) tabWorker.classList.add("active");
    if (panelStudent) panelStudent.style.display = "none";
    if (panelWorker) panelWorker.style.display = "block";
    const passInput = document.getElementById("login-worker-password");
    if (passInput) passInput.focus();
  } else {
    if (tabStudent) tabStudent.classList.add("active");
    if (tabWorker) tabWorker.classList.remove("active");
    if (panelStudent) panelStudent.style.display = "block";
    if (panelWorker) panelWorker.style.display = "none";
    const nameInput = document.getElementById("login-student-name");
    if (nameInput) nameInput.focus();
  }
};

window.handlePortalStudentLogin = function(e) {
  if (e) e.preventDefault();
  const nameInput = document.getElementById("login-student-name");
  const name = nameInput && nameInput.value.trim() ? nameInput.value.trim() : "Student";

  currentUser = { role: "student", name: name };
  try {
    localStorage.setItem("savitha_user", JSON.stringify(currentUser));
  } catch (err) {}

  renderUserAuthSlot();
  performSwitchMode("order");
  showToast(`Welcome ${name}! Food menu is ready 🍛`, "success");
};

window.quickPortalStudentLogin = function() {
  currentUser = { role: "student", name: "Student" };
  try {
    localStorage.setItem("savitha_user", JSON.stringify(currentUser));
  } catch (err) {}

  renderUserAuthSlot();
  performSwitchMode("order");
  showToast("Welcome! Browsing Food Menu 🍛", "success");
};

window.handlePortalWorkerLogin = function(e) {
  if (e) e.preventDefault();
  const passInput = document.getElementById("login-worker-password");
  const password = passInput ? passInput.value.trim() : "";

  if (verifyKitchenPassword(password)) {
    currentUser = { role: "worker", name: "Kitchen Staff", username: "staff" };
    try {
      localStorage.setItem("savitha_user", JSON.stringify(currentUser));
    } catch (err) {}

    renderUserAuthSlot();
    performSwitchMode("manager");
    showToast("🔓 Kitchen Staff Verified! Kitchen AI unlocked.", "success");
  } else {
    const currentPwd = getKitchenStaffPassword();
    showToast(`⚠️ Incorrect Password! Default password is '${currentPwd}'`, "warning");
    if (passInput) passInput.focus();
  }
};

// Modal Authentication Functions (for quick role switch from within app)
window.openAuthModal = function() {
  const modal = document.getElementById("auth-modal");
  if (modal) {
    modal.classList.add("show");
    if (currentUser && currentUser.role === "worker") {
      showAuthTab("worker");
    } else {
      showAuthTab("student");
    }
  }
};

window.closeAuthModal = function() {
  const modal = document.getElementById("auth-modal");
  if (modal) modal.classList.remove("show");
};

window.showAuthTab = function(role) {
  const tabStudent = document.getElementById("tab-btn-student");
  const tabWorker = document.getElementById("tab-btn-worker");
  const paneStudent = document.getElementById("auth-tab-student");
  const paneWorker = document.getElementById("auth-tab-worker");

  if (role === "worker") {
    if (tabStudent) tabStudent.classList.remove("active");
    if (tabWorker) tabWorker.classList.add("active");
    if (paneStudent) paneStudent.style.display = "none";
    if (paneWorker) paneWorker.style.display = "block";
    const passInput = document.getElementById("worker-password-input");
    if (passInput) {
      passInput.value = "";
      passInput.focus();
    }
  } else {
    if (tabStudent) tabStudent.classList.add("active");
    if (tabWorker) tabWorker.classList.remove("active");
    if (paneStudent) paneStudent.style.display = "block";
    if (paneWorker) paneWorker.style.display = "none";
    const nameInput = document.getElementById("modal-student-name");
    if (nameInput) {
      if (currentUser && currentUser.name) nameInput.value = currentUser.name;
      nameInput.focus();
    }
  }
};

window.handleStudentFormSubmit = function(e) {
  if (e) e.preventDefault();
  const nameInput = document.getElementById("modal-student-name");
  const name = nameInput && nameInput.value.trim() ? nameInput.value.trim() : "Student";

  currentUser = { role: "student", name: name };
  try {
    localStorage.setItem("savitha_user", JSON.stringify(currentUser));
  } catch (err) {}

  closeAuthModal();
  renderUserAuthSlot();
  performSwitchMode("order");
  showToast(`Welcome ${name}! Food menu is ready 🍛`, "success");
};

window.quickGatewayStudentLogin = function() {
  quickPortalStudentLogin();
};

window.handleGatewayStudentLogin = function(e) {
  handlePortalStudentLogin(e);
};

window.handleStudentLogin = function(e) {
  handlePortalStudentLogin(e);
};

window.quickStudentLogin = function() {
  quickPortalStudentLogin();
};

window.handleWorkerLogin = function(e) {
  if (e) e.preventDefault();
  const passInput = document.getElementById("worker-password-input");
  const password = passInput ? passInput.value.trim() : "";

  if (verifyKitchenPassword(password)) {
    currentUser = { role: "worker", name: "Kitchen Staff", username: "staff" };
    try {
      localStorage.setItem("savitha_user", JSON.stringify(currentUser));
    } catch (err) {}
    closeAuthModal();
    renderUserAuthSlot();
    performSwitchMode("manager");
    showToast("🔓 Kitchen Staff Verified! Kitchen AI unlocked.", "success");
  } else {
    const currentPwd = getKitchenStaffPassword();
    showToast(`⚠️ Incorrect Password! Use kitchen password: '${currentPwd}'`, "warning");
    if (passInput) passInput.focus();
  }
};

window.handleGatewayWorkerLogin = function(e) {
  handleWorkerLogin(e);
};

window.logoutUser = function() {
  currentUser = null;
  localStorage.removeItem("savitha_user");
  renderUserAuthSlot();
  performSwitchMode("order");
  showToast("Logged out successfully.", "info");
};

window.returnToGateway = function() {
  performSwitchMode("login");
};

window.handleBrandClick = function() {
  performSwitchMode("order");
};

window.switchMainMode = function(mode) {
  if (mode === "manager") {
    if (!currentUser || currentUser.role !== "worker") {
      openAuthModal();
      showAuthTab("worker");
      return;
    }
  }
  performSwitchMode(mode);
};

function performSwitchMode(mode) {
  const toggle = document.getElementById("main-view-toggle");
  const cartBtn = document.getElementById("header-cart-btn");
  const btnOrder = document.getElementById("btn-mode-order");
  const btnMgr = document.getElementById("btn-mode-manager");
  const viewLogin = document.getElementById("view-login");
  const viewOrder = document.getElementById("view-order");
  const viewMgr = document.getElementById("view-manager");
  const floatingBar = document.getElementById("cart-floating-bar");

  if (btnOrder) btnOrder.classList.remove("active");
  if (btnMgr) btnMgr.classList.remove("active");

  if (viewLogin) viewLogin.style.display = "none";
  if (viewOrder) viewOrder.style.display = "none";
  if (viewMgr) {
    viewMgr.style.display = "none";
    viewMgr.classList.remove("show");
  }

  if (mode === "manager") {
    if (toggle) toggle.style.display = "flex";
    if (cartBtn) cartBtn.style.display = "none";
    if (btnMgr) btnMgr.classList.add("active");
    if (floatingBar) floatingBar.classList.remove("show");

    if (viewMgr) {
      viewMgr.style.display = "block";
      viewMgr.classList.add("show");
      viewMgr.style.animation = "fadeIn 0.25s ease-out";
    }
    switchManagerTab("orders");
  } else {
    // default to food menu ("order")
    if (toggle) toggle.style.display = "flex";
    if (cartBtn) cartBtn.style.display = "flex";
    if (btnOrder) btnOrder.classList.add("active");

    if (viewOrder) {
      viewOrder.style.display = "block";
      viewOrder.style.animation = "fadeIn 0.25s ease-out";
    }
    updateCartBar();
  }

  window.scrollTo({ top: 0, behavior: "smooth" });
}

/* =========================================================================
   3. CANTEEN MANAGER AI PREDICTOR LOGIC & LIVE ORDERS
   ========================================================================= */

window.switchManagerTab = function(tabName) {
  const tabs = ["calc", "orders", "dailyplan", "stats", "hist", "viva", "pwd"];
  tabs.forEach(t => {
    const btn = document.getElementById(`subtab-${t}-btn`);
    const pane = document.getElementById(`manager-pane-${t}`);
    if (t === tabName) {
      if (btn) btn.classList.add("active");
      if (pane) pane.style.display = "block";
    } else {
      if (btn) btn.classList.remove("active");
      if (pane) pane.style.display = "none";
    }
  });

  if (tabName === "orders") {
    renderLiveOrders();
  } else if (tabName === "dailyplan") {
    generateFullDailyPlan();
  } else if (tabName === "hist") {
    renderHistoryTable();
  } else if (tabName === "pwd") {
    updateKitchenPasswordDisplay();
  }
};

/* --- Live Orders Management for Kitchen --- */
function updateLiveOrderBadge() {
  const badge = document.getElementById("live-order-badge");
  if (badge) {
    const activeCount = liveOrders.filter(o => !o.status.includes("Picked")).length;
    badge.textContent = activeCount;
    badge.style.display = activeCount > 0 ? "inline-block" : "none";
  }
}

window.renderLiveOrders = function(filter = "all") {
  const container = document.getElementById("live-orders-container");
  if (!container) return;

  let filtered = liveOrders;
  if (filter === "prep") {
    filtered = liveOrders.filter(o => o.status.includes("Preparing"));
  } else if (filter === "ready") {
    filtered = liveOrders.filter(o => o.status.includes("Ready"));
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="grid-column:1/-1; text-align:center; padding:40px 20px; color:var(--text-muted); background:#f8fafc; border-radius:14px; border:1.5px dashed #cbd5e1;">
        <div style="font-size:2.6rem; margin-bottom:8px;">🔔</div>
        <div style="font-weight:800; font-size:1.1rem; color:var(--text-main); margin-bottom:4px;">No orders in this filter</div>
        <div style="font-size:0.88rem;">When students place orders, you will immediately get the order notification here!</div>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(order => `
    <div class="order-live-card ${order.status.includes('Ready') ? 'order-ready' : 'order-preparing'}">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">
        <div>
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.45rem; font-weight:900; color:#ea580c;">${order.token}</span>
            <span style="font-size:0.95rem; font-weight:700; color:var(--text-main);">${order.customerName}</span>
          </div>
          <div style="font-size:0.8rem; color:var(--text-muted); margin-top:2px;">Ordered at ${order.time}</div>
        </div>
        <span class="order-status-badge ${order.status.includes('Ready') ? 'badge-ready' : 'badge-prep'}">
          ${order.status}
        </span>
      </div>
      <div style="background:#f8fafc; border-radius:8px; padding:10px 12px; margin-bottom:12px; font-size:0.88rem;">
        ${order.items.map(it => `
          <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
            <span>${it.qty}x ${it.name}</span>
            <strong style="color:var(--text-main);">₹${it.subtotal || (it.price * it.qty)}</strong>
          </div>
        `).join('')}
        <div style="border-top:1px dashed #e2e8f0; margin-top:6px; padding-top:6px; display:flex; justify-content:space-between; font-weight:800;">
          <span>Total</span>
          <span style="color:var(--primary);">₹${order.total}</span>
        </div>
      </div>
      <div style="display:flex; gap:8px;">
        ${order.status.includes('Ready')
          ? `<button type="button" class="btn-order-action btn-completed" onclick="markOrderCompleted('${order.id}')">✓ Mark Picked Up</button>`
          : `<button type="button" class="btn-order-action btn-ready" onclick="markOrderReady('${order.id}')">✅ Mark Ready for Pickup</button>`
        }
      </div>
    </div>
  `).join("");
};

window.filterLiveOrders = function(type, btn) {
  document.querySelectorAll("#manager-pane-orders .clickable-pill").forEach(p => p.classList.remove("active"));
  if (btn) btn.classList.add("active");
  renderLiveOrders(type);
};

window.markOrderReady = function(orderId) {
  const order = liveOrders.find(o => o.id === orderId);
  if (order) {
    order.status = "Ready at Counter! ✅";
    try { localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders)); } catch (e) {}
    renderLiveOrders();
    updateLiveOrderBadge();
    showToast(`Order ${order.token} for ${order.customerName} marked READY at counter!`, "success");
  }
};

window.markOrderCompleted = function(orderId) {
  liveOrders = liveOrders.filter(o => o.id !== orderId);
  try { localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders)); } catch (e) {}
  renderLiveOrders();
  updateLiveOrderBadge();
  showToast("Order marked picked up & completed! 🍽️", "info");
};

window.clearAllLiveOrders = function() {
  if (confirm("Clear all active live orders?")) {
    liveOrders = [];
    try { localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders)); } catch (e) {}
    renderLiveOrders();
    updateLiveOrderBadge();
    showToast("Live orders queue cleared.", "info");
  }
};

/* --- Simplified 1-Click AI Kitchen Functions --- */

window.selectKitchenDish = function(dishName, btn) {
  document.querySelectorAll(".dish-select-btn").forEach(b => b.classList.remove("active"));
  if (btn) btn.classList.add("active");

  const foodSelect = document.getElementById("mgr_food_item");
  if (foodSelect) foodSelect.value = dishName;

  const displayEl = document.getElementById("selected-dish-display");
  if (displayEl) displayEl.textContent = `Selected: ${dishName}`;

  // Auto-fill yesterday and 7-day average from baseline dataset
  if (window.FoodMLClientEngine) {
    const d = window.FoodMLClientEngine.getItemDefaults(dishName);
    const prevDayInput = document.getElementById("mgr_prev_day");
    const prevWeekInput = document.getElementById("mgr_prev_week");
    if (prevDayInput) prevDayInput.value = d.prevDay;
    if (prevWeekInput) prevWeekInput.value = d.prevWeek;
  }

  // Automatically calculate instantly!
  runEasyKitchenPrediction();
};

window.autoRecalculateKitchen = function() {
  runEasyKitchenPrediction();
};

window.runEasyKitchenPrediction = async function() {
  const foodSelect = document.getElementById("mgr_food_item");
  const weatherEl = document.getElementById("mgr_weather");
  const eventEl = document.getElementById("mgr_event");
  const daySelect = document.getElementById("mgr_day");
  const prevDayInput = document.getElementById("mgr_prev_day");
  const prevWeekInput = document.getElementById("mgr_prev_week");
  const holidayInput = document.getElementById("mgr_holiday");
  const dateInput = document.getElementById("mgr_date");

  const dishName = foodSelect ? foodSelect.value : "Veg Biryani";
  const payload = {
    food_item: dishName,
    date: dateInput && dateInput.value ? dateInput.value : new Date().toISOString().split("T")[0],
    day_of_week: daySelect ? daySelect.value : "Tuesday",
    weather: weatherEl ? weatherEl.value : "Sunny",
    is_holiday: parseInt(holidayInput ? holidayInput.value : 0) || 0,
    special_event: eventEl ? eventEl.value : "None",
    previous_day_sales: parseInt(prevDayInput ? prevDayInput.value : 140) || 140,
    previous_week_sales: parseInt(prevWeekInput ? prevWeekInput.value : 140) || 140
  };

  const btn = document.getElementById("mgr-predict-btn");
  if (btn) {
    btn.innerHTML = `<span>⏳</span> Calculating What to Cook...`;
  }

  let result = null;
  if (isBackendConnected) {
    try {
      const res = await fetch(`${API_BASE}/api/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        result = await res.json();
      }
    } catch (err) {
      console.warn("Falling back to client ML engine:", err);
    }
  }

  if (!result || result.status !== "success") {
    if (window.FoodMLClientEngine) {
      result = window.FoodMLClientEngine.predict(payload);
    }
  }

  if (result) {
    displayManagerResult(result);
    saveHistoryEntry(result);
  }

  if (btn) {
    btn.innerHTML = `<span>👨‍🍳</span> Calculate What to Cook`;
  }
};

/* --- Full Daily Menu Preparation Board (All Dishes at Once) --- */
window.generateFullDailyPlan = function() {
  const container = document.getElementById("daily-plan-board");
  if (!container || !window.FoodMLClientEngine) return;

  const weatherEl = document.getElementById("mgr_weather");
  const eventEl = document.getElementById("mgr_event");
  const daySelect = document.getElementById("mgr_day");

  const weather = weatherEl ? weatherEl.value : "Sunny";
  const event = eventEl ? eventEl.value : "None";
  const day = daySelect ? daySelect.value : "Tuesday";

  const allItems = window.FoodMLClientEngine.getAllItems();
  let totalMeals = 0;

  const results = allItems.map(item => {
    const defaults = window.FoodMLClientEngine.getItemDefaults(item);
    const pred = window.FoodMLClientEngine.predict({
      food_item: item,
      day_of_week: day,
      weather: weather,
      special_event: event,
      is_holiday: 0,
      previous_day_sales: defaults.prevDay,
      previous_week_sales: defaults.prevWeek
    });
    totalMeals += pred.recommended_portions;
    const dishObj = DISHES.find(d => d.name === item);
    return { item, pred, dishObj };
  });

  container.innerHTML = results.map(r => `
    <div class="plan-card">
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <div>
          <span style="font-size:1.6rem; display:block; margin-bottom:4px;">${r.dishObj ? r.dishObj.image ? '' : '🍽️' : '🍽️'}</span>
          <h3 style="font-size:1.1rem; font-weight:800; color:var(--text-main); margin:0;">${r.item}</h3>
          <span style="font-size:0.78rem; color:var(--text-muted); font-weight:600;">${r.dishObj ? r.dishObj.category.toUpperCase() : 'CANTEEN'}</span>
        </div>
        <span style="background:#fff7ed; color:#ea580c; font-size:0.75rem; font-weight:800; padding:4px 8px; border-radius:6px;">
          +${r.pred.buffer_portions} buffer
        </span>
      </div>

      <div style="background:#f8fafc; border-radius:10px; padding:12px; text-align:center;">
        <div style="font-size:0.75rem; font-weight:700; color:var(--text-muted); text-transform:uppercase;">Cook Quantity</div>
        <div style="font-size:2.2rem; font-weight:900; color:#ea580c; line-height:1.1; margin:4px 0;">${r.pred.recommended_portions}</div>
        <div style="font-size:0.8rem; color:var(--text-muted);">plates to prepare</div>
      </div>

      <div style="font-size:0.82rem; color:#166534; background:#f0fdf4; padding:8px 10px; border-radius:8px;">
        👥 Expected Demand: ~${r.pred.predicted_quantity} plates
      </div>
    </div>
  `).join("");
};

function initManagerDefaults() {
  const dateInput = document.getElementById("mgr_date");
  const daySelect = document.getElementById("mgr_day");
  const foodSelect = document.getElementById("mgr_food_item");
  const prevDayInput = document.getElementById("mgr_prev_day");
  const prevWeekInput = document.getElementById("mgr_prev_week");
  const holidayInput = document.getElementById("mgr_holiday");

  const today = new Date();
  if (dateInput) {
    dateInput.value = today.toISOString().split("T")[0];
    const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const dayName = days[today.getDay()];
    if (daySelect) daySelect.value = dayName;
    if (holidayInput) holidayInput.value = (dayName === "Saturday" || dayName === "Sunday") ? "1" : "0";
  }

  // Pre-calculate first dish (Veg Biryani) so the kitchen sees instant result
  setTimeout(() => {
    runEasyKitchenPrediction();
  }, 400);
}

/* =========================================================================
   4. SYSTEM HEALTH & UTILITIES
   ========================================================================= */

async function checkServerHealth() {
  const pill = document.getElementById("backend-status");
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 1200);
    const res = await fetch(`${API_BASE}/api/health`, { signal: controller.signal });
    clearTimeout(timeoutId);
    if (res.ok) {
      isBackendConnected = true;
      if (pill) {
        pill.innerHTML = "● Kitchen API Online";
        pill.style.background = "#dcfce7";
        pill.style.color = "#16a34a";
      }
      return;
    }
  } catch (e) {}

  isBackendConnected = false;
  if (pill) {
    if (window.FoodMLClientEngine) {
      pill.innerHTML = "● AI Engine Online";
      pill.style.background = "#dcfce7";
      pill.style.color = "#16a34a";
    } else {
      pill.innerHTML = "● Kitchen Ready";
      pill.style.background = "#fff2ea";
      pill.style.color = "#ea580c";
    }
  }
}

function showToast(message, type = "info") {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = "fadeOut 0.3s ease-out forwards";
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

function loadHistory() {
  try {
    const saved = localStorage.getItem("canteen_history");
    historyRecords = saved ? JSON.parse(saved) : [];
  } catch (e) {
    historyRecords = [];
  }
}

function renderHistoryTable() {
  const tbody = document.getElementById("history-table-body");
  if (!tbody) return;

  if (historyRecords.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:var(--text-muted); padding:20px;">No calculation history recorded yet. Run a prediction to save records!</td></tr>`;
    return;
  }

  let html = "";
  historyRecords.slice(-15).reverse().forEach(r => {
    html += `
      <tr>
        <td>${r.date || "N/A"}</td>
        <td><strong>${r.food_item || "N/A"}</strong></td>
        <td>${r.predicted_portions || 0}</td>
        <td>${r.batch_prep_kg || 0} kg</td>
        <td>${r.weather || "N/A"}</td>
        <td>${r.is_holiday ? "Yes" : "No"}</td>
        <td><span class="status-pill status-ready" style="font-size:0.75rem;">Verified</span></td>
      </tr>
    `;
  });
  tbody.innerHTML = html;
}

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initUserAuth();
  updateKitchenPasswordDisplay();
  renderDishes();
  initManagerDefaults();
  updateLiveOrderBadge();
  loadHistory();
  checkServerHealth();
  setInterval(checkServerHealth, 12000);
});
