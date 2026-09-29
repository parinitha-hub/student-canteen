import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

def update_app_js():
    with open("js/app.js", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update initial myOrders declaration and add isOrderForUser helper
    old_init = """let myOrders = [];
try {
  const savedMy = localStorage.getItem("savitha_my_orders");
  myOrders = savedMy ? JSON.parse(savedMy) : [];
} catch (e) {
  myOrders = [];
}"""

    new_init = """// Strict user-order isolation helper: matches order by user.id or 10-digit phone
function isOrderForUser(order, user) {
  if (!order || !user) return false;
  // Match on user id
  if (user.id && (order.userId === user.id || order.user_id === user.id)) return true;
  // Match on clean 10-digit phone
  const userPhone = String(user.phone || "").replace(/\\D/g, '').slice(-10);
  const orderPhone = String(order.customerPhone || order.customer_phone || "").replace(/\\D/g, '').slice(-10);
  if (userPhone && orderPhone && userPhone.length === 10 && userPhone === orderPhone) return true;
  // Match on username only if non-empty and non-guest
  if (typeof user.username === "string" && user.username.trim() && user.username.trim() !== "guest" &&
      typeof order.username === "string" && order.username.trim() && order.username.trim() !== "guest" &&
      user.username.trim().toLowerCase() === order.username.trim().toLowerCase()) {
    return true;
  }
  return false;
}

let myOrders = [];
try {
  const savedUser = localStorage.getItem("savitha_user");
  if (savedUser) {
    const u = JSON.parse(savedUser);
    if (u && u.id) {
      const savedMy = localStorage.getItem(`savitha_my_orders_${u.id}`);
      myOrders = savedMy ? JSON.parse(savedMy) : [];
    }
  }
} catch (e) {
  myOrders = [];
}"""

    if old_init in content:
        content = content.replace(old_init, new_init, 1)
        print("✓ Successfully replaced initial myOrders and added isOrderForUser helper")
    else:
        print("✗ Could not find old_init")

    # 2. Update placeOrderAndGenerateToken to calculate arrival time and save user-scoped orders
    old_place_order_pattern = re.compile(
        r'const newOrder = \{\s*id: "ord_" \+ Date\.now\(\),.*?status: "Cooking",\s*prepTime: "6-8 mins"\s*\};',
        re.DOTALL
    )

    new_order_code = """const totalQty = items.reduce((sum, it) => sum + (it.qty || 1), 0);
  const prepMinutes = Math.min(25, Math.max(8, 8 + Math.floor(totalQty * 2)));
  const arrivalDate = new Date(now.getTime() + prepMinutes * 60000);
  const arrivalTimeStr = arrivalDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  const newOrder = {
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
    prepTime: `${prepMinutes - 2}-${prepMinutes + 2} mins`,
    arrivalTime: arrivalTimeStr,
    arrival_time: arrivalTimeStr,
    arrivalMinutes: prepMinutes,
    arrival_minutes: prepMinutes
  };"""

    if old_place_order_pattern.search(content):
        content = old_place_order_pattern.sub(new_order_code, content, count=1)
        print("✓ Successfully updated newOrder creation with arrival time")
    else:
        print("✗ Could not match old_place_order_pattern")

    # Update saving after placeOrder
    old_save_place = """  liveOrders.unshift(newOrder);
  myOrders.unshift(newOrder);
  lastPlacedOrder = newOrder;

  try {
    localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders));
    localStorage.setItem("savitha_my_orders", JSON.stringify(myOrders));
    localStorage.setItem("savitha_student_active_order", JSON.stringify(newOrder));
  } catch (e) {}"""

    new_save_place = """  liveOrders.unshift(newOrder);
  myOrders.unshift(newOrder);
  lastPlacedOrder = newOrder;

  try {
    localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders));
    if (currentUser && currentUser.id) {
      localStorage.setItem(`savitha_my_orders_${currentUser.id}`, JSON.stringify(myOrders));
    }
    localStorage.setItem("savitha_student_active_order", JSON.stringify(newOrder));
  } catch (e) {}

  saveUserData();"""

    if old_save_place in content:
        content = content.replace(old_save_place, new_save_place, 1)
        print("✓ Successfully updated order placement save block")
    else:
        print("✗ Could not find old_save_place")

    # 3. Update openTokenModal to populate arrival time elements
    old_token_modal = """    if (orderMsg) {
      orderMsg.textContent = `The kitchen is preparing order for ${target.customer || "Student"} hot and fresh.`;
    }

    if (itemsList && target.items) {"""

    new_token_modal = """    if (orderMsg) {
      orderMsg.textContent = `The kitchen is preparing order for ${target.customer || "Student"} hot and fresh.`;
    }

    const arrivalTimeEl = document.getElementById("token-arrival-time");
    const arrivalCountdownEl = document.getElementById("token-arrival-countdown");
    if (arrivalTimeEl) {
      arrivalTimeEl.textContent = target.arrivalTime || target.arrival_time || "Ready in ~10 mins";
    }
    if (arrivalCountdownEl) {
      arrivalCountdownEl.textContent = target.arrivalMinutes ? `~${target.arrivalMinutes} mins` : "~10 mins";
    }

    if (itemsList && target.items) {"""

    if old_token_modal in content:
        content = content.replace(old_token_modal, new_token_modal, 1)
        print("✓ Successfully updated openTokenModal with arrival time")
    else:
        print("✗ Could not find old_token_modal")

    # 4. Update updateMyOrdersCount and renderMyOrdersList
    old_count = """function updateMyOrdersCount() {
  const countMenu = document.getElementById("menu-my-orders-count");
  const countTop = document.getElementById("my-orders-count");
  const count = myOrders.length;"""

    new_count = """function updateMyOrdersCount() {
  const countMenu = document.getElementById("menu-my-orders-count");
  const countTop = document.getElementById("my-orders-count");
  const userOrders = (!currentUser || !currentUser.id)
    ? []
    : myOrders.filter(ord => isOrderForUser(ord, currentUser));
  const count = userOrders.length;"""

    if old_count in content:
        content = content.replace(old_count, new_count, 1)
        print("✓ Successfully updated updateMyOrdersCount with user filter")
    else:
        print("✗ Could not find old_count")

    old_filter = """  // Strict user-specific isolation: Only display orders belonging to the currently logged in user!
  const userOrders = (!currentUser || !currentUser.id) 
    ? [] 
    : myOrders.filter(ord => ord.userId === currentUser.id || ord.username === currentUser.username || (ord.customer && ord.customer === currentUser.name && ord.userId === currentUser.id));"""

    new_filter = """  // Strict user-specific isolation: Only display orders belonging to the currently logged in user!
  const userOrders = (!currentUser || !currentUser.id) 
    ? [] 
    : myOrders.filter(ord => isOrderForUser(ord, currentUser));"""

    if old_filter in content:
        content = content.replace(old_filter, new_filter, 1)
        print("✓ Successfully updated renderMyOrdersList userOrders filter")
    else:
        print("✗ Could not find old_filter")

    # Add arrival time badge to renderMyOrdersList card
    old_order_card_top = """        <div style="background:#f8fafc; border-radius:10px; padding:10px 12px; margin-bottom:10px; border:1px solid #f1f5f9;">
          <div style="font-size:0.75rem; font-weight:700; color:var(--text-muted); text-transform:uppercase; margin-bottom:6px;">Order Summary</div>"""

    new_order_card_top = """        <!-- FOOD ARRIVAL ESTIMATE BANNER -->
        <div style="background:#fffbeb; border:1px solid #fde68a; border-radius:10px; padding:8px 12px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
          <span style="font-size:0.82rem; font-weight:700; color:#92400e; display:inline-flex; align-items:center; gap:5px;">
            <span>🛵</span> <strong>Estimated Food Arrival:</strong> <span style="color:#b45309; font-weight:800; font-size:0.92rem;">${ord.arrivalTime || ord.arrival_time || 'Ready in ~10 mins'}</span>
          </span>
          <span style="font-size:0.76rem; font-weight:800; color:#d97706; background:#fef3c7; padding:2px 8px; border-radius:999px;">
            ${ord.arrivalMinutes ? `~${ord.arrivalMinutes} mins wait` : 'Fast Kitchen Prep'}
          </span>
        </div>

        <div style="background:#f8fafc; border-radius:10px; padding:10px 12px; margin-bottom:10px; border:1px solid #f1f5f9;">
          <div style="font-size:0.75rem; font-weight:700; color:var(--text-muted); text-transform:uppercase; margin-bottom:6px;">Order Summary</div>"""

    if old_order_card_top in content:
        content = content.replace(old_order_card_top, new_order_card_top, 1)
        print("✓ Successfully added arrival estimate banner into order card")
    else:
        print("✗ Could not find old_order_card_top")

    # 5. Update loadUserData to strictly isolate orders and fetch phone-scoped orders from backend
    old_load_user_data = """function loadUserData(user) {
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
}"""

    new_load_user_data = """function loadUserData(user) {
  if (!user || !user.id) {
    cart = {};
    myOrders = [];
    activeCoupon = null;
    lastPlacedOrder = null;
    updateCartBar();
    updateMyOrdersCount();
    renderMyOrdersList();
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

  // Strictly synchronize matching orders from liveOrders using isOrderForUser
  if (Array.isArray(liveOrders)) {
    const matching = liveOrders.filter(o => isOrderForUser(o, user));
    matching.forEach(ord => {
      if (!myOrders.some(m => m.id === ord.id)) {
        myOrders.unshift(ord);
      }
    });
  }

  // Also query backend for this user's phone if available
  if (user.phone) {
    const cleanPhone = String(user.phone).replace(/\\D/g, '').slice(-10);
    if (cleanPhone.length === 10) {
      fetch(`${API_BASE}/api/orders?phone=${cleanPhone}`)
        .then(res => res.ok ? res.json() : null)
        .then(data => {
          if (data && Array.isArray(data.orders)) {
            let changed = false;
            data.orders.forEach(backendOrder => {
              if (isOrderForUser(backendOrder, user)) {
                const existing = myOrders.find(m => m.id === backendOrder.id);
                if (!existing) {
                  myOrders.unshift(backendOrder);
                  changed = true;
                } else if (existing.status !== backendOrder.status) {
                  Object.assign(existing, backendOrder);
                  changed = true;
                }
              }
            });
            if (changed) {
              saveUserData();
              updateMyOrdersCount();
              renderMyOrdersList();
            }
          }
        }).catch(() => {});
    }
  }

  lastPlacedOrder = myOrders.length > 0 ? myOrders[0] : null;

  updateCartBar();
  updateMyOrdersCount();
  renderLoyaltyStampCard();
  renderMyOrdersList();
}"""

    if old_load_user_data in content:
        content = content.replace(old_load_user_data, new_load_user_data, 1)
        print("✓ Successfully updated loadUserData")
    else:
        print("✗ Could not find old_load_user_data")

    # 6. Update loginUser to clear previous session completely
    old_login_user = """function loginUser(userAccount) {
  currentUser = userAccount;
  try {
    localStorage.setItem("savitha_user", JSON.stringify(currentUser));
  } catch (e) {}

  // Load user's isolated data store
  loadUserData(currentUser);"""

    new_login_user = """function loginUser(userAccount) {
  // Clear any active cart and orders from previous session in memory
  cart = {};
  myOrders = [];
  lastPlacedOrder = null;
  activeCoupon = null;

  currentUser = userAccount;
  try {
    localStorage.setItem("savitha_user", JSON.stringify(currentUser));
  } catch (e) {}

  // Load user's isolated data store
  loadUserData(currentUser);"""

    if old_login_user in content:
        content = content.replace(old_login_user, new_login_user, 1)
        print("✓ Successfully updated loginUser")
    else:
        print("✗ Could not find old_login_user")

    # 7. Update handlePortalStudentLogin to ONLY require Name and Phone (and Semester), NO USN and NO PASSWORD!
    old_portal_login = """function handlePortalStudentLogin(e) {
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
}"""

    new_portal_login = """function handlePortalStudentLogin(e) {
  if (e) {
    try { e.preventDefault(); } catch (err) {}
    try { e.stopPropagation(); } catch (err) {}
  }

  const nameInput = document.getElementById("login-student-name") || document.getElementById("modal-student-name");
  const phoneInput = document.getElementById("login-student-phone") || document.getElementById("modal-student-phone");
  const semInput = document.getElementById("login-student-sem") || document.getElementById("login-student-year") || document.getElementById("modal-student-sem");

  const name = nameInput && nameInput.value.trim() ? nameInput.value.trim() : "";
  const rawPhone = phoneInput && phoneInput.value.trim() ? phoneInput.value.trim() : "";
  const cleanPhone = rawPhone.replace(/\\D/g, '').slice(-10);
  const sem = semInput && semInput.value ? semInput.value : "Sem 4 • 2nd Year";

  if (!name) {
    showToast("⚠️ Please enter your Full Name to login!", "warning");
    if (nameInput) nameInput.focus();
    return false;
  }

  if (!cleanPhone || cleanPhone.length !== 10) {
    showToast("⚠️ Please enter a valid 10-digit mobile number!", "warning");
    if (phoneInput) phoneInput.focus();
    return false;
  }

  // Create isolated account deterministically tied to student's 10-digit phone
  const userId = "usr_" + cleanPhone;
  const username = name.toLowerCase().replace(/[^a-z0-9]/g, "") + "_" + cleanPhone.slice(-4);
  const account = {
    id: userId,
    userId: userId,
    username: username,
    name: name,
    phone: cleanPhone,
    year: sem,
    sem: sem,
    role: "student"
  };

  const accounts = getAccounts();
  const existingIdx = accounts.findIndex(a => a.id === userId || (a.phone && a.phone.replace(/\\D/g, '').slice(-10) === cleanPhone));
  if (existingIdx >= 0) {
    accounts[existingIdx] = { ...accounts[existingIdx], ...account };
  } else {
    accounts.push(account);
  }
  saveAccounts(accounts);

  loginUser(account);
  showToast(`Welcome ${account.name}! (${account.sem}) Food menu is ready 🍛`, "success");
  return false;
}"""

    if old_portal_login in content:
        content = content.replace(old_portal_login, new_portal_login, 1)
        print("✓ Successfully updated handlePortalStudentLogin (No USN/password, Name+Phone+Sem)")
    else:
        print("✗ Could not find old_portal_login")

    # 8. Update logoutUser to ensure all state is wiped clean
    old_logout = """function logoutUser() {
  if (currentUser) {
    saveUserData();
  }
  currentUser = null;
  cart = {};
  myOrders = [];
  activeCoupon = null;
  lastPlacedOrder = null;
  try {
    localStorage.removeItem("savitha_user");
    sessionStorage.removeItem("savitha_user");
  } catch (e) {}"""

    new_logout = """function logoutUser() {
  if (currentUser) {
    saveUserData();
  }
  currentUser = null;
  cart = {};
  myOrders = [];
  activeCoupon = null;
  lastPlacedOrder = null;
  try {
    localStorage.removeItem("savitha_user");
    sessionStorage.removeItem("savitha_user");
    localStorage.removeItem("savitha_student_active_order");
    localStorage.removeItem("savitha_my_orders");
  } catch (e) {}"""

    if old_logout in content:
        content = content.replace(old_logout, new_logout, 1)
        print("✓ Successfully updated logoutUser")
    else:
        print("✗ Could not find old_logout")

    # 9. Update renderFeedbackList to show Name and Semester
    old_fb_render = """              <div style="width:38px; height:38px; min-width:38px; border-radius:50%; background:linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%); color:var(--primary); font-weight:900; font-size:1rem; display:flex; align-items:center; justify-content:center; border:1.5px solid #c7d2fe;">🎓</div>
              <div>
                <div style="font-weight:800; font-size:0.94rem; color:var(--text-main); display:flex; align-items:center; gap:6px;">
                  <span>Verified ${fb.year && fb.year.toLowerCase().includes("faculty") ? "Faculty" : "Student"}</span>
                  <span style="font-size:0.7rem; color:#10b981; background:#ecfdf5; border:1px solid #a7f3d0; padding:1px 6px; border-radius:999px; font-weight:700;">✓ Verified</span>
                </div>
                <div style="font-size:0.76rem; color:var(--text-muted);">${escapeHtml(fb.year || "Campus Dining")}</div>
              </div>"""

    new_fb_render = """              <div style="width:38px; height:38px; min-width:38px; border-radius:50%; background:linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%); color:var(--primary); font-weight:900; font-size:1rem; display:flex; align-items:center; justify-content:center; border:1.5px solid #c7d2fe;">🎓</div>
              <div>
                <div style="font-weight:800; font-size:0.96rem; color:var(--text-main); display:flex; align-items:center; gap:6px;">
                  <span>${escapeHtml(fb.name || "Student Reviewer")}</span>
                  <span style="font-size:0.7rem; color:#10b981; background:#ecfdf5; border:1px solid #a7f3d0; padding:1px 6px; border-radius:999px; font-weight:700;">✓ Verified</span>
                </div>
                <div style="font-size:0.78rem; font-weight:700; color:var(--primary);">${escapeHtml(fb.sem || fb.year || "Sem 4 • Student")}</div>
              </div>"""

    if old_fb_render in content:
        content = content.replace(old_fb_render, new_fb_render, 1)
        print("✓ Successfully updated renderFeedbackList (Name and Sem prominently displayed)")
    else:
        print("✗ Could not find old_fb_render")

    # Also in handleWebsiteReviewSubmit, ensure sem is included
    old_review_submit = """  const payload = {
    name,
    year,
    rating,
    category,
    comment,
    date: new Date().toISOString().split("T")[0],
    timestamp: Date.now()
  };"""

    new_review_submit = """  const payload = {
    name,
    year,
    sem: year,
    rating,
    category,
    comment,
    date: new Date().toISOString().split("T")[0],
    timestamp: Date.now()
  };"""

    if old_review_submit in content:
        content = content.replace(old_review_submit, new_review_submit, 1)
        print("✓ Successfully updated handleWebsiteReviewSubmit payload with sem")
    else:
        print("✗ Could not find old_review_submit")

    with open("js/app.js", "w", encoding="utf-8") as f:
        f.write(content)

    print("Finished updating js/app.js")

if __name__ == "__main__":
    update_app_js()
