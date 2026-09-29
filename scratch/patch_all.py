import os
import shutil
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# =============================================================================
# 1. PATCH index.html
# =============================================================================
print("Patching index.html...")
index_path = os.path.join(ROOT, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1.1 Change Free Meal to Free Small Item in Loyalty Banner
html = html.replace(
    '10th Order 100% FREE!</span>',
    '10th Order: Free Drink or Snack! ☕</span>'
)
html = html.replace(
    '10 orders to FREE meal\n                🎁</span>',
    '10 orders to Free Small Item (Drink/Snack) ☕</span>'
)
html = html.replace(
    '10 orders to FREE meal 🎁</span>',
    '10 orders to Free Small Item (Drink/Snack) ☕</span>'
)
html = html.replace(
    '🎁 FREE10 (Free Meal)',
    '🎁 FREE10 (Free Drink/Snack)'
)

# 1.2 Update Quick Tap Coupons Strip in index.html to reflect that coupons are not given every time
old_coupon_strip = '''          <!-- Quick Tap Coupons Strip -->
          <div style="display:flex; gap:6px; overflow-x:auto; padding-top:2px;">
            <button type="button" class="mini-coupon-chip" onclick="applyQuickCoupon('FREE10')"
              style="font-size:0.72rem; padding:3px 8px;">🎁 FREE10 (Free Drink/Snack)</button>
            <button type="button" class="mini-coupon-chip" onclick="applyQuickCoupon('SAVITHA30')"
              style="font-size:0.72rem; padding:3px 8px;">🏷️ SAVITHA30 (₹30 OFF)</button>
            <button type="button" class="mini-coupon-chip" onclick="applyQuickCoupon('SPECIAL50')"
              style="font-size:0.72rem; padding:3px 8px;">⚡ SPECIAL50 (₹50 Deal)</button>
          </div>'''

new_coupon_strip = '''          <!-- Fair Canteen Coupon & Reward Policy Notice -->
          <div style="padding-top:4px;">
            <div style="font-size:0.76rem; color:var(--text-muted); display:flex; align-items:center; gap:5px; flex-wrap:wrap; line-height:1.4;">
              <span>💡 <strong>Canteen Reward Policy:</strong> 10th order unlocks a Free Small Item (Beverage/Snack up to ₹35). Promo coupons are earned on lucky orders &amp; milestones (limit 1 coupon redemption per day).</span>
            </div>
          </div>'''

if old_coupon_strip in html:
    html = html.replace(old_coupon_strip, new_coupon_strip)
else:
    # Try with original Free Meal
    alt_old = '''          <!-- Quick Tap Coupons Strip -->
          <div style="display:flex; gap:6px; overflow-x:auto; padding-top:2px;">
            <button type="button" class="mini-coupon-chip" onclick="applyQuickCoupon('FREE10')"
              style="font-size:0.72rem; padding:3px 8px;">🎁 FREE10 (Free Meal)</button>
            <button type="button" class="mini-coupon-chip" onclick="applyQuickCoupon('SAVITHA30')"
              style="font-size:0.72rem; padding:3px 8px;">🏷️ SAVITHA30 (₹30 OFF)</button>
            <button type="button" class="mini-coupon-chip" onclick="applyQuickCoupon('SPECIAL50')"
              style="font-size:0.72rem; padding:3px 8px;">⚡ SPECIAL50 (₹50 Deal)</button>
          </div>'''
    if alt_old in html:
        html = html.replace(alt_old, new_coupon_strip)
    else:
        print("Note: coupon strip might have already been modified or differs slightly")

# 1.3 Add subtab-inventory-btn in Kitchen Dashboard tabs
inventory_tab_btn = '''          <button type="button" class="clickable-pill" id="subtab-inventory-btn"
            onclick="switchManagerTab('inventory')">
            📦 Inventory &amp; Stock <span id="inv-low-stock-badge"
              style="display:none; background:#ef4444; color:#ffffff; font-size:0.75rem; font-weight:800; padding:2px 7px; border-radius:999px; margin-left:4px;">0</span>
          </button>'''

if 'id="subtab-inventory-btn"' not in html:
    html = html.replace(
        'id="subtab-orders-btn"',
        'id="subtab-orders-btn"'
    )
    # Insert inventory button right after orders tab button
    target_btn_close = '</span>\n\n          </button>'
    pos = html.find('id="subtab-orders-btn"')
    if pos != -1:
        end_pos = html.find('</button>', pos) + len('</button>')
        html = html[:end_pos] + '\n\n' + inventory_tab_btn + html[end_pos:]
        print("Added subtab-inventory-btn to Kitchen Dashboard nav.")

# 1.4 Add manager-pane-inventory in view-manager
inventory_pane_html = '''      <!-- Tab: Kitchen Inventory & Stock Monitoring -->
      <div id="manager-pane-inventory" style="display:none;">
        <!-- Top Metrics Cards -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:12px; margin-bottom:16px;">
          <div class="manager-card" style="padding:14px 16px; border-left:4px solid var(--primary); background:#ffffff;">
            <div style="font-size:0.78rem; font-weight:800; color:var(--text-muted); text-transform:uppercase;">📦 Total Items</div>
            <div id="inv-stat-total" style="font-size:1.8rem; font-weight:900; color:var(--text-main); margin-top:4px;">24</div>
            <div style="font-size:0.75rem; color:var(--text-muted);">Active dishes on menu</div>
          </div>
          <div class="manager-card" style="padding:14px 16px; border-left:4px solid #10b981; background:#ffffff;">
            <div style="font-size:0.78rem; font-weight:800; color:#059669; text-transform:uppercase;">🟢 In Stock &amp; Available</div>
            <div id="inv-stat-instock" style="font-size:1.8rem; font-weight:900; color:#059669; margin-top:4px;">24</div>
            <div style="font-size:0.75rem; color:var(--text-muted);">Ready to serve students</div>
          </div>
          <div class="manager-card" style="padding:14px 16px; border-left:4px solid #f59e0b; background:#ffffff;">
            <div style="font-size:0.78rem; font-weight:800; color:#d97706; text-transform:uppercase;">🟡 Low Stock Alert</div>
            <div id="inv-stat-lowstock" style="font-size:1.8rem; font-weight:900; color:#d97706; margin-top:4px;">0</div>
            <div style="font-size:0.75rem; color:var(--text-muted);">&lt; 10 portions remaining</div>
          </div>
          <div class="manager-card" style="padding:14px 16px; border-left:4px solid #ef4444; background:#ffffff;">
            <div style="font-size:0.78rem; font-weight:800; color:#dc2626; text-transform:uppercase;">🔴 Sold Out / Depleted</div>
            <div id="inv-stat-soldout" style="font-size:1.8rem; font-weight:900; color:#dc2626; margin-top:4px;">0</div>
            <div style="font-size:0.75rem; color:var(--text-muted);">Blocked on student menu</div>
          </div>
        </div>

        <!-- Low Stock Warning Alert Banner -->
        <div id="inv-warning-banner" style="display:none; background:#fffbeb; border:1.5px solid #fde68a; border-radius:12px; padding:12px 16px; margin-bottom:16px;">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-size:1.3rem;">⚠️</span>
              <div>
                <strong style="color:#b45309; font-size:0.92rem;">Kitchen Inventory Alert</strong>
                <p id="inv-warning-text" style="color:#92400e; font-size:0.82rem; margin:2px 0 0 0;">Some items are running low on prepared stock.</p>
              </div>
            </div>
            <button type="button" class="btn-calc" onclick="restockAll(20)" style="padding:6px 14px; font-size:0.82rem; background:#d97706;">
              ⚡ Restock All (+20 Portions)
            </button>
          </div>
        </div>

        <!-- Controls Toolbar -->
        <div class="manager-card" style="margin-bottom:16px; padding:14px 16px;">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <!-- Search -->
            <div style="flex:1; min-width:220px;">
              <input type="text" id="inv-search-input" placeholder="🔍 Search item name (e.g. Biryani, Dosa, Chai)..."
                oninput="searchInventory(this.value)"
                style="width:100%; padding:9px 12px; border:1.5px solid var(--border); border-radius:8px; font-size:0.88rem; outline:none;">
            </div>
            <!-- Category and Status filter pills -->
            <div style="display:flex; gap:6px; flex-wrap:wrap; align-items:center;">
              <button type="button" class="clickable-pill active inv-filter-pill" onclick="filterInventoryCategory('all', this)" style="font-size:0.78rem; padding:5px 10px;">All</button>
              <button type="button" class="clickable-pill inv-filter-pill" onclick="filterInventoryCategory('lunch', this)" style="font-size:0.78rem; padding:5px 10px;">🍛 Lunch</button>
              <button type="button" class="clickable-pill inv-filter-pill" onclick="filterInventoryCategory('breakfast', this)" style="font-size:0.78rem; padding:5px 10px;">🥞 Breakfast</button>
              <button type="button" class="clickable-pill inv-filter-pill" onclick="filterInventoryCategory('snacks', this)" style="font-size:0.78rem; padding:5px 10px;">☕ Snacks</button>
              <button type="button" class="clickable-pill inv-filter-pill" onclick="filterInventoryStatus('low_stock', this)" style="font-size:0.78rem; padding:5px 10px; color:#d97706;">🟡 Low Stock</button>
              <button type="button" class="clickable-pill inv-filter-pill" onclick="filterInventoryStatus('out_of_stock', this)" style="font-size:0.78rem; padding:5px 10px; color:#dc2626;">🔴 Sold Out</button>
              <button type="button" class="btn-calc" onclick="restockAll(25)" style="font-size:0.78rem; padding:5px 12px; background:var(--primary); margin-left:4px;">⚡ Restock All (+25)</button>
            </div>
          </div>
        </div>

        <!-- Inventory List / Table -->
        <div class="manager-card" style="padding:0; overflow:hidden;">
          <div style="padding:14px 18px; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center;">
            <div>
              <h3 style="font-size:1.05rem; font-weight:800; color:var(--text-main); margin:0;">Live Item Stock &amp; Portions Monitoring</h3>
              <p style="font-size:0.8rem; color:var(--text-muted); margin:2px 0 0 0;">Adjust portions in real time. Items marked Sold Out will automatically be blocked on student menus.</p>
            </div>
          </div>
          <div style="overflow-x:auto;">
            <table class="pnl-table" style="width:100%; border-collapse:collapse; min-width:680px;">
              <thead>
                <tr style="background:#f8fafc; border-bottom:1.5px solid var(--border); text-align:left;">
                  <th style="padding:12px 16px;">Dish / Food Item</th>
                  <th style="padding:12px 14px;">Category</th>
                  <th style="padding:12px 14px;">Price</th>
                  <th style="padding:12px 14px; text-align:center;">Current Stock (Portions)</th>
                  <th style="padding:12px 14px;">Status</th>
                  <th style="padding:12px 16px; text-align:right;">Actions / Toggle</th>
                </tr>
              </thead>
              <tbody id="inventory-table-body">
                <!-- Populated dynamically by app.js -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
'''

if 'id="manager-pane-inventory"' not in html:
    calc_marker = '<div id="manager-pane-calc"'
    if calc_marker in html:
        html = html.replace(calc_marker, inventory_pane_html + '\n\n      ' + calc_marker)
        print("Added manager-pane-inventory to index.html.")

# 1.5 Add Cancel Order Modal right after my-orders-modal
cancel_modal_html = '''  <!-- Last-Minute Order Cancellation Confirmation Modal -->
  <div id="cancel-order-modal" class="modal-overlay">
    <div class="modal-box" style="max-width:440px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid var(--border); padding-bottom:10px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:1.3rem;">⚠️</span>
          <h2 style="font-size:1.2rem; font-weight:800; color:var(--text-main); margin:0;">Cancel Order Confirmation</h2>
        </div>
        <button type="button" onclick="closeCancelOrderModal()"
          style="background:transparent; border:none; font-size:1.3rem; cursor:pointer; color:var(--text-muted); line-height:1;"
          aria-label="Close modal">✕</button>
      </div>

      <div id="cancel-modal-content">
        <!-- Dynamically rendered with exact fee, elapsed time, and refund breakdown -->
      </div>
    </div>
  </div>
'''

if 'id="cancel-order-modal"' not in html:
    cart_marker = '<div id="cart-modal"'
    if cart_marker in html:
        html = html.replace(cart_marker, cancel_modal_html + '\n\n  ' + cart_marker)
        print("Added cancel-order-modal to index.html.")

# 1.6 Update Cart Modal coupon section
html = html.replace(
    'onclick="applyQuickCoupon(\'FREE10\')">🎁 FREE10 (10th\n            Free)</button>',
    'onclick="applyQuickCoupon(\'FREE10\')">🎁 FREE10 (Free Drink/Snack)</button>'
)
html = html.replace(
    'onclick="applyQuickCoupon(\'FREE10\')">🎁 FREE10 (10th Free)</button>',
    'onclick="applyQuickCoupon(\'FREE10\')">🎁 FREE10 (Free Drink/Snack)</button>'
)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

# Also copy to frontend/index.html
frontend_index = os.path.join(ROOT, "frontend", "index.html")
if os.path.exists(os.path.dirname(frontend_index)):
    with open(frontend_index, "w", encoding="utf-8") as f:
        f.write(html)
print("Updated index.html and frontend/index.html.")
