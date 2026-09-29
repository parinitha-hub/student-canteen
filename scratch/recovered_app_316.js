import shutil
import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add myOrders state initialization
my_orders_init = """
let myOrders = [];
try {
  const savedMy = localStorage.getItem("savitha_my_orders");
  myOrders = savedMy ? JSON.parse(savedMy) : [];
} catch (e) {
  myOrders = [];
}
"""

if "let myOrders = [];" not in js:
    # Insert right after `let liveOrders = []; ... } catch (e) { ... }`
    target = 'const API_BASE ='
    assert target in js, "Failed to find API_BASE target"
    js = js.replace(target, my_orders_init + "\n" + target, 1)

# 2. Update placeOrderAndGenerateToken to push to myOrders
old_place_order = """  liveOrders.unshift(newOrder);
  lastPlacedOrder = newOrder;
  try {
    localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders));
    localStorage.setItem("savitha_student_active_order", JSON.stringify(newOrder));
  } catch (e) {}"""

new_place_order = """  liveOrders.unshift(newOrder);
  myOrders.unshift(newOrder);
  lastPlacedOrder = newOrder;
  try {
    localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders));
    localStorage.setItem("savitha_my_orders", JSON.stringify(myOrders));
    localStorage.setItem("savitha_student_active_order", JSON.stringify(newOrder));
  } catch (e) {}
  updateMyOrdersCount();"""

if "myOrders.unshift(newOrder);" not in js:
    # Handle possible CRLF or whitespace
    pattern = re.compile(r'liveOrders\.unshift\(newOrder\);[\r\n\s]+lastPlacedOrder\s*=\s*newOrder;[\r\n\s]+try\s*\{[\r\n\s]+localStorage\.setItem\("savitha_live_orders",\s*JSON\.stringify\(liveOrders\)\);[\r\n\s]+localStorage\.setItem\("savitha_student_active_order",\s*JSON\.stringify\(newOrder\)\);[\r\n\s]+\}\s*catch\s*\(e\)\s*\{\}')
    m = pattern.search(js)
    assert m, "Failed to regex match placeOrder save block"
    js = js[:m.start()] + new_place_order + js[m.end():]

# 3. Update cancelOrder to also remove from myOrders
new_cancel_order = """  // Remove from live queue immediately ("after ordering the item if i cancle it should go")
  liveOrders = liveOrders.filter(o => o.id !== target.id && o.token !== target.token);
  myOrders = myOrders.filter(o => o.id !== target.id && o.token !== target.token);
  try {
    localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders));
    localStorage.setItem("savitha_my_orders", JSON.stringify(myOrders));
  } catch (e) {}
  updateMyOrdersCount();
  renderMyOrdersList();"""

if "myOrders = myOrders.filter" not in js:
    pattern_cancel = re.compile(r'// Remove from live queue immediately[^\r\n]*[\r\n\s]+liveOrders\s*=\s*liveOrders\.filter\([^\)]+\);[\r\n\s]+try\s*\{[\r\n\s]+localStorage\.setItem\("savitha_live_orders",\s*JSON\.stringify\(liveOrders\)\);[\r\n\s]+\}\s*catch\s*\(e\)\s*\{\}')
    m2 = pattern_cancel.search(js)
    assert m2, "Failed to regex match cancelOrder save block"
    js = js[:m2.start()] + new_cancel_order + js[m2.end():]

