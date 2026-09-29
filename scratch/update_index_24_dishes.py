import shutil

ALL_SELECTOR_BUTTONS = '''          <div class="dish-selector-grid" id="quick-dish-selector">

            <button type="button" class="dish-select-btn active" onclick="selectKitchenDish('Veg Biryani', this)">
              <span class="dish-icon">🍛</span>
              <span class="dish-name-label">Veg Biryani</span>
              <span class="dish-base-hint">Avg: ~140</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Chicken Biryani', this)">
              <span class="dish-icon">🍗</span>
              <span class="dish-name-label">Chicken Biryani</span>
              <span class="dish-base-hint">Avg: ~175</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Masala Dosa', this)">
              <span class="dish-icon">🥞</span>
              <span class="dish-name-label">Masala Dosa</span>
              <span class="dish-base-hint">Avg: ~125</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Idli Vada Combo', this)">
              <span class="dish-icon">🥞</span>
              <span class="dish-name-label">Idli Vada</span>
              <span class="dish-base-hint">Avg: ~135</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Golden Puri Bhaji', this)">
              <span class="dish-icon">🥞</span>
              <span class="dish-name-label">Puri Bhaji</span>
              <span class="dish-base-hint">Avg: ~130</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Paneer Thali', this)">
              <span class="dish-icon">🥘</span>
              <span class="dish-name-label">Paneer Thali</span>
              <span class="dish-base-hint">Avg: ~110</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Paneer Butter Masala & Roti', this)">
              <span class="dish-icon">🥘</span>
              <span class="dish-name-label">Paneer Roti</span>
              <span class="dish-base-hint">Avg: ~125</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Chole Bhature', this)">
              <span class="dish-icon">🍛</span>
              <span class="dish-name-label">Chole Bhature</span>
              <span class="dish-base-hint">Avg: ~130</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('South Indian Curd Rice', this)">
              <span class="dish-icon">🌿</span>
              <span class="dish-name-label">Curd Rice</span>
              <span class="dish-base-hint">Avg: ~105</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Veg Fried Rice', this)">
              <span class="dish-icon">🍚</span>
              <span class="dish-name-label">Fried Rice</span>
              <span class="dish-base-hint">Avg: ~115</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Egg Fried Rice', this)">
              <span class="dish-icon">🍳</span>
              <span class="dish-name-label">Egg Rice</span>
              <span class="dish-base-hint">Avg: ~120</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Veg Hakka Noodles', this)">
              <span class="dish-icon">🍜</span>
              <span class="dish-name-label">Hakka Noodles</span>
              <span class="dish-base-hint">Avg: ~145</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Chicken Kathi Roll', this)">
              <span class="dish-icon">🌯</span>
              <span class="dish-name-label">Chicken Roll</span>
              <span class="dish-base-hint">Avg: ~140</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Paneer Tikka Kathi Roll', this)">
              <span class="dish-icon">🌯</span>
              <span class="dish-name-label">Paneer Roll</span>
              <span class="dish-base-hint">Avg: ~125</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Mumbai Pav Bhaji', this)">
              <span class="dish-icon">🍲</span>
              <span class="dish-name-label">Pav Bhaji</span>
              <span class="dish-base-hint">Avg: ~150</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Samosa & Cutting Chai', this)">
              <span class="dish-icon">☕</span>
              <span class="dish-name-label">Samosa &amp; Chai</span>
              <span class="dish-base-hint">Avg: ~220</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Crispy Onion Pakoda', this)">
              <span class="dish-icon">🧅</span>
              <span class="dish-name-label">Onion Pakoda</span>
              <span class="dish-base-hint">Avg: ~160</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Cheese Masala Maggi', this)">
              <span class="dish-icon">🍜</span>
              <span class="dish-name-label">Cheese Maggi</span>
              <span class="dish-base-hint">Avg: ~165</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Grilled Cheese Sandwich', this)">
              <span class="dish-icon">🥪</span>
              <span class="dish-name-label">Sandwich</span>
              <span class="dish-base-hint">Avg: ~95</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Thick Cold Coffee', this)">
              <span class="dish-icon">🥤</span>
              <span class="dish-name-label">Cold Coffee</span>
              <span class="dish-base-hint">Avg: ~120</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Royal Mango Lassi', this)">
              <span class="dish-icon">🥭</span>
              <span class="dish-name-label">Mango Lassi</span>
              <span class="dish-base-hint">Avg: ~90</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Fresh Sparkling Lime Soda', this)">
              <span class="dish-icon">🍋</span>
              <span class="dish-name-label">Lime Soda</span>
              <span class="dish-base-hint">Avg: ~85</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Hot Gulab Jamun', this)">
              <span class="dish-icon">🍯</span>
              <span class="dish-name-label">Gulab Jamun</span>
              <span class="dish-base-hint">Avg: ~180</span>
            </button>

            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Brownie with Ice Cream', this)">
              <span class="dish-icon">🍫</span>
              <span class="dish-name-label">Brownie</span>
              <span class="dish-base-hint">Avg: ~95</span>
            </button>

          </div>'''

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '<div class="dish-selector-grid" id="quick-dish-selector">'
end_marker = '<!-- Portions Result Box -->'

s_idx = html.find(start_marker)
e_idx = html.find(end_marker, s_idx)

if s_idx != -1 and e_idx != -1:
    # Find the closing </div> of quick-dish-selector before end_marker
    div_close_idx = html.rfind('</div>', s_idx, e_idx) + len('</div>')
    html = html[:s_idx] + ALL_SELECTOR_BUTTONS + html[div_close_idx:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Replaced quick-dish-selector with all 24 dishes in index.html!")
else:
    print("Markers not found in index.html")

shutil.copyfile('index.html', 'frontend/index.html')
print("Synchronized index.html to frontend/index.html!")
