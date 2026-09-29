import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app_path = os.path.join(ROOT, "js", "app.js")
frontend_app_path = os.path.join(ROOT, "frontend", "js", "app.js")

with open(app_path, "r", encoding="utf-8") as f:
    code = f.read()

# -----------------------------------------------------------------------------
# 1. INVENTORY SYSTEM & DATA MODEL
# -----------------------------------------------------------------------------
inventory_code = """
// =========================================================================
// KITCHEN INVENTORY & STOCK MONITORING ENGINE
// =========================================================================
let inventory = [];
let currentInventoryCategory = "all";
let currentInventoryStatus = "all";
let inventorySearchQuery = "";

function initInventory() {
  try {
    const raw = localStorage.getItem("savitha_inventory");
    if (raw) {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed) && parsed.length > 0) {
        inventory = parsed;
        updateInventoryBadge();
        return inventory;
      }
    }
  } catch (e) {}

  inventory = DISHES.map(d => ({
    id: d.id,
    name: d.name,
    category: d.category,
    price: d.price,
    image: d.image,
    isVeg: d.isVeg,
    stock: d.id === "chicken_biryani" ? 45 : (d.id === "samosa_chai" ? 75 : (d.id === "veg_biryani" ? 60 : 40)),
    threshold: 10,
    status: "in_stock",
    lastUpdated: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }));
  saveInventory();
  updateInventoryBadge();
  return inventory;
}

function getInventory() {
  if (!inventory || inventory.length === 0) {
    initInventory();
  }
  return inventory;
}

function getInventoryItem(dishId) {
  const inv = getInventory();
  return inv.find(i => i.id === dishId) || null;
}

function saveInventory() {
  try {
    localStorage.setItem("savitha_inventory", JSON.stringify(inventory));
  } catch (e) {}
}

function updateInventoryBadge() {
  const badge = document.getElementById("inv-low-stock-badge");
  const inv = getInventory();
  const lowCount = inv.filter(i => i.status === "low_stock" || i.status === "out_of_stock").length;
  if (badge) {
    badge.textContent = lowCount;
    badge.style.display = lowCount > 0 ? "inline-block" : "none";
  }
}

function updateItemStock(dishId, newStock) {
  const item = getInventoryItem(dishId);
  if (!item) return;
  const num = Math.max(0, parseInt(newStock) || 0);
  item.stock = num;
  if (num === 0) {
    item.status = "out_of_stock";
  } else if (num <= item.threshold) {
    item.status = "low_stock";
  } else {
    item.status = "in_stock";
  }
  item.lastUpdated = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  saveInventory();
  renderInventoryDashboard();
  renderDishes();
  updateInventoryBadge();
  showToast(`Updated stock for ${item.name}: ${item.stock} portions`, "info");
}

function adjustItemStock(dishId, delta) {
  const item = getInventoryItem(dishId);
  if (!item) return;
  updateItemStock(dishId, item.stock + delta);
}

function toggleItemStatus(dishId) {
  const item = getInventoryItem(dishId);
  if (!item) return;
  if (item.status === "out_of_stock") {
    item.status = item.stock <= item.threshold ? (item.stock > 0 ? "low_stock" : "in_stock") : "in_stock";
    if (item.stock === 0) item.stock = 25;
  } else {
    item.status = "out_of_stock";
  }
  item.lastUpdated = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  saveInventory();
  renderInventoryDashboard();
  renderDishes();
  updateInventoryBadge();
  showToast(`${item.name} is now ${item.status === "out_of_stock" ? "Marked Sold Out 🔴" : "Available In Stock 🟢"}`, "info");
}

function restockAll(addedPortions = 20) {
  const inv = getInventory();
  inv.forEach(item => {
    item.stock += addedPortions;
    if (item.status === "out_of_stock" && item.stock > 0) {
      item.status = item.stock <= item.threshold ? "low_stock" : "in_stock";
    }
  });
  saveInventory();
  renderInventoryDashboard();
  renderDishes();
  updateInventoryBadge();
  showToast(`⚡ Restocked all items (+${addedPortions} portions)!`, "success");
}

function decrementOrderInventory(items) {
  if (!Array.isArray(items)) return;
  const inv = getInventory();
  let changed = false;
  items.forEach(orderItem => {
    const invItem = inv.find(i => i.id === orderItem.dishId);
    if (invItem) {
      invItem.stock = Math.max(0, invItem.stock - (orderItem.qty || 1));
      if (invItem.stock === 0) {
        invItem.status = "out_of_stock";
      } else if (invItem.stock <= invItem.threshold) {
        invItem.status = "low_stock";
      }
      changed = true;
    }
  });
  if (changed) {
    saveInventory();
    renderInventoryDashboard();
    renderDishes();
    updateInventoryBadge();
  }
}

function filterInventoryCategory(cat, btn) {
  currentInventoryCategory = cat;
  document.querySelectorAll(".inv-filter-pill").forEach(p => p.classList.remove("active"));
  if (btn) btn.classList.add("active");
  renderInventoryDashboard();
}

function filterInventoryStatus(status, btn) {
  currentInventoryStatus = (currentInventoryStatus === status) ? "all" : status;
  document.querySelectorAll(".inv-filter-pill").forEach(p => p.classList.remove("active"));
  if (btn && currentInventoryStatus !== "all") btn.classList.add("active");
  renderInventoryDashboard();
}

function searchInventory(query) {
  inventorySearchQuery = (query || "").trim().toLowerCase();
  renderInventoryDashboard();
}

function renderInventoryDashboard() {
  const tableBody = document.getElementById("inventory-table-body");
  const statTotal = document.getElementById("inv-stat-total");
  const statInStock = document.getElementById("inv-stat-instock");
  const statLowStock = document.getElementById("inv-stat-lowstock");
  const statSoldOut = document.getElementById("inv-stat-soldout");
  const warningBanner = document.getElementById("inv-warning-banner");
  const warningText = document.getElementById("inv-warning-text");

  const inv = getInventory();

  const total = inv.length;
  const inStock = inv.filter(i => i.status === "in_stock").length;
  const lowStock = inv.filter(i => i.status === "low_stock").length;
  const soldOut = inv.filter(i => i.status === "out_of_stock").length;

  if (statTotal) statTotal.textContent = total;
  if (statInStock) statInStock.textContent = inStock;
  if (statLowStock) statLowStock.textContent = lowStock;
  if (statSoldOut) statSoldOut.textContent = soldOut;

  const lowItems = inv.filter(i => i.status === "low_stock");
  if (warningBanner && warningText) {
    if (lowItems.length > 0) {
      warningBanner.style.display = "block";
      const names = lowItems.slice(0, 3).map(i => `${i.name} (${i.stock} left)`).join(", ");
      warningText.textContent = `Low stock alert: ${names}. Restock soon.`;
    } else {
      warningBanner.style.display = "none";
    }
  }

  if (!tableBody) return;

  let filtered = inv;
  if (currentInventoryCategory !== "all") {
    filtered = filtered.filter(i => i.category === currentInventoryCategory);
  }
  if (currentInventoryStatus === "low_stock") {
    filtered = filtered.filter(i => i.status === "low_stock");
  } else if (currentInventoryStatus === "out_of_stock") {
    filtered = filtered.filter(i => i.status === "out_of_stock");
  }
  if (inventorySearchQuery) {
    filtered = filtered.filter(i => i.name.toLowerCase().includes(inventorySearchQuery));
  }

  if (filtered.length === 0) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="6" style="text-align:center; padding:32px 16px; color:var(--text-muted); font-size:0.9rem;">
          No items match the selected filter.
        </td>
      </tr>
    `;
    return;
  }

  tableBody.innerHTML = filtered.map(item => {
    let badgeHtml = '';
    if (item.status === "in_stock") {
      badgeHtml = `<span class="badge-instock">🟢 In Stock (${item.stock})</span>`;
    } else if (item.status === "low_stock") {
      badgeHtml = `<span class="badge-lowstock">🟡 Low Stock (${item.stock} left)</span>`;
    } else {
      badgeHtml = `<span class="badge-outstock">🔴 Sold Out</span>`;
    }

    const typeIcon = item.isVeg ? '<span style="color:#10b981; font-size:0.8rem;">● Veg</span>' : '<span style="color:#e11d48; font-size:0.8rem;">▲ Non-Veg</span>';

    return `
      <tr style="border-bottom:1px solid var(--border);">
        <td style="padding:12px 16px;">
          <div style="display:flex; align-items:center; gap:10px;">
            <img src="${item.image}" alt="${item.name}" style="width:40px; height:40px; border-radius:8px; object-fit:cover;" onerror="this.src='assets/hero_banner.jpg'">
            <div>
              <strong style="font-size:0.9rem; color:var(--text-main); display:block;">${item.name}</strong>
              <div style="font-size:0.75rem; color:var(--text-muted);">${typeIcon} • Updated ${item.lastUpdated || 'recently'}</div>
            </div>
          </div>
        </td>
        <td style="padding:12px 14px; text-transform:capitalize; font-size:0.85rem; color:var(--text-muted);">${item.category}</td>
        <td style="padding:12px 14px; font-weight:800; color:var(--text-main);">₹${item.price}</td>
        <td style="padding:12px 14px; text-align:center;">
          <div style="display:inline-flex; align-items:center; gap:4px;">
            <button type="button" class="btn-stock-adjust" onclick="adjustItemStock('${item.id}', -5)" title="Decrease 5">-5</button>
            <button type="button" class="btn-stock-adjust" onclick="adjustItemStock('${item.id}', -1)" title="Decrease 1">-1</button>
            <input type="number" min="0" value="${item.stock}" class="stock-input-field"
              onchange="updateItemStock('${item.id}', this.value)"
              onkeydown="if(event.key==='Enter') this.blur();">
            <button type="button" class="btn-stock-adjust" onclick="adjustItemStock('${item.id}', 1)" title="Increase 1">+1</button>
            <button type="button" class="btn-stock-adjust" onclick="adjustItemStock('${item.id}', 5)" title="Increase 5">+5</button>
            <button type="button" class="btn-stock-adjust" onclick="adjustItemStock('${item.id}', 10)" title="Increase 10">+10</button>
          </div>
        </td>
        <td style="padding:12px 14px;">${badgeHtml}</td>
        <td style="padding:12px 16px; text-align:right;">
          <button type="button" onclick="toggleItemStatus('${item.id}')"
            style="padding:6px 12px; font-size:0.78rem; font-weight:800; border-radius:6px; cursor:pointer; border:1px solid ${item.status === 'out_of_stock' ? '#86efac' : '#fca5a5'}; background:${item.status === 'out_of_stock' ? '#f0fdf4' : '#fef2f2'}; color:${item.status === 'out_of_stock' ? '#15803d' : '#b91c1c'};">
            ${item.status === 'out_of_stock' ? '✓ Mark Available' : '✕ Mark Sold Out'}
          </button>
        </td>
      </tr>
    `;
  }).join('');
}
"""

