import re
with open('js/app.js', encoding='utf-8') as f:
    text = f.read()
keys = set(re.findall(r'localStorage\.(?:getItem|setItem|removeItem)\(["\']([^"\']+)["\']', text))
print('localStorage keys found in app.js:')
for k in sorted(keys):
    print(' -', k)
