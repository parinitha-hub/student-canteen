import os
import shutil
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Starting restoration of login portal, reviews, and animations...")

# --- 1. UPDATE index.html ---
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1.1 Insert reviews section and close view-about, then insert view-login
# Find the end of developer-spotlight-card
dev_card_end = html.find("""<div id="view-order" style="display:none;">""")
if dev_card_end == -1:
    print("! Could not find view-order marker in index.html")
    sys.exit(1)

# Find where developer card ends before view-order
dev_spotlight_idx = html.find("""<!-- Official Developer & AI Architect Spotlight: Parinitha.S -->""")
if dev_spotlight_idx == -1:
    print("! Could not find developer spotlight comment")
    # Try finding Parinitha.S
    dev_spotlight_idx = html.find("Parinitha.S")

# Let's inspect the block between dev_spotlight_idx and view-order
snippet = html[dev_spotlight_idx:dev_card_end]
print(f"Snippet between developer spotlight and view-order is {len(snippet)} chars")

# We want:
# 1. Developer spotlight card
# 2. Campus Reviews Section (<section id="reviews-section">)
# 3. </div> <!-- close view-about -->
# 4. <div id="view-login"> (complete Login portal for Student and Kitchen Staff)
# 5. <!-- 3. SIMPLE FOOD ORDERING & MENU EXPERIENCE -->
#    <div id="view-order" style="display:none;">

