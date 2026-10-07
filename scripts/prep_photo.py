from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove

src = Path(sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg")
out = Path("source-prepped.png")

if not src.exists():
    raise SystemExit(f"Missing {src}. Add a portrait photo and run: python scripts/prep_photo.py <photo>")

img = Image.open(src).convert("RGBA")
cut = remove(img)

# Composite the isolated subject onto pure white.
bg = Image.new("RGBA", cut.size, (255, 255, 255, 255))
composite = Image.alpha_composite(bg, cut).convert("RGB")
arr = np.array(composite)

gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8))
gray = clahe.apply(gray)

Image.fromarray(gray).save(out)
print(f"Wrote {out}")
