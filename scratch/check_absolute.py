import re

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

print("--- Checking all position: absolute in css/style.css ---")
rules = re.findall(r'([^{}]*\{[^{}]*position\s*:\s*absolute[^{}]*\})', css)
for r in rules:
    # check if it has inset:0 or width:100% and height:100%
    if any(k in r for k in ['inset', '100%', 'height', 'top: 0', 'z-index']):
        print(r.strip())
        print("---")
