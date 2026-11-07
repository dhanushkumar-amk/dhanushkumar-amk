"""source-prepped.png -> ascii.svg (monochrome, types itself in row by row, plays once)."""
import sys
from PIL import Image
from xml.sax.saxutils import escape

SRC = sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png"
COLS = 100
RAMP = " .`:-=+*cs#%@"          # dark/background (sparse) -> bright (dense)
FONT, CW, LH = 8, 4.8, 8.6      # font size, char width, line height
COLOR, BG = "#c9d1d9", "#0d1117"

img = Image.open(SRC).convert("L")
rows = max(1, int(COLS * img.height / img.width * 0.5))   # chars are ~2x taller than wide
img = img.resize((COLS, rows), Image.LANCZOS)
px = img.load()

W, H = COLS * CW + 20, rows * LH + 20
parts = []
for y in range(rows):
    line = "".join(RAMP[px[x, y] * (len(RAMP) - 1) // 255] for x in range(COLS))
    if not line.strip():
        continue
    top = 10 + y * LH
    begin = round(y * 0.07, 2)
    parts.append(
        f'<clipPath id="r{y}"><rect x="10" y="{top}" height="{LH+1}" width="0">'
        f'<animate attributeName="width" from="0" to="{COLS*CW}" dur="0.5s" '
        f'begin="{begin}s" fill="freeze"/></rect></clipPath>'
        f'<text x="10" y="{top + FONT}" clip-path="url(#r{y})" xml:space="preserve" '
        f'style="white-space:pre">{escape(line)}</text>')

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}">
<style>text{{font:{FONT}px ui-monospace,Menlo,Consolas,monospace;fill:{COLOR}}}</style>
<rect width="100%" height="100%" rx="8" fill="{BG}"/>
{"".join(parts)}
</svg>'''
open("ascii.svg", "w", encoding="utf-8").write(svg)
print(f"wrote ascii.svg ({COLS}x{rows} chars)")