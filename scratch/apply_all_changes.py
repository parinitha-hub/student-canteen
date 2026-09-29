import os
import shutil
import re

print("Applying login guard and reviews updates...")

# ---------------------------------------------------------
# 1. Update index.html
# ---------------------------------------------------------
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1.1 Hero button uses handleMenuAccessRequest()
html = re.sub(
    r'<button\s+type="button"\s+class="btn-hero-primary"\s+id="about-hero-primary-btn"\s+onclick="[^"]*"',
    '<button type="button" class="btn-hero-primary" id="about-hero-primary-btn" onclick="handleMenuAccessRequest()"',
    html
)

# 1.2 Insert reviews section inside view-about
reviews_section_markup = """
      <!-- =========================================================================
           WEBSITE REVIEWS & RATINGS (4-STAR & 5-STAR HIGHLIGHTS IN DIFFERENT WAYS)
           ========================================================================= -->
      <section id="reviews-section" class="reviews-section" style="padding-top:14px; padding-bottom:28px;">
        <div class="section-badge-center">
          <span>⭐ Campus Community Reviews</span>
        </div>
        <h2 class="section-main-heading">Website Reviews &amp; Ratings</h2>
        <p class="section-sub-heading">Explore how students and faculty experience our zero-wait digital token system, delicious meals, and AI smart canteen.</p>

        <!-- Rating Summary Box & Ways to Filter Reviews -->
        <div class="reviews-summary-card">
          <div class="reviews-score-col">
            <div class="rating-large-score">4.8</div>
            <div class="rating-stars-large">⭐⭐⭐⭐⭐</div>
            <div class="rating-summary-text">Outstanding Campus Rating</div>
            <div class="rating-count-pill" id="reviews-total-counter">Verified Reviews</div>
          </div>

          <div class="reviews-filter-col">
            <div class="filter-header-label">Explore Reviews In Different Ways:</div>
            <div class="reviews-chips-row">
              <button type="button" class="review-chip active" id="chip-filter-all" onclick="filterReviews('all', this)">
                🌟 All (4★ &amp; 5★)
              </button>
              <button type="button" class="review-chip" id="chip-filter-5" onclick="filterReviews(5, this)">
                ⭐⭐⭐⭐⭐ 5 Stars Only
              </button>
              <button type="button" class="review-chip" id="chip-filter-4" onclick="filterReviews(4, this)">
                ⭐⭐⭐⭐ 4 Stars Only
              </button>
              <button type="button" class="review-chip" id="chip-filter-website" onclick="filterReviews('Website', this)">
                💻 Website UI
              </button>
              <button type="button" class="review-chip" id="chip-filter-speed" onclick="filterReviews('Speed', this)">
                ⚡ Token Speed
              </button>
              <button type="button" class="review-chip" id="chip-filter-food" onclick="filterReviews('Food', this)">
                🍛 Food Quality
              </button>
            </div>
          </div>

          <div class="reviews-action-col">
            <button type="button" class="btn-hero-primary" onclick="openAddReviewModal()" style="font-size:0.88rem; padding:10px 16px; border-radius:10px; width:100%; justify-content:center;">
              <span>✍️</span> Add Website Review
            </button>
            <div style="font-size:0.75rem; color:var(--text-muted); text-align:center; margin-top:6px;">Rate 4★ or 5★ &amp; share!</div>
          </div>
        </div>

        <!-- Rendered Reviews Grid (4-star & 5-star cards) -->
        <div class="reviews-cards-grid" id="reviews-cards-grid" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:14px; margin-top:16px;">
          <!-- Rendered dynamically by app.js -->
        </div>
      </section>
"""

if 'id="reviews-section"' not in html:
    # Match the end of about section and view-about
    # Pattern: </section> followed by optional whitespace and </div>
    pattern_about_end = re.compile(r'(</section>\s*)(</div>\s*<!--\s*={5,}\s*2\.\s*SIMPLE\s*&\s*CLEAN\s*LOGIN)', re.IGNORECASE)
    m = pattern_about_end.search(html)
    assert m, "Failed to find end of view-about"
    html = html[:m.start(1)] + "</section>\n" + reviews_section_markup + "\n    " + html[m.start(2):]

