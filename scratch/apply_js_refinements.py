import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update placeOrderAndGenerateToken to open My Orders directly
old_place_order_token_call = """  // Open the token modal immediately so student sees their pickup token
  openTokenModal();

  showToast(`🎉 Order placed! Token: ${token}`, "success");"""

new_place_order_token_call = """  // If we order anything, it is visible ONLY in My Orders, not anywhere else!
  openMyOrdersModal();
  showToast(`🎉 Order placed successfully! Token: ${token} (View in My Orders)`, "success");"""

assert old_place_order_token_call in js, "Failed to find old_place_order_token_call"
js = js.replace(old_place_order_token_call, new_place_order_token_call)
print("✓ Updated placeOrderAndGenerateToken to open My Orders directly")

# 2. Update renderMyOrdersList with clean, complete order cards with token and items
old_render_my_orders = """  container.innerHTML = myOrders.map(ord => {
    const isReady = ord.status === "Ready";
    const statusBg = isReady ? "#dcfce7" : "#fef3c7";
    const statusColor = isReady ? "#16a34a" : "#d97706";
    const statusIcon = isReady ? "✅" : "🔥";
    const statusText = isReady ? "Ready for Pickup" : "Cooking";

    const itemsSummary = (ord.items || []).map(i => `${i.qty}x ${i.name}`).join(", ");

    return `
      <div style="background:#ffffff; border:1.5px solid var(--border); border-radius:12px; padding:14px; margin-bottom:12px; box-shadow:var(--shadow-sm);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.2rem; font-weight:900; color:var(--primary); background:#eef2ff; padding:4px 10px; border-radius:8px; border:1px solid #c7d2fe;">${ord.token}</span>
            <span style="font-size:0.8rem; color:var(--text-muted);">Placed at ${ord.time || "Recently"}</span>
          </div>
          <span style="font-size:0.75rem; font-weight:800; padding:4px 10px; border-radius:999px; background:${statusBg}; color:${statusColor}; display:inline-flex; align-items:center; gap:4px;">
            ${statusIcon} ${statusText}
          </span>
        </div>

        <div style="font-size:0.88rem; color:var(--text-main); margin-bottom:10px; line-height:1.4;">
          <strong>Dishes:</strong> ${itemsSummary || "Selected Meals"}
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #f1f5f9; padding-top:10px;">
          <div style="font-size:1rem; font-weight:800; color:var(--text-main);">
            Total: ₹${ord.total}
          </div>
          <div style="display:flex; gap:8px;">
            <button type="button" class="btn-calc" onclick="viewOrderTokenDetails('${ord.id}')" style="padding:6px 14px; font-size:0.82rem; background:#f8fafc; border:1px solid var(--border); color:var(--text-main);">
              <span>🎫</span> View Token
            </button>
            <button type="button" class="btn-banner-cancel" onclick="cancelOrder('${ord.id}')" style="padding:6px 12px; font-size:0.82rem; background:#fee2e2; border:1px solid #fca5a5; color:#dc2626; border-radius:8px; cursor:pointer; font-weight:700;">
              <span>❌</span> Cancel
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');"""

new_render_my_orders = """  container.innerHTML = myOrders.map(ord => {
    const isReady = ord.status && (ord.status.includes("Ready") || ord.status === "Ready");
    const statusBg = isReady ? "#dcfce7" : "#fef3c7";
    const statusColor = isReady ? "#15803d" : "#b45309";
    const statusIcon = isReady ? "✅" : "⏳";
    const statusText = isReady ? "Ready for Pickup at Counter!" : (ord.status || "Preparing in Kitchen ⏳");

    const itemsRows = (ord.items || []).map(i => `
      <div style="display:flex; justify-content:space-between; margin-bottom:3px; font-size:0.86rem; color:var(--text-main);">
        <span>${i.qty}x ${i.name}</span>
        <strong>₹${i.price * i.qty}</strong>
      </div>
    `).join('');

    return `
      <div class="my-order-card" style="background:#ffffff; border:1.5px solid var(--border); border-radius:14px; padding:16px; margin-bottom:14px; box-shadow:var(--shadow-sm);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; flex-wrap:wrap; gap:8px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.35rem; font-weight:900; color:var(--primary); background:#eef2ff; padding:4px 12px; border-radius:8px; border:1.5px solid #c7d2fe; letter-spacing:0.5px;">${ord.token}</span>
            <span style="font-size:0.8rem; color:var(--text-muted);">🕒 ${ord.time || "Recently"}</span>
          </div>
          <span style="font-size:0.78rem; font-weight:800; padding:4px 10px; border-radius:999px; background:${statusBg}; color:${statusColor}; display:inline-flex; align-items:center; gap:4px;">
            ${statusIcon} ${statusText}
          </span>
        </div>

        <div style="background:#f8fafc; border-radius:10px; padding:10px 12px; margin-bottom:10px; border:1px solid #f1f5f9;">
          <div style="font-size:0.75rem; font-weight:700; color:var(--text-muted); text-transform:uppercase; margin-bottom:6px;">Order Summary</div>
          ${itemsRows || '<div style="font-size:0.86rem;">Selected Meals</div>'}
          <div style="border-top:1px dashed #e2e8f0; margin-top:6px; padding-top:6px; display:flex; justify-content:space-between; font-weight:800; font-size:0.95rem;">
            <span>Total Paid</span>
            <span style="color:var(--primary);">₹${ord.total}</span>
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:0.8rem; color:var(--text-muted);">Show token at counter to collect</span>
          <button type="button" class="btn-banner-cancel" onclick="cancelOrder('${ord.id}')"
            style="padding:6px 14px; font-size:0.82rem; background:#fee2e2; border:1.5px solid #fca5a5; color:#dc2626; border-radius:8px; cursor:pointer; font-weight:700; display:inline-flex; align-items:center; gap:4px;">
            <span>❌</span> Cancel Order
          </button>
        </div>
      </div>
    `;
  }).join('');"""

