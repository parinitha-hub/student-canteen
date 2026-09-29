import sys
import shutil

with open('js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize line endings to \n for editing
content_norm = content.replace('\r\n', '\n')

# 1. Update liveOrders initial state
old_live_orders = """let liveOrders = [];
try {
  const savedOrders = localStorage.getItem("savitha_live_orders");
  liveOrders = savedOrders ? JSON.parse(savedOrders) : [
    {
      id: "ORD-101",
      token: "#A-14",
      customerName: "Priya Sharma",
      customerYear: "3rd Year",
      customerPhone: "9876543210",
      items: [{ id: "chicken_biryani", name: "Chicken Biryani", qty: 1, price: 160, subtotal: 160 }],
      total: 160,
      time: "12:15 PM",
      status: "Ready at Counter! ✅",
      timestamp: Date.now() - 600000
    },
    {
      id: "ORD-102",
      token: "#B-28",
      customerName: "Arjun Verma",
      customerYear: "2nd Year",
      customerPhone: "9123456780",
      items: [{ id: "samosa_chai", name: "Samosa & Chai", qty: 2, price: 50, subtotal: 100 }],
      total: 100,
      time: "12:28 PM",
      status: "Preparing in Kitchen ⏳",
      timestamp: Date.now() - 120000
    }
  ];
} catch (e) {
  liveOrders = [];
}"""

new_live_orders = """let liveOrders = [];
try {
  const savedOrders = localStorage.getItem("savitha_live_orders");
  liveOrders = savedOrders ? JSON.parse(savedOrders) : [];
} catch (e) {
  liveOrders = [];
}"""

assert old_live_orders in content_norm, "Failed to find old_live_orders"
content_norm = content_norm.replace(old_live_orders, new_live_orders, 1)

# 2. Update renderDishes to remove login wall and add Order Now on selected items
old_render_dishes = """function renderDishes() {
  const container = document.getElementById("dishes-grid");
  if (!container) return;

  // Gating: without login, we should not get food menu items!
  if (!currentUser || currentUser.isGuest || currentUser.role !== "student") {
    container.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 48px 20px; background: var(--bg-card); border-radius: var(--radius-lg); border: 2px dashed var(--border);">
        <div style="font-size: 3rem; margin-bottom: 12px;">🔒</div>
        <h3 style="font-size: 1.3rem; font-weight: 800; color: var(--text-main); margin-bottom: 8px;">Login Required to View Menu</h3>
        <p style="color: var(--text-muted); font-size: 0.92rem; margin-bottom: 20px;">Please login with your Student profile to browse dishes and place orders.</p>
        <button type="button" class="btn-hero-primary" onclick="navigateToSection('login')">
          <span>🔐</span> Go to Login
        </button>
      </div>
    `;
    return;
  }

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
        <div style="display:flex; gap:6px; align-items:center;">
          <button type="button" class="btn-quick-order" onclick="quickOrderDish('${dish.id}')" title="Instant Order & Get Token">
            <span>⚡</span> Order Now
          </button>
          <button type="button" class="add-btn" onclick="updateDishQty('${dish.id}', 1)">
            ADD +
          </button>
        </div>
      `;
    }"""

new_render_dishes = """function renderDishes() {
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
        <div style="display:flex; gap:6px; align-items:center; flex-wrap:wrap;">
          <div class="qty-pill">
            <button type="button" onclick="updateDishQty('${dish.id}', -1)" title="Decrease quantity">-</button>
            <span class="qty-count">${qty}</span>
            <button type="button" onclick="updateDishQty('${dish.id}', 1)" title="Increase quantity">+</button>
          </div>
          <button type="button" class="btn-order-now-selected" onclick="openCartModal()" title="Order Now">
            <span>⚡</span> Order Now
          </button>
        </div>
      `;
    } else {
      buttonHtml = `
        <div style="display:flex; gap:6px; align-items:center;">
          <button type="button" class="btn-quick-order" onclick="quickOrderDish('${dish.id}')" title="Instant Order & Get Token">
            <span>⚡</span> Order Now
          </button>
          <button type="button" class="add-btn" onclick="updateDishQty('${dish.id}', 1)" title="Add to Cart">
            ADD +
          </button>
        </div>
      `;
    }"""

assert old_render_dishes in content_norm, "Failed to find old_render_dishes"
content_norm = content_norm.replace(old_render_dishes, new_render_dishes, 1)

# 3. Update updateDishQty and quickOrderDish
old_qty_and_quick = """function updateDishQty(dishId, delta) {
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

function quickOrderDish(dishId) {
  const dish = DISHES.find(d => d.id === dishId);
  if (!dish) return;

  if (!currentUser) {
    currentUser = { role: "student", name: "Student", year: "1st Year", phone: "9876543210" };
    try { localStorage.setItem("savitha_user", JSON.stringify(currentUser)); } catch (e) {}
    renderUserAuthSlot();
  }

  // Set cart to 1 of this dish
  cart = { [dishId]: 1 };
  updateCartBar();

  // Make sure customer name input has default
  const nameInput = document.getElementById("order-customer-name");
  if (nameInput && !nameInput.value.trim()) {
    nameInput.value = (currentUser && currentUser.name && currentUser.name !== "Student") ? currentUser.name : "Student";
  }

  // Immediately place order and generate token
  placeOrderAndGenerateToken();
};"""

new_qty_and_quick = """function updateDishQty(dishId, delta) {
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

function quickOrderDish(dishId) {
  const dish = DISHES.find(d => d.id === dishId);
  if (!dish) return;

  // Add 1 to cart
  cart[dishId] = (cart[dishId] || 0) + 1;
  renderDishes();
  updateCartBar();

  // Open cart modal immediately with Order Now
  openCartModal();
};"""

assert old_qty_and_quick in content_norm, "Failed to find old_qty_and_quick"
content_norm = content_norm.replace(old_qty_and_quick, new_qty_and_quick, 1)

# 4. Update updateCartBar
old_update_cart_bar = """function updateCartBar() {
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
}"""

new_update_cart_bar = """function updateCartBar() {
  const bar = document.getElementById("cart-floating-bar");
  const heroCount = document.getElementById("hero-cart-count");
  const counter = document.getElementById("cart-counter");
  const floatingCount = document.getElementById("floating-cart-count");
  const floatingTotal = document.getElementById("floating-cart-total");
  const totalVal = document.getElementById("cart-bar-total-val");
  const itemsVal = document.getElementById("cart-bar-items-val");

  let totalQty = 0;
  let totalPrice = 0;

  for (const [id, qty] of Object.entries(cart)) {
    const dish = DISHES.find(d => d.id === id);
    if (dish && qty > 0) {
      totalQty += qty;
      totalPrice += (dish.price * qty);
    }
  }

  if (heroCount) heroCount.textContent = totalQty;
  if (counter) counter.textContent = totalQty;
  if (floatingCount) floatingCount.textContent = `${totalQty} item${totalQty > 1 ? 's' : ''} selected`;
  if (floatingTotal) floatingTotal.textContent = `₹${totalPrice}`;
  if (totalVal) totalVal.textContent = `₹${totalPrice}`;
  if (itemsVal) itemsVal.textContent = `${totalQty} item${totalQty > 1 ? 's' : ''} in your order`;

  if (bar) {
    if (totalQty > 0) {
      bar.classList.add("show");
    } else {
      bar.classList.remove("show");
    }
  }
}"""

assert old_update_cart_bar in content_norm, "Failed to find old_update_cart_bar"
content_norm = content_norm.replace(old_update_cart_bar, new_update_cart_bar, 1)

# 5. Update openCartModal and placeOrderAndGenerateToken
old_open_cart = """// Cart Modal
function openCartModal() {
  if (!currentUser) {
    currentUser = { role: "student", name: "Student" };
    try { localStorage.setItem("savitha_user", JSON.stringify(currentUser)); } catch (e) {}
    renderUserAuthSlot();
  }

  const modal = document.getElementById("cart-modal");
  const list = document.getElementById("cart-items-list");
  const subtotal = document.getElementById("bill-subtotal");
  const total = document.getElementById("bill-total");

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

  // Pre-fill student name, year, and phone if already signed in
  const nameInput = document.getElementById("order-customer-name");
  const yearInput = document.getElementById("order-customer-year");
  const phoneInput = document.getElementById("order-customer-phone");

  if (nameInput && currentUser && currentUser.name && currentUser.name !== "Student") {
    nameInput.value = currentUser.name;
  }
  if (yearInput && currentUser && currentUser.year) {
    yearInput.value = currentUser.year;
  }
  if (phoneInput && currentUser && currentUser.phone) {
    phoneInput.value = currentUser.phone;
  }

  modal.classList.add("show");
};"""

new_open_cart = """// Cart Modal
function openCartModal() {
  const modal = document.getElementById("cart-modal");
  const list = document.getElementById("cart-items-container") || document.getElementById("cart-items-list");
  const modalTotal = document.getElementById("cart-modal-total") || document.getElementById("bill-total");
  const subtotal = document.getElementById("bill-subtotal");

  if (!modal) return;

  const entries = Object.entries(cart).filter(([_, qty]) => qty > 0);
  if (entries.length === 0) {
    showToast("Your cart is empty. Please select dishes first!", "info");
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
            <div class="qty-pill" style="padding:2px 6px;">
              <button type="button" onclick="updateDishQty('${dish.id}', -1); openCartModal();" style="width:18px; height:18px; font-size:0.85rem;">-</button>
              <span style="font-size:0.82rem; min-width:14px;">${qty}</span>
              <button type="button" onclick="updateDishQty('${dish.id}', 1); openCartModal();" style="width:18px; height:18px; font-size:0.85rem;">+</button>
            </div>
            <button type="button" onclick="delete cart['${dish.id}']; updateCartBar(); renderDishes(); openCartModal();" style="background:transparent; border:none; color:#ef4444; font-size:1.1rem; cursor:pointer;" aria-label="Remove item">✕</button>
          </div>
        </div>
      `;
    }
  });

  if (list) list.innerHTML = html;
  if (subtotal) subtotal.textContent = `₹${sum}`;
  if (modalTotal) modalTotal.textContent = `₹${sum}`;

  // Pre-fill user info ONLY if user previously provided a real name/phone
  const nameInput = document.getElementById("order-customer-name");
  const yearInput = document.getElementById("order-customer-year");
  const phoneInput = document.getElementById("order-customer-phone");

  if (nameInput) {
    if (currentUser && currentUser.name && currentUser.name !== "Student") {
      nameInput.value = currentUser.name;
    } else {
      nameInput.value = "";
    }
  }
  if (yearInput && currentUser && currentUser.year) {
    yearInput.value = currentUser.year;
  }
  if (phoneInput) {
    if (currentUser && currentUser.phone && currentUser.phone !== "9876543210") {
      phoneInput.value = currentUser.phone;
    } else {
      phoneInput.value = "";
    }
  }

  modal.classList.add("show");
};"""

assert old_open_cart in content_norm, "Failed to find old_open_cart"
content_norm = content_norm.replace(old_open_cart, new_open_cart, 1)

# 6. Update placeOrderAndGenerateToken
old_place_order = """// Place Order & Token Generation ("You Got the Order!")
function placeOrderAndGenerateToken() {
  const nameInput = document.getElementById("order-customer-name");
  const yearInput = document.getElementById("order-customer-year");
  const phoneInput = document.getElementById("order-customer-phone");

  const custName = (nameInput && nameInput.value.trim())
    ? nameInput.value.trim()
    : (currentUser && currentUser.name && currentUser.name !== "Student" ? currentUser.name : "Student");

  const custYear = (yearInput && yearInput.value)
    ? yearInput.value
    : (currentUser && currentUser.year ? currentUser.year : "1st Year");

  const rawPhone = (phoneInput && phoneInput.value.trim())
    ? phoneInput.value.trim()
    : (currentUser && currentUser.phone ? currentUser.phone : "9876543210");

  let cleanPhone = rawPhone.replace(/[^0-9]/g, "");
  if (!cleanPhone || cleanPhone.length < 5) {
    cleanPhone = "9876543210";
  }"""

new_place_order = """// Place Order & Token Generation ("You Got the Order!")
function placeOrderAndGenerateToken() {
  const nameInput = document.getElementById("order-customer-name");
  const yearInput = document.getElementById("order-customer-year");
  const phoneInput = document.getElementById("order-customer-phone");

  const custName = (nameInput && nameInput.value.trim())
    ? nameInput.value.trim()
    : (currentUser && currentUser.name && currentUser.name !== "Student" ? currentUser.name : "");

  if (!custName) {
    showToast("Please enter your name to place the order!", "warning");
    if (nameInput) {
      nameInput.focus();
      nameInput.classList.add("input-error");
    }
    return;
  }

  const custYear = (yearInput && yearInput.value)
    ? yearInput.value
    : (currentUser && currentUser.year ? currentUser.year : "1st Year");

  const rawPhone = (phoneInput && phoneInput.value.trim())
    ? phoneInput.value.trim()
    : (currentUser && currentUser.phone ? currentUser.phone : "");

  let cleanPhone = rawPhone.replace(/[^0-9]/g, "");"""

assert old_place_order in content_norm, "Failed to find old_place_order"
content_norm = content_norm.replace(old_place_order, new_place_order, 1)

# 7. Update msgEl in placeOrderAndGenerateToken
old_msg_el = """  const msgEl = document.getElementById("token-order-message");
  if (msgEl) {
    msgEl.innerHTML = `We got your order, <strong>${custName}</strong>! The kitchen is preparing your meal hot and fresh. We will notify you at <strong>📞 ${cleanPhone}</strong>.`;
  }"""

new_msg_el = """  const msgEl = document.getElementById("token-order-message");
  if (msgEl) {
    const phoneNotice = cleanPhone ? ` We will notify you at <strong>📞 ${cleanPhone}</strong>.` : '';
    msgEl.innerHTML = `We got your order, <strong>${custName}</strong>! The kitchen is preparing your meal hot and fresh.${phoneNotice}`;
  }"""

assert old_msg_el in content_norm, "Failed to find old_msg_el"
content_norm = content_norm.replace(old_msg_el, new_msg_el, 1)

# 8. Update applyRoleVisibility to keep only ONE login button on landing page
old_role_vis = """  if (heroPrimary) {
    if (isWorker) {
      heroPrimary.innerHTML = "<span>👨‍🍳</span> Go to Kitchen Dashboard →";
      heroPrimary.onclick = () => performSwitchMode("manager");
      if (heroSecondary) heroSecondary.style.display = "none";
    } else if (isStudent) {
      heroPrimary.innerHTML = "<span>🍽️</span> View Food Menu &amp; Order →";
      heroPrimary.onclick = () => performSwitchMode("order");
      if (heroSecondary) heroSecondary.style.display = "none";
    } else {
      // Guest: Without login, no menu button!
      heroPrimary.innerHTML = "<span>🔐</span> Login to Order Food (Student / Staff) →";
      heroPrimary.onclick = () => navigateToSection("login");
      if (heroSecondary) heroSecondary.style.display = "none";
    }
  }

  if (bottomPrimary) {
    if (isWorker) {
      bottomPrimary.innerHTML = "<span>👨‍🍳</span> Go to Kitchen Dashboard →";
      bottomPrimary.onclick = () => performSwitchMode("manager");
      if (bottomSecondary) bottomSecondary.style.display = "none";
    } else if (isStudent) {
      bottomPrimary.innerHTML = "<span>🍽️</span> View Food Menu &amp; Order →";
      bottomPrimary.onclick = () => performSwitchMode("order");
      if (bottomSecondary) bottomSecondary.style.display = "none";
    } else {
      // Guest: Without login, no menu button!
      bottomPrimary.innerHTML = "<span>🔐</span> Login to Order Food (Student / Staff) →";
      bottomPrimary.onclick = () => navigateToSection("login");
      if (bottomSecondary) bottomSecondary.style.display = "none";
    }
  }"""

new_role_vis = """  if (heroPrimary) {
    if (isWorker) {
      heroPrimary.innerHTML = "<span>👨‍🍳</span> Go to Kitchen Dashboard →";
      heroPrimary.onclick = () => performSwitchMode("manager");
      if (heroSecondary) heroSecondary.style.display = "none";
    } else if (isStudent) {
      heroPrimary.innerHTML = "<span>🍽️</span> View Food Menu &amp; Order →";
      heroPrimary.onclick = () => performSwitchMode("order");
      if (heroSecondary) heroSecondary.style.display = "none";
    } else {
      // Clean single login way in navbar; hero opens food menu directly!
      heroPrimary.innerHTML = "<span>🍽️</span> View Food Menu &amp; Order →";
      heroPrimary.onclick = () => performSwitchMode("order");
      if (heroSecondary) {
        heroSecondary.style.display = "inline-flex";
        heroSecondary.innerHTML = "<span>📖</span> About Savitha Canteen";
        heroSecondary.onclick = () => {
          const el = document.getElementById("about-website");
          if (el) el.scrollIntoView({ behavior: "smooth" });
        };
      }
    }
  }

  if (bottomPrimary) {
    if (isWorker) {
      bottomPrimary.innerHTML = "<span>👨‍🍳</span> Go to Kitchen Dashboard →";
      bottomPrimary.onclick = () => performSwitchMode("manager");
      if (bottomSecondary) bottomSecondary.style.display = "none";
    } else if (isStudent) {
      bottomPrimary.innerHTML = "<span>🍽️</span> Browse Food Menu &amp; Order →";
      bottomPrimary.onclick = () => performSwitchMode("order");
      if (bottomSecondary) bottomSecondary.style.display = "none";
    } else {
      bottomPrimary.innerHTML = "<span>🍽️</span> Explore Food Menu &amp; Order →";
      bottomPrimary.onclick = () => performSwitchMode("order");
      if (bottomSecondary) bottomSecondary.style.display = "none";
    }
  }"""

assert old_role_vis in content_norm, "Failed to find old_role_vis"
content_norm = content_norm.replace(old_role_vis, new_role_vis, 1)

# 9. Add toggleStaffLoginForm
old_switch_tab = """function switchLoginTab(tab) {"""

new_switch_tab = """function toggleStaffLoginForm() {
  const panelStudent = document.getElementById("login-panel-student");
  const panelWorker = document.getElementById("login-panel-worker");
  if (!panelWorker) return;

  if (panelWorker.style.display === "none" || !panelWorker.style.display) {
    if (panelStudent) panelStudent.style.display = "none";
    panelWorker.style.display = "block";
    const passInput = document.getElementById("login-worker-password");
    if (passInput) passInput.focus();
  } else {
    panelWorker.style.display = "none";
    if (panelStudent) panelStudent.style.display = "block";
    const nameInput = document.getElementById("login-student-name");
    if (nameInput) nameInput.focus();
  }
}

function switchLoginTab(tab) {"""

assert old_switch_tab in content_norm, "Failed to find old_switch_tab"
content_norm = content_norm.replace(old_switch_tab, new_switch_tab, 1)

# 10. Update handlePortalStudentLogin to not fallback to "Student"
old_handle_student = """function handlePortalStudentLogin(e) {
  if (e) {
    try { e.preventDefault(); } catch (err) {}
    try { e.stopPropagation(); } catch (err) {}
  }
  const nameInput = document.getElementById("login-student-name");
  const yearInput = document.getElementById("login-student-year");
  const phoneInput = document.getElementById("login-student-phone");

  const name = nameInput && nameInput.value.trim() ? nameInput.value.trim() : "Student";
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
  showToast(`Welcome ${name}! (${year}) Food menu is unlocked 🍛`, "success");
};"""

new_handle_student = """function handlePortalStudentLogin(e) {
  if (e) {
    try { e.preventDefault(); } catch (err) {}
    try { e.stopPropagation(); } catch (err) {}
  }
  const nameInput = document.getElementById("login-student-name");
  const yearInput = document.getElementById("login-student-year");
  const phoneInput = document.getElementById("login-student-phone");

  const name = nameInput && nameInput.value.trim() ? nameInput.value.trim() : "";
  if (!name) {
    showToast("Please enter your name to login!", "warning");
    if (nameInput) nameInput.focus();
    return;
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
};"""

assert old_handle_student in content_norm, "Failed to find old_handle_student"
content_norm = content_norm.replace(old_handle_student, new_handle_student, 1)

# 11. Remove gating in navigateToSection and performSwitchMode
old_nav = """  } else if (target === "home" || target === "order") {
    // If Kitchen Staff is logged in, they already know about dishes and should not get the menu
    if (currentUser && currentUser.role === "worker") {
      performSwitchMode("manager");
      return;
    }
    // Gating: without login we should not get food menu items!
    if (!currentUser || currentUser.isGuest || currentUser.role !== "student") {
      performSwitchMode("login");
      showToast("🔒 Please login as a Student to view food menu items!", "info");
      return;
    }
    const el = document.getElementById("nav-btn-home");
    if (el) el.classList.add("active");
    performSwitchMode("order");
    window.scrollTo({ top: 0, behavior: "smooth" });"""

new_nav = """  } else if (target === "home" || target === "order") {
    // If Kitchen Staff is logged in, they already know about dishes and should not get the menu
    if (currentUser && currentUser.role === "worker") {
      performSwitchMode("manager");
      return;
    }
    const el = document.getElementById("nav-btn-home");
    if (el) el.classList.add("active");
    performSwitchMode("order");
    window.scrollTo({ top: 0, behavior: "smooth" });"""

assert old_nav in content_norm, "Failed to find old_nav"
content_norm = content_norm.replace(old_nav, new_nav, 1)

old_switch_mode = """function performSwitchMode(mode) {
  // If Kitchen Staff is logged in, they already know about dishes and should not get the food menu
  if ((mode === "order" || mode === "home") && currentUser && currentUser.role === "worker") {
    performSwitchMode("manager");
    return;
  }

  // Gating: without login we should not get food menu items!
  if ((mode === "order" || mode === "home") && (!currentUser || currentUser.isGuest || currentUser.role !== "student")) {
    performSwitchMode("login");
    showToast("🔒 Please login as a Student to view food menu items!", "info");
    return;
  }"""

new_switch_mode = """function performSwitchMode(mode) {
  // If Kitchen Staff is logged in, they already know about dishes and should not get the food menu
  if ((mode === "order" || mode === "home") && currentUser && currentUser.role === "worker") {
    performSwitchMode("manager");
    return;
  }"""

assert old_switch_mode in content_norm, "Failed to find old_switch_mode"
content_norm = content_norm.replace(old_switch_mode, new_switch_mode, 1)

old_scroll = """    // Gating: without login we should not get food menu items!
    if (!currentUser || currentUser.isGuest || currentUser.role !== "student") {
      performSwitchMode("login");
      showToast("🔒 Please login as a Student to view food menu items!", "info");
      return;
    }
    performSwitchMode("order");"""

new_scroll = """    performSwitchMode("order");"""

assert old_scroll in content_norm, "Failed to find old_scroll"
content_norm = content_norm.replace(old_scroll, new_scroll, 1)

# 12. Add window exports
old_exports = """if (typeof window !== "undefined") window.quickOrderDish = quickOrderDish;
if (typeof window !== "undefined") window.confirmTokenInKitchen = confirmTokenInKitchen;
if (typeof window !== "undefined") window.DISHES = DISHES;"""

new_exports = """if (typeof window !== "undefined") window.quickOrderDish = quickOrderDish;
if (typeof window !== "undefined") window.confirmTokenInKitchen = confirmTokenInKitchen;
if (typeof window !== "undefined") window.DISHES = DISHES;
if (typeof window !== "undefined") window.toggleStaffLoginForm = toggleStaffLoginForm;
if (typeof window !== "undefined") window.openCartModal = openCartModal;
if (typeof window !== "undefined") window.closeCartModal = closeCartModal;
if (typeof window !== "undefined") window.updateDishQty = updateDishQty;
if (typeof window !== "undefined") window.placeOrderAndGenerateToken = placeOrderAndGenerateToken;"""

assert old_exports in content_norm, "Failed to find old_exports"
content_norm = content_norm.replace(old_exports, new_exports, 1)

# Write back with CRLF
output = content_norm.replace('\n', '\r\n')
with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(output)

shutil.copyfile('js/app.js', 'frontend/js/app.js')
print("Successfully updated js/app.js and synced to frontend/js/app.js!")