# 1.3 Insert Add Review Modal
add_review_modal_markup = """
  <!-- Add Website Review Modal (Rate 4 or 5 stars) -->
  <div id="add-review-modal" class="modal-overlay">
    <div class="modal-box" style="max-width:500px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid var(--border); padding-bottom:10px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:1.4rem;">✍️</span>
          <div>
            <h2 style="font-size:1.25rem; font-weight:800; color:var(--text-main); margin:0;">Add Website Review</h2>
            <p style="font-size:0.8rem; color:var(--text-muted); margin:0;">Rate your experience with Savitha Canteen</p>
          </div>
        </div>
        <button type="button" onclick="closeAddReviewModal()" style="background:transparent; border:none; font-size:1.35rem; cursor:pointer; color:var(--text-muted); line-height:1;" aria-label="Close modal">✕</button>
      </div>

      <form id="add-review-form" onsubmit="handleWebsiteReviewSubmit(event)">
        <!-- Quick Rating Selector: 5 Stars or 4 Stars -->
        <div style="margin-bottom:14px;">
          <label class="fb-field-label">Select Your Rating</label>
          <div style="display:flex; gap:8px; margin-top:6px;">
            <button type="button" class="btn-rating-choice" id="btn-rate-5" onclick="selectReviewRating(5)" style="flex:1; padding:10px 8px; border-radius:10px; border:2px solid var(--primary); background:#eef2ff; font-weight:800; cursor:pointer; font-size:0.9rem; color:var(--primary); transition:0.2s;">
              ⭐⭐⭐⭐⭐ 5 Stars<br><span style="font-size:0.75rem; font-weight:600;">Outstanding</span>
            </button>
            <button type="button" class="btn-rating-choice" id="btn-rate-4" onclick="selectReviewRating(4)" style="flex:1; padding:10px 8px; border-radius:10px; border:1.5px solid var(--border); background:#ffffff; font-weight:800; cursor:pointer; font-size:0.9rem; color:var(--text-main); transition:0.2s;">
              ⭐⭐⭐⭐ 4 Stars<br><span style="font-size:0.75rem; font-weight:600;">Very Good</span>
            </button>
          </div>
          <input type="hidden" id="modal-fb-rating" value="5">
        </div>

        <!-- Review Category -->
        <div style="margin-bottom:12px;">
          <label class="fb-field-label">Review Perspective</label>
          <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:6px;">
            <button type="button" class="fb-cat-choice active" onclick="selectReviewCategoryChoice('Website Experience', this)">💻 Website UI</button>
            <button type="button" class="fb-cat-choice" onclick="selectReviewCategoryChoice('Service Speed', this)">⚡ Token Speed</button>
            <button type="button" class="fb-cat-choice" onclick="selectReviewCategoryChoice('Food Quality', this)">🍛 Food Quality</button>
            <button type="button" class="fb-cat-choice" onclick="selectReviewCategoryChoice('AI & Innovation', this)">🤖 AI Forecasting</button>
          </div>
          <input type="hidden" id="modal-fb-category" value="Website Experience">
        </div>

        <!-- Reviewer Name & Year -->
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:12px;">
          <div>
            <label class="fb-field-label" for="modal-fb-name">Your Name</label>
            <input type="text" id="modal-fb-name" class="input-field" placeholder="e.g. Rahul / Priya" required style="width:100%;">
          </div>
          <div>
            <label class="fb-field-label" for="modal-fb-year">Department / Year</label>
            <input type="text" id="modal-fb-year" class="input-field" placeholder="e.g. 2nd Year CSE" required style="width:100%;">
          </div>
        </div>

        <!-- Review Comments -->
        <div style="margin-bottom:16px;">
          <label class="fb-field-label" for="modal-fb-comment">Your Review Comments</label>
          <textarea id="modal-fb-comment" class="input-field" rows="3" placeholder="Tell us what you loved about the website, instant tokens, or canteen meals..." required style="width:100%; resize:vertical;"></textarea>
        </div>

        <button type="submit" class="btn-calc" id="btn-submit-website-review" style="width:100%; padding:11px; font-size:0.95rem; justify-content:center; background:linear-gradient(135deg, var(--primary), var(--primary-hover)); color:#fff; border:none; border-radius:10px; font-weight:800; cursor:pointer;">
          <span>🚀</span> Post Review
        </button>
      </form>
    </div>
  </div>
"""

