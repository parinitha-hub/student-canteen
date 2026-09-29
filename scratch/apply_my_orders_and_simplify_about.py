import sys
import shutil

# --- 1. UPDATE index.html ---
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read().replace('\r\n', '\n')

# 1.1 Add My Orders button to navigation bar
old_nav = """      <!-- Navigation Bar contains ONLY Login -->
      <nav class="nav-links" id="main-nav-links">
        <div id="user-auth-slot">
          <button type="button" class="btn-top-login" id="btn-top-login" onclick="navigateToSection('login')" title="Go to Login Page">
            <span class="top-login-icon">👤</span>
            <span class="top-login-text">Login</span>
          </button>
        </div>
      </nav>"""

new_nav = """      <!-- Navigation Bar contains My Orders & Login -->
      <nav class="nav-links" id="main-nav-links" style="display:flex; align-items:center; gap:8px;">
        <button type="button" class="btn-top-orders" id="btn-top-orders" onclick="openMyOrdersModal()" title="View My Placed Orders">
          <span>📦</span>
          <span>My Orders</span>
          <span class="orders-count-badge" id="my-orders-count" style="display:none;">0</span>
        </button>
        <div id="user-auth-slot">
          <button type="button" class="btn-top-login" id="btn-top-login" onclick="navigateToSection('login')" title="Go to Login Page">
            <span class="top-login-icon">👤</span>
            <span class="top-login-text">Login</span>
          </button>
        </div>
      </nav>"""

assert old_nav in html, "Failed to find old_nav in index.html"
html = html.replace(old_nav, new_nav, 1)

