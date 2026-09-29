import os
import shutil
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("Starting clean redesign...")

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove gov-top-bar
old_gov_bar = re.search(r'<!--\s*={5,}\s*1\.\s*INSTITUTIONAL TOP BAR.*?</div>\s*</div>\s*</div>', html, re.DOTALL)
if old_gov_bar:
    html = html.replace(old_gov_bar.group(0), '')
    print("✓ Removed gov-top-bar")
else:
    print("! Could not find gov-top-bar regex")

# Remove official-announcement-bar
old_announcement = re.search(r'<!--\s*Official Campus Notice Ticker\s*-->\s*<div class="official-announcement-bar">.*?</div>\s*</div>', html, re.DOTALL)
if old_announcement:
    html = html.replace(old_announcement.group(0), '')
    print("✓ Removed official-announcement-bar")
else:
    print("! Could not find official-announcement-bar regex")

# Replace header navigation
old_header = re.search(r'<header>.*?</header>', html, re.DOTALL)
clean_header = """<header class="main-header">
    <div class="container nav-bar">
      <!-- Brand Logo -->
      <a href="#" class="brand" onclick="navigateToSection('about'); return false;"
        title="Savitha Canteen - Smart Campus Dining">
        <img src="assets/logo.png" alt="Savitha Canteen Logo" class="brand-logo-img">
        <div class="brand-text-wrap">
          <div class="brand-title">Savitha <span>Canteen</span></div>
          <div class="brand-dev-badge">Smart Campus Dining</div>
        </div>
      </a>

      <!-- Navigation Links: On About webpage, Menu and My Orders are hidden -->
      <nav class="nav-links" id="main-nav-links" style="display:flex; align-items:center; gap:8px;">
        <button type="button" class="official-nav-btn active" id="nav-btn-about" onclick="navigateToSection('about')">
          <span>🏛️</span> About
        </button>
        <button type="button" class="official-nav-btn" id="nav-btn-home" onclick="navigateToSection('home')" style="display:none;">
          <span>🍽️</span> Menu
        </button>
        <button type="button" class="official-nav-btn" id="btn-top-my-orders-nav" onclick="openMyOrdersModal()" style="display:none;">
          <span>📦</span> My Orders <span class="orders-count-badge" id="my-orders-count" style="display:none;">0</span>
        </button>
        <button type="button" class="official-nav-btn kitchen-only" id="nav-btn-kitchen" onclick="navigateToSection('kitchen')" style="display:none;">
          <span>👨‍🍳</span> Staff Portal
        </button>
        <div id="user-auth-slot">
          <button type="button" class="btn-top-login" id="btn-top-login" onclick="navigateToSection('login')"
            title="Go to Login Page">
            <span class="top-login-icon">👤</span>
            <span class="top-login-text">Login</span>
          </button>
        </div>
      </nav>
    </div>
  </header>"""

if old_header:
    html = html.replace(old_header.group(0), clean_header)
    print("✓ Replaced header with clean navigation")

# Replace view-about with clean, simple, elegant About section
old_about = re.search(r'<div id="view-about"[^>]*>.*?</div>\s*<!--\s*={5,}\s*2\.\s*SIMPLE & CLEAN LOGIN PORTAL', html, re.DOTALL)