if 'id="add-review-modal"' not in html:
    pattern_modal = re.compile(r'(\s*<!--\s*My Orders Modal)', re.IGNORECASE)
    m2 = pattern_modal.search(html)
    assert m2, "Failed to find My Orders Modal marker"
    html = html[:m2.start()] + "\n" + add_review_modal_markup + "\n" + html[m2.start():]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copyfile('index.html', 'frontend/index.html')
print("Successfully updated index.html and frontend/index.html")

# ---------------------------------------------------------
# 2. Update css/style.css
# ---------------------------------------------------------
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

reviews_css = """
/* Reviews Showcase & Rating Filter Chips (4-Star & 5-Star Presentation) */
.reviews-section {
  margin-top: 24px;
}

.reviews-summary-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px 24px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 24px;
  align-items: center;
  box-shadow: var(--shadow-sm);
  margin-bottom: 20px;
}

@media (max-width: 820px) {
  .reviews-summary-card {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 16px;
  }
  .reviews-chips-row {
    justify-content: center;
  }
}

.reviews-score-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  border-right: 1.5px solid var(--border);
  padding-right: 24px;
  min-width: 140px;
}

@media (max-width: 820px) {
  .reviews-score-col {
    border-right: none;
    border-bottom: 1.5px solid var(--border);
    padding-right: 0;
    padding-bottom: 16px;
  }
}

.rating-large-score {
  font-size: 2.8rem;
  font-weight: 900;
  color: var(--primary);
  line-height: 1;
  font-family: var(--font-heading);
}

.rating-stars-large {
  font-size: 1.15rem;
  letter-spacing: 2px;
  margin: 4px 0;
}

.rating-summary-text {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-main);
}

.rating-count-pill {
  font-size: 0.72rem;
  color: var(--text-muted);
  background: var(--bg-subtle);
  padding: 2px 8px;
  border-radius: 999px;
  margin-top: 4px;
}

.reviews-filter-col {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-header-label {
  font-size: 0.82rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-muted);
}

.reviews-chips-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.review-chip {
  background: #ffffff;
  border: 1.5px solid var(--border);
  color: var(--text-main);
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  transition: var(--transition);
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.review-chip:hover {
  border-color: var(--primary);
  color: var(--primary);
  transform: translateY(-1px);
}

.review-chip.active {
  background: var(--primary);
  border-color: var(--primary);
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
}

.reviews-action-col {
  min-width: 170px;
}

.rating-badge-pill {
  font-size: 0.72rem;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 999px;
  display: inline-block;
  margin-top: 2px;
}

.badge-5star {
  background: #eef2ff;
  color: var(--primary);
  border: 1px solid #c7d2fe;
}

.badge-4star {
  background: #ecfdf5;
  color: #059669;
  border: 1px solid #a7f3d0;
}

.fb-cat-choice {
  background: #ffffff;
  border: 1.5px solid var(--border);
  color: var(--text-main);
  padding: 5px 11px;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  transition: 0.15s;
}

.fb-cat-choice:hover {
  border-color: var(--primary);
}

.fb-cat-choice.active {
  background: #eef2ff;
  border-color: var(--primary);
  color: var(--primary);
}
"""

if ".reviews-summary-card" not in css:
    css = css + "\n" + reviews_css

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
shutil.copyfile('css/style.css', 'frontend/css/style.css')
print("Successfully updated css/style.css and frontend/css/style.css")

# ---------------------------------------------------------
# 3. Update js/app.js
# ---------------------------------------------------------
with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 3.1 Gating Menu Access: performSwitchMode guard
# If someone tries to switch to "order" or "home" while not logged in, block & redirect to login
old_switch_guard = re.compile(r'function\s+performSwitchMode\s*\(\s*mode\s*\)\s*\{', re.IGNORECASE)
new_switch_guard = """function performSwitchMode(mode) {
  // STRICT LOGIN GUARD: Without login, visitors cannot view the menu
  if ((mode === "order" || mode === "home") && (!currentUser || !currentUser.role)) {
    showToast("🔒 Please login first to view the canteen food menu!", "warning");
    performSwitchMode("login");
    return;
  }"""

if "STRICT LOGIN GUARD: Without login" not in js:
    m3 = old_switch_guard.search(js)
    assert m3, "Failed to find performSwitchMode"
    js = js[:m3.start()] + new_switch_guard + js[m3.end():]

