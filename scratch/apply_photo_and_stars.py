import os
import shutil
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Starting photo, LinkedIn, and star rating update...")

# --- 1. UPDATE index.html ---
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1.1 Brand logo subtitle: Official Campus Dining Portal
old_brand_badge = """<div class="brand-dev-badge">Smart Campus Dining</div>"""
new_brand_badge = """<div class="brand-dev-badge">Official Campus Dining Portal</div>"""
if old_brand_badge in html:
    html = html.replace(old_brand_badge, new_brand_badge)
    print("✓ Updated brand badge to Official Campus Dining Portal")

# 1.2 Hero banner: clean official pill
old_hero_pill = """          <div class="hero-developer-pill" style="margin-bottom:12px;">
            <span>⚡ Designed &amp; Developed by <strong>Parinitha.S</strong></span>
          </div>"""

new_hero_pill = """          <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(255,255,255,0.18); border:1px solid rgba(255,255,255,0.32); padding:5px 16px; border-radius:999px; margin-bottom:12px; font-size:0.84rem; font-weight:700; color:#ffffff; backdrop-filter:blur(8px);">
            <span>🏛️ Savitha University</span>
            <span>•</span>
            <span>Official Dining Services</span>
            <span>•</span>
            <span>⚡ By <strong>Parinitha.S</strong></span>
          </div>"""

if old_hero_pill in html:
    html = html.replace(old_hero_pill, new_hero_pill)
    print("✓ Updated hero banner official pill")

# 1.3 Developer card with real photo & LinkedIn button
old_dev_card_pattern = r'<!-- Clean Developer Attribution Card: Parinitha\.S -->.*?</div>\s*</div>\s*</div>\s*</div>'
match_dev_card = re.search(old_dev_card_pattern, html, re.DOTALL)

new_dev_card = """<!-- Official Developer & AI Architect Spotlight: Parinitha.S -->
        <div class="developer-spotlight-card" style="margin-top:24px; padding:24px 28px; background:#ffffff; border:1.5px solid var(--border); border-radius:16px; box-shadow:var(--shadow-sm);">
          <div class="dev-spotlight-grid" style="display:flex; align-items:center; gap:22px; flex-wrap:wrap;">
            <div class="dev-avatar-wrap" style="position:relative; width:92px; height:92px; min-width:92px;">
              <img src="assets/parinitha.jpg" alt="Parinitha.S - Website Developer & AI Architect" 
                   style="width:92px; height:92px; border-radius:50%; object-fit:cover; border:3px solid #6366f1; box-shadow:0 4px 16px rgba(99, 102, 241, 0.28);"
                   onerror="this.onerror=null; this.src='assets/logo.png';">
              <div class="dev-status-indicator" title="Verified Creator & Systems Architect"
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
        </div>"""

if match_dev_card:
    html = html.replace(match_dev_card.group(0), new_dev_card)
    print("✓ Replaced developer card with uploaded photo and LinkedIn profile")
else:
    print("! Could not regex match developer card, attempting fallback string replace")
    old_card_simple = """<div class="developer-spotlight-card" style="margin-top:20px; padding:20px 24px;">"""
    if old_card_simple in html:
        # Split around it
        start_idx = html.find("""<!-- Clean Developer Attribution Card: Parinitha.S -->""")
        end_idx = html.find("""</section>""", start_idx)
        html = html[:start_idx] + new_dev_card + "\n      " + html[end_idx:]
        print("✓ Replaced developer card via index slicing")

# 1.4 Update footer with official university credentials and LinkedIn link
old_footer = re.search(r'<footer.*?</footer\s*>', html, re.DOTALL)
new_footer = """<footer style="background:#0f172a; color:#cbd5e1; padding:28px 0; border-top:1px solid rgba(255,255,255,0.08); margin-top:40px;">
    <div class="container" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
      <div style="display:flex; align-items:center; gap:12px;">
        <img src="assets/logo.png" alt="Savitha Canteen Logo" style="width:36px; height:36px; border-radius:10px;">
        <div>
          <div style="font-size:1.05rem; font-weight:900; color:#ffffff;">Savitha <span style="color:#f59e0b;">Canteen</span></div>
          <div style="font-size:0.75rem; color:#94a3b8;">Savitha University • Official Campus Dining Portal</div>
        </div>
      </div>
      <div style="font-size:0.85rem; color:#94a3b8;">
        Designed &amp; Developed by <a href="https://www.linkedin.com/in/pari-parinitha-s-6196b8354?utm_source=share_via&amp;utm_content=profile&amp;utm_medium=member_android" 
           target="_blank" rel="noopener noreferrer" style="color:#f59e0b; font-weight:800; text-decoration:none;">Parinitha.S</a> (Lead Developer)
      </div>
      <div style="font-size:0.8rem; color:#64748b;">
        © 2026 Savitha Canteen Services. All rights reserved.
      </div>
    </div>
  </footer>"""