# 1.2 Simplify About Website section
old_about_section = """    <!-- =========================================================================
         1. ABOUT THE WEBSITE & DEVELOPER SPOTLIGHT (OPENS FIRST ON WEBSITE LOAD)
         ========================================================================= -->
    <div id="view-about" style="display:block;">
      
      <!-- Clean, Inviting Hero Banner -->
      <div class="hero-section">
        <img src="assets/hero_banner.jpg" alt="Delicious Canteen Food" class="hero-img" fetchpriority="high" onerror="this.style.display='none';">
        <div class="hero-content">
          <div class="hero-developer-pill">
            <span>⚡ Designed &amp; Developed by <strong>Parinitha.S</strong></span>
          </div>
          <h1 class="hero-title">Welcome to Savitha Canteen</h1>
          <p class="hero-subtitle">Smart Campus Food Ordering &amp; AI Demand Prediction. Fresh, hot meals with zero waiting!</p>
          <div class="hero-cta-row">
            <button type="button" class="btn-hero-primary" id="about-hero-primary-btn" onclick="navigateToSection('order')">
              <span>🍽️</span> View Food Menu &amp; Order →
            </button>
            <button type="button" class="btn-hero-secondary" id="about-hero-secondary-btn" onclick="document.getElementById('about-website').scrollIntoView({behavior:'smooth'})">
              <span>📖</span> About Savitha Canteen
            </button>
          </div>
        </div>
      </div>

      <!-- 3 Simple Core Highlights -->
      <section id="about-website" class="about-section">
        <div class="section-badge-center">
          <span>💡 Smart Campus Dining</span>
        </div>
        <h2 class="section-main-heading">About Savitha Canteen</h2>
        <p class="section-sub-heading">A simple, smart food ordering system designed to eliminate cafeteria counter queues and reduce food waste through AI prediction.</p>

        <div class="about-cards-grid">
          <div class="about-card">
            <div class="about-card-icon">🎫</div>
            <h3 class="about-card-title">Zero-Wait Digital Tokens</h3>
            <p class="about-card-desc">Order your food online and receive an instant pickup token (e.g. #A-14). Walk to the counter only when your food is ready—no waiting in lines!</p>
          </div>

          <div class="about-card">
            <div class="about-card-icon">🤖</div>
            <h3 class="about-card-title">AI Demand Prediction</h3>
            <p class="about-card-desc">Smart machine learning forecasts daily dish quantities based on weekdays and weather, keeping meals fresh and preventing food wastage.</p>
          </div>

          <div class="about-card">
            <div class="about-card-icon">🍛</div>
            <h3 class="about-card-title">Fresh Quality Meals</h3>
            <p class="about-card-desc">Over 30 delicious campus favorites—from hot Veg &amp; Chicken Biryani to Crispy Dosas and refreshing beverages, prepared daily with hygiene.</p>
          </div>
        </div>

        <!-- Developer Spotlight Card: Parinitha.S -->
        <div class="developer-spotlight-card">
          <div class="dev-spotlight-badge">🏆 Website Developer &amp; AI Architect</div>
          <div class="dev-spotlight-grid">
            <div class="dev-avatar-wrap">
              <div class="dev-avatar-placeholder">PS</div>
              <div class="dev-status-indicator" title="Creator Verified">✓</div>
            </div>
            <div class="dev-info-col">
              <h3 class="dev-name">Parinitha.S</h3>
              <div class="dev-role-title">Lead Website Developer &amp; AI Systems Architect</div>
              <p class="dev-bio">
                Designed and developed the <strong>Savitha Canteen</strong> platform to modernize campus cafeteria dining. Engineered the complete frontend experience, real-time token tracking, and machine learning demand forecasting to eliminate waiting queues and promote zero food waste on campus.
              </p>
              <div class="dev-skill-tags">
                <span class="skill-tag">Full-Stack Web Development</span>
                <span class="skill-tag">Machine Learning &amp; AI</span>
                <span class="skill-tag">Python &amp; Flask</span>
                <span class="skill-tag">Campus Dining Innovation</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Simple, Interactive Student Feedback Section -->
      <section id="feedback-section" class="feedback-section">
        <div class="section-badge-center">
          <span>⭐ Student &amp; Faculty Feedback</span>
        </div>
        <h2 class="section-main-heading">Community Feedback</h2>
        <p class="section-sub-heading">Share your dining experience or suggestions to help us serve you better!</p>

        <div class="feedback-layout-grid">
          <!-- Left: Simple Feedback Submission Card -->
          <div class="feedback-form-card">
            <div class="feedback-form-header">
              <h3 style="font-size:1.2rem; font-weight:800; color:var(--text-main); margin-bottom:4px;">Add Your Feedback</h3>
              <p style="font-size:0.86rem; color:var(--text-muted); margin:0;">Takes less than 30 seconds.</p>
            </div>

            <form id="feedback-form" onsubmit="handleFeedbackSubmit(event)">
              <!-- Interactive Star Rating -->
              <div class="star-rating-block">
                <label class="fb-field-label">How was your food &amp; service?</label>
                <div class="star-rating-stars" id="star-rating-container">
                  <button type="button" class="star-btn active" data-rating="1" onclick="setStarRating(1)" onmouseover="hoverStarRating(1)" onmouseleave="resetStarHover()">★</button>
                  <button type="button" class="star-btn active" data-rating="2" onclick="setStarRating(2)" onmouseover="hoverStarRating(2)" onmouseleave="resetStarHover()">★</button>
                  <button type="button" class="star-btn active" data-rating="3" onclick="setStarRating(3)" onmouseover="hoverStarRating(3)" onmouseleave="resetStarHover()">★</button>
                  <button type="button" class="star-btn active" data-rating="4" onclick="setStarRating(4)" onmouseover="hoverStarRating(4)" onmouseleave="resetStarHover()">★</button>
                  <button type="button" class="star-btn active" data-rating="5" onclick="setStarRating(5)" onmouseover="hoverStarRating(5)" onmouseleave="resetStarHover()">★</button>
                </div>
                <div class="rating-verbal-badge" id="rating-verbal-label">⭐⭐⭐⭐⭐ Outstanding (5/5)</div>
                <input type="hidden" id="fb-rating-value" value="5">
              </div>

              <!-- Category Pills -->
              <div class="fb-input-group">
                <label class="fb-field-label">Category</label>
                <div class="fb-category-pills" id="fb-category-pills">
                  <button type="button" class="fb-cat-btn active" onclick="selectFeedbackCategory('Food Quality', this)">🍛 Food</button>
                  <button type="button" class="fb-cat-btn" onclick="selectFeedbackCategory('Service Speed', this)">⚡ Speed</button>
                  <button type="button" class="fb-cat-btn" onclick="selectFeedbackCategory('Website Experience', this)">💻 Website</button>
                  <button type="button" class="fb-cat-btn" onclick="selectFeedbackCategory('General Suggestion', this)">💡 Suggestion</button>
                </div>
                <input type="hidden" id="fb-category-value" value="Food Quality">
              </div>

              <!-- Name & Year in 2 columns -->
              <div class="fb-form-row">
                <div class="fb-input-group">
                  <label class="fb-field-label" for="fb-name">Your Name</label>
                  <input type="text" id="fb-name" class="input-field" placeholder="Enter your name" required style="width:100%;">
                </div>
                <div class="fb-input-group">
                  <label class="fb-field-label" for="fb-year">College Year</label>
                  <input type="text" id="fb-year" class="input-field" placeholder="Your year / department" required style="width:100%;">
                </div>
              </div>

              <!-- Comment -->
              <div class="fb-input-group">
                <label class="fb-field-label" for="fb-comment">Comments</label>
                <textarea id="fb-comment" class="input-field" rows="2" placeholder="Tell us what you liked or how we can improve..." required style="width:100%; resize:vertical;"></textarea>
              </div>

              <button type="submit" class="btn-submit-feedback" id="btn-submit-fb">
                <span>🚀</span> Submit Feedback
              </button>
            </form>
          </div>

          <!-- Right: Live Customer Reviews Feed -->
          <div class="feedback-feed-col">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
              <h3 style="font-size:1.1rem; font-weight:800; color:var(--text-main); margin:0;">Recent Reviews</h3>
              <span class="reviews-count-badge" id="reviews-count-badge">3 Reviews</span>
            </div>
            <div class="feedback-cards-container" id="feedback-cards-container">
              <!-- Rendered dynamically by app.js -->
            </div>
          </div>
        </div>
      </section>

      <!-- Bottom Clean Call-To-Action Card -->
      <div class="manager-card" style="margin-top:24px; margin-bottom:28px; text-align:center; padding:28px 20px; background:linear-gradient(135deg, #f5f3ff 0%, #eef2ff 100%); border:1.5px solid #c7d2fe;">
        <h3 style="font-size:1.35rem; font-weight:900; color:#312e81; margin-bottom:6px;">Ready to Order Fresh Campus Meals?</h3>
        <p style="color:#4f46e5; font-size:0.92rem; margin-bottom:16px;">Browse our 30+ delicious campus favorites and get your instant zero-wait digital token.</p>
        <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
          <button type="button" class="btn-hero-primary" id="about-bottom-primary-btn" onclick="navigateToSection('order')">
            <span>🍽️</span> Explore Food Menu &amp; Order →
          </button>
        </div>
      </div>

    </div>"""