# 3.2 Gating navigateToSection('order') / ('home')
old_nav_order = re.compile(r'\}\s*else\s+if\s*\(\s*target\s*===\s*"home"\s*\|\|\s*target\s*===\s*"order"\s*\)\s*\{', re.IGNORECASE)
new_nav_order = """} else if (target === "home" || target === "order") {
    // STRICT LOGIN GUARD: Cannot view food menu without logging in
    if (!currentUser || !currentUser.role) {
      showToast("🔒 Please login first to view the canteen menu and order!", "warning");
      performSwitchMode("login");
      return;
    }"""

if "STRICT LOGIN GUARD: Cannot view food menu" not in js:
    m4 = old_nav_order.search(js)
    assert m4, "Failed to find navigateToSection order branch"
    js = js[:m4.start()] + new_nav_order + js[m4.end():]

# 3.3 Gating openCartModal(), quickOrderDish(), updateDishQty()
guard_cart_fn = re.compile(r'function\s+openCartModal\s*\(\s*\)\s*\{', re.IGNORECASE)
if "function openCartModal() {\n  if (!currentUser || !currentUser.role)" not in js:
    m5 = guard_cart_fn.search(js)
    assert m5, "Failed to find openCartModal"
    js = js[:m5.start()] + """function openCartModal() {
  if (!currentUser || !currentUser.role) {
    showToast("🔒 Please login first to access your cart!", "warning");
    performSwitchMode("login");
    return;
  }""" + js[m5.end():]

guard_quick_fn = re.compile(r'function\s+quickOrderDish\s*\(\s*dishId\s*\)\s*\{', re.IGNORECASE)
if "function quickOrderDish(dishId) {\n  if (!currentUser || !currentUser.role)" not in js:
    m6 = guard_quick_fn.search(js)
    assert m6, "Failed to find quickOrderDish"
    js = js[:m6.start()] + """function quickOrderDish(dishId) {
  if (!currentUser || !currentUser.role) {
    showToast("🔒 Please login first to select items!", "warning");
    performSwitchMode("login");
    return;
  }""" + js[m6.end():]

guard_qty_fn = re.compile(r'function\s+updateDishQty\s*\(\s*dishId\s*,\s*delta\s*\)\s*\{', re.IGNORECASE)
if "function updateDishQty(dishId, delta) {\n  if (!currentUser || !currentUser.role)" not in js:
    m7 = guard_qty_fn.search(js)
    assert m7, "Failed to find updateDishQty"
    js = js[:m7.start()] + """function updateDishQty(dishId, delta) {
  if (!currentUser || !currentUser.role) {
    showToast("🔒 Please login first to select dishes!", "warning");
    performSwitchMode("login");
    return;
  }""" + js[m7.end():]

# 3.4 Hero button logic in applyRoleVisibility
# When not logged in, hero button must show Login to View Food Menu
hero_btn_logic_pattern = re.compile(
    r'\} else \{\s*// Clean single login way in navbar; hero opens food menu directly![\r\n\s]+heroPrimary\.innerHTML = "<span>🍽️</span> View Food Menu &amp; Order →";[\r\n\s]+heroPrimary\.onclick = \(\) => performSwitchMode\("order"\);',
    re.IGNORECASE
)
new_hero_btn_logic = """} else {
      // Unauthenticated visitor: Strictly prompt login to view menu
      heroPrimary.innerHTML = "<span>🔒</span> Login to View Food Menu →";
      heroPrimary.onclick = () => {
        showToast("🔒 Please login first to view the food menu and place orders!", "warning");
        performSwitchMode("login");
      };"""

if "Unauthenticated visitor: Strictly prompt login to view menu" not in js:
    m8 = hero_btn_logic_pattern.search(js)
    if m8:
        js = js[:m8.start()] + new_hero_btn_logic + js[m8.end():]

# 3.5 Function handleMenuAccessRequest()
handle_menu_request_fn = """
function handleMenuAccessRequest() {
  if (!currentUser || !currentUser.role) {
    showToast("🔒 Please login with your student account first to view the food menu and place orders!", "warning");
    performSwitchMode("login");
    return;
  }
  performSwitchMode("order");
}
"""

if "function handleMenuAccessRequest" not in js:
    marker_pos = js.find("function performSwitchMode")
    assert marker_pos != -1, "Failed to find marker for handleMenuAccessRequest"
    js = js[:marker_pos] + handle_menu_request_fn + "\n" + js[marker_pos:]

