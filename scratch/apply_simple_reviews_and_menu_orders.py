import re
import shutil

print("Applying simple reviews, menu-only My Orders, and removing Order Now from individual food items...")

# =========================================================================
# 1. UPDATE index.html
# =========================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1.1 Remove btn-top-orders from Top Navbar (so it does not show on Home Page)
old_navbar_pattern = re.compile(
    r'<nav class="nav-links" id="main-nav-links"[^>]*>[\s\S]*?<div id="user-auth-slot">',
    re.IGNORECASE
)
new_navbar_start = """<nav class="nav-links" id="main-nav-links">
        <div id="user-auth-slot">"""

m_nav = old_navbar_pattern.search(html)
assert m_nav, "Failed to find main-nav-links in index.html"
html = html[:m_nav.start()] + new_navbar_start + html[m_nav.end():]

# 1.2 Remove My Orders button from Home Page hero (view-about)
# Replace hero-cta-row in view-about
old_hero_cta = re.compile(
    r'<div class="hero-cta-row">\s*<button type="button" class="btn-hero-primary" id="about-hero-primary-btn" onclick="[^"]*">[\s\S]*?</div>\s*</div>\s*</div>\s*<!--\s*Simple Highlights',
    re.IGNORECASE
)

new_hero_cta = """<div class="hero-cta-row">
            <button type="button" class="btn-hero-primary" id="about-hero-primary-btn" onclick="handleMenuAccessRequest()">
              <span>🍽️</span> View Food Menu &amp; Order →
            </button>
            <button type="button" class="btn-hero-secondary" onclick="document.getElementById('about-website').scrollIntoView({behavior:'smooth'})">
              <span>📖</span> About Savitha Canteen
            </button>
          </div>
        </div>
      </div>

      <!-- Simple Highlights"""

m_hero = old_hero_cta.search(html)
assert m_hero, "Failed to match home hero-cta-row in index.html"
html = html[:m_hero.start()] + new_hero_cta + html[m_hero.end():]

# 1.3 Simplify the Reviews section on the website to be simple like all standard websites have
old_reviews_section = re.compile(
    r'<!--\s*={5,}\s*WEBSITE REVIEWS & RATINGS[\s\S]*?</section>',
    re.IGNORECASE
)

new_reviews_section = """<!-- =========================================================================
           STUDENT REVIEWS (SIMPLE, CLEAN & GENUINE)
           ========================================================================= -->
      <section id="reviews-section" class="reviews-section" style="padding-top:14px; padding-bottom:28px;">
        <div class="section-badge-center">
          <span>⭐ Campus Reviews</span>
        </div>
        <h2 class="section-main-heading">What Students Say</h2>
        <p class="section-sub-heading">Real feedback from students and faculty dining at Savitha Canteen.</p>

        <!-- Clean, Simple Reviews Cards Grid -->
        <div class="reviews-cards-grid" id="reviews-cards-grid" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(270px, 1fr)); gap:14px; margin-top:16px;">
          <!-- Rendered dynamically by app.js with clean standard cards -->
        </div>

        <!-- Simple Clean Action: Leave a Review -->
        <div style="text-align:center; margin-top:20px;">
          <button type="button" class="btn-hero-secondary" onclick="openAddReviewModal()" style="padding:9px 22px; font-size:0.88rem; display:inline-flex; align-items:center; gap:6px;">
            <span>✍️</span> Leave a Review
          </button>
        </div>
      </section>"""

m_rev = old_reviews_section.search(html)
assert m_rev, "Failed to find old reviews section in index.html"
html = html[:m_rev.start()] + new_reviews_section + html[m_rev.end():]

# 1.4 In view-order (Student Menu), place My Orders prominently at the top!
old_menu_header = re.compile(
    r'<div id="view-order" style="display:none;">\s*<!--\s*Simple Menu Header\s*-->\s*<div class="hero-section"[^>]*>[\s\S]*?<div class="hero-cta-row">[\s\S]*?</div>\s*</div>\s*</div>',
    re.IGNORECASE
)

new_menu_header = """<div id="view-order" style="display:none;">
      
      <!-- Prominent Student Menu Top Header Bar with My Orders AT THE TOP -->
      <div class="student-menu-top-bar" style="display:flex; justify-content:space-between; align-items:center; background:#ffffff; border:1.5px solid var(--border); border-radius:12px; padding:12px 18px; margin-bottom:16px; box-shadow:var(--shadow-sm); flex-wrap:wrap; gap:10px;">
        <div style="display:flex; align-items:center; gap:10px;">
          <span style="font-size:1.4rem;">🍽️</span>
          <div>
            <div style="font-size:1.05rem; font-weight:800; color:var(--text-main);">Student Food Menu</div>
            <div style="font-size:0.78rem; color:var(--text-muted);">Choose your dishes &amp; get instant pickup token</div>
          </div>
        </div>

        <div style="display:flex; align-items:center; gap:8px;">
          <button type="button" class="btn-top-orders" id="btn-menu-top-my-orders" onclick="openMyOrdersModal()" title="View your placed orders" style="display:inline-flex; background:#eef2ff; border:1.5px solid #c7d2fe; color:var(--primary); padding:8px 18px; border-radius:999px; font-weight:800; font-size:0.9rem; cursor:pointer; align-items:center; gap:8px;">
            <span>📦</span> My Orders (<span id="menu-my-orders-count">0</span>)
          </button>
          <button type="button" class="btn-hero-primary btn-menu-order-now" id="btn-hero-order-now" onclick="openCartModal()" style="padding:8px 18px; font-size:0.9rem; border-radius:999px;">
            <span>⚡</span> Order Now (<span id="hero-cart-count">0</span>)
          </button>
        </div>
      </div>"""

