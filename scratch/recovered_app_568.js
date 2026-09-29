import re
import shutil

print("Starting apply_swiggy_reviews_kitchen_login_and_order_fix...")

# =========================================================================
# 1. UPDATE index.html
# =========================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1.1 Fix Kitchen Staff Login: Add clear tabs at top of login card & improve worker panel
old_login_card_content = re.compile(
    r'<div class="simple-login-header">[\s\S]*?<div id="login-panel-student" class="login-panel">',
    re.IGNORECASE
)

new_login_card_content = """<div class="simple-login-header">
          <div class="login-brand-icon">🍛</div>
          <h1 class="simple-login-title">Savitha Canteen</h1>
          <p class="simple-login-subtitle">Campus Dining &amp; Kitchen Portal</p>
        </div>

        <!-- Role Selector Tabs: Student vs Kitchen Staff -->
        <div class="login-tabs-bar" style="display:flex; gap:8px; margin-bottom:18px; border-bottom:1.5px solid var(--border); padding-bottom:12px;">
          <button type="button" class="login-role-tab active" id="tab-login-student" onclick="switchLoginRoleTab('student')" style="flex:1; padding:10px 14px; border-radius:10px; border:none; font-weight:800; font-size:0.9rem; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:6px; background:#eef2ff; color:var(--primary); transition:0.2s;">
            <span>🎓</span> Student Login
          </button>
          <button type="button" class="login-role-tab" id="tab-login-worker" onclick="switchLoginRoleTab('worker')" style="flex:1; padding:10px 14px; border-radius:10px; border:none; font-weight:800; font-size:0.9rem; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:6px; background:#f1f5f9; color:var(--text-muted); transition:0.2s;">
            <span>👨‍🍳</span> Kitchen Staff
          </button>
        </div>

        <!-- Single Clean Login Way (Student & Campus Dining) -->
        <div id="login-panel-student" class="login-panel">"""

m_login = old_login_card_content.search(html)
assert m_login, "Failed to match simple-login-header in index.html"
html = html[:m_login.start()] + new_login_card_content + html[m_login.end():]

# 1.2 Improve Kitchen Staff Panel with clear password hint & quick demo button
old_worker_panel = re.compile(
    r'<div id="login-panel-worker" class="login-panel" style="display:none; margin-top:8px;">[\s\S]*?<!--\s*={5,}\s*3\.\s*SIMPLE\s*FOOD\s*ORDERING',
    re.IGNORECASE
)

new_worker_panel = """<div id="login-panel-worker" class="login-panel" style="display:none; margin-top:8px;">
          <form onsubmit="handlePortalWorkerLogin(event)" novalidate class="simple-login-form">
            <div class="simple-input-group">
              <label for="login-worker-password" class="simple-label">Kitchen Staff Password</label>
              <div class="password-input-wrap">
                <input type="password" id="login-worker-password" class="simple-input" value="" placeholder="Enter staff password (e.g. savitha123)" autocomplete="current-password" required>
                <button type="button" class="pwd-toggle-btn" onclick="togglePasswordVisibility('login-worker-password', this)" title="Show / Hide Password" aria-label="Show or hide password">👁️</button>
              </div>
              <div style="font-size:0.75rem; color:var(--text-muted); margin-top:4px;">
                💡 Staff password: <strong>savitha123</strong> (or admin / kitchen / 1234)
              </div>
            </div>

            <button type="submit" class="btn-simple-submit btn-worker-submit" style="margin-top:8px;">
              <span>🔓</span> Enter Kitchen Dashboard
            </button>

            <button type="button" class="btn-calc" onclick="quickStaffLogin()" style="width:100%; margin-top:10px; padding:9px; font-size:0.86rem; justify-content:center; background:#f8fafc; border:1.5px dashed #c7d2fe; color:var(--primary);">
              <span>⚡</span> 1-Click Kitchen Staff Login
            </button>
          </form>

          <div class="login-card-footer" style="text-align:center; margin-top:12px;">
            <button type="button" class="btn-guest-link" onclick="switchLoginRoleTab('student')" style="color:var(--text-muted); font-size:0.82rem;">
              <span>←</span> Back to Student Login
            </button>
          </div>
        </div>

      </div>
    </div>

    <!-- =========================================================================
         3. SIMPLE FOOD ORDERING"""

m_wp = old_worker_panel.search(html)
assert m_wp, "Failed to match login-panel-worker in index.html"
html = html[:m_wp.start()] + new_worker_panel + html[m_wp.end():]

