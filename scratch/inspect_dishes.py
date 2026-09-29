import re
import os

with open('js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

dishes = re.findall(r'id:\s*["\']([^"\']+)["\'],\s*name:\s*["\']([^"\']+)["\']', text)
print(f"Total dishes: {len(dishes)}")
for d in dishes:
    print(f" - {d[0]}: {d[1]}")

print("\nAll files in assets directory:")
for f in os.listdir("assets"):
    print(f" - {f}")
