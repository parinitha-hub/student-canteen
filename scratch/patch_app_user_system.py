import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app_path = os.path.join(ROOT, "js", "app.js")
frontend_app_path = os.path.join(ROOT, "frontend", "js", "app.js")

with open(app_path, "r", encoding="utf-8") as f:
    code = f.read()

# -----------------------------------------------------------------------------
# 1. USER ACCOUNTS & DATA ISOLATION ENGINE
# -----------------------------------------------------------------------------
user_engine = """
// =========================================================================
// USER-SPECIFIC ACCOUNTS, CREDENTIALS & ISOLATED DATA STORE
// =========================================================================
const DEFAULT_ACCOUNTS = [
  {
    id: "usr_srinath",
    username: "SAV101",
    password: "pass123",
    name: "Srinath Kumar",
    year: "3rd Year CSE",
    phone: "9876543210",
    role: "student"
  },
  {
    id: "usr_divya",
    username: "SAV102",
    password: "pass123",
    name: "Divya Krishnan",
    year: "Final Year IT",
    phone: "9876543211",
    role: "student"
  },
  {
    id: "usr_aarav",
    username: "SAV103",
    password: "pass123",
    name: "Aarav Menon",
    year: "2nd Year ECE",
    phone: "9876543212",
    role: "student"
  },
  {
    id: "usr_staff",
    username: "staff",
    password: "savi123",
    name: "Kitchen Staff",
    year: "Campus Dining",
    phone: "9876543200",
    role: "worker"
  }
];

function getAccounts() {
  try {
    const raw = localStorage.getItem("savitha_user_accounts");
    if (raw) {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed) && parsed.length > 0) return parsed;
    }
  } catch (e) {}
  saveAccounts(DEFAULT_ACCOUNTS);
  return DEFAULT_ACCOUNTS;
}

function saveAccounts(accounts) {
  try {
    localStorage.setItem("savitha_user_accounts", JSON.stringify(accounts));
  } catch (e) {}
}

function findAccount(identifier) {
  const accounts = getAccounts();
  const u = String(identifier || "").trim().toUpperCase();
  return accounts.find(a => a.username.toUpperCase() === u || a.name.toUpperCase() === u || a.id.toUpperCase() === u) || null;
}

function switchStudentAuthMode(mode) {
  const btnSignIn = document.getElementById("subtab-auth-signin");
  const btnRegister = document.getElementById("subtab-auth-register");
  const formSignIn = document.getElementById("student-signin-form");
  const formRegister = document.getElementById("student-register-form");

  if (mode === "register") {
    if (btnSignIn) {
      btnSignIn.style.background = "transparent";
      btnSignIn.style.color = "var(--text-muted)";
      btnSignIn.style.boxShadow = "none";
    }
    if (btnRegister) {
      btnRegister.style.background = "#ffffff";
      btnRegister.style.color = "#10b981";
      btnRegister.style.boxShadow = "0 1px 3px rgba(0,0,0,0.1)";
    }
    if (formSignIn) formSignIn.style.display = "none";
    if (formRegister) formRegister.style.display = "block";
    const nameInp = document.getElementById("register-student-name");
    if (nameInp) nameInp.focus();
  } else {
    if (btnSignIn) {
      btnSignIn.style.background = "#ffffff";
      btnSignIn.style.color = "var(--primary)";
      btnSignIn.style.boxShadow = "0 1px 3px rgba(0,0,0,0.1)";
    }
    if (btnRegister) {
      btnRegister.style.background = "transparent";
      btnRegister.style.color = "var(--text-muted)";
      btnRegister.style.boxShadow = "none";
    }
    if (formSignIn) formSignIn.style.display = "block";
    if (formRegister) formRegister.style.display = "none";
    const userInp = document.getElementById("login-student-username");
    if (userInp) userInp.focus();
  }
}

function fillDemoStudent(username, password) {
  switchStudentAuthMode("signin");
  const userInp = document.getElementById("login-student-username");
  const passInp = document.getElementById("login-student-password");
  if (userInp) userInp.value = username;
  if (passInp) passInp.value = password;
  showToast(`Loaded test account ${username}. Click Sign In to log in!`, "info");
}

function loadUserData(user) {
  if (!user || !user.id) {
    cart = {};
    myOrders = [];
    activeCoupon = null;
    return;
  }

  // Load user's private cart
  try {
    const userCartRaw = localStorage.getItem(`savitha_cart_${user.id}`);
    cart = userCartRaw ? JSON.parse(userCartRaw) : {};
  } catch (e) {
    cart = {};
  }

  // Load user's private orders
  try {
    const userOrdersRaw = localStorage.getItem(`savitha_my_orders_${user.id}`);
    myOrders = userOrdersRaw ? JSON.parse(userOrdersRaw) : [];
  } catch (e) {
    myOrders = [];
  }

  // Synchronize any matching orders from liveOrders
  if (Array.isArray(liveOrders)) {
    const matching = liveOrders.filter(o => o.userId === user.id || o.username === user.username);
    matching.forEach(ord => {
      if (!myOrders.some(m => m.id === ord.id)) {
        myOrders.unshift(ord);
      }
    });
  }

  lastPlacedOrder = myOrders.length > 0 ? myOrders[0] : null;

  updateCartBar();
  updateMyOrdersCount();
  renderLoyaltyStampCard();
  renderMyOrdersList();
}

function saveUserData() {
  if (!currentUser || !currentUser.id) return;
  try {
    localStorage.setItem(`savitha_cart_${currentUser.id}`, JSON.stringify(cart));
    localStorage.setItem(`savitha_my_orders_${currentUser.id}`, JSON.stringify(myOrders));
  } catch (e) {}
}

function loginUser(userAccount) {
  currentUser = userAccount;
  try {
    localStorage.setItem("savitha_user", JSON.stringify(currentUser));
  } catch (e) {}

  // Load user's isolated data store
  loadUserData(currentUser);

  renderUserAuthSlot();
  applyRoleVisibility();

  if (currentUser.role === "worker") {
    performSwitchMode("manager");
  } else {
    performSwitchMode("order");
    renderDishes();
  }
}

function handleStudentSignIn(e) {
  if (e) {
    try { e.preventDefault(); } catch (err) {}
    try { e.stopPropagation(); } catch (err) {}
  }
  const userInp = document.getElementById("login-student-username");
  const passInp = document.getElementById("login-student-password");
  const username = userInp ? userInp.value.trim() : "";
  const password = passInp ? passInp.value.trim() : "";

  if (!username) {
    showToast("⚠️ Please enter your Student ID or Username!", "warning");
    if (userInp) userInp.focus();
    return false;
  }
  if (!password) {
    showToast("⚠️ Please enter your account password!", "warning");
    if (passInp) passInp.focus();
    return false;
  }

  const account = findAccount(username);
  if (!account || account.password !== password) {
    showToast("❌ Invalid Student ID or password! Please check credentials or register.", "warning");
    if (passInp) {
      passInp.style.borderColor = "#ef4444";
      setTimeout(() => { if (passInp) passInp.style.borderColor = ""; }, 2500);
    }
    return false;
  }

  loginUser(account);
  showToast(`Welcome back, ${account.name}! Logged into ${account.username}.`, "success");
  return false;
}

function handleStudentRegister(e) {
  if (e) {
    try { e.preventDefault(); } catch (err) {}
    try { e.stopPropagation(); } catch (err) {}
  }
  const nameInp = document.getElementById("register-student-name");
  const userInp = document.getElementById("register-student-username");
  const yearInp = document.getElementById("register-student-year");
  const phoneInp = document.getElementById("register-student-phone");
  const passInp = document.getElementById("register-student-password");

  const name = nameInp ? nameInp.value.trim() : "";
  const username = userInp ? userInp.value.trim().toUpperCase() : "";
  const year = yearInp ? yearInp.value : "1st Year";
  const phone = phoneInp ? phoneInp.value.trim() : "";
  const password = passInp ? passInp.value.trim() : "";

  if (!name) {
    showToast("⚠️ Please enter your full name!", "warning");
    if (nameInp) nameInp.focus();
    return false;
  }
  if (!username) {
    showToast("⚠️ Please enter a Student ID / Roll No!", "warning");
    if (userInp) userInp.focus();
    return false;
  }
  if (!password || password.length < 3) {
    showToast("⚠️ Password must be at least 3 characters long!", "warning");
    if (passInp) passInp.focus();
    return false;
  }

  if (findAccount(username)) {
    showToast(`⚠️ Account with ID '${username}' already exists. Please sign in!`, "warning");
    switchStudentAuthMode("signin");
    const uInp = document.getElementById("login-student-username");
    if (uInp) uInp.value = username;
    return false;
  }

  const newAccount = {
    id: "usr_" + username.toLowerCase().replace(/[^a-z0-9]/g, ""),
    username: username,
    password: password,
    name: name,
    year: year,
    phone: phone,
    role: "student",
    created_at: new Date().toISOString()
  };

  const accounts = getAccounts();
  accounts.push(newAccount);
  saveAccounts(accounts);

  // Sync to backend if available
  try {
    fetch(`${API_BASE}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newAccount)
    }).catch(() => {});
  } catch (e) {}

  loginUser(newAccount);
  showToast(`🎉 Account created successfully! Welcome to Savitha Canteen, ${name}.`, "success");
  return false;
}

function openProfileModal() {
  if (!currentUser || !currentUser.role) {
    showToast("Please login first to view your profile.", "warning");
    performSwitchMode("login");
    return;
  }

  const modal = document.getElementById("profile-modal");
  const body = document.getElementById("profile-modal-body");
  if (!modal || !body) return;

  const isWorker = currentUser.role === "worker";
  const icon = isWorker ? "👨‍🍳" : "🎓";
  const totalOrders = myOrders.length;
  const streak = parseInt(localStorage.getItem(`savitha_streak_${currentUser.id}`) || String(totalOrders), 10);
  const activeOrdersCount = myOrders.filter(o => o.status === "Cooking").length;

  body.innerHTML = `
    <div style="text-align:center; padding:10px 0 16px 0; border-bottom:1px solid var(--border);">
      <div style="width:68px; height:68px; border-radius:50%; background:linear-gradient(135deg, #4f46e5 0%, #818cf8 100%); color:#fff; font-size:2rem; display:inline-flex; align-items:center; justify-content:center; margin-bottom:10px; box-shadow:0 4px 12px rgba(79, 70, 229, 0.25);">
        ${icon}
      </div>
      <h3 style="font-size:1.25rem; font-weight:900; color:var(--text-main); margin:0;">${currentUser.name || "Student"}</h3>
      <div style="font-size:0.84rem; color:var(--primary); font-weight:800; margin-top:2px;">
        Account ID: ${currentUser.username || currentUser.id || "SAV101"}
      </div>
      <div style="display:inline-block; font-size:0.75rem; background:#e0e7ff; color:#3730a3; padding:2px 10px; border-radius:999px; font-weight:800; margin-top:6px;">
        ${isWorker ? "Kitchen Staff Member" : "Registered Student Account"}
      </div>
    </div>

    <div style="padding:14px 0; font-size:0.88rem;">
      <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px dashed #e2e8f0;">
        <span style="color:var(--text-muted);">Department / Year:</span>
        <strong style="color:var(--text-main);">${currentUser.year || "3rd Year"}</strong>
      </div>
      <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px dashed #e2e8f0;">
        <span style="color:var(--text-muted);">Mobile Number:</span>
        <strong style="color:var(--text-main);">${currentUser.phone || "Not specified"}</strong>
      </div>
      <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px dashed #e2e8f0;">
        <span style="color:var(--text-muted);">Total Orders Placed:</span>
        <strong style="color:var(--primary);">${totalOrders} orders</strong>
      </div>
      <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px dashed #e2e8f0;">
        <span style="color:var(--text-muted);">Loyalty Stamp Streak:</span>
        <strong style="color:#059669;">${streak % 10} / 10 Orders</strong>
      </div>
      <div style="display:flex; justify-content:space-between; padding:8px 0;">
        <span style="color:var(--text-muted);">Active In-Kitchen Orders:</span>
        <strong style="color:${activeOrdersCount > 0 ? '#ea580c' : 'var(--text-main)'};">${activeOrdersCount} active</strong>
      </div>
    </div>

    <div style="display:flex; gap:10px; margin-top:6px;">
      ${!isWorker ? `
        <button type="button" class="btn-hero-primary" onclick="closeProfileModal(); openMyOrdersModal();"
          style="flex:1; padding:10px; font-size:0.86rem; border-radius:10px; justify-content:center;">
          📦 View My Orders (${totalOrders})
        </button>
      ` : ''}
      <button type="button" class="btn-banner-cancel" onclick="logoutUser();"
        style="flex:1; padding:10px; font-size:0.86rem; background:#fee2e2; border:1.5px solid #fca5a5; color:#dc2626; border-radius:10px; font-weight:800; cursor:pointer; justify-content:center;">
        Sign Out
      </button>
    </div>
  `;

  modal.classList.add("show");
}

function closeProfileModal() {
  const modal = document.getElementById("profile-modal");
  if (modal) modal.classList.remove("show");
}
"""

