from pathlib import Path
import html
import math

from PIL import Image

SRC = Path("source-prepped.png")
OUT = Path("sanjay-ascii.svg")

RAMP = " .`:-=+*cs#%@"
COLS, ROWS = 100, 53
CELL_W, CELL_H = 7.2, 12
FONT = "monospace"
FG = "#c9d1d9"

if not SRC.exists():
    raise SystemExit("Run prep_photo.py first to create source-prepped.png")

img = Image.open(SRC).convert("L")
img.thumbnail((COLS, ROWS))
canvas = Image.new("L", (COLS, ROWS), 255)
x = (COLS - img.width) // 2
y = (ROWS - img.height) // 2
canvas.paste(img, (x, y))

rows = []
for r in range(ROWS):
    chars = []
    for c in range(COLS):
        v = canvas.getpixel((c, r))
        idx = int((255 - v) / 255 * (len(RAMP) - 1))
        chars.append(RAMP[idx])
    rows.append("".join(chars).rstrip())

height = ROWS * CELL_H + 20
width = COLS * CELL_W + 20

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">',
    "<rect width=\"100%\" height=\"100%\" rx=\"12\" fill=\"#0d1117\"/>",
    f'<g fill="{FG}" font-family="{FONT}" font-size="10" xml:space="preserve">'
]

for r, line in enumerate(rows):
    safe = html.escape(line)
    delay = r * 0.055
    y = 16 + r * CELL_H
    parts.append(
        f'<text x="10" y="{y:.1f}" opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.10s" fill="freeze"/>'
        f'{safe}</text>'
    )

parts += ["</g>", "</svg>"]
OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"Wrote {OUT}")
