"""Neofetch-style info card -> info-card.svg. Edit the ROWS below, then run it."""
from xml.sax.saxutils import escape

TITLE = "dhanush@github"
ROWS = [  # (key, value)
    ("Role",       "AI Engineer / Full-Stack Developer"),
    ("Location",   "Tamil Nadu, India"),
    ("Now",        "Building production-grade AI systems"),
    ("Focus",      "Multi-agent systems, LLM security"),
    ("Stack",      "LangGraph, FastAPI, Node.js, React"),
    ("Data",       "PostgreSQL, Redis, Qdrant"),
    ("Infra",      "Docker, AWS, GitHub Actions"),
    ("Highlight",  "1000+ DSA problems solved"),
    ("Highlight",  "Open source: Appwrite, n8n, Hoppscotch"),
    ("Open to",    "AI / LLM / Backend roles"),
]
W, LH, TOPPAD = 490, 22, 58
H = TOPPAD + len(ROWS) * LH + 24
BG, KEY, VAL, DIM = "#0d1117", "#6366f1", "#c9d1d9", "#8b949e"

lines = []
for i, (k, v) in enumerate(ROWS):
    y = TOPPAD + i * LH
    lines.append(f'<g class="l" style="animation-delay:{0.3 + i*0.15:.2f}s">'
                 f'<text x="20" y="{y}" class="k">{escape(k)}</text>'
                 f'<text x="120" y="{y}" class="v">{escape(v)}</text></g>')

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
text{{font:13px ui-monospace,Menlo,Consolas,monospace}}
.k{{fill:{KEY};font-weight:bold}} .v{{fill:{VAL}}} .d{{fill:{DIM}}}
.l{{opacity:0;animation:in .4s ease-out forwards}}
@keyframes in{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:none}}}}
</style>
<rect width="100%" height="100%" rx="8" fill="{BG}"/>
<circle cx="20" cy="18" r="5" fill="#ff5f56"/><circle cx="38" cy="18" r="5" fill="#ffbd2e"/><circle cx="56" cy="18" r="5" fill="#27c93f"/>
<text x="{W//2}" y="22" text-anchor="middle" class="d">{escape(TITLE)}</text>
<text x="20" y="46" class="d">$ neofetch</text>
{"".join(lines)}
</svg>'''
open("info-card.svg", "w", encoding="utf-8").write(svg)
print("wrote info-card.svg")