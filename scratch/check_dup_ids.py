import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

ids = re.findall(r'id=["\']([^"\']+)["\']', html)
from collections import Counter
counts = Counter(ids)
duplicates = {k: v for k, v in counts.items() if v > 1}
print("Duplicate IDs in index.html:", duplicates)
