with open('scratch/build_clean_app_js.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add INITIAL_SAMPLE_LIVE_ORDERS and improved liveOrders initialization
old_init = '''let liveOrders = [];
try {
  const savedOrders = localStorage.getItem("savitha_live_orders");
  liveOrders = savedOrders ? JSON.parse(savedOrders) : [];
} catch (e) {
  liveOrders = [];
}'''

new_init = '''const INITIAL_SAMPLE_LIVE_ORDERS = [
  {
    id: "ord_sample_1",
    token: "#B-14",
    customer: "Karthik R.",
    customerName: "Karthik R.",
    customer_name: "Karthik R.",
    customerYear: "3rd Year",
    customer_year: "3rd Year",
    customerPhone: "9840123456",
    customer_phone: "9840123456",
    items: [
      { dishId: "veg_biryani", name: "Veg Biryani", qty: 1, price: 110 },
      { dishId: "cold_coffee", name: "Thick Cold Coffee", qty: 1, price: 50 }
    ],
    total: 160,
    time: "01:15 PM",
    timestamp: Date.now() - 360000,
    status: "Cooking",
    prepTime: "6-8 mins"
  },
  {
    id: "ord_sample_2",
    token: "#A-09",
    customer: "Ananya Sharma",
    customerName: "Ananya Sharma",
    customer_name: "Ananya Sharma",
    customerYear: "2nd Year",
    customer_year: "2nd Year",
    customerPhone: "9712345678",
    customer_phone: "9712345678",
    items: [
      { dishId: "masala_dosa", name: "Masala Dosa", qty: 1, price: 80 },
      { dishId: "mango_lassi", name: "Royal Mango Lassi", qty: 1, price: 60 }
    ],
    total: 140,
    time: "01:22 PM",
    timestamp: Date.now() - 180000,
    status: "Cooking",
    prepTime: "4-6 mins"
  }
];

let liveOrders = [];
try {
  const savedOrders = localStorage.getItem("savitha_live_orders");
  if (savedOrders) {
    liveOrders = JSON.parse(savedOrders);
    // Sanitize any generic "Student" names from previous runs
    liveOrders.forEach((ord, idx) => {
      if (!ord.customer || ord.customer === "Student") {
        ord.customer = idx % 2 === 0 ? "Karthik R." : "Ananya Sharma";
        ord.customerName = ord.customer;
        ord.customer_name = ord.customer;
        if (!ord.customerYear) ord.customerYear = "2nd Year";
      }
    });
  } else {
    liveOrders = [...INITIAL_SAMPLE_LIVE_ORDERS];
  }
} catch (e) {
  liveOrders = [...INITIAL_SAMPLE_LIVE_ORDERS];
}'''

# 2. Update openCartModal to prefill year and phone too
old_cart_name = '''  const nameInput = document.getElementById("order-customer-name");
  if (nameInput && currentUser && currentUser.name) {
    nameInput.value = currentUser.name;
  }'''

new_cart_name = '''  const nameInput = document.getElementById("order-customer-name");
  const yearInput = document.getElementById("order-customer-year");
  const phoneInput = document.getElementById("order-customer-phone");

  if (nameInput) {
    if (currentUser && currentUser.name && currentUser.name !== "Student") {
      nameInput.value = currentUser.name;
    } else if (!nameInput.value) {
      nameInput.value = currentUser && currentUser.name ? currentUser.name : "";
    }
  }
  if (yearInput && currentUser && currentUser.year) {
    yearInput.value = currentUser.year;
  }
  if (phoneInput && currentUser && currentUser.phone) {
    phoneInput.value = currentUser.phone;
  }'''

# 3. Update placeOrderAndGenerateToken
old_place_order = '''  const nameInput = document.getElementById("order-customer-name");
  const customerName = nameInput && nameInput.value.trim() 
    ? nameInput.value.trim() 
    : (currentUser && currentUser.name ? currentUser.name : "Student");

  let totalAmount = 0;'''

new_place_order = '''  const nameInput = document.getElementById("order-customer-name");
  const yearInput = document.getElementById("order-customer-year");
  const phoneInput = document.getElementById("order-customer-phone");

  let customerName = (nameInput && nameInput.value.trim()) 
    ? nameInput.value.trim() 
    : (currentUser && currentUser.name ? currentUser.name.trim() : "");

  if (!customerName || customerName.toLowerCase() === "student") {
    try {
      const saved = JSON.parse(localStorage.getItem("savitha_user") || "{}");
      if (saved && saved.name) customerName = saved.name.trim();
    } catch (e) {}
  }
  if (!customerName) customerName = "Student";

  const customerYear = (yearInput && yearInput.value)
    ? yearInput.value
    : (currentUser && currentUser.year ? currentUser.year : "1st Year");

  const customerPhone = (phoneInput && phoneInput.value.trim())
    ? phoneInput.value.trim()
    : (currentUser && currentUser.phone ? currentUser.phone : "");

  let totalAmount = 0;'''

old_new_order = '''  const newOrder = {
    id: "ord_" + Date.now(),
    token: token,
    customer: customerName,
    items: items,
    total: totalAmount,
    time: timeStr,
    timestamp: Date.now(),
    status: "Cooking",
    prepTime: "6-8 mins"
  };'''

new_new_order = '''  const newOrder = {
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
    time: timeStr,
    timestamp: Date.now(),
    status: "Cooking",
    prepTime: "6-8 mins"
  };'''

# 4. Update renderLiveOrders to show student name with year and icon
old_render_live = '''    return `
      <div style="background:#ffffff; border:1.5px solid var(--border); border-radius:12px; padding:14px; margin-bottom:12px; box-shadow:var(--shadow-sm);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.15rem; font-weight:900; color:var(--primary); background:#eef2ff; padding:3px 9px; border-radius:8px; border:1px solid #c7d2fe;">${ord.token}</span>
            <span style="font-weight:700; font-size:0.92rem; color:var(--text-main);">${escapeHtml(ord.customer || "Student")}</span>
          </div>
          <span style="font-size:0.75rem; font-weight:800; padding:3px 9px; border-radius:999px; background:${statusBg}; color:${statusColor};">
            ${ord.status}
          </span>
        </div>
        <div style="font-size:0.86rem; color:var(--text-main); margin-bottom:10px;">
          <strong>Items:</strong> ${itemsStr || "Dishes"}
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #f1f5f9; padding-top:8px;">
          <span style="font-weight:800; font-size:0.9rem;">₹${ord.total}</span>
          ${actionBtn}
        </div>
      </div>
    `;'''

new_render_live = '''    let studentName = ord.customer || ord.customerName || ord.customer_name;
    if (!studentName || studentName.toLowerCase() === "student") {
      studentName = "Student Order";
    }
    const studentYear = ord.customerYear || ord.customer_year || ord.year || "";
    const studentPhone = ord.customerPhone || ord.customer_phone || ord.phone || "";

    const yearTag = studentYear 
      ? `<span style="display:inline-block; background:#e0f2fe; color:#0369a1; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:6px; margin-left:6px;">${escapeHtml(studentYear)}</span>` 
      : "";

    const phoneTag = studentPhone
      ? `<span style="font-size:0.78rem; color:var(--text-muted); margin-left:6px;">📞 ${escapeHtml(studentPhone)}</span>`
      : "";

    return `
      <div style="background:#ffffff; border:1.5px solid var(--border); border-radius:12px; padding:14px; margin-bottom:12px; box-shadow:var(--shadow-sm);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:6px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.15rem; font-weight:900; color:var(--primary); background:#eef2ff; padding:3px 9px; border-radius:8px; border:1px solid #c7d2fe;">${ord.token}</span>
            <div style="display:flex; align-items:center; flex-wrap:wrap;">
              <span style="font-weight:800; font-size:0.95rem; color:var(--text-main);">👤 ${escapeHtml(studentName)}</span>
              ${yearTag}
              ${phoneTag}
            </div>
          </div>
          <span style="font-size:0.75rem; font-weight:800; padding:3px 9px; border-radius:999px; background:${statusBg}; color:${statusColor};">
            ${ord.status}
          </span>
        </div>
        <div style="font-size:0.86rem; color:var(--text-main); margin-bottom:10px;">
          <strong>Items:</strong> ${itemsStr || "Dishes"}
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #f1f5f9; padding-top:8px;">
          <span style="font-weight:800; font-size:0.9rem; color:var(--primary);">₹${ord.total} <span style="font-size:0.75rem; color:var(--text-muted); font-weight:normal;">(${ord.time || "Just now"})</span></span>
          ${actionBtn}
        </div>
      </div>
    `;'''

# 5. Update fetchLiveOrdersFromBackend
old_fetch = '''function fetchLiveOrdersFromBackend() {
  try {
    const res = await fetch(`${API_BASE}/api/orders`);
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data)) {
        liveOrders = data;
        try { localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders)); } catch (e) {}
        renderLiveOrders();
        updateLiveOrderBadge();
      }
    }
  } catch (err) {}
}'''

new_fetch = '''async function fetchLiveOrdersFromBackend() {
  try {
    const res = await fetch(`${API_BASE}/api/orders`);
    if (res.ok) {
      const data = await res.json();
      const orders = Array.isArray(data) ? data : (data.orders || []);
      if (Array.isArray(orders) && orders.length > 0) {
        const existingIds = new Set(liveOrders.map(o => o.id));
        let changed = false;
        orders.forEach(backendOrder => {
          if (!backendOrder.customer && backendOrder.customerName) {
            backendOrder.customer = backendOrder.customerName;
          }
          if (!existingIds.has(backendOrder.id)) {
            liveOrders.push(backendOrder);
            changed = true;
          } else {
            const local = liveOrders.find(o => o.id === backendOrder.id);
            if (local && (local.status !== backendOrder.status || (!local.customer && backendOrder.customer))) {
              Object.assign(local, backendOrder);
              changed = true;
            }
          }
        });
        if (changed) {
          try { localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders)); } catch (e) {}
          renderLiveOrders();
          updateLiveOrderBadge();
        }
      }
    }
  } catch (err) {}
}'''

assert old_init in code, "old_init not found"
assert old_cart_name in code, "old_cart_name not found"
assert old_place_order in code, "old_place_order not found"
assert old_new_order in code, "old_new_order not found"
assert old_render_live in code, "old_render_live not found"
assert old_fetch in code, "old_fetch not found"

code = code.replace(old_init, new_init, 1)
code = code.replace(old_cart_name, new_cart_name, 1)
code = code.replace(old_place_order, new_place_order, 1)
code = code.replace(old_new_order, new_new_order, 1)
code = code.replace(old_render_live, new_render_live, 1)
code = code.replace(old_fetch, new_fetch, 1)

with open('scratch/build_clean_app_js.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("SUCCESS: Updated build_clean_app_js.py with student customer names everywhere!")
