import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<header')
end = text.find('</header>')
header_section = text[start:end+9]
print("--- HEADER BUTTONS ---")
for line in header_section.splitlines():
    if '<button' in line or '<a ' in line or 'onclick' in line or 'id=' in line:
        print(line.strip()[:100])
