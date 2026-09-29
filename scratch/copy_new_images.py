import os
import shutil
import glob

brain_dir = r"C:\Users\srina\.gemini\antigravity-ide\brain\20e971cb-0d00-4045-8d1c-25a9a4f41ad9"

targets = [
    ("hakka_noodles", "hakka_noodles.jpg"),
    ("puri_bhaji", "puri_bhaji.jpg"),
    ("curd_rice", "curd_rice.jpg"),
    ("onion_pakoda", "onion_pakoda.jpg"),
    ("paneer_roll", "paneer_roll.jpg"),
    ("egg_fried_rice", "egg_fried_rice.jpg"),
    ("lime_soda", "lime_soda.jpg"),
    ("brownie_icecream", "brownie_icecream.jpg")
]

for prefix, dest_name in targets:
    pattern = os.path.join(brain_dir, f"{prefix}_*.jpg")
    matches = glob.glob(pattern)
    if matches:
        # Get the newest file
        newest = max(matches, key=os.path.getmtime)
        dest_assets = os.path.join("assets", dest_name)
        dest_frontend = os.path.join("frontend", "assets", dest_name)
        shutil.copyfile(newest, dest_assets)
        shutil.copyfile(newest, dest_frontend)
        print(f"Copied {dest_name} (from {os.path.basename(newest)}) to assets/ and frontend/assets/")
    else:
        print(f"ERROR: No match found for {prefix} in {brain_dir}")
