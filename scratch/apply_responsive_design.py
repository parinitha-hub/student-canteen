import sys
import re
import shutil

sys.stdout.reconfigure(encoding='utf-8')

def update_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update <meta name="viewport">
    old_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    new_meta = '''<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes, viewport-fit=cover">
  <meta name="theme-color" content="#4f46e5">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="mobile-web-app-capable" content="yes">'''

    if old_meta in html:
        html = html.replace(old_meta, new_meta, 1)
        print("✓ Updated viewport and mobile app meta tags in index.html")
    else:
        print("ℹ Old meta tag not found verbatim (may already be updated)")

    # 2. Add Phone / Share button in Header
    old_header_slot = '''        <div id="user-auth-slot">'''
    new_header_slot = '''        <!-- Quick Device Link: Scan QR to open on phones or other laptops -->
        <button type="button" class="btn-network-qr-btn" onclick="openNetworkShareModal()"
          title="Open website on your phone or other laptops"
          style="background:linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border:1.5px solid #93c5fd; color:#1d4ed8; font-size:0.8rem; font-weight:800; padding:6px 12px; border-radius:999px; cursor:pointer; display:inline-flex; align-items:center; gap:5px; transition:transform 0.15s ease;">
          <span>📱</span> <span class="hide-on-mobile-text">Phone / Share</span>
        </button>

        <div id="user-auth-slot">'''

    if old_header_slot in html and 'btn-network-qr-btn' not in html:
        html = html.replace(old_header_slot, new_header_slot, 1)
        print("✓ Added Phone / Share button to header in index.html")
    else:
        print("ℹ Header Phone button already present or target not found")

    # 3. Add Mobile Bottom Nav & Network Share Modal before </body>
    modal_and_nav = '''
  <!-- =========================================================================
       MODERN MOBILE BOTTOM NAVIGATION BAR (Smartphones & Tablets <= 768px)
       ========================================================================= -->
  <nav class="mobile-bottom-nav" id="mobile-bottom-nav" aria-label="Mobile Navigation">
    <button type="button" class="mobile-nav-item active" id="mob-nav-about" onclick="navigateToSection('about')">
      <span class="mob-nav-icon">🏛️</span>
      <span class="mob-nav-label">About</span>
    </button>
    <button type="button" class="mobile-nav-item" id="mob-nav-menu" onclick="handleMenuAccessRequest()">
      <span class="mob-nav-icon">🍽️</span>
      <span class="mob-nav-label">Food Menu</span>
    </button>
    <button type="button" class="mobile-nav-item" id="mob-nav-orders" onclick="openMyOrdersModal()">
      <span class="mob-nav-icon">📦</span>
      <span class="mob-nav-label">Orders</span>
      <span class="mob-nav-badge" id="mob-orders-badge" style="display:none;">0</span>
    </button>
    <button type="button" class="mobile-nav-item" id="mob-nav-cart" onclick="openCartModal()">
      <span class="mob-nav-icon">🛒</span>
      <span class="mob-nav-label">Cart</span>
      <span class="mob-nav-badge" id="mob-cart-badge" style="display:none;">0</span>
    </button>
    <button type="button" class="mobile-nav-item" id="mob-nav-share" onclick="openNetworkShareModal()">
      <span class="mob-nav-icon">📱</span>
      <span class="mob-nav-label">Phone View</span>
    </button>
  </nav>

  <!-- =========================================================================
       NETWORK SHARE / OPEN ON PHONE MODAL (WITH LIVE QR CODE & IP LINK)
       ========================================================================= -->
  <div id="network-share-modal" class="custom-modal" role="dialog" aria-modal="true" aria-labelledby="share-modal-title">
    <div class="custom-modal-backdrop" onclick="closeNetworkShareModal()"></div>
    <div class="modal-box network-share-box" style="max-width:440px; text-align:center; padding:24px 20px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:1.4rem;">📱</span>
          <h3 id="share-modal-title" style="font-size:1.15rem; font-weight:800; color:var(--text-main); margin:0;">Open on Other Phones &amp; Laptops</h3>
        </div>
        <button type="button" class="modal-close-btn" onclick="closeNetworkShareModal()" aria-label="Close modal">×</button>
      </div>

      <p style="font-size:0.86rem; color:var(--text-muted); margin:0 0 16px 0; line-height:1.4;">
        Connect your phone or other device to the same Wi-Fi network and scan the QR code or open this URL:
      </p>

      <!-- QR Code Display Area -->
      <div style="background:#ffffff; padding:16px; border-radius:14px; border:2px solid #e2e8f0; display:inline-block; margin-bottom:14px; box-shadow:0 4px 12px rgba(0,0,0,0.06);">
        <img id="network-qr-image" src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&amp;data=http://10.209.246.16:5000" 
             alt="QR code to open Savitha Canteen on phone" 
             style="width:180px; height:180px; display:block; border-radius:8px;"
             onerror="this.onerror=null; this.src='https://chart.googleapis.com/chart?cht=qr&amp;chs=200x200&amp;chl=http://10.209.246.16:5000';">
        <div style="font-size:0.75rem; font-weight:700; color:#64748b; margin-top:8px;">📷 Scan with Phone Camera</div>
      </div>

      <!-- LAN URL Box with 1-Click Copy -->
      <div style="background:#f1f5f9; border:1.5px solid #cbd5e1; border-radius:10px; padding:10px 12px; display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:14px;">
        <span id="network-share-url-text" style="font-size:0.92rem; font-weight:800; color:var(--primary); font-family:monospace; word-break:break-all;">http://10.209.246.16:5000</span>
        <button type="button" class="btn-copy-link" onclick="copyNetworkShareLink()" 
                style="padding:6px 12px; font-size:0.8rem; font-weight:700; background:var(--primary); color:#ffffff; border:none; border-radius:6px; cursor:pointer; white-space:nowrap;">
          📋 Copy
        </button>
      </div>

      <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:10px; padding:10px 12px; text-align:left; font-size:0.8rem; color:#1e40af; line-height:1.4;">
        💡 <strong>Quick Tip:</strong> Both devices must be on the same Wi-Fi hotspot or campus network. Any phone (Android or iPhone) can place orders hot and fresh!
      </div>
    </div>
  </div>
'''

    if 'id="mobile-bottom-nav"' not in html:
        pos = html.rfind('</body>')
        if pos != -1:
            html = html[:pos] + modal_and_nav + '\n' + html[pos:]
            print("✓ Added mobile bottom nav bar and network share modal to index.html")
    else:
        print("ℹ mobile-bottom-nav already present in index.html")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