if "function initInventory()" not in code:
    code = code.replace(
        "// 4. FOOD MENU & CART CONTROLLER",
        inventory_code + "\n// 4. FOOD MENU & CART CONTROLLER"
    )
    print("Added Inventory Engine to js/app.js")

# -----------------------------------------------------------------------------
# 2. UPDATE renderDishes WITH QUANTITY UPDATE BUTTONS & OUT OF STOCK BADGE
# -----------------------------------------------------------------------------
old_render_dishes = '''function renderDishes() {
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
          <button type="button" onclick="updateDishQty('${dish.id}', -1)" aria-label="Decrease quantity">-</button>
          <span>${qty}</span>
          <button type="button" onclick="updateDishQty('${dish.id}', 1)" aria-label="Increase quantity">+</button>
        </div>
      `;
    } else {
      buttonHtml = `
        <button type="button" class="add-btn" onclick="updateDishQty('${dish.id}', 1)">
          ADD +
        </button>
      `;
    }

    // Compute 5-star visual representation for food items
    const fullStars = Math.floor(dish.rating);
    const hasHalf = (dish.rating - fullStars) >= 0.5;
    let starsStr = "★".repeat(fullStars);
    if (hasHalf && starsStr.length < 5) starsStr += "★";
    const emptyCount = Math.max(0, 5 - starsStr.length);
    const emptyStr = "☆".repeat(emptyCount);

    html += `
      <div class="dish-card">
        <div class="dish-img-wrap">
          <img src="${dish.image}" alt="${dish.name}" class="dish-img" onerror="this.src='assets/hero_banner.jpg'">
          <div class="food-type-icon ${typeClass}"></div>
          <span class="rating-badge">★ ${dish.rating}</span>
          <div class="dish-img-overlay"></div>
        </div>
        <div class="dish-body">
          <div class="dish-title-row">
            <h3 class="dish-name">${dish.name}</h3>
          </div>

          <!-- Prominent Star Rating for Food Item -->
          <div class="dish-star-rating-row" style="display:flex; align-items:center; gap:6px; margin:4px 0 8px 0;">
            <div class="dish-stars-graphic" style="color:#f59e0b; font-size:1.08rem; letter-spacing:1px; line-height:1;" title="${dish.rating} out of 5 stars">
              <span>${starsStr}</span><span style="color:#cbd5e1;">${emptyStr}</span>
            </div>
            <span class="dish-rating-score" style="font-size:0.88rem; font-weight:800; color:var(--text-main);">${dish.rating}</span>
            <span class="dish-reviews-count" style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">(${dish.reviews} reviews)</span>
          </div>

          <p class="dish-desc">${dish.desc}</p>
          <div class="demand-tag">${dish.demandStatus}</div>
          <div class="dish-footer">
            <div class="dish-price">
              ${dish.originalPrice ? `<span style="text-decoration:line-through; font-size:0.85rem; color:#94a3b8; margin-right:4px;">₹${dish.originalPrice}</span> ` : ''}₹${dish.price}
              ${dish.originalPrice ? `<span style="font-size:0.75rem; color:#10b981; font-weight:800; margin-left:4px;">58% OFF</span>` : ''}
            </div>
            <div id="btn-wrap-${dish.id}">
              ${buttonHtml}
            </div>
          </div>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}'''

