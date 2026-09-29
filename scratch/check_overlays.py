import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("--- Modals and Overlays in index.html ---")
for m in re.finditer(r'<[a-zA-Z0-9]+[^>]+(class|id)=["\'][^"\']*(modal|overlay|backdrop|floating|drawer|toast|banner)[^"\']*["\'][^>]*>', html, re.IGNORECASE):
    print(m.group(0))

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

print("\n--- Fixed position elements in css/style.css ---")
for m in re.finditer(r'([^{}]*position\s*:\s*fixed[^{}]*\{[^{}]*\}|[^{}]*\{[^{}]*position\s*:\s*fixed[^{}]*\})', css):
    print(m.group(0).strip())
    print("---")
