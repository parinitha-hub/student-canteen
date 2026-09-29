import os
import shutil
import re

print("Starting apply_login_guard_and_reviews...")

# =========================================================================
# 1. UPDATE backend/app.py (Seed feedback with diverse 4-star & 5-star reviews)
# =========================================================================
with open('backend/app.py', 'r', encoding='utf-8') as f:
    backend_code = f.read()

old_seed_snippet = '''        seed_feedback = [
            (
                "Sneha Reddy",
                "2nd Year ECE",
                5,
                "Website Experience",
                "Brilliant website! The zero-wait token system saves so much time between lectures. Kudos to developer Parinitha.S for creating this!",
                "2026-09-20",
                int(datetime.now().timestamp() * 1000) - 172800000
            ),
            (
                "Aarav Menon",
                "3rd Year CSE",
                5,
                "Food Quality",
                "The Veg Biryani and Paneer Thali taste authentic and fresh. Hot food right when token is called!",
                "2026-09-21",
                int(datetime.now().timestamp() * 1000) - 86400000
            ),
            (
                "Karthik Raj",
                "Final Year Mech",
                5,
                "Service Speed",
                "Token pickup is lightning fast! The AI portions ensure items don't run out during peak rush hours.",
                "2026-09-22",
                int(datetime.now().timestamp() * 1000) - 14400000
            )
        ]'''

new_seed_snippet = '''        seed_feedback = [
            (
                "Sneha Reddy",
                "2nd Year ECE",
                5,
                "Website Experience",
                "Brilliant website! The zero-wait token system saves so much time between lectures. Kudos to developer Parinitha.S for creating this!",
                "2026-09-24",
                int(datetime.now().timestamp() * 1000) - 3600000
            ),
            (
                "Divya Krishnan",
                "Final Year IT",
                4,
                "Website UI",
                "Very clean, modern, and fast website! Ordering food takes under 15 seconds. The real-time token tracking makes lunchtime so convenient.",
                "2026-09-24",
                int(datetime.now().timestamp() * 1000) - 7200000
            ),
            (
                "Aarav Menon",
                "3rd Year CSE",
                5,
                "Food Quality",
                "The Veg Biryani and Paneer Thali taste authentic and fresh. Hot food right when token is called at the counter!",
                "2026-09-23",
                int(datetime.now().timestamp() * 1000) - 86400000
            ),
            (
                "Karthik Raj",
                "Final Year Mech",
                5,
                "Service Speed",
                "Zero-wait pickup is lightning fast! The AI portions ensure popular items do not run out during peak rush hours.",
                "2026-09-23",
                int(datetime.now().timestamp() * 1000) - 90000000
            ),
            (
                "Rithanya S",
                "2nd Year AI & DS",
                4,
                "AI & Innovation",
                "Love how the AI demand predictor keeps meals hot and fresh with zero food wastage. Beautiful responsive mobile design!",
                "2026-09-22",
                int(datetime.now().timestamp() * 1000) - 172800000
            ),
            (
                "Manoj Kumar",
                "3rd Year EEE",
                5,
                "Website Experience",
                "Best cafeteria platform! I order directly from the lecture hall, walk in, show my token, and grab my fresh lunch without lines.",
                "2026-09-22",
                int(datetime.now().timestamp() * 1000) - 180000000
            ),
            (
                "Pooja Patel",
                "1st Year Civil",
                4,
                "Service Speed",
                "Super easy to use even for freshers. The instant token notification and live kitchen status are fantastic.",
                "2026-09-21",
                int(datetime.now().timestamp() * 1000) - 250000000
            ),
            (
                "Sanjay Verma",
                "Faculty - CSE Dept",
                5,
                "Website Experience",
                "Outstanding work by Parinitha.S. Modernizes campus dining, streamlines cafeteria operations, and eliminates crowded counter queues.",
                "2026-09-20",
                int(datetime.now().timestamp() * 1000) - 340000000
            )
        ]'''

if old_seed_snippet in backend_code:
    backend_code = backend_code.replace(old_seed_snippet, new_seed_snippet, 1)
    with open('backend/app.py', 'w', encoding='utf-8') as f:
        f.write(backend_code)
    print("Updated backend/app.py seed feedback successfully!")

# =========================================================================
# 2. UPDATE index.html (Add Reviews Showcase & Add Review Modal)
# =========================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read().replace('\r\n', '\n')

# 2.1 Update Hero button in about section to use handleMenuAccessRequest
old_hero_btn = '<button type="button" class="btn-hero-primary" id="about-hero-primary-btn" onclick="navigateToSection(\'order\')">'
new_hero_btn = '<button type="button" class="btn-hero-primary" id="about-hero-primary-btn" onclick="handleMenuAccessRequest()">'
if old_hero_btn in html:
    html = html.replace(old_hero_btn, new_hero_btn, 1)

# 2.2 Add Reviews Showcase section inside view-about after the developer card
old_about_end = """        <!-- Clean Developer Attribution Card -->
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

reviews_section_html = """        <!-- Clean Developer Attribution Card -->
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

      <!-- =========================================================================
           WEBSITE REVIEWS & RATINGS (4-STAR & 5-STAR HIGHLIGHTS IN DIFFERENT WAYS)
           ========================================================================= -->
      <section id="reviews-section" class="reviews-section" style="padding-top:10px; padding-bottom:28px;">
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

    </div>"""

assert old_about_end in html, "Failed to find old_about_end in index.html"
html = html.replace(old_about_end, reviews_section_html, 1)

# 2.3 Add Add Review Modal before my-orders-modal
add_review_modal_html = """  <!-- Add Website Review Modal (Rate 4 or 5 stars) -->
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

  <!-- My Orders Modal (View all placed orders & tokens) -->"""

old_orders_modal_start = "  <!-- My Orders Modal (View all placed orders & tokens) -->"
assert old_orders_modal_start in html, "Failed to find old_orders_modal_start in index.html"
html = html.replace(old_orders_modal_start, add_review_modal_html, 1)

# Save index.html and sync
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html.replace('\n', '\r\n'))

shutil.copyfile('index.html', 'frontend/index.html')
print("Successfully updated index.html and frontend/index.html!")

# =========================================================================
# 3. UPDATE css/style.css (Add Reviews Showcase CSS)
# =========================================================================
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read().replace('\r\n', '\n')

reviews_css = """
/* ==========================================================================
   Reviews Showcase & Rating Filter Chips (4-Star & 5-Star Presentation)
   ========================================================================== */
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
    css = css + reviews_css

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css.replace('\n', '\r\n'))

shutil.copyfile('css/style.css', 'frontend/css/style.css')
print("Successfully updated css/style.css and frontend/css/style.css!")

print("Step 1-3 finished.")
