import re
import os

with open('js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
    js = f.read()

image_refs = re.findall(r'["\'](assets/[^"\']+)["\']', js)
print("Assets referenced in js/app.js:", len(image_refs))
missing_assets = [a for a in set(image_refs) if not os.path.exists(a)]
if missing_assets:
    print("MISSING IN ROOT:", missing_assets)
else:
    print("All referenced assets exist in root assets/!")

missing_in_frontend = [a for a in set(image_refs) if not os.path.exists(os.path.join('frontend', a))]
if missing_in_frontend:
    print("MISSING IN FRONTEND:", missing_in_frontend)
else:
    print("All referenced assets exist in frontend/assets/!")