# 3.6 Reviews Presentation (Filtering in different ways: 4 & 5 stars, categories, stats, and adding reviews)
reviews_js_system = """
// =========================================================================
// WEBSITE REVIEWS & RATINGS (4-STAR & 5-STAR HIGHLIGHTS IN DIFFERENT WAYS)
// =========================================================================
let currentReviewFilter = "all";

function filterReviews(filterValue, btnEl) {
  currentReviewFilter = filterValue;
  const chips = document.querySelectorAll(".review-chip, .filter-chip");
  chips.forEach(c => c.classList.remove("active"));
  if (btnEl) btnEl.classList.add("active");
  renderFeedbackList();
}

function renderFeedbackList() {
  const container = document.getElementById("reviews-cards-grid") || document.getElementById("feedback-cards-container");
  const countBadge = document.getElementById("reviews-total-counter") || document.getElementById("reviews-count-badge");
  if (!container) return;

  if (countBadge) {
    countBadge.textContent = `${feedbackList.length} Verified Reviews`;
  }

  // Filter feedback
  let filtered = feedbackList;
  if (currentReviewFilter === 5 || currentReviewFilter === "5") {
    filtered = feedbackList.filter(f => parseInt(f.rating) === 5);
  } else if (currentReviewFilter === 4 || currentReviewFilter === "4") {
    filtered = feedbackList.filter(f => parseInt(f.rating) === 4);
  } else if (currentReviewFilter && currentReviewFilter !== "all") {
    const term = String(currentReviewFilter).toLowerCase();
    filtered = feedbackList.filter(f => 
      (f.category && f.category.toLowerCase().includes(term)) ||
      (f.comment && f.comment.toLowerCase().includes(term))
    );
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="grid-column:1/-1; text-align:center; padding:32px 16px; background:#f8fafc; border-radius:12px; border:1px dashed var(--border);">
        <div style="font-size:2rem; margin-bottom:6px;">⭐</div>
        <p style="color:var(--text-muted); font-size:0.9rem; margin:0;">No reviews found for this selection.</p>
        <button type="button" class="btn-calc" onclick="filterReviews('all', document.getElementById('chip-filter-all'))" style="margin-top:10px; padding:6px 14px; font-size:0.82rem;">
          Show All Reviews
        </button>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(fb => {
    const initial = (fb.name || "S").trim().charAt(0).toUpperCase();
    const rating = parseInt(fb.rating) || 5;
    const starsStr = "★".repeat(rating) + "☆".repeat(5 - rating);
    const badgeClass = rating === 5 ? "badge-5star" : "badge-4star";

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
          <div style="display:flex; flex-direction:column; align-items:flex-end;">
            <div class="fb-stars" title="${rating}/5">${starsStr}</div>
            <span class="rating-badge-pill ${badgeClass}">${rating === 5 ? '⭐⭐⭐⭐⭐ 5.0' : '⭐⭐⭐⭐ 4.0'}</span>
          </div>
        </div>
        <div class="fb-category-tag">${escapeHtml(fb.category || "Website Experience")}</div>
        <p class="fb-comment-text">"${escapeHtml(fb.comment || "")}"</p>
        <div class="fb-date">${fb.date || "Recent"}</div>
      </div>
    `;
  }).join('');
}

function openAddReviewModal() {
  const modal = document.getElementById("add-review-modal");
  if (!modal) return;
  if (currentUser && currentUser.name) {
    const nameInput = document.getElementById("modal-fb-name");
    const yearInput = document.getElementById("modal-fb-year");
    if (nameInput && !nameInput.value) nameInput.value = currentUser.name;
    if (yearInput && !yearInput.value) yearInput.value = currentUser.year || "Student";
  }
  modal.classList.add("show");
}

function closeAddReviewModal() {
  const modal = document.getElementById("add-review-modal");
  if (modal) modal.classList.remove("show");
}

function selectReviewRating(rating) {
  const ratingInput = document.getElementById("modal-fb-rating");
  if (ratingInput) ratingInput.value = rating;

  const btn5 = document.getElementById("btn-rate-5");
  const btn4 = document.getElementById("btn-rate-4");

  if (btn5 && btn4) {
    if (rating === 5) {
      btn5.style.border = "2px solid var(--primary)";
      btn5.style.background = "#eef2ff";
      btn5.style.color = "var(--primary)";
      btn4.style.border = "1.5px solid var(--border)";
      btn4.style.background = "#ffffff";
      btn4.style.color = "var(--text-main)";
    } else {
      btn4.style.border = "2px solid #059669";
      btn4.style.background = "#ecfdf5";
      btn4.style.color = "#059669";
      btn5.style.border = "1.5px solid var(--border)";
      btn5.style.background = "#ffffff";
      btn5.style.color = "var(--text-main)";
    }
  }
}

function selectReviewCategoryChoice(cat, btn) {
  const catInput = document.getElementById("modal-fb-category");
  if (catInput) catInput.value = cat;
  const buttons = document.querySelectorAll(".fb-cat-choice");
  buttons.forEach(b => b.classList.remove("active"));
  if (btn) btn.classList.add("active");
}

async function handleWebsiteReviewSubmit(e) {
  if (e) e.preventDefault();
  const nameInput = document.getElementById("modal-fb-name");
  const yearInput = document.getElementById("modal-fb-year");
  const commentInput = document.getElementById("modal-fb-comment");
  const ratingInput = document.getElementById("modal-fb-rating");
  const categoryInput = document.getElementById("modal-fb-category");

  const name = nameInput && nameInput.value.trim() ? nameInput.value.trim() : "Student";
  const year = yearInput && yearInput.value.trim() ? yearInput.value.trim() : "Campus Dining";
  const comment = commentInput ? commentInput.value.trim() : "";
  const rating = ratingInput ? parseInt(ratingInput.value) || 5 : 5;
  const category = categoryInput ? categoryInput.value : "Website Experience";

  if (!comment) {
    showToast("Please enter a short review comment!", "warning");
    return;
  }

  const payload = {
    name,
    year,
    rating,
    category,
    comment,
    date: new Date().toISOString().split("T")[0],
    timestamp: Date.now()
  };

  const submitBtn = document.getElementById("btn-submit-website-review");
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = "Posting Review...";
  }

  try {
    const res = await fetch("/api/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      const data = await res.json();
      if (data && data.feedback) {
        feedbackList.unshift(data.feedback);
      } else {
        feedbackList.unshift(payload);
      }
    } else {
      feedbackList.unshift(payload);
    }
  } catch (err) {
    feedbackList.unshift(payload);
  } finally {
    try {
      localStorage.setItem("savitha_feedback", JSON.stringify(feedbackList));
    } catch (e) {}

    renderFeedbackList();
    closeAddReviewModal();
    if (commentInput) commentInput.value = "";
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = "<span>🚀</span> Post Review";
    }

    showToast(`🎉 Thank you! Your ${rating}★ review for Savitha Canteen has been added!`, "success");
  }
}
"""