if "function switchStudentAuthMode(" not in code:
    code = code.replace(
        "// 6. AUTHENTICATION & LOGIN PORTAL",
        user_engine + "\n// 6. AUTHENTICATION & LOGIN PORTAL"
    )
    print("Added User Management Engine to js/app.js")

# -----------------------------------------------------------------------------
# 2. UPDATE handlePortalStudentLogin FOR BACKWARD COMPATIBILITY
# -----------------------------------------------------------------------------
old_handle_student_login = '''function handlePortalStudentLogin(e) {
  if (e) {
    try { e.preventDefault(); } catch (err) {}
    try { e.stopPropagation(); } catch (err) {}
  }
  const nameInput = document.getElementById("login-student-name");
  const yearInput = document.getElementById("login-student-year");
  const phoneInput = document.getElementById("login-student-phone");

  const name = nameInput && nameInput.value.trim() ? nameInput.value.trim() : "";
  if (!name) {
    showToast("⚠️ Please enter your full name to login!", "warning");
    if (nameInput) nameInput.focus();
    return false;
  }

  const year = yearInput && yearInput.value ? yearInput.value : "1st Year";
  const phone = phoneInput && phoneInput.value.trim() ? phoneInput.value.trim() : "";

  currentUser = { role: "student", name: name, year: year, phone: phone };
  try {
    localStorage.setItem("savitha_user", JSON.stringify(currentUser));
  } catch (err) {}

  renderUserAuthSlot();
  applyRoleVisibility();
  performSwitchMode("order");
  renderDishes();
  showToast(`Welcome ${name}! (${year}) Food menu is ready 🍛`, "success");
  return false;
}'''