# 4. Add my_orders modal functions
my_orders_fns = """
// ==========================================
// MY ORDERS MANAGEMENT (ACTIVE PICKUP TOKENS)
// ==========================================
function openMyOrdersModal() {
  const modal = document.getElementById("my-orders-modal");
  if (!modal) return;
  renderMyOrdersList();
  modal.classList.add("show");
}

function closeMyOrdersModal() {
  const modal = document.getElementById("my-orders-modal");
  if (modal) modal.classList.remove("show");
}

function updateMyOrdersCount() {
  const badgeTop = document.getElementById("my-orders-count");
  const countMenu = document.getElementById("menu-my-orders-count");
  const count = myOrders.length;

  if (badgeTop) {
    badgeTop.textContent = count;
    badgeTop.style.display = count > 0 ? "inline-block" : "none";
  }
  if (countMenu) {
    countMenu.textContent = count;
  }
}

function renderMyOrdersList() {
  const container = document.getElementById("my-orders-list-container");
  if (!container) return;

  if (myOrders.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:36px 16px; background:#f8fafc; border-radius:12px; border:1.5px dashed var(--border);">
        <div style="font-size:2.8rem; margin-bottom:8px;">📦</div>
        <h3 style="font-size:1.15rem; font-weight:800; color:var(--text-main); margin-bottom:4px;">No Orders Placed Yet</h3>
        <p style="font-size:0.86rem; color:var(--text-muted); margin-bottom:14px;">When you select dishes and order, your pickup tokens and live kitchen status will appear right here.</p>
        <button type="button" class="btn-calc" onclick="closeMyOrdersModal(); navigateToSection('order');" style="padding:9px 18px; font-size:0.88rem;">
          <span>🍽️</span> Browse Menu &amp; Order
        </button>
      </div>
    `;
    return;
  }

  container.innerHTML = myOrders.map(order => `
    <div class="my-order-card">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px; flex-wrap:wrap; gap:6px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:1.35rem; font-weight:900; color:var(--primary); background:#eef2ff; border:1px solid #c7d2fe; padding:2px 10px; border-radius:8px;">${order.token}</span>
          <span style="font-size:0.8rem; color:var(--text-muted);">🕒 ${order.time}</span>
        </div>
        <span class="order-status-badge ${order.status && order.status.includes('Ready') ? 'badge-ready' : 'badge-prep'}">
          ${order.status || 'Preparing in Kitchen ⏳'}
        </span>
      </div>

      <div style="background:#f8fafc; border-radius:8px; padding:8px 10px; margin-bottom:10px; font-size:0.85rem;">
        ${order.items.map(it => `
          <div style="display:flex; justify-content:space-between; margin-bottom:2px;">
            <span>${it.qty}x ${it.name}</span>
            <strong style="color:var(--text-main);">₹${it.subtotal || (it.price * it.qty)}</strong>
          </div>
        `).join('')}
        <div style="border-top:1px dashed #e2e8f0; margin-top:4px; padding-top:4px; display:flex; justify-content:space-between; font-weight:800;">
          <span>Total Paid</span>
          <span style="color:var(--primary); font-size:0.95rem;">₹${order.total}</span>
        </div>
      </div>

      <div style="display:flex; gap:8px;">
        <button type="button" class="btn-calc" onclick="viewOrderTokenDetails('${order.id}')" style="flex:1; padding:7px 12px; font-size:0.82rem; justify-content:center;">
          <span>👁️</span> View Pickup Token
        </button>
        <button type="button" class="btn-order-cancel" onclick="cancelOrder('${order.id}')" style="padding:7px 12px; font-size:0.82rem;">
          <span>❌</span> Cancel
        </button>
      </div>
    </div>
  `).join('');
}

function viewOrderTokenDetails(orderId) {
  const order = myOrders.find(o => o.id === orderId) || liveOrders.find(o => o.id === orderId);
  if (!order) {
    showToast("Order not found.", "warning");
    return;
  }
  closeMyOrdersModal();
  lastPlacedOrder = order;
  openTokenModal();
}
"""

if "function openMyOrdersModal" not in js:
    # Insert before window attachments
    marker = 'if (typeof window !== "undefined") window.performSwitchMode ='
    assert marker in js, "Failed to find marker for my_orders_fns"
    js = js.replace(marker, my_orders_fns + "\n" + marker, 1)

# 5. Export functions to window
my_orders_exports = """
if (typeof window !== "undefined") window.openMyOrdersModal = openMyOrdersModal;
if (typeof window !== "undefined") window.closeMyOrdersModal = closeMyOrdersModal;
if (typeof window !== "undefined") window.updateMyOrdersCount = updateMyOrdersCount;
if (typeof window !== "undefined") window.renderMyOrdersList = renderMyOrdersList;
if (typeof window !== "undefined") window.viewOrderTokenDetails = viewOrderTokenDetails;
if (typeof window !== "undefined") {
  try {
    Object.defineProperty(window, "myOrders", {
      get: () => myOrders,
      set: (v) => { myOrders = v; },
      configurable: true
    });
  } catch (e) {
    window.myOrders = myOrders;
  }
}
"""

if "window.openMyOrdersModal = openMyOrdersModal;" not in js:
    end_marker = 'if (typeof window !== "undefined") window.quickOrderDish = quickOrderDish;'
    assert end_marker in js, "Failed to find end_marker"
    js = js.replace(end_marker, end_marker + "\n" + my_orders_exports, 1)

# 6. Update initUserAuth and DOMContentLoaded to call updateMyOrdersCount
if "updateMyOrdersCount();" not in js[:js.find("function toggleStaffLoginForm")]:
    target_init = "applyRoleVisibility();\r\n  // Open About"
    if target_init not in js:
        target_init = "applyRoleVisibility();\n  // Open About"
    js = js.replace(target_init, "applyRoleVisibility();\n  updateMyOrdersCount();\n  // Open About", 1)

if "updateMyOrdersCount();" not in js[js.find("document.addEventListener(\"DOMContentLoaded\""):js.find("checkServerHealth();")]:
    target_dom = "initUserAuth();\r\n  updateKitchenPasswordDisplay();"
    if target_dom not in js:
        target_dom = "initUserAuth();\n  updateKitchenPasswordDisplay();"
    js = js.replace(target_dom, "initUserAuth();\n  updateMyOrdersCount();\n  updateKitchenPasswordDisplay();", 1)

# Write to js/app.js and frontend/js/app.js
with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

shutil.copyfile('js/app.js', 'frontend/js/app.js')
print("Successfully updated js/app.js and frontend/js/app.js!")
