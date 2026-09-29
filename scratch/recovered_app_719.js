import re
import os
import shutil

def update_index_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove orphaned active-order-actions block and extra closing </div> that prematurely closed #view-order
    pattern_orphan = r'\s*<div class="active-order-actions">[\s\S]*?</div>\s*</div>\s*(?=\s*<!-- Category Filter Bar -->)'
    match_orphan = re.search(pattern_orphan, content)
    if match_orphan:
        content = re.sub(pattern_orphan, '\n\n', content, count=1)
        print(f"[{filepath}] Successfully removed orphaned active-order-actions and fixed view-order nesting.")
    else:
        print(f"[{filepath}] WARNING: could not match orphan active-order-actions with regex, checking alternative.")

    # 2. Update Kitchen Staff Panel to make password not visible (clean placeholder, remove hint, remove 1-click login)
    old_worker_panel = re.search(r'<div id="login-panel-worker" class="login-panel" style="display:none; margin-top:8px;">[\s\S]*?</div>\s*</div>\s*(?=\s*<!-- =========================================================================\s*3\. SIMPLE FOOD ORDERING)', content)
    if old_worker_panel:
        new_worker_panel = '''<div id="login-panel-worker" class="login-panel" style="display:none; margin-top:8px;">
          <form onsubmit="handlePortalWorkerLogin(event)" novalidate class="simple-login-form">
            <div class="simple-input-group">
              <label for="login-worker-password" class="simple-label">Kitchen Staff Password</label>
              <div class="password-input-wrap">
                <input type="password" id="login-worker-password" class="simple-input" value="" placeholder="Enter staff password" autocomplete="current-password" required>
              </div>
            </div>

            <button type="submit" class="btn-simple-submit btn-worker-submit" style="margin-top:12px;">
              <span>🔓</span> Enter Kitchen Dashboard
            </button>
          </form>

          <div class="login-card-footer" style="text-align:center; margin-top:14px;">
            <button type="button" class="btn-guest-link" onclick="switchLoginRoleTab('student')" style="color:var(--text-muted); font-size:0.82rem;">
              <span>←</span> Back to Student Login
            </button>
          </div>
        </div>
      </div>'''
        content = content[:old_worker_panel.start()] + new_worker_panel + content[old_worker_panel.end():]
        print(f"[{filepath}] Successfully updated Kitchen Staff login form (password hidden).")
    else:
        print(f"[{filepath}] WARNING: could not match old_worker_panel")

    # 3. Simplify Add Review modal: rating can be chosen as user wishes, no forced example strings or e.g. placeholders
    pattern_review_form = re.search(r'<form id="add-review-form" onsubmit="handleWebsiteReviewSubmit\(event\)">[\s\S]*?</form>', content)
    if pattern_review_form:
        new_review_form = '''<form id="add-review-form" onsubmit="handleWebsiteReviewSubmit(event)">
        <!-- Clean Star Rating (1 to 5 Stars as User Wishes) -->
        <div style="text-align:center; padding:16px 12px; background:#f8fafc; border-radius:14px; margin-bottom:16px; border:1px solid var(--border);">
          <div class="swiggy-stars-row" id="swiggy-star-row" style="font-size:2.6rem; letter-spacing:6px; cursor:pointer; user-select:none; margin-bottom:6px;">
            <span class="swiggy-star active" data-val="1" onclick="setSwiggyRating(1)" onmouseover="hoverSwiggyRating(1)" onmouseleave="resetSwiggyRatingHover()">★</span>
            <span class="swiggy-star active" data-val="2" onclick="setSwiggyRating(2)" onmouseover="hoverSwiggyRating(2)" onmouseleave="resetSwiggyRatingHover()">★</span>
            <span class="swiggy-star active" data-val="3" onclick="setSwiggyRating(3)" onmouseover="hoverSwiggyRating(3)" onmouseleave="resetSwiggyRatingHover()">★</span>
            <span class="swiggy-star active" data-val="4" onclick="setSwiggyRating(4)" onmouseover="hoverSwiggyRating(4)" onmouseleave="resetSwiggyRatingHover()">★</span>
            <span class="swiggy-star active" data-val="5" onclick="setSwiggyRating(5)" onmouseover="hoverSwiggyRating(5)" onmouseleave="resetSwiggyRatingHover()">★</span>
          </div>
          <div id="swiggy-rating-verbal" style="font-size:0.95rem; font-weight:800; color:#10b981;">5 Stars</div>
          <input type="hidden" id="modal-fb-rating" value="5">
          <input type="hidden" id="modal-fb-category" value="Food & Service">
        </div>

        <!-- Clean, Simple Name & Dept Inputs -->
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:12px;">
          <div>
            <label class="fb-field-label" for="modal-fb-name">Your Name</label>
            <input type="text" id="modal-fb-name" class="input-field" placeholder="Your Name" required style="width:100%;">
          </div>
          <div>
            <label class="fb-field-label" for="modal-fb-year">Department (Optional)</label>
            <input type="text" id="modal-fb-year" class="input-field" placeholder="College Year / Dept" style="width:100%;">
          </div>
        </div>

        <!-- Clean Review Comments Area -->
        <div style="margin-bottom:16px;">
          <label class="fb-field-label" for="modal-fb-comment">Write your review</label>
          <textarea id="modal-fb-comment" class="input-field" rows="3" placeholder="Share your experience dining at Savitha Canteen..." required style="width:100%; resize:vertical;"></textarea>
        </div>

        <button type="submit" class="btn-calc" id="btn-submit-website-review" style="width:100%; padding:13px; font-size:1rem; font-weight:800; background:linear-gradient(135deg, #10b981 0%, #059669 100%); color:#ffffff; border:none; border-radius:12px; cursor:pointer; box-shadow:0 4px 12px rgba(16, 185, 129, 0.25);">
          Submit Review
        </button>
      </form>'''
        content = content[:pattern_review_form.start()] + new_review_form + content[pattern_review_form.end():]
        print(f"[{filepath}] Successfully updated add review form.")
    else:
        print(f"[{filepath}] WARNING: could not match pattern_review_form")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[{filepath}] Saved successfully.")

