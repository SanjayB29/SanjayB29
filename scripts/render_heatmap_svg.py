from pathlib import Path
import json
from datetime import date, timedelta

DATA = Path("data/contributions.json")
OUT = Path("contrib-heatmap.svg")
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

payload = json.loads(DATA.read_text())
days = {x["date"]: x["level"] for x in payload["days"]}

# Use the latest 53 weeks ending on Sunday.
end = date.today()
end += timedelta(days=(6 - end.weekday()) % 7)
start = end - timedelta(days=7 * 53 - 1)

cell = 12
gap = 3
left, top = 32, 28
grid_w = 53 * (cell + gap)
grid_h = 7 * (cell + gap)
W, H = left + grid_w + 20, top + grid_h + 62

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    '<rect width="100%" height="100%" rx="12" fill="#0d1117"/>',
    '<text x="20" y="18" fill="#c9d1d9" font-family="monospace" font-size="12">SanjayB29 · contribution activity</text>',
]

# Draw by week, with diagonal stagger.
for week in range(53):
    for dow in range(7):
        d = start + timedelta(days=week * 7 + dow)
        level = days.get(d.isoformat(), 0)
        x = left + week * (cell + gap)
        y = top + dow * (cell + gap)
        delay = (week + dow) * 0.018
        parts.append(
            f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{PALETTE[level]}" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.22s" fill="freeze"/>'
            f'</rect>'
        )

legend_y = H - 25
parts.append(f'<text x="20" y="{legend_y}" fill="#8b949e" font-family="monospace" font-size="10">Less</text>')
for i, color in enumerate(PALETTE):
    x = 55 + i * 18
    parts.append(f'<rect x="{x}" y="{legend_y-9}" width="12" height="12" rx="3" fill="{color}"/>')
parts.append(f'<text x="{55 + len(PALETTE)*18 + 5}" y="{legend_y}" fill="#8b949e" font-family="monospace" font-size="10">More</text>')
parts.append(f'<text x="{W-220}" y="{legend_y}" fill="#6e7681" font-family="monospace" font-size="10">updated {payload["fetched_at"][:10]}</text>')
parts.append("</svg>")

OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"Wrote {OUT}")