m_menu = old_menu_header.search(html)
assert m_menu, "Failed to match view-order header in index.html"
html = html[:m_menu.start()] + new_menu_header + html[m_menu.end():]

# Write index.html and sync
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copyfile('index.html', 'frontend/index.html')
print("Successfully updated index.html and frontend/index.html!")

# =========================================================================
# 2. UPDATE js/app.js (Remove Order Now from food items, simplify reviews)
# =========================================================================
with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 2.1 Remove Order Now button from individual food items in renderDishes()
old_button_html = re.compile(
    r'if\s*\(\s*qty\s*>\s*0\s*\)\s*\{[\s\S]*?buttonHtml\s*=\s*`[\s\S]*?`\s*;\s*\}\s*else\s*\{[\s\S]*?buttonHtml\s*=\s*`[\s\S]*?`\s*;\s*\}',
    re.IGNORECASE
)

new_button_html = """if (qty > 0) {
      buttonHtml = `
        <div class="qty-pill">
          <button type="button" onclick="updateDishQty('${dish.id}', -1)" title="Decrease quantity">-</button>
          <span class="qty-count">${qty}</span>
          <button type="button" onclick="updateDishQty('${dish.id}', 1)" title="Increase quantity">+</button>
        </div>
      `;
    } else {
      buttonHtml = `
        <button type="button" class="add-btn" onclick="updateDishQty('${dish.id}', 1)" title="Add to Cart">
          ADD +
        </button>
      `;
    }"""

m_dish_btn = old_button_html.search(js)
assert m_dish_btn, "Failed to match buttonHtml in renderDishes"
js = js[:m_dish_btn.start()] + new_button_html + js[m_dish_btn.end():]

# 2.2 Simplify renderFeedbackList() to render clean standard review cards
old_render_fb = re.compile(
    r'function\s+renderFeedbackList\s*\(\s*\)\s*\{[\s\S]*?\}\s*function\s+openAddReviewModal',
    re.IGNORECASE
)

new_render_fb = """function renderFeedbackList() {
  const container = document.getElementById("reviews-cards-grid") || document.getElementById("feedback-cards-container");
  if (!container) return;

  if (!feedbackList || feedbackList.length === 0) {
    container.innerHTML = `
      <div style="grid-column:1/-1; text-align:center; padding:28px 16px; background:#f8fafc; border-radius:12px; border:1px dashed var(--border);">
        <p style="color:var(--text-muted); font-size:0.9rem; margin:0;">No reviews yet. Be the first to leave a review!</p>
      </div>
    `;
    return;
  }

  // Render clean, standard 4-star and 5-star review cards
  container.innerHTML = feedbackList.slice(0, 6).map(fb => {
    const initial = (fb.name || "S").trim().charAt(0).toUpperCase();
    const rating = parseInt(fb.rating) || 5;
    const starsStr = "★".repeat(rating) + "☆".repeat(5 - rating);

    return `
      <div class="fb-review-card">
        <div class="fb-review-header">
          <div class="fb-user-info">
            <div class="fb-user-avatar">${initial}</div>
            <div>
              <div class="fb-user-name">${escapeHtml(fb.name || "Student")}</div>
              <div class="fb-user-year">${escapeHtml(fb.year || "Campus Dining")}</div>
            </div>
          </div>
          <div class="fb-stars" title="${rating}/5">${starsStr}</div>
        </div>
        <p class="fb-comment-text">"${escapeHtml(fb.comment || "")}"</p>
        <div class="fb-date">${fb.date || "Recent"}</div>
      </div>
    `;
  }).join('');
}

function openAddReviewModal"""

m_rfb = old_render_fb.search(js)
assert m_rfb, "Failed to match renderFeedbackList in js/app.js"
js = js[:m_rfb.start()] + new_render_fb + js[m_rfb.end():]

# 2.3 Ensure updateMyOrdersCount updates menu-my-orders-count
# Check updateMyOrdersCount
old_orders_count_fn = re.compile(
    r'function\s+updateMyOrdersCount\s*\(\s*\)\s*\{[\s\S]*?\}',
    re.IGNORECASE
)

new_orders_count_fn = """function updateMyOrdersCount() {
  const countMenu = document.getElementById("menu-my-orders-count");
  const count = (typeof myOrders !== "undefined" && Array.isArray(myOrders)) ? myOrders.length : 0;

  if (countMenu) {
    countMenu.textContent = count;
  }
  const badgeTop = document.getElementById("my-orders-count");
  if (badgeTop) {
    badgeTop.textContent = count;
    badgeTop.style.display = count > 0 ? "inline-block" : "none";
  }
}"""

m_oc = old_orders_count_fn.search(js)
assert m_oc, "Failed to match updateMyOrdersCount in js/app.js"
js = js[:m_oc.start()] + new_orders_count_fn + js[m_oc.end():]

# Save js/app.js and sync
with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
shutil.copyfile('js/app.js', 'frontend/js/app.js')
print("Successfully updated js/app.js and frontend/js/app.js!")
print("All tasks completed successfully!")
