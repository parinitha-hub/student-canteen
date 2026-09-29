with open('scratch/build_clean_app_js.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('async async function', 'async function')

with open('scratch/build_clean_app_js.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed async async in build script!")