# Reconstruct that entire section cleanly:
reviews_and_login_html = """
        <!-- Official Developer & AI Architect Spotlight: Parinitha.S -->
        <div class="developer-spotlight-card" style="margin-top:24px; padding:24px 28px; background:#ffffff; border:1.5px solid var(--border); border-radius:16px; box-shadow:var(--shadow-sm); transition:transform 0.3s ease, box-shadow 0.3s ease;">
          <div class="dev-spotlight-grid" style="display:flex; align-items:center; gap:22px; flex-wrap:wrap;">
            <div class="dev-avatar-wrap" style="position:relative; width:92px; height:92px; min-width:92px;">
              <img src="assets/parinitha.jpg" alt="Parinitha.S - Website Developer &amp; AI Architect" 
                   style="width:92px; height:92px; border-radius:50%; object-fit:cover; border:3px solid #6366f1; box-shadow:0 4px 16px rgba(99, 102, 241, 0.28);"
                   onerror="this.onerror=null; this.src='assets/logo.png';">
              <div class="dev-status-indicator" title="Verified Creator &amp; Systems Architect"
                   style="position:absolute; bottom:2px; right:2px; background:#10b981; color:#fff; width:24px; height:24px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:900; border:2.5px solid #ffffff;">✓</div>
            </div>
            <div class="dev-info-col" style="flex:1; min-width:260px;">
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:6px;">
                <span style="font-size:0.75rem; font-weight:800; color:var(--primary); background:#eef2ff; border:1px solid #c7d2fe; padding:3px 10px; border-radius:999px; text-transform:uppercase; letter-spacing:0.5px;">
                  🏆 Lead Developer &amp; Systems Architect
                </span>
                <span style="font-size:0.75rem; font-weight:700; color:#10b981; background:#ecfdf5; border:1px solid #a7f3d0; padding:3px 10px; border-radius:999px;">
                  Official Campus Portal Creator
                </span>
              </div>
              <h3 class="dev-name" style="font-size:1.35rem; font-weight:900; color:var(--text-main); margin-bottom:6px;">Parinitha.S</h3>
              <p class="dev-bio" style="font-size:0.9rem; margin-bottom:12px; color:var(--text-muted); line-height:1.5;">
                Architected and developed the official <strong>Savitha Canteen</strong> platform. Engineered the digital token ordering flow, zero-queue counter dispatch, and machine learning demand prediction to streamline campus dining.
              </p>
              <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
                <a href="https://www.linkedin.com/in/pari-parinitha-s-6196b8354?utm_source=share_via&amp;utm_content=profile&amp;utm_medium=member_android" 
                   target="_blank" rel="noopener noreferrer" class="btn-linkedin"
                   style="display:inline-flex; align-items:center; gap:8px; background:#0a66c2; color:#ffffff; padding:8px 18px; border-radius:8px; font-size:0.88rem; font-weight:700; text-decoration:none; transition:all 0.2s; box-shadow:0 2px 8px rgba(10, 102, 194, 0.3);">
                  <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 10.9v8.37H9.2V10.9H6.46M7.83 6.64c-.87 0-1.58.7-1.58 1.58s.71 1.58 1.58 1.58 1.58-.71 1.58-1.58-.71-1.58-1.58-1.58Z"/>
                  </svg>
                  <span>Connect on LinkedIn</span>
                </a>
                <span style="font-size:0.82rem; color:var(--text-muted);">View Official Profile &amp; Research</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- =========================================================================
           CAMPUS REVIEWS SECTION (STUDENTS & FACULTY)
           ========================================================================= -->
      <section id="reviews-section" class="reviews-section" style="padding-top:16px; padding-bottom:30px;">
        <div class="section-badge-center">
          <span>⭐ Campus Dining Reviews</span>
        </div>
        <h2 class="section-main-heading">What Students &amp; Faculty Say</h2>
        <p class="section-sub-heading">Real dining experiences and feedback from the Savitha University campus community.</p>

        <!-- Clean Filter Chips for Reviews -->
        <div style="display:flex; justify-content:center; gap:8px; margin-bottom:16px; flex-wrap:wrap;">
          <button type="button" class="filter-chip active" onclick="filterReviews('all', this)" style="padding:6px 14px; border-radius:999px; border:1.5px solid #c7d2fe; background:#eef2ff; color:var(--primary); font-weight:700; font-size:0.82rem; cursor:pointer;">
            🌟 All Reviews
          </button>
          <button type="button" class="filter-chip" onclick="filterReviews('5', this)" style="padding:6px 14px; border-radius:999px; border:1px solid var(--border); background:#ffffff; color:var(--text-muted); font-weight:700; font-size:0.82rem; cursor:pointer;">
            ⭐⭐⭐⭐⭐ 5 Stars
          </button>
          <button type="button" class="filter-chip" onclick="filterReviews('4', this)" style="padding:6px 14px; border-radius:999px; border:1px solid var(--border); background:#ffffff; color:var(--text-muted); font-weight:700; font-size:0.82rem; cursor:pointer;">
            ⭐⭐⭐⭐ 4 Stars
          </button>
        </div>

        <!-- Dynamic Reviews Cards Grid -->
        <div class="reviews-cards-grid" id="reviews-cards-grid"
          style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:16px; margin-top:12px;">
          <!-- Rendered dynamically by app.js -->
        </div>

        <!-- Clean Action: Leave a Review -->
        <div style="text-align:center; margin-top:22px;">
          <button type="button" class="btn-hero-secondary" onclick="openAddReviewModal()"
            style="padding:10px 24px; font-size:0.9rem; display:inline-flex; align-items:center; gap:8px; border-radius:999px; font-weight:700;">
            <span>✍️</span> Leave Your Review
          </button>
        </div>
      </section>

    </div>

    <!-- =========================================================================
         2. SIMPLE & CLEAN LOGIN PORTAL (STUDENT & KITCHEN STAFF)
         ========================================================================= -->
    <div id="view-login" class="login-screen-wrap" style="display:none;">
      <div class="simple-login-card animate-pop" style="max-width:440px; margin:24px auto; background:#ffffff; border:1.5px solid var(--border); border-radius:18px; padding:28px 24px; box-shadow:0 10px 30px rgba(0, 0, 0, 0.06);">

        <!-- Back to About Navigation Button -->
        <div style="text-align:left; margin-bottom:14px;">
          <button type="button" class="btn-back-about" onclick="navigateToSection('about')"
            style="background:transparent; border:none; color:var(--text-muted); font-size:0.88rem; font-weight:700; cursor:pointer; display:inline-flex; align-items:center; gap:6px;">
            <span>←</span> Back to About Website
          </button>
        </div>

        <!-- Official Brand Header -->
        <div class="simple-login-header" style="text-align:center; margin-bottom:20px;">
          <img src="assets/logo.png" alt="Savitha Canteen Logo" class="login-brand-logo-img"
            style="width:58px; height:58px; border-radius:14px; margin-bottom:8px; box-shadow:0 4px 14px rgba(79, 70, 229, 0.25);">
          <h1 class="simple-login-title" style="font-size:1.45rem; font-weight:900; color:var(--text-main); margin-bottom:2px;">Savitha Canteen</h1>
          <p class="simple-login-subtitle" style="font-size:0.84rem; color:var(--text-muted); margin:0;">Official Campus Dining &amp; Kitchen Portal</p>
        </div>

        <!-- Role Selector Tabs: Student vs Kitchen Staff -->
        <div class="login-tabs-bar"
          style="display:flex; gap:8px; margin-bottom:18px; border-bottom:1.5px solid var(--border); padding-bottom:12px;">
          <button type="button" class="login-role-tab active" id="tab-login-student"
            onclick="switchLoginRoleTab('student')"
            style="flex:1; padding:10px 14px; border-radius:10px; border:none; font-weight:800; font-size:0.9rem; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:6px; background:#eef2ff; color:var(--primary); transition:all 0.2s;">
            <span>🎓</span> Student Login
          </button>
          <button type="button" class="login-role-tab" id="tab-login-worker" onclick="switchLoginRoleTab('worker')"
            style="flex:1; padding:10px 14px; border-radius:10px; border:none; font-weight:800; font-size:0.9rem; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:6px; background:#f1f5f9; color:var(--text-muted); transition:all 0.2s;">
            <span>👨‍🍳</span> Kitchen Staff
          </button>
        </div>

        <!-- Student Login Panel -->
        <div id="login-panel-student" class="login-panel">
          <form onsubmit="handlePortalStudentLogin(event)" novalidate class="simple-login-form">
            <div class="simple-input-group" style="margin-bottom:12px; text-align:left;">
              <label for="login-student-name" class="simple-label" style="display:block; font-size:0.82rem; font-weight:700; margin-bottom:4px; color:var(--text-main);">Your Full Name</label>
              <input type="text" id="login-student-name" class="simple-input" placeholder="e.g. Karthik Raj"
                autocomplete="name" required style="width:100%; padding:10px 12px; border:1.5px solid var(--border); border-radius:10px; font-size:0.92rem; outline:none; transition:border 0.2s;">
            </div>

            <div class="simple-input-group" style="margin-bottom:12px; text-align:left;">
              <label for="login-student-year" class="simple-label" style="display:block; font-size:0.82rem; font-weight:700; margin-bottom:4px; color:var(--text-main);">College Year / Department</label>
              <select id="login-student-year" class="simple-select" style="width:100%; padding:10px 12px; border:1.5px solid var(--border); border-radius:10px; font-size:0.92rem; outline:none; background:#ffffff;">
                <option value="1st Year" selected>1st Year</option>
                <option value="2nd Year">2nd Year</option>
                <option value="3rd Year">3rd Year</option>
                <option value="4th Year (Final Year)">4th Year (Final Year)</option>
                <option value="Faculty / Staff">Faculty / Staff</option>
              </select>
            </div>

            <div class="simple-input-group" style="margin-bottom:16px; text-align:left;">
              <label for="login-student-phone" class="simple-label" style="display:block; font-size:0.82rem; font-weight:700; margin-bottom:4px; color:var(--text-main);">Mobile Number (Optional)</label>
              <input type="tel" id="login-student-phone" class="simple-input" placeholder="e.g. 9840123456"
                maxlength="10" style="width:100%; padding:10px 12px; border:1.5px solid var(--border); border-radius:10px; font-size:0.92rem; outline:none;">
            </div>

            <button type="submit" class="btn-simple-submit btn-student-submit" id="btn-login-student-submit"
              style="width:100%; padding:13px; font-size:1rem; font-weight:800; background:linear-gradient(135deg, #4f46e5 0%, #6366f1 100%); color:#ffffff; border:none; border-radius:12px; cursor:pointer; box-shadow:0 4px 14px rgba(79, 70, 229, 0.3); display:flex; align-items:center; justify-content:center; gap:8px;">
              <span>🍽️</span> Login &amp; View Food Menu
            </button>
          </form>

          <div class="login-card-footer"
            style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-top:16px; border-top:1px solid var(--border); padding-top:12px;">
            <button type="button" class="btn-guest-link" onclick="navigateToSection('about')"
              style="background:transparent; border:none; color:var(--text-muted); font-size:0.84rem; cursor:pointer;">
              <span>←</span> About Website
            </button>
            <button type="button" class="btn-guest-link" id="link-toggle-staff" onclick="toggleStaffLoginForm()"
              style="background:transparent; border:none; color:var(--primary); font-size:0.84rem; font-weight:700; cursor:pointer;">
              <span>👨‍🍳</span> Kitchen Staff Login →
            </button>
          </div>
        </div>

        <!-- Kitchen Staff Login Panel -->
        <div id="login-panel-worker" class="login-panel" style="display:none;">
          <form onsubmit="handlePortalWorkerLogin(event)" novalidate class="simple-login-form">
            <div class="simple-input-group" style="margin-bottom:16px; text-align:left;">
              <label for="login-worker-password" class="simple-label" style="display:block; font-size:0.82rem; font-weight:700; margin-bottom:4px; color:var(--text-main);">Kitchen Staff Password</label>
              <div class="password-input-wrap">
                <input type="password" id="login-worker-password" class="simple-input"
                  placeholder="Enter staff password" autocomplete="current-password" required
                  style="width:100%; padding:10px 12px; border:1.5px solid var(--border); border-radius:10px; font-size:0.92rem; outline:none;">
              </div>
            </div>

            <button type="submit" class="btn-simple-submit btn-worker-submit"
              style="width:100%; padding:13px; font-size:1rem; font-weight:800; background:linear-gradient(135deg, #0284c7 0%, #0369a1 100%); color:#ffffff; border:none; border-radius:12px; cursor:pointer; box-shadow:0 4px 14px rgba(2, 132, 199, 0.3); display:flex; align-items:center; justify-content:center; gap:8px;">
              <span>🔓</span> Enter Kitchen Dashboard
            </button>
          </form>

          <div class="login-card-footer" style="text-align:center; margin-top:16px; border-top:1px solid var(--border); padding-top:12px;">
            <button type="button" class="btn-guest-link" onclick="switchLoginRoleTab('student')"
              style="background:transparent; border:none; color:var(--text-muted); font-size:0.84rem; cursor:pointer;">
              <span>←</span> Back to Student Login
            </button>
          </div>
        </div>

      </div>
    </div>
"""

