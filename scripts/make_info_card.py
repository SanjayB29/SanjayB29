from pathlib import Path
import os

OUT = Path("info-card.svg")
STATIC = os.getenv("STATIC") == "1"

rows = [
    ("Name", "Sanjay Balamurugan"),
    ("Role", "Software Developer"),
    ("Focus", "AI / Governance / Backend"),
    ("Stack", "Java · Python · TypeScript"),
    ("Tools", "Git · Podman · Kubernetes"),
    ("Building", "Developer tools & AI systems"),
    ("Based", "India"),
]

W, H = 490, 360
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    '<rect width="100%" height="100%" rx="12" fill="#0d1117" stroke="#30363d"/>',
    '<circle cx="22" cy="22" r="6" fill="#ff5f56"/><circle cx="42" cy="22" r="6" fill="#ffbd2e"/><circle cx="62" cy="22" r="6" fill="#27c93f"/>',
    '<text x="85" y="27" fill="#8b949e" font-family="monospace" font-size="13">sanjay@github — neofetch</text>',
    '<text x="24" y="65" fill="#58a6ff" font-family="monospace" font-size="18" font-weight="bold">Sanjay Balamurugan</text>',
]

for i, (k, v) in enumerate(rows):
    y = 100 + i * 34
    delay = i * 0.12
    if STATIC:
        parts.append(f'<text x="24" y="{y}" fill="#8b949e" font-family="monospace" font-size="13">{k:10}:</text>')
        parts.append(f'<text x="125" y="{y}" fill="#c9d1d9" font-family="monospace" font-size="13">{v}</text>')
    else:
        anim = f'<animate attributeName="opacity" values="0;1" keyTimes="0;1" begin="{delay:.2f}s" dur="0.25s" fill="freeze"/>'
        parts.append(f'<g opacity="0">{anim}<text x="24" y="{y}" fill="#8b949e" font-family="monospace" font-size="13">{k:10}:</text><text x="125" y="{y}" fill="#c9d1d9" font-family="monospace" font-size="13">{v}</text></g>')

parts.append('<text x="24" y="338" fill="#6e7681" font-family="monospace" font-size="11">always willing to learn more_</text>')
parts.append("</svg>")
OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"Wrote {OUT}")