new_render_dishes = '''function renderDishes() {
  const container = document.getElementById("dishes-grid");
  if (!container) return;

  const filtered = currentCategory === "all" 
    ? DISHES 
    : DISHES.filter(d => d.category === currentCategory);

  let html = "";
  filtered.forEach(dish => {
    const inv = getInventoryItem(dish.id);
    const isSoldOut = inv ? (inv.status === "out_of_stock" || inv.stock <= 0) : false;
    const isLowStock = inv ? (!isSoldOut && inv.stock <= inv.threshold) : false;
    const qty = cart[dish.id] || 0;
    const typeClass = dish.isVeg ? "veg" : "non-veg";
    let buttonHtml = "";

    if (isSoldOut) {
      buttonHtml = `
        <button type="button" class="btn-sold-out" disabled title="Currently Sold Out in kitchen">
          Sold Out
        </button>
      `;
    } else if (qty > 0) {
      buttonHtml = `
        <div style="display:flex; align-items:center; gap:6px;">
          <div class="qty-pill">
            <button type="button" class="qty-btn-minus" onclick="updateDishQty('${dish.id}', -1)" aria-label="Decrease quantity" title="Decrease quantity">−</button>
            <span class="qty-val">${qty}</span>
            <button type="button" class="qty-btn-plus" onclick="updateDishQty('${dish.id}', 1)" aria-label="Increase quantity" title="Increase quantity">+</button>
          </div>
          <button type="button" class="btn-order-now-selected" onclick="openCartModal()" title="View in cart & order now">
            Order Now
          </button>
        </div>
      `;
    } else {
      buttonHtml = `
        <button type="button" class="add-btn" onclick="updateDishQty('${dish.id}', 1)" title="Add to cart">
          ADD +
        </button>
      `;
    }

    // Compute 5-star visual representation for food items
    const fullStars = Math.floor(dish.rating);
    const hasHalf = (dish.rating - fullStars) >= 0.5;
    let starsStr = "★".repeat(fullStars);
    if (hasHalf && starsStr.length < 5) starsStr += "★";
    const emptyCount = Math.max(0, 5 - starsStr.length);
    const emptyStr = "☆".repeat(emptyCount);

    html += `
      <div class="dish-card ${isSoldOut ? 'out-of-stock' : ''}">
        <div class="dish-img-wrap">
          <img src="${dish.image}" alt="${dish.name}" class="dish-img" onerror="this.src='assets/hero_banner.jpg'">
          <div class="food-type-icon ${typeClass}"></div>
          <span class="rating-badge">★ ${dish.rating}</span>
          ${isSoldOut ? '<div style="position:absolute; top:12px; left:12px; z-index:4;"><span class="badge-sold-out">🔴 SOLD OUT</span></div>' : ''}
          <div class="dish-img-overlay"></div>
        </div>
        <div class="dish-body">
          <div class="dish-title-row">
            <h3 class="dish-name">${dish.name}</h3>
          </div>

          <!-- Prominent Star Rating for Food Item -->
          <div class="dish-star-rating-row" style="display:flex; align-items:center; gap:6px; margin:4px 0 8px 0;">
            <div class="dish-stars-graphic" style="color:#f59e0b; font-size:1.08rem; letter-spacing:1px; line-height:1;" title="${dish.rating} out of 5 stars">
              <span>${starsStr}</span><span style="color:#cbd5e1;">${emptyStr}</span>
            </div>
            <span class="dish-rating-score" style="font-size:0.88rem; font-weight:800; color:var(--text-main);">${dish.rating}</span>
            <span class="dish-reviews-count" style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">(${dish.reviews} reviews)</span>
          </div>

          <p class="dish-desc">${dish.desc}</p>
          <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap; margin-bottom:8px;">
            <div class="demand-tag">${dish.demandStatus}</div>
            ${isLowStock ? `<span style="font-size:0.72rem; color:#d97706; font-weight:800; background:#fef3c7; padding:2px 8px; border-radius:6px;">⚠️ Only ${inv.stock} portions left!</span>` : ''}
          </div>
          <div class="dish-footer">
            <div class="dish-price">
              ${dish.originalPrice ? `<span style="text-decoration:line-through; font-size:0.85rem; color:#94a3b8; margin-right:4px;">₹${dish.originalPrice}</span> ` : ''}₹${dish.price}
              ${dish.originalPrice ? `<span style="font-size:0.75rem; color:#10b981; font-weight:800; margin-left:4px;">58% OFF</span>` : ''}
            </div>
            <div id="btn-wrap-${dish.id}">
              ${buttonHtml}
            </div>
          </div>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}'''