new_about_section = """    <!-- =========================================================================
         1. ABOUT THE WEBSITE (CLEAN, SIMPLE & ELEGANT)
         ========================================================================= -->
    <div id="view-about" style="display:block;">
      
      <!-- Clean, Inviting Hero Banner -->
      <div class="hero-section" style="margin-bottom:20px;">
        <img src="assets/hero_banner.jpg" alt="Delicious Canteen Food" class="hero-img" fetchpriority="high" onerror="this.style.display='none';">
        <div class="hero-content">
          <div class="hero-developer-pill">
            <span>⚡ Designed &amp; Developed by <strong>Parinitha.S</strong></span>
          </div>
          <h1 class="hero-title">Savitha Canteen</h1>
          <p class="hero-subtitle">Fast campus food ordering with instant digital pickup tokens &amp; zero waiting.</p>
          <div class="hero-cta-row">
            <button type="button" class="btn-hero-primary" id="about-hero-primary-btn" onclick="navigateToSection('order')">
              <span>🍽️</span> View Food Menu &amp; Order →
            </button>
            <button type="button" class="btn-hero-secondary" onclick="openMyOrdersModal()">
              <span>📦</span> My Orders
            </button>
          </div>
        </div>
      </div>

      <!-- Simple Highlights & Developer Info (Clean & Concise) -->
      <section id="about-website" class="about-section" style="padding-top:10px; padding-bottom:24px;">
        <div class="section-badge-center">
          <span>💡 Campus Dining Made Simple</span>
        </div>
        <h2 class="section-main-heading">How Savitha Canteen Works</h2>
        <p class="section-sub-heading">Three simple steps to order fresh food without standing in cafeteria lines.</p>

        <div class="about-cards-grid">
          <div class="about-card">
            <div class="about-card-icon">🍽️</div>
            <h3 class="about-card-title">1. Select Your Dishes</h3>
            <p class="about-card-desc">Choose from 30+ hot meals, biryanis, dosas, and snacks directly from your phone or laptop.</p>
          </div>

          <div class="about-card">
            <div class="about-card-icon">🎫</div>
            <h3 class="about-card-title">2. Get Instant Token</h3>
            <p class="about-card-desc">Click Order Now to receive your unique pickup token (e.g. #A-14) with live kitchen status.</p>
          </div>

          <div class="about-card">
            <div class="about-card-icon">⚡</div>
            <h3 class="about-card-title">3. Zero-Wait Pickup</h3>
            <p class="about-card-desc">Walk up to the counter when your token is called and collect your hot, fresh meal immediately.</p>
          </div>
        </div>

        <!-- Clean Developer Attribution Card -->
        <div class="developer-spotlight-card" style="margin-top:20px; padding:18px 24px;">
          <div class="dev-spotlight-grid" style="align-items:center;">
            <div class="dev-avatar-wrap" style="width:58px; height:58px; min-width:58px;">
              <div class="dev-avatar-placeholder" style="font-size:1.35rem; width:58px; height:58px; line-height:58px;">PS</div>
              <div class="dev-status-indicator" title="Creator Verified">✓</div>
            </div>
            <div class="dev-info-col">
              <div style="font-size:0.75rem; font-weight:800; color:var(--primary); text-transform:uppercase; margin-bottom:2px;">🏆 Website Developer &amp; AI Architect</div>
              <h3 class="dev-name" style="font-size:1.2rem; margin-bottom:4px;">Parinitha.S</h3>
              <p class="dev-bio" style="font-size:0.88rem; margin-bottom:0; color:var(--text-muted);">
                Engineered the complete Savitha Canteen online ordering system and AI demand forecasting model to eliminate waiting lines and reduce campus food wastage.
              </p>
            </div>
          </div>
        </div>
      </section>

    </div>"""

