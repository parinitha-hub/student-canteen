import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('id="view-about"')
end = text.find('id="view-login"')
about_section = text[start:end]
print("--- VIEW ABOUT BUTTONS ---")
for line in about_section.splitlines():
    if '<button' in line or '<a ' in line or 'onclick' in line:
        print(line.strip()[:100])

start2 = text.find('id="view-order"')
end2 = text.find('id="view-manager"')
order_section = text[start2:end2]
print("\n--- VIEW ORDER BUTTONS ---")
for line in order_section.splitlines():
    if '<button' in line or '<a ' in line or 'onclick' in line:
        print(line.strip()[:100])