if old_render_dishes in code:
    code = code.replace(old_render_dishes, new_render_dishes)
    print("Updated renderDishes with inventory checks and quantity update button.")
else:
    print("Warning: old renderDishes did not match exactly, checking alternatives...")

# -----------------------------------------------------------------------------
# 3. UPDATE updateDishQty WITH INVENTORY LIMITS
# -----------------------------------------------------------------------------
old_update_qty = '''function updateDishQty(dishId, delta) {
  // STRICT LOGIN GUARD: Without login, cannot select dishes
  if (!currentUser || !currentUser.role) {
    showToast("🔒 Please login first to select dishes and order!", "warning");
    performSwitchMode("login");
    return;
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
}'''

new_update_qty = '''function updateDishQty(dishId, delta) {
  // STRICT LOGIN GUARD: Without login, cannot select dishes
  if (!currentUser || !currentUser.role) {
    showToast("🔒 Please login first to select dishes and order!", "warning");
    performSwitchMode("login");
    return;
  }

  const invItem = getInventoryItem(dishId);
  const current = cart[dishId] || 0;
  const next = current + delta;

  // Inventory validation when incrementing quantity
  if (delta > 0 && invItem) {
    if (invItem.status === "out_of_stock" || invItem.stock <= 0) {
      showToast(`Sorry, ${invItem.name} is currently Sold Out in the kitchen!`, "warning");
      return;
    }
    if (next > invItem.stock) {
      showToast(`Only ${invItem.stock} portion(s) available in kitchen stock for ${invItem.name}!`, "warning");
      return;
    }
  }

  if (next <= 0) {
    delete cart[dishId];
  } else {
    cart[dishId] = next;
  }

  renderDishes();
  updateCartBar();
}'''