html = html[:dev_spotlight_idx] + reviews_and_login_html + "\n    " + html[dev_card_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copyfile('index.html', 'frontend/index.html')
print("✓ Successfully restored reviews-section and view-login in index.html & frontend/index.html!")

# --- 2. UPDATE js/app.js FOR REVIEWS AND SMOOTH ANIMATIONS ---
with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 2.1 Fix loadFeedback to parse both { feedback: [...] } and [...]
old_load_feedback = """async function loadFeedback() {
  try {
    const res = await fetch(`${API_BASE}/api/feedback`);
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data)) {
        feedbackList = data;
      }
    }
  } catch (e) {
    try {
      const saved = localStorage.getItem("savitha_feedback");
      if (saved) feedbackList = JSON.parse(saved);
    } catch (err) {}
  }"""

new_load_feedback = """async function loadFeedback() {
  try {
    const res = await fetch(`${API_BASE}/api/feedback`);
    if (res.ok) {
      const data = await res.json();
      if (data && Array.isArray(data.feedback)) {
        feedbackList = data.feedback;
      } else if (Array.isArray(data)) {
        feedbackList = data;
      }
    }
  } catch (e) {
    try {
      const saved = localStorage.getItem("savitha_feedback");
      if (saved) feedbackList = JSON.parse(saved);
    } catch (err) {}
  }"""

if old_load_feedback in js:
    js = js.replace(old_load_feedback, new_load_feedback)
    print("✓ Fixed loadFeedback API response parsing in js/app.js")

# 2.2 Make renderFeedbackList render authentic cards with star rating badges
old_render_fb = """    return `
      <div class="fb-review-card" style="background:#ffffff; border:1.5px solid var(--border); border-radius:14px; padding:16px; box-shadow:var(--shadow-sm); display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div style="display:flex; align-items:center; gap:10px;">
              <div style="width:38px; height:38px; border-radius:50%; background:linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%); color:#ffffff; font-weight:800; font-size:1rem; display:flex; align-items:center; justify-content:center;">${initial}</div>
              <div>
                <div style="font-size:0.95rem; font-weight:800; color:var(--text-main); line-height:1.2;">${escapeHtml(fb.name)}</div>
                <div style="font-size:0.75rem; color:var(--text-muted);">${escapeHtml(fb.year || "Campus Community")}</div>
              </div>
            </div>
            <div style="color:#f59e0b; font-size:0.95rem; letter-spacing:1px;">${starsStr}</div>
          </div>
          <div style="font-size:0.86rem; color:var(--text-muted); line-height:1.5; margin-bottom:10px;">
            "${escapeHtml(fb.comment)}"
          </div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.75rem; color:var(--text-muted); border-top:1px solid #f1f5f9; padding-top:8px;">
          <span style="background:#f1f5f9; padding:2px 8px; border-radius:999px; font-weight:700;">${escapeHtml(fb.category || "General")}</span>
          <span>${escapeHtml(fb.date || "Verified Dining Review")}</span>
        </div>
      </div>
    `;"""

new_render_fb = """    const starsGold = "★".repeat(rating);
    const starsEmpty = "☆".repeat(5 - rating);

    return `
      <div class="fb-review-card animate-card" style="background:#ffffff; border:1.5px solid var(--border); border-radius:16px; padding:18px; box-shadow:0 2px 10px rgba(0,0,0,0.03); display:flex; flex-direction:column; justify-content:space-between; transition:transform 0.25s ease, box-shadow 0.25s ease;">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div style="display:flex; align-items:center; gap:10px;">
              <div style="width:40px; height:40px; border-radius:50%; background:linear-gradient(135deg, #6366f1 0%, #4338ca 100%); color:#ffffff; font-weight:800; font-size:1.05rem; display:flex; align-items:center; justify-content:center; box-shadow:0 2px 6px rgba(99, 102, 241, 0.25);">${initial}</div>
              <div>
                <div style="font-size:0.95rem; font-weight:800; color:var(--text-main); line-height:1.2;">${escapeHtml(fb.name)}</div>
                <div style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">${escapeHtml(fb.year || "Campus Community")}</div>
              </div>
            </div>
            <div style="display:flex; flex-direction:column; align-items:flex-end;">
              <div style="color:#f59e0b; font-size:1rem; letter-spacing:1px; line-height:1;">
                <span>${starsGold}</span><span style="color:#cbd5e1;">${starsEmpty}</span>
              </div>
              <span style="font-size:0.75rem; font-weight:800; color:#10b981; margin-top:2px;">${rating}.0 ★</span>
            </div>
          </div>
          <div style="font-size:0.88rem; color:var(--text-main); line-height:1.5; margin-bottom:12px; font-style:italic;">
            "${escapeHtml(fb.comment)}"
          </div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.75rem; color:var(--text-muted); border-top:1px solid #f1f5f9; padding-top:8px;">
          <span style="background:#eef2ff; color:var(--primary); padding:3px 10px; border-radius:999px; font-weight:700; border:1px solid #c7d2fe;">${escapeHtml(fb.category || "Food Quality")}</span>
          <span style="color:#64748b; font-weight:600;">✓ Verified Dining</span>
        </div>
      </div>
    `;"""

if old_render_fb in js:
    js = js.replace(old_render_fb, new_render_fb)
    print("✓ Updated renderFeedbackList card rendering")

# 2.3 Also call loadFeedback() in initUserAuth
init_auth_marker = """  renderUserAuthSlot();
  applyRoleVisibility();
  updateMyOrdersCount();
  // Open About the Website page first on website startup!
  performSwitchMode("about");"""

new_init_auth = """  renderUserAuthSlot();
  applyRoleVisibility();
  updateMyOrdersCount();
  loadFeedback();
  // Open About the Website page first on website startup!
  performSwitchMode("about");"""

if init_auth_marker in js:
    js = js.replace(init_auth_marker, new_init_auth)
    print("✓ Added loadFeedback() to initUserAuth()")

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
shutil.copyfile('js/app.js', 'frontend/js/app.js')
print("Successfully updated js/app.js and frontend/js/app.js!")

# --- 3. ADD MODERN ANIMATIONS TO css/style.css ---
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

animations_css = """
/* =========================================================================
   MODERN WEB ANIMATIONS & AUTHENTIC POLISH
   ========================================================================= */

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(14px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes animatePop {
  0% {
    opacity: 0;
    transform: scale(0.96) translateY(8px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes pulseGlow {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(99, 102, 241, 0);
  }
}

@keyframes pulseLive {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.35);
    opacity: 0.6;
  }
}

.animate-pop {
  animation: animatePop 0.28s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-card {
  animation: fadeInUp 0.35s ease-out forwards;
}

.dish-card {
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease !important;
}

.dish-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 14px 28px rgba(79, 70, 229, 0.12) !important;
}

.developer-spotlight-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 24px rgba(99, 102, 241, 0.12) !important;
}

.fb-review-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 22px rgba(0, 0, 0, 0.08) !important;
  border-color: #c7d2fe !important;
}

.status-indicator-live {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  animation: pulseLive 1.8s infinite;
}

.btn-hero-primary {
  transition: transform 0.2s, box-shadow 0.2s !important;
}

.btn-hero-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(79, 70, 229, 0.35) !important;
}
"""

if '@keyframes animatePop' not in css:
    css = css + "\n" + animations_css
    with open('css/style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    shutil.copyfile('css/style.css', 'frontend/css/style.css')
    print("✓ Appended modern animations to css/style.css & frontend/css/style.css")
else:
    print("Animations already present in css/style.css")

print("\nRestoration and animation updates complete!")
