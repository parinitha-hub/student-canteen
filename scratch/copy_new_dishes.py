import shutil
import os

images = {
    "peri_peri_fries.jpg": r"C:\Users\srina\.gemini\antigravity-ide\brain\4290bb00-bb38-4812-98e0-fc886a23b33b\peri_peri_fries_1790358194218.jpg",
    "campus_burger.jpg": r"C:\Users\srina\.gemini\antigravity-ide\brain\4290bb00-bb38-4812-98e0-fc886a23b33b\campus_burger_1790358218104.jpg",
    "chicken_noodles.jpg": r"C:\Users\srina\.gemini\antigravity-ide\brain\4290bb00-bb38-4812-98e0-fc886a23b33b\chicken_noodles_1790358265514.jpg",
    "medu_vada.jpg": r"C:\Users\srina\.gemini\antigravity-ide\brain\4290bb00-bb38-4812-98e0-fc886a23b33b\medu_vada_1790358294453.jpg"
}

for name, src in images.items():
    if os.path.exists(src):
        shutil.copyfile(src, os.path.join("assets", name))
        shutil.copyfile(src, os.path.join("frontend", "assets", name))
        print(f"Copied {name} successfully!")
    else:
        print(f"Source not found: {src}")