if old_update_qty in code:
    code = code.replace(old_update_qty, new_update_qty)
    print("Updated updateDishQty with inventory guards.")

# -----------------------------------------------------------------------------
# 4. UPDATE openCartModal WITH QUANTITY UPDATE BUTTONS IN CART
# -----------------------------------------------------------------------------
old_cart_item_row = '''        <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid var(--border);">
          <div style="display:flex; align-items:center; gap:10px;">
            <img src="${dish.image}" alt="${dish.name}" style="width:44px; height:44px; border-radius:8px; object-fit:cover;" onerror="this.src='assets/hero_banner.jpg'">
            <div>
              <strong style="color:var(--text-main); font-size:0.95rem;">${dish.name}</strong>
              <div style="font-size:0.8rem; color:var(--text-muted);">₹${dish.price} x ${qty}</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:12px;">
            <strong style="color:var(--text-main);">₹${itemCost}</strong>
            <button type="button" onclick="updateDishQty('${dish.id}', -1); openCartModal();" style="background:transparent; border:none; color:#ef4444; font-size:1.1rem; cursor:pointer;" aria-label="Remove item">✕</button>
          </div>
        </div>'''

new_cart_item_row = '''        <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid var(--border); gap:8px;">
          <div style="display:flex; align-items:center; gap:10px; flex:1; min-width:0;">
            <img src="${dish.image}" alt="${dish.name}" style="width:44px; height:44px; border-radius:8px; object-fit:cover; flex-shrink:0;" onerror="this.src='assets/hero_banner.jpg'">
            <div style="overflow:hidden;">
              <strong style="color:var(--text-main); font-size:0.92rem; display:block; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;">${dish.name}</strong>
              <div style="font-size:0.78rem; color:var(--text-muted);">₹${dish.price} each</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:8px; flex-shrink:0;">
            <!-- Student Quantity Update Button in Cart Modal -->
            <div class="cart-qty-ctrl">
              <button type="button" class="cart-qty-btn cart-qty-minus" onclick="updateDishQty('${dish.id}', -1); openCartModal();" aria-label="Decrease quantity" title="Decrease quantity">−</button>
              <span class="cart-qty-val">${qty}</span>
              <button type="button" class="cart-qty-btn cart-qty-plus" onclick="updateDishQty('${dish.id}', 1); openCartModal();" aria-label="Increase quantity" title="Increase quantity">+</button>
            </div>
            <strong style="color:var(--text-main); min-width:50px; text-align:right; font-size:0.92rem;">₹${itemCost}</strong>
            <button type="button" onclick="updateDishQty('${dish.id}', -${qty}); openCartModal();" style="background:#fee2e2; border:1px solid #fca5a5; color:#ef4444; border-radius:6px; width:26px; height:26px; display:inline-flex; align-items:center; justify-content:center; font-size:0.85rem; cursor:pointer;" aria-label="Remove item" title="Remove item">✕</button>
          </div>
        </div>'''

if old_cart_item_row in code:
    code = code.replace(old_cart_item_row, new_cart_item_row)
    print("Updated openCartModal with Quantity Update Buttons.")

# -----------------------------------------------------------------------------
# 5. CHANGE FREE MEAL TO SMALL ITEM (BEVERAGE / SNACK) AFTER 10 ORDERS
# -----------------------------------------------------------------------------
code = code.replace(
    '🎉 10th Order FREE MEAL Unlocked! Tap \'FREE10\' to claim!',
    '🎉 10th Order FREE SMALL ITEM Unlocked! Tap \'FREE10\' to claim up to ₹35 off beverages/snacks! ☕'
)
code = code.replace(
    'unlock your 100% FREE Meal! 🎁',
    'unlock your Free Small Item (Beverage / Snack)! ☕'
)
code = code.replace(
    '10th Order: 100% FREE Meal!',
    '10th Order: Free Beverage or Snack Item (Up to ₹35 OFF)'
)
code = code.replace(
    '${isTenth ? \'FREE\' : \'#\' + i}',
    '${isTenth ? \'☕ FREE\' : \'#\' + i}'
)
code = code.replace(
    '100% FREE Food Coupon (FREE10) activated! 🎁',
    'Free Small Item (Beverage/Snack) Coupon (FREE10) activated! ☕'
)