new_handle_student_login = '''function handlePortalStudentLogin(e) {
  if (e) {
    try { e.preventDefault(); } catch (err) {}
    try { e.stopPropagation(); } catch (err) {}
  }
  const userInp = document.getElementById("login-student-username");
  const passInp = document.getElementById("login-student-password");
  if (userInp && userInp.value.trim()) {
    return handleStudentSignIn(e);
  }

  const nameInput = document.getElementById("login-student-name");
  const yearInput = document.getElementById("login-student-year");
  const phoneInput = document.getElementById("login-student-phone");

  const name = nameInput && nameInput.value.trim() ? nameInput.value.trim() : "";
  if (!name) {
    showToast("⚠️ Please enter your Student ID or Name to login!", "warning");
    if (userInp) userInp.focus();
    return false;
  }

  let account = findAccount(name);
  if (!account) {
    const year = yearInput && yearInput.value ? yearInput.value : "1st Year";
    const phone = phoneInput && phoneInput.value.trim() ? phoneInput.value.trim() : "";
    account = {
      id: "usr_" + name.toLowerCase().replace(/[^a-z0-9]/g, ""),
      username: name.toUpperCase().slice(0, 8),
      password: "pass123",
      name: name,
      year: year,
      phone: phone,
      role: "student"
    };
    const accounts = getAccounts();
    accounts.push(account);
    saveAccounts(accounts);
  }

  loginUser(account);
  showToast(`Welcome ${account.name}! (${account.year}) Food menu is ready 🍛`, "success");
  return false;
}'''