def update_css():
    with open('css/style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    if 'mobile-bottom-nav' in css:
        print("ℹ Responsive CSS rules already present in css/style.css")
        return

    responsive_css = '''

/* =========================================================================
   COMPREHENSIVE RESPONSIVE DESIGN FOR PHONES, TABLETS & LAPTOPS
   ========================================================================= */

/* Prevent horizontal overflow on all screen sizes */
html, body {
  overflow-x: hidden !important;
  max-width: 100vw !important;
  width: 100% !important;
  -webkit-text-size-adjust: 100%;
}

button, select, input, .clickable-pill, .official-nav-btn {
  touch-action: manipulation;
}

/* Fluid responsive container */
@media (max-width: 1200px) {
  .container {
    max-width: 100% !important;
    padding-left: 20px !important;
    padding-right: 20px !important;
  }
}

/* Tablet adjustments (769px to 1024px) */
@media (min-width: 769px) and (max-width: 1024px) {
  .mobile-bottom-nav {
    display: none !important;
  }
  .dishes-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 16px !important;
  }
  .reviews-cards-grid, #reviews-cards-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 14px !important;
  }
  .features-grid, .about-features-grid {
    grid-template-columns: repeat(2, 1fr) !important;
  }
  .nav-bar {
    padding: 0 10px !important;
  }
}

/* Mobile Phones (max-width: 768px) */
@media (max-width: 768px) {
  .container {
    padding-left: 12px !important;
    padding-right: 12px !important;
  }

  /* Main Header adjustments */
  .main-header {
    position: sticky !important;
    top: 0 !important;
    z-index: 100 !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
  }
  .nav-bar {
    height: 58px !important;
    padding: 0 4px !important;
    gap: 8px !important;
  }
  .brand-logo-img {
    width: 34px !important;
    height: 34px !important;
  }
  .brand-title {
    font-size: 1.1rem !important;
  }
  .brand-dev-badge {
    display: none !important;
  }
  .hide-on-mobile-text {
    display: none !important;
  }

  /* Desktop nav buttons hidden when mobile bottom bar is active */
  #nav-btn-about, #nav-btn-reviews, #nav-btn-home, #btn-top-my-orders-nav {
    display: none !important;
  }

  /* Hero Section */
  .hero-section {
    padding: 24px 16px !important;
    min-height: auto !important;
    margin-bottom: 16px !important;
    border-radius: 16px !important;
  }
  .hero-floating-badge {
    font-size: 0.72rem !important;
    padding: 3px 10px !important;
    flex-wrap: wrap !important;
    justify-content: center !important;
  }
  .hero-title {
    font-size: 1.7rem !important;
    line-height: 1.15 !important;
  }
  .hero-subtitle {
    font-size: 0.88rem !important;
    margin-bottom: 14px !important;
  }
  .hero-cta-row {
    flex-direction: column !important;
    gap: 8px !important;
  }
  .btn-hero-primary, .btn-hero-secondary {
    width: 100% !important;
    padding: 12px 18px !important;
    font-size: 0.92rem !important;
    justify-content: center !important;
  }

  /* Feature highlights grid on About page */
  .features-grid, .about-features-grid {
    grid-template-columns: 1fr 1fr !important;
    gap: 10px !important;
  }

  /* Today's Special & Offers Grid */
  .simple-offers-grid {
    grid-template-columns: 1fr !important;
    gap: 10px !important;
  }
  .special-deal-card {
    padding: 12px 14px !important;
  }

  /* Food Menu Dishes Grid */
  .dishes-grid {
    grid-template-columns: 1fr !important;
    gap: 12px !important;
  }
  .dish-card {
    border-radius: 14px !important;
    padding: 14px !important;
  }
  .dish-card-img-wrap {
    height: 160px !important;
  }

  /* Category pills horizontal smooth scroll */
  .category-bar {
    overflow-x: auto !important;
    flex-wrap: nowrap !important;
    padding: 4px 2px 8px 2px !important;
    -webkit-overflow-scrolling: touch !important;
    scrollbar-width: none !important;
  }
  .category-bar::-webkit-scrollbar {
    display: none !important;
  }
  .category-pill {
    flex-shrink: 0 !important;
    padding: 8px 14px !important;
    font-size: 0.84rem !important;
  }

  /* Reviews Cards Grid */
  .reviews-cards-grid, #reviews-cards-grid {
    grid-template-columns: 1fr !important;
    gap: 12px !important;
  }

  /* Modals: Convert into elegant Bottom Sheets on Mobile */
  .modal-box {
    width: 100% !important;
    max-width: 100% !important;
    border-radius: 20px 20px 0 0 !important;
    max-height: 88vh !important;
    overflow-y: auto !important;
    margin: auto 0 0 0 !important;
    padding: 18px 16px !important;
    -webkit-overflow-scrolling: touch !important;
  }
  .custom-modal {
    align-items: flex-end !important;
    padding: 0 !important;
  }

  /* Forms on Mobile */
  .input-field, select, input[type="text"], input[type="tel"], input[type="password"] {
    font-size: 16px !important; /* Prevents auto-zoom in mobile Safari */
  }

  /* Cart Floating Preview Bar */
  .cart-floating-bar, #cart-floating-bar {
    bottom: 74px !important; /* Sits right above the mobile bottom nav bar */
    left: 10px !important;
    right: 10px !important;
    padding: 10px 14px !important;
    border-radius: 14px !important;
  }

  /* Ensure footer has padding so mobile bottom nav doesn't cover text */
  footer {
    padding-bottom: 84px !important;
  }

  /* Show Mobile Bottom Navigation Bar */
  .mobile-bottom-nav {
    display: flex !important;
  }
}

/* Very Small Mobile Phones (screens <= 380px) */
@media (max-width: 380px) {
  .features-grid, .about-features-grid {
    grid-template-columns: 1fr !important;
  }
  .hero-title {
    font-size: 1.45rem !important;
  }
  .mob-nav-label {
    font-size: 0.65rem !important;
  }
  .mob-nav-icon {
    font-size: 1.15rem !important;
  }
}

/* Mobile Bottom Navigation Bar Base Styles */
.mobile-bottom-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-top: 1.5px solid rgba(226, 232, 240, 0.9);
  z-index: 990;
  justify-content: space-around;
  align-items: center;
  padding: 0 4px;
  padding-bottom: env(safe-area-inset-bottom, 0px);
  box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.08);
}

.mobile-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 6px 10px;
  border-radius: 10px;
  position: relative;
  transition: all 0.2s ease;
  flex: 1;
  max-width: 72px;
}

.mobile-nav-item.active {
  color: var(--primary, #4f46e5);
}

.mobile-nav-item.active .mob-nav-icon {
  transform: translateY(-2px) scale(1.1);
}

.mob-nav-icon {
  font-size: 1.3rem;
  line-height: 1;
  margin-bottom: 3px;
  transition: transform 0.2s ease;
}

.mob-nav-label {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.2px;
  white-space: nowrap;
}

.mob-nav-badge {
  position: absolute;
  top: 4px;
  right: 14px;
  background: #ea580c;
  color: #ffffff;
  font-size: 0.65rem;
  font-weight: 900;
  padding: 1px 5px;
  border-radius: 999px;
  min-width: 16px;
  text-align: center;
  border: 1.5px solid #ffffff;
  box-shadow: 0 2px 5px rgba(234, 88, 12, 0.3);
}
'''
    with open('css/style.css', 'a', encoding='utf-8') as f:
        f.write(responsive_css)
    print("✓ Appended comprehensive responsive styles to css/style.css")

def update_js():
    with open('js/app.js', 'r', encoding='utf-8') as f:
        js = f.read()

    # 1. Add Network Share functions
    share_functions = '''
// =========================================================================
// NETWORK SHARE / OPEN ON MOBILE PHONE OR OTHER LAPTOPS
// =========================================================================
function openNetworkShareModal() {
  const modal = document.getElementById("network-share-modal");
  if (!modal) return;

  let targetUrl = window.location.origin;
  if (!targetUrl || targetUrl.includes("localhost") || targetUrl.includes("127.0.0.1")) {
    targetUrl = "http://10.209.246.16:5000";
  }

  fetch(`${API_BASE}/api/network-info`)
    .then(r => r.ok ? r.json() : null)
    .then(data => {
      if (data && data.lan_url) {
        targetUrl = data.lan_url;
      }
      applyNetworkShareUrl(targetUrl);
    })
    .catch(() => {
      applyNetworkShareUrl(targetUrl);
    });

  modal.classList.add("show");
}

function applyNetworkShareUrl(url) {
  const textEl = document.getElementById("network-share-url-text");
  const imgEl = document.getElementById("network-qr-image");
  if (textEl) textEl.textContent = url;
  if (imgEl) {
    imgEl.src = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(url)}`;
  }
}

function closeNetworkShareModal() {
  const modal = document.getElementById("network-share-modal");
  if (modal) modal.classList.remove("show");
}

function copyNetworkShareLink() {
  const textEl = document.getElementById("network-share-url-text");
  const url = textEl ? textEl.textContent : window.location.href;
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(url)
      .then(() => showToast("📋 Link copied! Open it on other phones or laptops.", "success"))
      .catch(() => fallbackCopy(url));
  } else {
    fallbackCopy(url);
  }
}

function fallbackCopy(text) {
  const ta = document.createElement("textarea");
  ta.value = text;
  document.body.appendChild(ta);
  ta.select();
  document.execCommand("copy");
  document.body.removeChild(ta);
  showToast("📋 Link copied! Open it on other phones or laptops.", "success");
}
'''

    if 'openNetworkShareModal' not in js:
        js += '\n' + share_functions
        print("✓ Added network share & QR functions to js/app.js")

    # 2. Update navigateToSection to highlight mobile bottom nav
    old_nav = '''function updateActiveNavBtn(section) {'''
    new_nav = '''function updateActiveNavBtn(section) {
  // Update mobile bottom nav items
  const mobItems = document.querySelectorAll(".mobile-nav-item");
  mobItems.forEach(b => b.classList.remove("active"));
  if (section === "about" || section === "reviews") {
    const mobAbout = document.getElementById("mob-nav-about");
    if (mobAbout) mobAbout.classList.add("active");
  } else if (section === "order" || section === "home") {
    const mobMenu = document.getElementById("mob-nav-menu");
    if (mobMenu) mobMenu.classList.add("active");
  }'''

    if old_nav in js and 'mob-nav-about' not in js:
        js = js.replace(old_nav, new_nav, 1)
        print("✓ Updated updateActiveNavBtn for mobile bottom nav in js/app.js")

    # 3. Update updateCartBar to update mobile cart badge
    old_cart_bar = '''function updateCartBar() {'''
    new_cart_bar = '''function updateCartBar() {
  // Update mobile bottom nav cart badge
  const totalCount = Object.values(cart).reduce((a, b) => a + b, 0);
  const mobCartBadge = document.getElementById("mob-cart-badge");
  if (mobCartBadge) {
    mobCartBadge.textContent = totalCount;
    mobCartBadge.style.display = totalCount > 0 ? "inline-block" : "none";
  }'''

    if old_cart_bar in js and 'mob-cart-badge' not in js:
        js = js.replace(old_cart_bar, new_cart_bar, 1)
        print("✓ Updated updateCartBar for mobile cart badge in js/app.js")

    # 4. Update updateMyOrdersCount to update mobile orders badge
    old_orders_count = '''  if (countTop) {
    countTop.textContent = count;
    countTop.style.display = count > 0 ? "inline-block" : "none";
  }'''
    new_orders_count = '''  if (countTop) {
    countTop.textContent = count;
    countTop.style.display = count > 0 ? "inline-block" : "none";
  }
  const mobOrdersBadge = document.getElementById("mob-orders-badge");
  if (mobOrdersBadge) {
    mobOrdersBadge.textContent = count;
    mobOrdersBadge.style.display = count > 0 ? "inline-block" : "none";
  }'''

    if old_orders_count in js and 'mob-orders-badge' not in js:
        js = js.replace(old_orders_count, new_orders_count, 1)
        print("✓ Updated updateMyOrdersCount for mobile orders badge in js/app.js")

    # 5. Expose window functions
    if 'window.openNetworkShareModal' not in js:
        old_expose = 'window.initUserAuth = initUserAuth;'
        new_expose = '''window.openNetworkShareModal = openNetworkShareModal;
  window.closeNetworkShareModal = closeNetworkShareModal;
  window.copyNetworkShareLink = copyNetworkShareLink;
  window.initUserAuth = initUserAuth;'''
        js = js.replace(old_expose, new_expose, 1)
        print("✓ Exposed network share modal functions on window")

    with open('js/app.js', 'w', encoding='utf-8') as f:
        f.write(js)

def mirror_files():
    shutil.copyfile('index.html', 'frontend/index.html')
    shutil.copyfile('css/style.css', 'frontend/css/style.css')
    shutil.copyfile('js/app.js', 'frontend/js/app.js')
    print("✓ Successfully mirrored all files to frontend/")

if __name__ == '__main__':
    update_html()
    update_css()
    update_js()
    mirror_files()
    print("ALL RESPONSIVE DESIGN UPDATES COMPLETED!")