assert old_render_my_orders in js, "Failed to find old_render_my_orders"
js = js.replace(old_render_my_orders, new_render_my_orders)
print("✓ Updated renderMyOrdersList with self-contained order cards")

# 3. Update performSwitchMode: Hide Menu & My Orders on About
old_perform_switch = """  if (mode === "about") {
    if (toggle) toggle.style.display = "none";
    if (cartBtn) cartBtn.style.display = "none";
    if (floatingBar) floatingBar.classList.remove("show");
    const navAbout = document.getElementById("nav-btn-about");
    if (navAbout) navAbout.classList.add("active");

    if (viewAbout) {
      viewAbout.style.display = "block";
      viewAbout.style.animation = "fadeIn 0.25s ease-out";
    }
  } else if (mode === "login") {
    if (toggle) toggle.style.display = "none";
    if (cartBtn) cartBtn.style.display = "none";
    if (floatingBar) floatingBar.classList.remove("show");
    const navLogin = document.getElementById("nav-btn-login");
    if (navLogin) navLogin.classList.add("active");

    if (viewLogin) {
      viewLogin.style.display = "block";
      viewLogin.style.animation = "fadeIn 0.25s ease-out";
    }
  } else if (mode === "manager") {
    if (toggle) toggle.style.display = "flex";
    if (cartBtn) cartBtn.style.display = "none";
    if (btnMgr) btnMgr.classList.add("active");
    if (floatingBar) floatingBar.classList.remove("show");
    const navKitchen = document.getElementById("nav-btn-kitchen");
    if (navKitchen) navKitchen.classList.add("active");

    if (viewMgr) {
      viewMgr.style.display = "block";
      viewMgr.classList.add("show");
      viewMgr.style.animation = "fadeIn 0.25s ease-out";
    }
    switchManagerTab("orders");
  } else {
    // Mode is "order" or "home"
    if (toggle) toggle.style.display = "flex";
    if (cartBtn) cartBtn.style.display = "flex";
    if (btnOrder) btnOrder.classList.add("active");
    const navHome = document.getElementById("nav-btn-home");
    if (navHome) navHome.classList.add("active");

    if (viewOrder) {
      viewOrder.style.display = "block";
      viewOrder.style.animation = "fadeIn 0.25s ease-out";
    }
    renderDishes();
    updateCartBar();
    updateMyOrdersCount();
  }"""

new_perform_switch = """  const navHome = document.getElementById("nav-btn-home");
  const navOrders = document.getElementById("btn-top-my-orders-nav");
  const navAbout = document.getElementById("nav-btn-about");
  const navLogin = document.getElementById("nav-btn-login");
  const navKitchen = document.getElementById("nav-btn-kitchen");

  // Ensure modals are closed upon mode switch
  closeMyOrdersModal();
  closeCartModal();

  if (mode === "about") {
    // In About webpage, we should NOT be able to see Menu and My Orders!
    if (navHome) navHome.style.display = "none";
    if (navOrders) navOrders.style.display = "none";
    if (navKitchen) navKitchen.style.display = "none";
    if (navAbout) navAbout.classList.add("active");

    if (toggle) toggle.style.display = "none";
    if (cartBtn) cartBtn.style.display = "none";
    if (floatingBar) floatingBar.classList.remove("show");

    if (viewAbout) {
      viewAbout.style.display = "block";
      viewAbout.style.animation = "fadeIn 0.25s ease-out";
    }
  } else if (mode === "login") {
    // In Login view, Menu and My Orders are also hidden
    if (navHome) navHome.style.display = "none";
    if (navOrders) navOrders.style.display = "none";
    if (navKitchen) navKitchen.style.display = "none";
    if (navLogin) navLogin.classList.add("active");

    if (toggle) toggle.style.display = "none";
    if (cartBtn) cartBtn.style.display = "none";
    if (floatingBar) floatingBar.classList.remove("show");

    if (viewLogin) {
      viewLogin.style.display = "block";
      viewLogin.style.animation = "fadeIn 0.25s ease-out";
    }
  } else if (mode === "manager") {
    if (navHome) navHome.style.display = "none";
    if (navOrders) navOrders.style.display = "none";
    if (navKitchen) {
      navKitchen.style.display = "inline-flex";
      navKitchen.classList.add("active");
    }

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
    // Mode is "order" or "home" - Menu and My Orders are visible
    if (navHome) {
      navHome.style.display = "inline-flex";
      navHome.classList.add("active");
    }
    if (navOrders) {
      navOrders.style.display = "inline-flex";
    }
    if (navKitchen) {
      navKitchen.style.display = (currentUser && currentUser.role === "worker") ? "inline-flex" : "none";
    }

    if (toggle) toggle.style.display = "flex";
    if (cartBtn) cartBtn.style.display = "flex";
    if (btnOrder) btnOrder.classList.add("active");

    if (viewOrder) {
      viewOrder.style.display = "block";
      viewOrder.style.animation = "fadeIn 0.25s ease-out";
    }
    renderDishes();
    updateCartBar();
    updateMyOrdersCount();
  }"""

assert old_perform_switch in js, "Failed to find old_perform_switch"
js = js.replace(old_perform_switch, new_perform_switch)
print("✓ Updated performSwitchMode to hide Menu & My Orders on About")

# Write out js/app.js and copy to frontend/js/app.js
with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

shutil.copyfile('js/app.js', 'frontend/js/app.js')
print("Successfully updated js/app.js and frontend/js/app.js!")