if old_handle_student_login in code:
    code = code.replace(old_handle_student_login, new_handle_student_login)
    print("Updated handlePortalStudentLogin with user-specific account resolution.")

# -----------------------------------------------------------------------------
# 3. UPDATE logoutUser TO SECURELY CLEAR SESSION & PREVENT DATA LEAKS
# -----------------------------------------------------------------------------
old_logout = '''function logoutUser() {
  currentUser = null;
  try {
    localStorage.removeItem("savitha_user");
  } catch (err) {}

  renderUserAuthSlot();
  applyRoleVisibility();
  performSwitchMode("about");
  showToast("Logged out successfully. Thank you for visiting Savitha Canteen!", "info");
}'''

new_logout = '''function logoutUser() {
  saveUserData();
  currentUser = null;
  cart = {};
  myOrders = [];
  lastPlacedOrder = null;
  activeCoupon = null;

  try {
    localStorage.removeItem("savitha_user");
  } catch (err) {}

  renderUserAuthSlot();
  applyRoleVisibility();
  updateCartBar();
  updateMyOrdersCount();
  renderLoyaltyStampCard();
  closeMyOrdersModal();
  closeCartModal();
  closeTokenModal();
  closeProfileModal();

  performSwitchMode("about");
  showToast("Logged out securely. Session ended.", "info");
}'''

