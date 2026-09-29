import os
import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

views = re.findall(r'id=[\'"](view-[^\'"]+)[\'"]', html)
print("Views:", views)

# Check all image and script references
scripts = re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', html)
print("Scripts:", scripts)

links = re.findall(r'<link[^>]*href=[\'"]([^\'"]+)[\'"]', html)
print("CSS/Links:", links)

images = re.findall(r'<img[^>]*src=[\'"]([^\'"]+)[\'"]', html)
print("Images count:", len(images))
for img in set(images):
    exists = os.path.exists(img)
    if not exists:
        print(f"MISSING IMAGE: {img}")
    else:
        print(f"Image OK: {img}")
