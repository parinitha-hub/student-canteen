with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
matches = re.findall(r'(\.navbar[^{]*\{[^}]+\})', css)
for m in matches:
    print(m)
    print("---")
matches2 = re.findall(r'(\.container[^{]*\{[^}]+\})', css)
for m in matches2:
    print(m)
    print("---")