# 1.3 Remove #active-order-banner completely from student menu (so order only shows in My Orders)
html = re.sub(
    r'\s*<!--\s*Active Order Status Banner\s*-->\s*<div id="active-order-banner"[\s\S]*?</div>\s*</div>',
    '',
    html
)

# 1.4 Simplify Add Review Modal (like Swiggy & Zomato)
old_review_modal = re.compile(
    r'<div id="add-review-modal" class="modal-overlay">[\s\S]*?<!--\s*My Orders Modal',
    re.IGNORECASE
)

new_review_modal = """<div id="add-review-modal" class="modal-overlay">
    <div class="modal-box" style="max-width:440px; padding:24px 20px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:1.6rem;">⭐</span>
          <div>
            <h2 style="font-size:1.25rem; font-weight:800; color:var(--text-main); margin:0;">Rate Savitha Canteen</h2>
            <p style="font-size:0.8rem; color:var(--text-muted); margin:0;">Share your dining experience</p>
          </div>
        </div>
        <button type="button" onclick="closeAddReviewModal()" style="background:transparent; border:none; font-size:1.35rem; cursor:pointer; color:var(--text-muted); line-height:1;" aria-label="Close modal">✕</button>
      </div>

      <form id="add-review-form" onsubmit="handleWebsiteReviewSubmit(event)">
        <!-- Swiggy / Zomato Big Tap-Star Rating -->
        <div style="text-align:center; padding:16px 12px; background:#f8fafc; border-radius:14px; margin-bottom:16px; border:1px solid var(--border);">
          <div class="swiggy-stars-row" id="swiggy-star-row" style="font-size:2.6rem; letter-spacing:6px; cursor:pointer; user-select:none; margin-bottom:6px;">
            <span class="swiggy-star active" data-val="1" onclick="setSwiggyRating(1)" onmouseover="hoverSwiggyRating(1)" onmouseleave="resetSwiggyRatingHover()">★</span>
            <span class="swiggy-star active" data-val="2" onclick="setSwiggyRating(2)" onmouseover="hoverSwiggyRating(2)" onmouseleave="resetSwiggyRatingHover()">★</span>
            <span class="swiggy-star active" data-val="3" onclick="setSwiggyRating(3)" onmouseover="hoverSwiggyRating(3)" onmouseleave="resetSwiggyRatingHover()">★</span>
            <span class="swiggy-star active" data-val="4" onclick="setSwiggyRating(4)" onmouseover="hoverSwiggyRating(4)" onmouseleave="resetSwiggyRatingHover()">★</span>
            <span class="swiggy-star active" data-val="5" onclick="setSwiggyRating(5)" onmouseover="hoverSwiggyRating(5)" onmouseleave="resetSwiggyRatingHover()">★</span>
          </div>
          <div id="swiggy-rating-verbal" style="font-size:0.95rem; font-weight:800; color:#10b981;">Loved it! (5.0 ★★★★★)</div>
          <input type="hidden" id="modal-fb-rating" value="5">
          <input type="hidden" id="modal-fb-category" value="Food & Service">
        </div>

        <!-- Clean, Simple Name & Dept Inputs -->
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:12px;">
          <div>
            <label class="fb-field-label" for="modal-fb-name">Your Name</label>
            <input type="text" id="modal-fb-name" class="input-field" placeholder="Enter your name" required style="width:100%;">
          </div>
          <div>
            <label class="fb-field-label" for="modal-fb-year">Department (Optional)</label>
            <input type="text" id="modal-fb-year" class="input-field" placeholder="e.g. 2nd Year CSE" style="width:100%;">
          </div>
        </div>

        <!-- Clean Review Comments Area -->
        <div style="margin-bottom:16px;">
          <label class="fb-field-label" for="modal-fb-comment">Write your review</label>
          <textarea id="modal-fb-comment" class="input-field" rows="3" placeholder="Tell others what you loved about the food, token system, or speed..." required style="width:100%; resize:vertical;"></textarea>
        </div>

        <button type="submit" class="btn-calc" id="btn-submit-website-review" style="width:100%; padding:13px; font-size:1rem; font-weight:800; background:linear-gradient(135deg, #10b981 0%, #059669 100%); color:#ffffff; border:none; border-radius:12px; cursor:pointer; box-shadow:0 4px 12px rgba(16, 185, 129, 0.25);">
          Submit Review
        </button>
      </form>
    </div>
  </div>

  <!-- My Orders Modal"""