# -----------------------------------------------------------------------------
# 6. ENFORCE COUPON RULES: DON'T GIVE COUPONS EVERYTIME & MILESTONE LOCK
# -----------------------------------------------------------------------------
old_coupon_block = '''  const validCodes = {
    "FREE10": {
      name: "10th Order FREE Meal",
      calc: (subtotal) => Math.min(subtotal, 150),
      desc: "100% FREE (Up to ₹150 OFF)"
    },
    "SPECIAL50": {
      name: "Today's Special Deal",
      calc: (subtotal) => Math.min(subtotal, 50),
      desc: "Flat ₹50 Deal Applied"
    },
    "SAVITHA30": {
      name: "Campus Savings",
      calc: (subtotal) => (subtotal >= 99 ? 30 : 0),
      minSubtotal: 99,
      desc: "Flat ₹30 OFF"
    },
    "FREEDRINK": {
      name: "Complimentary Beverage",
      calc: (subtotal) => (subtotal >= 70 ? 25 : 0),
      minSubtotal: 70,
      desc: "Free Drink (₹25 OFF)"
    }
  };'''

new_coupon_block = '''  const validCodes = {
    "FREE10": {
      name: "10th Order Free Small Item (Beverage / Snack)",
      calc: (subtotal) => Math.min(subtotal, 35),
      desc: "Free Small Item (Up to ₹35 OFF on Snacks/Drinks)"
    },
    "SPECIAL50": {
      name: "Today's Special Deal",
      calc: (subtotal) => Math.min(subtotal, 50),
      desc: "Flat ₹50 Deal Applied"
    },
    "SAVITHA30": {
      name: "Campus Savings",
      calc: (subtotal) => (subtotal >= 99 ? 30 : 0),
      minSubtotal: 99,
      desc: "Flat ₹30 OFF"
    },
    "FREEDRINK": {
      name: "Complimentary Beverage",
      calc: (subtotal) => (subtotal >= 70 ? 25 : 0),
      minSubtotal: 70,
      desc: "Free Drink (₹25 OFF)"
    }
  };'''

if old_coupon_block in code:
    code = code.replace(old_coupon_block, new_coupon_block)
    print("Updated FREE10 calculation to max Rs.35 (Free Small Item).")

old_coupon_check = '''  const coupon = validCodes[code];
  if (!coupon) {
    if (msgEl) {
      msgEl.style.display = "block";
      msgEl.style.color = "#ef4444";
      msgEl.textContent = `❌ Invalid coupon code '${code}'. Try FREE10, SAVITHA30, or SPECIAL50.`;
    }
    showToast(`Invalid coupon code '${code}'`, "warning");
    return;
  }'''

new_coupon_check = '''  const coupon = validCodes[code];
  if (!coupon) {
    if (msgEl) {
      msgEl.style.display = "block";
      msgEl.style.color = "#ef4444";
      msgEl.textContent = `❌ Invalid coupon code '${code}'. Try FREE10, SAVITHA30, or SPECIAL50.`;
    }
    showToast(`Invalid coupon code '${code}'`, "warning");
    return;
  }

  // Strict Milestone Check for FREE10: Must complete 10 orders!
  if (code === "FREE10") {
    let streak = parseInt(localStorage.getItem("savitha_user_order_count") || "0", 10);
    const isTenthUnlocked = streak > 0 && (streak % 10 === 0 || streak >= 10);
    if (!isTenthUnlocked) {
      const remaining = 10 - (streak % 10);
      const msg = `⚠️ FREE10 unlocks only after completing 10 orders! (${remaining} more order${remaining !== 1 ? 's' : ''} needed).`;
      if (msgEl) {
        msgEl.style.display = "block";
        msgEl.style.color = "#f59e0b";
        msgEl.textContent = msg;
      }
      showToast(msg, "warning");
      return;
    }
  }

  // Daily Cooldown Check: Don't give coupons on every order!
  const todayStr = new Date().toDateString();
  let usedCoupons = {};
  try {
    usedCoupons = JSON.parse(localStorage.getItem("savitha_used_coupons") || "{}");
  } catch (e) {}
  if (usedCoupons[code] && usedCoupons[code] === todayStr) {
    const msg = `⚠️ Coupon '${code}' has already been redeemed today! Promotional coupons are limited to 1 per student per day.`;
    if (msgEl) {
      msgEl.style.display = "block";
      msgEl.style.color = "#f59e0b";
      msgEl.textContent = msg;
    }
    showToast(msg, "warning");
    return;
  }'''

if old_coupon_check in code:
    code = code.replace(old_coupon_check, new_coupon_check)
    print("Updated coupon execution with milestone check and daily cooldown.")

# In placeOrderAndGenerateToken, decrement inventory and record coupon usage
old_place_order_sync = '''  cart = {};
  renderDishes();
  updateCartBar();
  updateMyOrdersCount();
  updateLiveOrderBadge();
  renderLoyaltyStampCard();'''

