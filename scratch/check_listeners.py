import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

print("--- addEventListener in js/app.js ---")
for m in re.finditer(r'addEventListener\([^)]+\)', js):
    print(m.group(0))

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("\n--- onkey/oninput in index.html ---")
for m in re.finditer(r'on(key|input|change|focus|blur|click)[a-z]*="[^"]+"', html, re.IGNORECASE):
    print(m.group(0))
