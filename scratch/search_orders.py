import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'id=["\']([^"\']+)["\']', text)
print('IDs in index.html:')
for m in matches:
    if any(k in m.lower() for k in ['order', 'token', 'ticket', 'queue', 'recent']):
        print(' -', m)

print('\nChecking views:')
views = re.findall(r'<div[^>]*id=["\'](view-[^"\']+)["\']', text)
print('Views:', views)