new_place_order_sync = '''  // Decrement inventory portions in kitchen stock
  decrementOrderInventory(items);

  // Record used coupon in daily cooldown
  if (usedCoupon) {
    try {
      const used = JSON.parse(localStorage.getItem("savitha_used_coupons") || "{}");
      used[usedCoupon] = new Date().toDateString();
      localStorage.setItem("savitha_used_coupons", JSON.stringify(used));
    } catch (e) {}
  }

  // Random lucky coupon roll: Only 25% chance (don't give coupons everytime!)
  if (Math.random() < 0.25 && usedCoupon !== "SAVITHA30") {
    try {
      localStorage.setItem("savitha_pending_lucky_coupon", "SAVITHA30");
      showToast("🍀 Lucky Order Bonus! You won a ₹30 campus coupon (SAVITHA30) for a future meal!", "success");
    } catch (e) {}
  }

  cart = {};
  renderDishes();
  updateCartBar();
  updateMyOrdersCount();
  updateLiveOrderBadge();
  renderLoyaltyStampCard();'''

if old_place_order_sync in code:
    code = code.replace(old_place_order_sync, new_place_order_sync)
    print("Updated placeOrderAndGenerateToken with inventory decrement & coupon limits.")

code = code.replace(
    'showToast(`🎉 10th ORDER FREE MEAL CLAIMED! Token: ${token} (₹0 Paid)`, "success");',
    'showToast(`🎉 10th ORDER FREE ITEM (Drink/Snack) CLAIMED! Token: ${token}`, "success");'
)

# -----------------------------------------------------------------------------
# 7. LAST MINUTE CANCELLATION CHARGE SYSTEM
# -----------------------------------------------------------------------------
cancellation_system_code = """
// =========================================================================
// LAST MINUTE CANCELLATION CHARGE ENGINE
// =========================================================================
let pendingCancelOrderId = null;

function openCancelOrderModal(orderId) {
  const target = liveOrders.find(o => o.id === orderId || o.token === orderId)
    || myOrders.find(o => o.id === orderId || o.token === orderId)
    || (lastPlacedOrder && (lastPlacedOrder.id === orderId || lastPlacedOrder.token === orderId) ? lastPlacedOrder : null);

  if (!target) {
    showToast("Order not found or already cancelled.", "warning");
    return;
  }

  pendingCancelOrderId = target.id;
  const modal = document.getElementById("cancel-order-modal");
  const content = document.getElementById("cancel-modal-content");
  if (!modal || !content) {
    confirmCancellationWithCharge(target.id, 20, Math.max(0, target.total - 20));
    return;
  }

  const orderTime = target.timestamp || Date.now();
  const elapsedSec = Math.max(0, Math.floor((Date.now() - orderTime) / 1000));
  const isGracePeriod = (elapsedSec <= 60);

  const cancellationFee = isGracePeriod ? 0 : Math.min(20, target.total);
  const refundAmount = Math.max(0, target.total - cancellationFee);

  content.innerHTML = `
    <div style="background:#f8fafc; border-radius:12px; padding:14px; margin-bottom:14px; border:1px solid #e2e8f0;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <span style="font-size:1.15rem; font-weight:900; color:var(--primary);">${target.token}</span>
        <span style="font-size:0.78rem; font-weight:800; padding:3px 8px; border-radius:999px; background:${isGracePeriod ? '#dcfce7' : '#fef3c7'}; color:${isGracePeriod ? '#15803d' : '#b45309'};">
          ${isGracePeriod ? '🟢 Within 1-Min Grace Period' : '⚠️ Last-Minute Cancellation'}
        </span>
      </div>

      <div style="font-size:0.84rem; color:var(--text-main); margin-bottom:8px; line-height:1.4;">
        ${isGracePeriod 
          ? 'You are within the <strong>1-minute grace window</strong>. Food preparation has not started, so <strong>no cancellation fee</strong> applies!'
          : `The kitchen has already begun food preparation (<strong>${elapsedSec}s elapsed</strong>). As per canteen policy to reduce food waste, a <strong>Last-Minute Cancellation Fee of ₹${cancellationFee}</strong> applies.`
        }
      </div>

      <div style="border-top:1px dashed #cbd5e1; padding-top:8px; font-size:0.86rem;">
        <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
          <span style="color:var(--text-muted);">Order Total:</span>
          <strong>₹${target.total}</strong>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:3px; color:${cancellationFee > 0 ? '#ef4444' : '#10b981'};">
          <span>Cancellation Charge:</span>
          <strong>${cancellationFee > 0 ? '-₹' + cancellationFee : '₹0 (Free)'}</strong>
        </div>
        <div style="border-top:1px solid #e2e8f0; margin-top:4px; padding-top:4px; display:flex; justify-content:space-between; font-weight:900; font-size:0.95rem;">
          <span>Refund to Account:</span>
          <span style="color:#10b981;">₹${refundAmount}</span>
        </div>
      </div>
    </div>

    <div style="display:flex; gap:10px;">
      <button type="button" class="btn-hero-secondary" onclick="closeCancelOrderModal();"
        style="flex:1; padding:10px; font-size:0.88rem; justify-content:center;">
        Keep My Order
      </button>
      <button type="button" class="btn-banner-cancel" onclick="confirmCancellationWithCharge('${target.id}', ${cancellationFee}, ${refundAmount});"
        style="flex:1; padding:10px; font-size:0.88rem; background:#fee2e2; border:1.5px solid #fca5a5; color:#dc2626; border-radius:10px; font-weight:800; cursor:pointer; justify-content:center;">
        Confirm Cancel ${cancellationFee > 0 ? '(₹' + cancellationFee + ' Fee)' : ''}
      </button>
    </div>
  `;

  modal.classList.add("show");
}

function closeCancelOrderModal() {
  const modal = document.getElementById("cancel-order-modal");
  if (modal) modal.classList.remove("show");
  pendingCancelOrderId = null;
}

function confirmCancellationWithCharge(orderId, fee, refund) {
  closeCancelOrderModal();
  const target = liveOrders.find(o => o.id === orderId || o.token === orderId)
    || myOrders.find(o => o.id === orderId || o.token === orderId)
    || (lastPlacedOrder && (lastPlacedOrder.id === orderId || lastPlacedOrder.token === orderId) ? lastPlacedOrder : null);

  if (!target) return;

  // Remove from live cooking queue in kitchen
  liveOrders = liveOrders.filter(o => o.id !== target.id && o.token !== target.token);

  // Update in myOrders with cancellation status and fee
  const myOrd = myOrders.find(o => o.id === target.id || o.token === target.token);
  if (myOrd) {
    myOrd.status = fee > 0 ? `Cancelled (₹${fee} Late Fee Applied)` : `Cancelled (Full Refund)`;
    myOrd.cancellationFee = fee;
    myOrd.refundAmount = refund;
  }

  try {
    localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders));
    localStorage.setItem("savitha_my_orders", JSON.stringify(myOrders));
    localStorage.removeItem("savitha_student_active_order");
  } catch (e) {}

  try {
    fetch(`${API_BASE}/api/orders/${target.id}/cancel`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cancellation_fee: fee, refund: refund, reason: fee > 0 ? "Last-minute cancellation charge" : "Grace window cancellation" })
    }).catch(() => {});
  } catch (e) {}

  updateMyOrdersCount();
  renderMyOrdersList();
  updateLiveOrderBadge();
  closeTokenModal();

  if (fee > 0) {
    showToast(`Order ${target.token} cancelled. ₹${fee} late fee applied (₹${refund} refunded).`, "warning");
  } else {
    showToast(`Order ${target.token} cancelled within grace window. Full refund of ₹${refund} issued.`, "info");
  }
}
"""