clean_about = """<div id="view-about" style="display:block;">

      <!-- Clean, Inviting Hero Banner -->
      <div class="hero-section" style="margin-bottom:24px; min-height:220px; padding:36px 24px; text-align:center;">
        <img src="assets/hero_banner.jpg" alt="Delicious Canteen Food" class="hero-img" fetchpriority="high"
          onerror="this.style.display='none';">

        <div class="hero-content" style="position:relative; z-index:2; max-width:760px; margin:0 auto;">
          <div class="hero-developer-pill" style="margin-bottom:12px;">
            <span>⚡ Designed &amp; Developed by <strong>Parinitha.S</strong></span>
          </div>

          <h1 class="hero-title" style="font-size:2.4rem; font-weight:900; margin-bottom:8px;">Savitha Canteen</h1>

          <p class="hero-subtitle" style="font-size:1.05rem; margin-bottom:20px; color:#f1f5f9;">
            Smart campus food ordering with instant digital pickup tokens &amp; zero waiting.
          </p>

          <div class="hero-cta-row" style="justify-content:center;">
            <button type="button" class="btn-hero-primary" id="about-hero-primary-btn"
              onclick="handleMenuAccessRequest()">
              <span>🍽️</span> Login to Order Food →
            </button>
            <button type="button" class="btn-hero-secondary"
              onclick="document.getElementById('about-website').scrollIntoView({behavior:'smooth'})">
              <span>📖</span> How It Works
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
            <p class="about-card-desc">Order to receive your unique pickup token (e.g. #A-14) with live kitchen status.</p>
          </div>

          <div class="about-card">
            <div class="about-card-icon">⚡</div>
            <h3 class="about-card-title">3. Zero-Wait Pickup</h3>
            <p class="about-card-desc">Walk up to the counter when your token is called and collect your hot, fresh meal immediately.</p>
          </div>
        </div>

        <!-- Clean Canteen Info Card -->
        <div style="background:#ffffff; border:1.5px solid var(--border); border-radius:14px; padding:16px 20px; margin-top:20px; display:flex; justify-content:space-around; align-items:center; flex-wrap:wrap; gap:12px; box-shadow:var(--shadow-sm);">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.3rem;">🕒</span>
            <div>
              <div style="font-size:0.88rem; font-weight:800; color:var(--text-main);">Daily Dining Hours</div>
              <div style="font-size:0.78rem; color:var(--text-muted);">7:30 AM – 8:30 PM (Mon – Sun)</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.3rem;">📍</span>
            <div>
              <div style="font-size:0.88rem; font-weight:800; color:var(--text-main);">Location</div>
              <div style="font-size:0.78rem; color:var(--text-muted);">Main Dining Complex, Counters 1–4</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.3rem;">🛡️</span>
            <div>
              <div style="font-size:0.88rem; font-weight:800; color:var(--text-main);">Quality Assured</div>
              <div style="font-size:0.78rem; color:var(--text-muted);">FSSAI Certified Fresh Campus Meals</div>
            </div>
          </div>
        </div>

        <!-- Clean Developer Attribution Card: Parinitha.S -->
        <div class="developer-spotlight-card" style="margin-top:20px; padding:20px 24px;">
          <div class="dev-spotlight-grid" style="align-items:center;">
            <div class="dev-avatar-wrap" style="width:60px; height:60px; min-width:60px;">
              <div class="dev-avatar-placeholder" style="font-size:1.35rem; width:60px; height:60px; line-height:60px;">PS</div>
              <div class="dev-status-indicator" title="Creator Verified">✓</div>
            </div>
            <div class="dev-info-col">
              <div style="font-size:0.75rem; font-weight:800; color:var(--primary); text-transform:uppercase; margin-bottom:2px; letter-spacing:0.5px;">
                🏆 Website Developer &amp; AI Architect
              </div>
              <h3 class="dev-name" style="font-size:1.25rem; margin-bottom:4px;">Parinitha.S</h3>
              <p class="dev-bio" style="font-size:0.88rem; margin-bottom:0; color:var(--text-muted); line-height:1.5;">
                Designed and developed the Savitha Canteen platform to eliminate counter queues and reduce campus food waste through AI demand forecasting.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Student Reviews Section -->
      <section id="reviews-section" class="reviews-section" style="padding-top:10px; padding-bottom:24px;">
        <div class="section-badge-center">
          <span>⭐ Campus Reviews</span>
        </div>
        <h2 class="section-main-heading">What Students Say</h2>
        <p class="section-sub-heading">Real feedback from students and faculty dining at Savitha Canteen.</p>

        <div class="reviews-cards-grid" id="reviews-cards-grid"
          style="display:grid; grid-template-columns:repeat(auto-fill, minmax(270px, 1fr)); gap:14px; margin-top:16px;">
        </div>

        <div style="text-align:center; margin-top:18px;">
          <button type="button" class="btn-hero-secondary" onclick="openAddReviewModal()"
            style="padding:9px 22px; font-size:0.88rem; display:inline-flex; align-items:center; gap:6px;">
            <span>✍️</span> Leave a Review
          </button>
        </div>
      </section>

    </div>

    <!-- =========================================================================
         2. SIMPLE & CLEAN LOGIN PORTAL"""

if old_about:
    html = html.replace(old_about.group(0), clean_about)
    print("✓ Replaced view-about with clean, simple version")

# Replace footer with clean, modern footer
old_footer = re.search(r'<footer style="background:#0b1120;.*?</footer>', html, re.DOTALL)
clean_footer = """<footer style="background:#0f172a; color:#cbd5e1; padding:28px 0; border-top:1px solid rgba(255,255,255,0.08); margin-top:40px;">
    <div class="container" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
      <div style="display:flex; align-items:center; gap:12px;">
        <img src="assets/logo.png" alt="Savitha Canteen Logo" style="width:36px; height:36px; border-radius:10px;">
        <div>
          <div style="font-size:1.05rem; font-weight:900; color:#ffffff;">Savitha <span style="color:#f59e0b;">Canteen</span></div>
          <div style="font-size:0.75rem; color:#94a3b8;">Smart Campus Dining • Zero-Wait Pickup</div>
        </div>
      </div>
      <div style="font-size:0.85rem; color:#94a3b8;">
        Designed &amp; Developed with ❤️ by <strong style="color:#f59e0b;">Parinitha.S</strong>
      </div>
      <div style="font-size:0.8rem; color:#64748b;">
        © 2026 Savitha Canteen. All rights reserved.
      </div>
    </div>
  </footer>"""

if old_footer:
    html = html.replace(old_footer.group(0), clean_footer)
    print("✓ Replaced footer with clean modern footer")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

shutil.copyfile('index.html', 'frontend/index.html')
print("Successfully updated index.html and frontend/index.html!")
