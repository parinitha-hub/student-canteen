import os
import shutil
from PIL import Image

src_img_path = r"C:\Users\srina\.gemini\antigravity-ide\brain\4290bb00-bb38-4812-98e0-fc886a23b33b\savitha_canteen_logo_1790356151454.jpg"

if not os.path.exists(src_img_path):
    print("Error: Source image not found at", src_img_path)
    exit(1)

im = Image.open(src_img_path)

dest_dirs = ["assets", os.path.join("frontend", "assets")]

for d in dest_dirs:
    os.makedirs(d, exist_ok=True)
    # Save high-res PNG & JPG
    im.save(os.path.join(d, "logo.png"), "PNG")
    im.save(os.path.join(d, "logo.jpg"), "JPEG", quality=95)
    
    # Save Favicon PNG (128x128 and 64x64)
    fav = im.resize((128, 128), Image.Resampling.LANCZOS)
    fav.save(os.path.join(d, "favicon.png"), "PNG")
    fav.save(os.path.join(d, "favicon.ico"), format="ICO", sizes=[(64, 64), (32, 32), (16, 16)])

print("Successfully created logo.png, logo.jpg, favicon.png, favicon.ico in assets/ and frontend/assets/!")