def update_app_js(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update initUserAuth to ensure user is NOT logged in without explicit login action
    old_init = '''function initUserAuth() {

  let saved = null;

  try {

    saved = JSON.parse(localStorage.getItem("savitha_user") || "null");

  } catch (e) {}



  if (saved && saved.role && !saved.isGuest) {

    currentUser = saved;

  } else {

    // Unauthenticated visitor by default - cannot access menu without login

    currentUser = null;

  }



  renderUserAuthSlot();

  applyRoleVisibility();

  // Open About the Website page first on website startup!

  performSwitchMode("about");

}'''

    new_init = '''function initUserAuth() {
  // Visitor starts strictly unauthenticated; menu is not accessible without explicit login
  currentUser = null;
  try {
    localStorage.removeItem("savitha_user");
    sessionStorage.removeItem("savitha_user");
  } catch (e) {}

  renderUserAuthSlot();
  applyRoleVisibility();
  // Open About the Website page first on website startup
  performSwitchMode("about");
}'''

    if old_init in content:
        content = content.replace(old_init, new_init, 1)
        print(f"[{filepath}] Successfully updated initUserAuth.")
    else:
        # try regex for initUserAuth
        pattern_init = r'function initUserAuth\(\)\s*\{[\s\S]*?performSwitchMode\("about"\);\s*\}'
        m = re.search(pattern_init, content)
        if m:
            content = content[:m.start()] + new_init + content[m.end():]
            print(f"[{filepath}] Successfully updated initUserAuth via regex.")
        else:
            print(f"[{filepath}] WARNING: could not match initUserAuth")

    # 2. Update renderUserAuthSlot to also update the hero CTA button text (Login to View Menu vs View Menu)
    slot_pattern = r'(function renderUserAuthSlot\(\)\s*\{[\s\S]*?)(const slot = document\.getElementById\("user-auth-slot"\);[\s\S]*?slot\.innerHTML = `[\s\S]*?`;\s*\})'
    slot_match = re.search(slot_pattern, content)
    if slot_match:
        addition = '''
  const heroBtn = document.getElementById("about-hero-primary-btn");
  if (heroBtn) {
    if (currentUser && currentUser.name) {
      heroBtn.innerHTML = `<span>🍽️</span> View Food Menu &amp; Order →`;
    } else {
      heroBtn.innerHTML = `<span>🔒</span> Login to View Menu &amp; Order →`;
    }
  }
}'''
        # Replace the closing of renderUserAuthSlot
        content = content[:slot_match.end() - 1] + addition
        print(f"[{filepath}] Successfully updated renderUserAuthSlot to sync hero CTA button.")

    # 3. Update updateSwiggyStarDisplay so rating displays clean "#{rating} Stars" without forced verbal descriptions
    star_disp_pattern = r'function updateSwiggyStarDisplay\(rating\)\s*\{[\s\S]*?verbal\.textContent\s*=\s*labels\[rating\][^;]*;[\s\S]*?\}'
    new_star_disp = '''function updateSwiggyStarDisplay(rating) {
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
    verbal.textContent = `${rating} Star${rating > 1 ? 's' : ''}`;
    verbal.style.color = rating >= 4 ? "#10b981" : (rating === 3 ? "#f59e0b" : "#ef4444");
  }
}'''
    if re.search(star_disp_pattern, content):
        content = re.sub(star_disp_pattern, new_star_disp, content, count=1)
        print(f"[{filepath}] Successfully updated updateSwiggyStarDisplay.")
    else:
        print(f"[{filepath}] WARNING: could not match updateSwiggyStarDisplay")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[{filepath}] Saved successfully.")

if __name__ == '__main__':
    update_index_html('index.html')
    update_app_js('js/app.js')
    
    # Sync to frontend/
    shutil.copy('index.html', 'frontend/index.html')
    shutil.copy('js/app.js', 'frontend/js/app.js')
    print("Synchronized to frontend/index.html and frontend/js/app.js")
