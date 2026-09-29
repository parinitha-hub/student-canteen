import os
import shutil

source = r'C:\Users\srina\.gemini\antigravity-ide\brain\d82bdb71-a54f-4e4c-902d-d0cdf29318f7\scratch\clean_app.js'
with open(source, 'r', encoding='utf-8') as f:
    base_js = f.read()

print("Base js lines:", len(base_js.splitlines()), "chars:", len(base_js))
with open("scratch/test_rebuild_app.js", "w", encoding="utf-8") as f:
    f.write(base_js)
