import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r'window\.([a-zA-Z0-9_]+)\s*=\s*function\s*\((.*?)\)\s*\{'

converted_names = []

def replacer(match):
    name = match.group(1)
    args = match.group(2)
    converted_names.append(name)
    return f'function {name}({args}) {{'

new_code = re.sub(pattern, replacer, code)

print(f'Converted {len(converted_names)} functions: {converted_names}')

attachments = '\n\n// Global Window Attachments for HTML Event Handlers\n'
for name in converted_names:
    attachments += f'if (typeof window !== "undefined") window.{name} = {name};\n'

new_code += attachments

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(new_code)

print('Saved successfully.')
