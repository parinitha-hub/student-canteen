import shutil

ADDITIONAL_SELECTOR_BTNS = '''            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Idli Vada Combo', this)">
              <span class="dish-icon">🥞</span>
              <span class="dish-name-label">Idli Vada</span>
              <span class="dish-base-hint">Avg: ~135</span>
            </button>
            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Paneer Butter Masala & Roti', this)">
              <span class="dish-icon">🥘</span>
              <span class="dish-name-label">Paneer Roti</span>
              <span class="dish-base-hint">Avg: ~125</span>
            </button>
            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Chicken Kathi Roll', this)">
              <span class="dish-icon">🌯</span>
              <span class="dish-name-label">Kathi Roll</span>
              <span class="dish-base-hint">Avg: ~140</span>
            </button>
            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Mumbai Pav Bhaji', this)">
              <span class="dish-icon">🍲</span>
              <span class="dish-name-label">Pav Bhaji</span>
              <span class="dish-base-hint">Avg: ~150</span>
            </button>
            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Cheese Masala Maggi', this)">
              <span class="dish-icon">🍜</span>
              <span class="dish-name-label">Cheese Maggi</span>
              <span class="dish-base-hint">Avg: ~165</span>
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
            <button type="button" class="dish-select-btn" onclick="selectKitchenDish('Hot Gulab Jamun', this)">
              <span class="dish-icon">🍯</span>
              <span class="dish-name-label">Gulab Jamun</span>
              <span class="dish-base-hint">Avg: ~180</span>
            </button>
'''

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = '<span class="dish-name-label">Sandwich</span>'
sandwich_idx = html.find(target)

if sandwich_idx != -1:
    btn_close_idx = html.find('</button>', sandwich_idx) + len('</button>')
    if 'Idli Vada' not in html:
        html = html[:btn_close_idx] + '\n\n' + ADDITIONAL_SELECTOR_BTNS + html[btn_close_idx:]
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Updated index.html with all 16 dish selector buttons!")
    else:
        print("index.html already has new selector buttons")
else:
    print("Could not find sandwich in index.html")

shutil.copyfile('index.html', 'frontend/index.html')
print("Synchronized index.html to frontend/index.html successfully!")
