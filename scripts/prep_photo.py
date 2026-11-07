"""Prep a photo for ASCII conversion: remove background, boost contrast, put on BLACK.
Usage: python scripts/prep_photo.py my-photo.jpg   ->  source-prepped.png
"""
import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove, new_session

if len(sys.argv) < 2:
    sys.exit("Usage: python scripts/prep_photo.py my-photo.jpg")

session = new_session("u2net_human_seg")   # ~170MB, made for people
img = Image.open(sys.argv[1]).convert("RGB")
cut = remove(img, session=session)          # RGBA, background transparent
rgba = np.array(cut)
gray = cv2.cvtColor(rgba[:, :, :3], cv2.COLOR_RGB2GRAY)
gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)
alpha = rgba[:, :, 3] / 255.0
out = (gray * alpha).astype(np.uint8)       # subject on pure black
Image.fromarray(out).save("source-prepped.png")
print("wrote source-prepped.png")