assert old_about_section in html, "Failed to find old_about_section in index.html"
html = html.replace(old_about_section, new_about_section, 1)

# 1.3 Add My Orders button to Menu Header
old_menu_header = """          <div class="hero-cta-row">
            <button type="button" class="btn-hero-primary btn-menu-order-now" id="btn-hero-order-now" onclick="openCartModal()">
              <span>⚡</span> Order Now (<span id="hero-cart-count">0</span>)
            </button>
            <button type="button" class="btn-hero-secondary" onclick="openCartModal()">
              <span>🛒</span> View Cart
            </button>
            <button type="button" class="btn-hero-secondary" onclick="navigateToSection('about')">
              <span>📖</span> About Website
            </button>
          </div>"""

new_menu_header = """          <div class="hero-cta-row">
            <button type="button" class="btn-hero-primary btn-menu-order-now" id="btn-hero-order-now" onclick="openCartModal()">
              <span>⚡</span> Order Now (<span id="hero-cart-count">0</span>)
            </button>
            <button type="button" class="btn-hero-secondary" onclick="openCartModal()">
              <span>🛒</span> View Cart
            </button>
            <button type="button" class="btn-hero-secondary" id="btn-menu-my-orders" onclick="openMyOrdersModal()">
              <span>📦</span> My Orders (<span id="menu-my-orders-count">0</span>)
            </button>
            <button type="button" class="btn-hero-secondary" onclick="navigateToSection('about')">
              <span>📖</span> About
            </button>
          </div>"""

assert old_menu_header in html, "Failed to find old_menu_header in index.html"
html = html.replace(old_menu_header, new_menu_header, 1)