if old_logout in code:
    code = code.replace(old_logout, new_logout)
    print("Updated logoutUser to cleanly clear in-memory state.")

# -----------------------------------------------------------------------------
# 4. UPDATE renderUserAuthSlot TO SHOW USER ID BADGE & PROFILE LINK
# -----------------------------------------------------------------------------
old_auth_slot = '''  if (currentUser && currentUser.role && !currentUser.isGuest && !isLoginPage) {
    const isWorker = currentUser.role === "worker";
    const icon = isWorker ? "👨‍🍳" : "🎓";
    const displayName = currentUser.name || (isWorker ? "Staff" : "Student");
    slot.innerHTML = `
      <div class="user-session-chip">
        <span>${icon} ${displayName}</span>
        <button type="button" class="btn-logout-tiny" onclick="logoutUser()" title="Sign Out">Sign Out</button>
      </div>
    `;'''

new_auth_slot = '''  if (currentUser && currentUser.role && !currentUser.isGuest && !isLoginPage) {
    const isWorker = currentUser.role === "worker";
    const icon = isWorker ? "👨‍🍳" : "🎓";
    const displayName = currentUser.name || (isWorker ? "Staff" : "Student");
    const idBadge = currentUser.username ? `<span style="font-size:0.72rem; background:rgba(255,255,255,0.22); padding:1px 6px; border-radius:4px; font-weight:800;">${currentUser.username}</span>` : '';
    slot.innerHTML = `
      <div class="user-session-chip" onclick="openProfileModal()" style="cursor:pointer;" title="View Your Profile">
        <span style="display:inline-flex; align-items:center; gap:6px;">${icon} ${displayName} ${idBadge}</span>
        <button type="button" class="btn-logout-tiny" onclick="event.stopPropagation(); logoutUser()" title="Sign Out">Sign Out</button>
      </div>
    `;'''

if old_auth_slot in code:
    code = code.replace(old_auth_slot, new_auth_slot)
    print("Updated renderUserAuthSlot with profile link and username badge.")

# -----------------------------------------------------------------------------
# 5. UPDATE renderMyOrdersList TO FILTER STRICTLY BY CURRENT USER
# -----------------------------------------------------------------------------
old_my_orders_render = '''function renderMyOrdersList() {
  const container = document.getElementById("my-orders-list-container");
  if (!container) return;

  if (myOrders.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:32px 16px; background:#f8fafc; border-radius:12px; border:1px dashed var(--border);">
        <div style="font-size:2.4rem; margin-bottom:8px;">🍽️</div>
        <div style="font-size:1.05rem; font-weight:800; color:var(--text-main);">No active orders yet</div>
        <p style="font-size:0.84rem; color:var(--text-muted); margin:4px 0 14px 0;">Select your dishes from the menu to get your digital pickup token!</p>
        <button type="button" class="btn-hero-primary" onclick="closeMyOrdersModal(); performSwitchMode('order');" style="padding:8px 18px; font-size:0.88rem; border-radius:999px;">
          Browse Food Menu
        </button>
      </div>
    `;
    return;
  }'''

new_my_orders_render = '''function renderMyOrdersList() {
  const container = document.getElementById("my-orders-list-container");
  if (!container) return;

  // Strict user-specific isolation: Only display orders belonging to the currently logged in user!
  const userOrders = (!currentUser || !currentUser.id) 
    ? [] 
    : myOrders.filter(ord => ord.userId === currentUser.id || ord.username === currentUser.username || (ord.customer && ord.customer === currentUser.name && ord.userId === currentUser.id));

  if (userOrders.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:32px 16px; background:#f8fafc; border-radius:12px; border:1px dashed var(--border);">
        <div style="font-size:2.4rem; margin-bottom:8px;">🍽️</div>
        <div style="font-size:1.05rem; font-weight:800; color:var(--text-main);">No active orders for ${currentUser ? currentUser.name : 'you'}</div>
        <p style="font-size:0.84rem; color:var(--text-muted); margin:4px 0 14px 0;">Select your dishes from the menu to get your digital pickup token!</p>
        <button type="button" class="btn-hero-primary" onclick="closeMyOrdersModal(); performSwitchMode('order');" style="padding:8px 18px; font-size:0.88rem; border-radius:999px;">
          Browse Food Menu
        </button>
      </div>
    `;
    return;
  }'''

if old_my_orders_render in code:
    code = code.replace(old_my_orders_render, new_my_orders_render)
    code = code.replace("container.innerHTML = myOrders.map(ord => {", "container.innerHTML = userOrders.map(ord => {")
    print("Updated renderMyOrdersList with strict user-specific order isolation.")