if "function openCancelOrderModal(" not in code:
    code = code.replace(
        "function cancelOrder(orderId) {",
        cancellation_system_code + "\nfunction cancelOrder(orderId) {\n  openCancelOrderModal(orderId);\n  return;\n"
    )
    print("Added Cancellation System to js/app.js")

# -----------------------------------------------------------------------------
# 8. UPDATE switchManagerTab TO SUPPORT INVENTORY TAB
# -----------------------------------------------------------------------------
old_switch_tab = '''function switchManagerTab(tabName) {
  const tabs = ["orders", "calc", "dailyplan", "stats", "history", "pwd", "pnl"];'''

new_switch_tab = '''function switchManagerTab(tabName) {
  const tabs = ["orders", "inventory", "calc", "dailyplan", "stats", "history", "pwd", "pnl"];'''

if old_switch_tab in code:
    code = code.replace(old_switch_tab, new_switch_tab)
    code = code.replace(
        'if (tabName === "orders") {',
        'if (tabName === "inventory") {\n    renderInventoryDashboard();\n  } else if (tabName === "orders") {'
    )
    print("Updated switchManagerTab to support inventory.")

# -----------------------------------------------------------------------------
# 9. EXPORT NEW FUNCTIONS ON WINDOW
# -----------------------------------------------------------------------------
exports_to_add = """  window.initInventory = initInventory;
  window.getInventory = getInventory;
  window.getInventoryItem = getInventoryItem;
  window.updateItemStock = updateItemStock;
  window.adjustItemStock = adjustItemStock;
  window.toggleItemStatus = toggleItemStatus;
  window.restockAll = restockAll;
  window.decrementOrderInventory = decrementOrderInventory;
  window.filterInventoryCategory = filterInventoryCategory;
  window.filterInventoryStatus = filterInventoryStatus;
  window.searchInventory = searchInventory;
  window.renderInventoryDashboard = renderInventoryDashboard;
  window.openCancelOrderModal = openCancelOrderModal;
  window.closeCancelOrderModal = closeCancelOrderModal;
  window.confirmCancellationWithCharge = confirmCancellationWithCharge;
"""

if "window.initInventory = initInventory;" not in code:
    code = code.replace(
        "window.DEFAULT_PNL_DATA = DEFAULT_PNL_DATA;",
        "window.DEFAULT_PNL_DATA = DEFAULT_PNL_DATA;\n" + exports_to_add
    )
    print("Added window exports in js/app.js")

# In DOMContentLoaded, initialize inventory
if "initInventory();" not in code:
    code = code.replace(
        "initTheme();",
        "initTheme();\n    initInventory();"
    )
    print("Initialized inventory in DOMContentLoaded.")

with open(app_path, "w", encoding="utf-8") as f:
    f.write(code)

with open(frontend_app_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Saved js/app.js and frontend/js/app.js successfully!")