# 1.4 Add View My Orders button in Token Modal
old_token_modal_btns = """      <div style="display:flex; gap:10px;">
        <button type="button" class="btn-calc" onclick="closeTokenModal()" style="flex:1; padding:10px;">
          <span>🍽️</span> Back to Menu
        </button>
        <button type="button" class="btn-cancel-modal" id="btn-cancel-token-order" onclick="cancelCurrentTokenOrder()" style="flex:1; padding:10px;">
          <span>❌</span> Cancel
        </button>
      </div>"""

new_token_modal_btns = """      <div style="display:flex; gap:8px; margin-bottom:8px;">
        <button type="button" class="btn-calc" onclick="closeTokenModal(); openMyOrdersModal();" style="flex:1; padding:10px; background:#4f46e5;">
          <span>📦</span> View in My Orders
        </button>
        <button type="button" class="btn-calc" onclick="closeTokenModal()" style="flex:1; padding:10px;">
          <span>🍽️</span> Menu
        </button>
      </div>
      <div>
        <button type="button" class="btn-cancel-modal" id="btn-cancel-token-order" onclick="cancelCurrentTokenOrder()" style="width:100%; padding:8px; font-size:0.85rem;">
          <span>❌</span> Cancel This Order
        </button>
      </div>"""

assert old_token_modal_btns in html, "Failed to find old_token_modal_btns in index.html"
html = html.replace(old_token_modal_btns, new_token_modal_btns, 1)

# 1.5 Add My Orders Modal to Modals section
old_modals_start = """  <!-- Simple Cart Modal -->"""
new_my_orders_modal = """  <!-- My Orders Modal (View all placed orders & tokens) -->
  <div id="my-orders-modal" class="modal-overlay">
    <div class="modal-box" style="max-width:520px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid var(--border); padding-bottom:10px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:1.4rem;">📦</span>
          <div>
            <h2 style="font-size:1.25rem; font-weight:800; color:var(--text-main); margin:0;">My Orders</h2>
            <p style="font-size:0.8rem; color:var(--text-muted); margin:0;">Active pickup tokens &amp; placed meals</p>
          </div>
        </div>
        <button type="button" onclick="closeMyOrdersModal()" style="background:transparent; border:none; font-size:1.35rem; cursor:pointer; color:var(--text-muted); line-height:1;" aria-label="Close modal">✕</button>
      </div>

      <div id="my-orders-list-container" style="max-height:360px; overflow-y:auto; padding-right:2px;">
        <!-- Populated dynamically by app.js -->
      </div>

      <div style="margin-top:14px; display:flex; justify-content:space-between; gap:10px;">
        <button type="button" class="btn-calc" onclick="closeMyOrdersModal(); navigateToSection('order');" style="width:100%; padding:10px; font-size:0.9rem; justify-content:center;">
          <span>🍽️</span> Order More Dishes
        </button>
      </div>
    </div>
  </div>

  <!-- Simple Cart Modal -->"""

assert old_modals_start in html, "Failed to find old_modals_start in index.html"
html = html.replace(old_modals_start, new_my_orders_modal, 1)

# Write updated index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html.replace('\n', '\r\n'))

shutil.copyfile('index.html', 'frontend/index.html')
print("Successfully updated index.html and frontend/index.html!")

# --- 2. UPDATE css/style.css ---
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read().replace('\r\n', '\n')

my_orders_css = """
/* My Orders Button & Badges */
.btn-top-orders {
  background: rgba(99, 102, 241, 0.08);
  border: 1.5px solid rgba(99, 102, 241, 0.25);
  color: var(--primary);
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-weight: 700;
  font-size: 0.88rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: var(--transition);
  font-family: var(--font-heading);
}

.btn-top-orders:hover {
  background: rgba(99, 102, 241, 0.16);
  transform: translateY(-1px);
}

.orders-count-badge {
  background: var(--primary);
  color: #ffffff;
  font-size: 0.72rem;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 999px;
  min-width: 18px;
  text-align: center;
}

.my-order-card {
  background: #ffffff;
  border: 1.5px solid var(--border);
  border-radius: 12px;
  padding: 12px 14px;
  margin-bottom: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
"""

if '.btn-top-orders' not in css:
    css = css + my_orders_css

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css.replace('\n', '\r\n'))