# -----------------------------------------------------------------------------
# 6. UPDATE placeOrderAndGenerateToken TO TAG USER ID & USERNAME
# -----------------------------------------------------------------------------
old_new_order_obj = '''  const newOrder = {
    id: "ord_" + Date.now(),
    token: token,
    customer: customerName,
    customerName: customerName,
    customer_name: customerName,
    customerYear: customerYear,
    customer_year: customerYear,
    customerPhone: customerPhone,
    customer_phone: customerPhone,
    items: items,
    total: totalAmount,
    coupon: usedCoupon,
    discount: discountAmount,
    time: timeStr,
    timestamp: Date.now(),
    status: "Cooking",
    prepTime: "6-8 mins"
  };'''

new_new_order_obj = '''  const newOrder = {
    id: "ord_" + Date.now(),
    token: token,
    userId: currentUser ? currentUser.id : "usr_guest",
    user_id: currentUser ? currentUser.id : "usr_guest",
    username: currentUser ? (currentUser.username || currentUser.id) : "guest",
    customer: customerName,
    customerName: customerName,
    customer_name: customerName,
    customerYear: customerYear,
    customer_year: customerYear,
    customerPhone: customerPhone,
    customer_phone: customerPhone,
    items: items,
    total: totalAmount,
    coupon: usedCoupon,
    discount: discountAmount,
    time: timeStr,
    timestamp: Date.now(),
    status: "Cooking",
    prepTime: "6-8 mins"
  };'''

if old_new_order_obj in code:
    code = code.replace(old_new_order_obj, new_new_order_obj)
    print("Updated placeOrderAndGenerateToken with user_id and username tagging.")

# Update streak to be user-specific
code = code.replace(
    'let streak = parseInt(localStorage.getItem("savitha_user_order_count") || "0", 10);',
    'const streakKey = (currentUser && currentUser.id) ? `savitha_streak_${currentUser.id}` : "savitha_user_order_count";\n  let streak = parseInt(localStorage.getItem(streakKey) || "0", 10);'
)
code = code.replace(
    'let currentStreak = parseInt(localStorage.getItem("savitha_user_order_count") || "0", 10) + 1;\n  localStorage.setItem("savitha_user_order_count", String(currentStreak));',
    'const streakKey = (currentUser && currentUser.id) ? `savitha_streak_${currentUser.id}` : "savitha_user_order_count";\n  let currentStreak = parseInt(localStorage.getItem(streakKey) || "0", 10) + 1;\n  localStorage.setItem(streakKey, String(currentStreak));'
)
code = code.replace(
    'localStorage.setItem("savitha_user_order_count", "10");',
    'const sKey = (currentUser && currentUser.id) ? `savitha_streak_${currentUser.id}` : "savitha_user_order_count";\n  localStorage.setItem(sKey, "10");'
)

# In updateDishQty, save cart to user-specific storage
code = code.replace(
    'updateCartBar();\n}',
    'updateCartBar();\n  saveUserData();\n}'
)

# -----------------------------------------------------------------------------
# 7. ADD WINDOW EXPORTS
# -----------------------------------------------------------------------------
new_exports = """  window.getAccounts = getAccounts;
  window.saveAccounts = saveAccounts;
  window.findAccount = findAccount;
  window.switchStudentAuthMode = switchStudentAuthMode;
  window.fillDemoStudent = fillDemoStudent;
  window.handleStudentSignIn = handleStudentSignIn;
  window.handleStudentRegister = handleStudentRegister;
  window.loginUser = loginUser;
  window.loadUserData = loadUserData;
  window.saveUserData = saveUserData;
  window.openProfileModal = openProfileModal;
  window.closeProfileModal = closeProfileModal;
"""

if "window.handleStudentSignIn = handleStudentSignIn;" not in code:
    code = code.replace(
        "window.initInventory = initInventory;",
        new_exports + "  window.initInventory = initInventory;"
    )
    print("Added new user auth exports to window.")

# In initUserAuth, call loadUserData
if "loadUserData(currentUser);" not in code:
    code = code.replace(
        "currentUser = parsed;\n      }",
        "currentUser = parsed;\n        loadUserData(currentUser);\n      }"
    )
    print("Connected loadUserData to initUserAuth.")

with open(app_path, "w", encoding="utf-8") as f:
    f.write(code)

with open(frontend_app_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Saved user-specific engine in js/app.js and frontend/js/app.js successfully!")