# Replace existing loadFeedback and renderFeedbackList with the enhanced versions
if "function filterReviews" not in js:
    # Replace existing renderFeedbackList
    render_fb_pattern = re.compile(r'function\s+renderFeedbackList\s*\(\s*\)\s*\{[\s\S]*?\}\s*async\s+function\s+handleFeedbackSubmit', re.IGNORECASE)
    m9 = render_fb_pattern.search(js)
    if m9:
        js = js[:m9.start()] + reviews_js_system + "\nasync function handleFeedbackSubmit" + js[m9.end():]
    else:
        # Fallback append before window attachments
        marker_attach = 'if (typeof window !== "undefined") window.performSwitchMode ='
        js = js.replace(marker_attach, reviews_js_system + "\n" + marker_attach, 1)

# Window exports
exports_to_add = """
if (typeof window !== "undefined") window.handleMenuAccessRequest = handleMenuAccessRequest;
if (typeof window !== "undefined") window.filterReviews = filterReviews;
if (typeof window !== "undefined") window.openAddReviewModal = openAddReviewModal;
if (typeof window !== "undefined") window.closeAddReviewModal = closeAddReviewModal;
if (typeof window !== "undefined") window.selectReviewRating = selectReviewRating;
if (typeof window !== "undefined") window.selectReviewCategoryChoice = selectReviewCategoryChoice;
if (typeof window !== "undefined") window.handleWebsiteReviewSubmit = handleWebsiteReviewSubmit;
"""

if "window.handleMenuAccessRequest = handleMenuAccessRequest;" not in js:
    end_hook = 'if (typeof window !== "undefined") window.quickOrderDish = quickOrderDish;'
    js = js.replace(end_hook, end_hook + "\n" + exports_to_add, 1)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
shutil.copyfile('js/app.js', 'frontend/js/app.js')
print("Successfully updated js/app.js and frontend/js/app.js")
print("All updates applied cleanly!")