shutil.copyfile('css/style.css', 'frontend/css/style.css')
print("Successfully updated css/style.css and frontend/css/style.css!")

# --- 3. UPDATE js/app.js ---
with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read().replace('\r\n', '\n')

# 3.1 Initialize myOrders
old_live_orders_def = """let liveOrders = [];
try {
  const savedOrders = localStorage.getItem("savitha_live_orders");
  liveOrders = savedOrders ? JSON.parse(savedOrders) : [];
} catch (e) {
  liveOrders = [];
}"""

new_my_orders_def = """let liveOrders = [];
try {
  const savedOrders = localStorage.getItem("savitha_live_orders");
  liveOrders = savedOrders ? JSON.parse(savedOrders) : [];
} catch (e) {
  liveOrders = [];
}

let myOrders = [];
try {
  const savedMy = localStorage.getItem("savitha_my_orders");
  myOrders = savedMy ? JSON.parse(savedMy) : [];
} catch (e) {
  myOrders = [];
}"""

assert old_live_orders_def in js, "Failed to find old_live_orders_def in js/app.js"
js = js.replace(old_live_orders_def, new_my_orders_def, 1)

# 3.2 Add My Orders handling functions
my_orders_functions = """
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

old_cancel_order = """  // Remove from live queue immediately ("after ordering the item if i cancle it should go")
  liveOrders = liveOrders.filter(o => o.id !== target.id && o.token !== target.token);
  try {
    localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders));
  } catch (e) {}"""

new_cancel_order = """  // Remove from live queue and myOrders immediately
  liveOrders = liveOrders.filter(o => o.id !== target.id && o.token !== target.token);
  myOrders = myOrders.filter(o => o.id !== target.id && o.token !== target.token);
  try {
    localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders));
    localStorage.setItem("savitha_my_orders", JSON.stringify(myOrders));
  } catch (e) {}
  updateMyOrdersCount();
  renderMyOrdersList();"""

assert old_cancel_order in js, "Failed to find old_cancel_order in js/app.js"
js = js.replace(old_cancel_order, new_cancel_order, 1)

# 3.3 Add to myOrders in placeOrderAndGenerateToken
old_token_save = """  liveOrders.unshift(newOrder);
  lastPlacedOrder = newOrder;
  try {
    localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders));
    localStorage.setItem("savitha_student_active_order", JSON.stringify(newOrder));
  } catch (e) {}"""

new_token_save = """  liveOrders.unshift(newOrder);
  myOrders.unshift(newOrder);
  lastPlacedOrder = newOrder;
  try {
    localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders));
    localStorage.setItem("savitha_my_orders", JSON.stringify(myOrders));
    localStorage.setItem("savitha_student_active_order", JSON.stringify(newOrder));
  } catch (e) {}
  updateMyOrdersCount();"""

assert old_token_save in js, "Failed to find old_token_save in js/app.js"
js = js.replace(old_token_save, new_token_save, 1)

# 3.4 Append functions before window exports
window_marker = """if (typeof window !== "undefined") window.quickOrderDish = quickOrderDish;"""
assert window_marker in js, "Failed to find window_marker in js/app.js"

new_exports = """if (typeof window !== "undefined") window.openMyOrdersModal = openMyOrdersModal;
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

js = js.replace(window_marker, my_orders_functions + "\n" + new_exports + window_marker, 1)

# 3.5 Also call updateMyOrdersCount() on DOMContentLoaded / initUserAuth
init_marker = """  renderUserAuthSlot();
  applyRoleVisibility();
  // Open About the Website page first on website startup!
  performSwitchMode("about");"""

new_init = """  renderUserAuthSlot();
  applyRoleVisibility();
  updateMyOrdersCount();
  // Open About the Website page first on website startup!
  performSwitchMode("about");"""

assert init_marker in js, "Failed to find init_marker in js/app.js"
js = js.replace(init_marker, new_init, 1)

# Write updated js/app.js
with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js.replace('\n', '\r\n'))

shutil.copyfile('js/app.js', 'frontend/js/app.js')
print("Successfully updated js/app.js and frontend/js/app.js!")