if old_footer:
    html = html.replace(old_footer.group(0), new_footer)
    print("✓ Replaced footer with official university attribution and LinkedIn link")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copyfile('index.html', 'frontend/index.html')
print("Successfully written index.html and frontend/index.html!")

# --- 2. UPDATE js/app.js FOR PROMINENT STAR RATINGS ON FOOD ITEMS ---
with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_render_dish_card = """    html += `
      <div class="dish-card">
        <div class="dish-img-wrap">
          <img src="${dish.image}" alt="${dish.name}" class="dish-img" onerror="this.src='assets/hero_banner.jpg'">
          <div class="food-type-icon ${typeClass}"></div>
          <span class="rating-badge">⭐ ${dish.rating}</span>
          <div class="dish-img-overlay"></div>
        </div>
        <div class="dish-body">
          <div class="dish-title-row">
            <h3 class="dish-name">${dish.name}</h3>
          </div>
          <p class="dish-desc">${dish.desc}</p>
          <div class="demand-tag">${dish.demandStatus}</div>
          <div class="dish-footer">
            <div class="dish-price">₹${dish.price}</div>
            <div id="btn-wrap-${dish.id}">
              ${buttonHtml}
            </div>
          </div>
        </div>
      </div>
    `;"""

new_render_dish_card = """    // Compute 5-star visual representation for food items
    const fullStars = Math.floor(dish.rating);
    const hasHalf = (dish.rating - fullStars) >= 0.5;
    let starsStr = "★".repeat(fullStars);
    if (hasHalf && starsStr.length < 5) starsStr += "★";
    const emptyCount = Math.max(0, 5 - starsStr.length);
    const emptyStr = "☆".repeat(emptyCount);

    html += `
      <div class="dish-card">
        <div class="dish-img-wrap">
          <img src="${dish.image}" alt="${dish.name}" class="dish-img" onerror="this.src='assets/hero_banner.jpg'">
          <div class="food-type-icon ${typeClass}"></div>
          <span class="rating-badge">★ ${dish.rating}</span>
          <div class="dish-img-overlay"></div>
        </div>
        <div class="dish-body">
          <div class="dish-title-row">
            <h3 class="dish-name">${dish.name}</h3>
          </div>

          <!-- Prominent Star Rating for Food Item -->
          <div class="dish-star-rating-row" style="display:flex; align-items:center; gap:6px; margin:4px 0 8px 0;">
            <div class="dish-stars-graphic" style="color:#f59e0b; font-size:1.08rem; letter-spacing:1px; line-height:1;" title="${dish.rating} out of 5 stars">
              <span>${starsStr}</span><span style="color:#cbd5e1;">${emptyStr}</span>
            </div>
            <span class="dish-rating-score" style="font-size:0.88rem; font-weight:800; color:var(--text-main);">${dish.rating}</span>
            <span class="dish-reviews-count" style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">(${dish.reviews} reviews)</span>
          </div>

          <p class="dish-desc">${dish.desc}</p>
          <div class="demand-tag">${dish.demandStatus}</div>
          <div class="dish-footer">
            <div class="dish-price">₹${dish.price}</div>
            <div id="btn-wrap-${dish.id}">
              ${buttonHtml}
            </div>
          </div>
        </div>
      </div>
    `;"""

assert old_render_dish_card in js, "Failed to find old_render_dish_card in js/app.js"
js = js.replace(old_render_dish_card, new_render_dish_card)
print("✓ Updated js/app.js with prominent star rating for each food item")

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
shutil.copyfile('js/app.js', 'frontend/js/app.js')
print("Successfully updated js/app.js and frontend/js/app.js!")

# --- 3. UPDATE css/style.css FOR LINKEDIN BUTTON & STAR RATINGS ---
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

extra_css = """
/* Developer Card LinkedIn Button */
.btn-linkedin:hover {
  background: #004182 !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(10, 102, 194, 0.4) !important;
}

/* Food Item Star Rating */
.dish-star-rating-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.dish-stars-graphic {
  color: #f59e0b;
  font-size: 1.05rem;
  letter-spacing: 1px;
}
"""

if '.btn-linkedin:hover' not in css:
    css = css + "\n" + extra_css
    with open('css/style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    shutil.copyfile('css/style.css', 'frontend/css/style.css')
    print("✓ Appended styles to css/style.css and frontend/css/style.css")
else:
    print("css/style.css already contains btn-linkedin styles")

print("\nAll updates completed successfully!")