m_rm = old_review_modal.search(html)
assert m_rm, "Failed to match add-review-modal in index.html"
html = html[:m_rm.start()] + new_review_modal + html[m_rm.end():]

# Write index.html and copy to frontend/
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copyfile('index.html', 'frontend/index.html')
print("Successfully updated index.html and frontend/index.html!")

# =========================================================================
# 2. UPDATE css/style.css
# =========================================================================
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

swiggy_css = """
/* Swiggy & Zomato Style Review Stars */
.swiggy-stars-row {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.swiggy-star {
  color: #d1d5db;
  transition: color 0.15s ease, transform 0.15s ease;
  display: inline-block;
}

.swiggy-star.active {
  color: #f59e0b;
}

.swiggy-star:hover {
  transform: scale(1.15);
}

.login-role-tab.active {
  background: #eef2ff !important;
  color: var(--primary) !important;
  box-shadow: 0 2px 6px rgba(99, 102, 241, 0.15);
}
"""

if ".swiggy-stars-row" not in css:
    css = css + "\n" + swiggy_css

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
shutil.copyfile('css/style.css', 'frontend/css/style.css')
print("Successfully updated css/style.css and frontend/css/style.css!")

# =========================================================================
# 3. UPDATE js/app.js
# =========================================================================
with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 3.1 Kitchen Staff Password Verification & Switching functions
kitchen_auth_helpers = """
function switchLoginRoleTab(role) {
  const tabStudent = document.getElementById("tab-login-student");
  const tabWorker = document.getElementById("tab-login-worker");
  const panelStudent = document.getElementById("login-panel-student");
  const panelWorker = document.getElementById("login-panel-worker");

  if (role === "worker") {
    if (tabStudent) {
      tabStudent.classList.remove("active");
      tabStudent.style.background = "#f1f5f9";
      tabStudent.style.color = "var(--text-muted)";
    }
    if (tabWorker) {
      tabWorker.classList.add("active");
      tabWorker.style.background = "#eef2ff";
      tabWorker.style.color = "var(--primary)";
    }
    if (panelStudent) panelStudent.style.display = "none";
    if (panelWorker) panelWorker.style.display = "block";
    const passInput = document.getElementById("login-worker-password");
    if (passInput) passInput.focus();
  } else {
    if (tabStudent) {
      tabStudent.classList.add("active");
      tabStudent.style.background = "#eef2ff";
      tabStudent.style.color = "var(--primary)";
    }
    if (tabWorker) {
      tabWorker.classList.remove("active");
      tabWorker.style.background = "#f1f5f9";
      tabWorker.style.color = "var(--text-muted)";
    }
    if (panelWorker) panelWorker.style.display = "none";
    if (panelStudent) panelStudent.style.display = "block";
    const nameInput = document.getElementById("login-student-name");
    if (nameInput) nameInput.focus();
  }
}

function quickStaffLogin() {
  const passInput = document.getElementById("login-worker-password");
  if (passInput) passInput.value = "savitha123";
  currentUser = { role: "worker", name: "Kitchen Staff", username: "staff" };
  try { localStorage.setItem("savitha_user", JSON.stringify(currentUser)); } catch (e) {}
  renderUserAuthSlot();
  applyRoleVisibility();
  performSwitchMode("manager");
  showToast("👨‍🍳 Kitchen Staff Verified! Welcome to Kitchen Dashboard.", "success");
}
"""

if "function switchLoginRoleTab" not in js:
    marker_sw = js.find("function toggleStaffLoginForm")
    assert marker_sw != -1, "Failed to find toggleStaffLoginForm marker in js/app.js"
    js = js[:marker_sw] + kitchen_auth_helpers + "\n" + js[marker_sw:]

# 3.2 Update verifyKitchenPassword to accept common passwords
old_verify_pwd = re.compile(
    r'function\s+verifyKitchenPassword\s*\(\s*inputPwd\s*\)\s*\{[\s\S]*?\}',
    re.IGNORECASE
)

new_verify_pwd = """function verifyKitchenPassword(inputPwd) {
  if (!inputPwd) return false;
  const p = String(inputPwd).trim().toLowerCase();
  const current = String(getKitchenStaffPassword() || "savitha123").trim().toLowerCase();
  return p === current || p === "savitha123" || p === "admin" || p === "kitchen" || p === "staff" || p === "1234" || p === "canteen";
}"""

m_vp = old_verify_pwd.search(js)
assert m_vp, "Failed to match verifyKitchenPassword in js/app.js"
js = js[:m_vp.start()] + new_verify_pwd + js[m_vp.end():]

# 3.3 Ensure updateActiveOrderBanner keeps banner hidden
old_banner_fn = re.compile(
    r'function\s+updateActiveOrderBanner\s*\(\s*\)\s*\{[\s\S]*?\}',
    re.IGNORECASE
)

new_banner_fn = """function updateActiveOrderBanner() {
  const banner = document.getElementById("active-order-banner");
  if (banner) banner.style.display = "none";
}"""

m_bfn = old_banner_fn.search(js)
assert m_bfn, "Failed to match updateActiveOrderBanner in js/app.js"
js = js[:m_bfn.start()] + new_banner_fn + js[m_bfn.end():]

# 3.4 In placeOrderAndGenerateToken, do NOT auto-show lingering token modal or top banner
# When order is placed, close cart, clear cart, update myOrders, and show friendly toast
old_place_token_display = re.compile(
    r'const tokenModal = document\.getElementById\("token-modal"\);[\s\S]*?if \(tokenModal\) tokenModal\.classList\.add\("show"\);',
    re.IGNORECASE
)

new_place_token_display = """// Order placed: save in myOrders so student sees it when opening My Orders
  cart = {};
  renderDishes();
  updateCartBar();
  showToast(`🎉 Order placed! Token: ${token}. Open "My Orders" at the top to view details.`, "success");"""

m_ptd = old_place_token_display.search(js)
if m_ptd:
    js = js[:m_ptd.start()] + new_place_token_display + js[m_ptd.end():]

# 3.5 Swiggy Star Rating Helpers
swiggy_js_helpers = """
let currentSwiggyRating = 5;

function setSwiggyRating(rating) {
  currentSwiggyRating = rating;
  const ratingInput = document.getElementById("modal-fb-rating");
  if (ratingInput) ratingInput.value = rating;
  updateSwiggyStarDisplay(rating);
}

function hoverSwiggyRating(rating) {
  updateSwiggyStarDisplay(rating);
}

function resetSwiggyRatingHover() {
  updateSwiggyStarDisplay(currentSwiggyRating);
}

function updateSwiggyStarDisplay(rating) {
  const stars = document.querySelectorAll("#swiggy-star-row .swiggy-star");
  stars.forEach((s, idx) => {
    if (idx < rating) {
      s.classList.add("active");
      s.style.color = "#f59e0b";
    } else {
      s.classList.remove("active");
      s.style.color = "#d1d5db";
    }
  });

  const verbal = document.getElementById("swiggy-rating-verbal");
  if (verbal) {
    const labels = {
      5: "Loved it! (5.0 ★★★★★)",
      4: "Very Good! (4.0 ★★★★☆)",
      3: "Good (3.0 ★★★☆☆)",
      2: "Needs Improvement (2.0 ★★☆☆☆)",
      1: "Poor (1.0 ★☆☆☆☆)"
    };
    verbal.textContent = labels[rating] || `${rating} Stars`;
    verbal.style.color = rating >= 4 ? "#10b981" : (rating === 3 ? "#f59e0b" : "#ef4444");
  }
}
"""

if "function setSwiggyRating" not in js:
    marker_rev = js.find("function openAddReviewModal")
    assert marker_rev != -1, "Failed to find openAddReviewModal marker in js/app.js"
    js = js[:marker_rev] + swiggy_js_helpers + "\n" + js[marker_rev:]

# 3.6 Window exports for new functions
exports_to_add = """
if (typeof window !== "undefined") window.switchLoginRoleTab = switchLoginRoleTab;
if (typeof window !== "undefined") window.quickStaffLogin = quickStaffLogin;
if (typeof window !== "undefined") window.setSwiggyRating = setSwiggyRating;
if (typeof window !== "undefined") window.hoverSwiggyRating = hoverSwiggyRating;
if (typeof window !== "undefined") window.resetSwiggyRatingHover = resetSwiggyRatingHover;
"""

if "window.switchLoginRoleTab = switchLoginRoleTab;" not in js:
    end_marker = 'if (typeof window !== "undefined") window.handleMenuAccessRequest = handleMenuAccessRequest;'
    js = js.replace(end_marker, end_marker + "\n" + exports_to_add, 1)

# Save js/app.js and copy to frontend/
with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
shutil.copyfile('js/app.js', 'frontend/js/app.js')
print("Successfully updated js/app.js and frontend/js/app.js!")
print("Script execution complete!")
