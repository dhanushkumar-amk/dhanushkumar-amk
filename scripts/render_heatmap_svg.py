"""Render data/contributions.json -> contrib-heatmap.svg (animated, plays once)."""
import json
from datetime import date

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
BOX, GAP, LEFT, TOP = 12, 3, 34, 28
STEP = BOX + GAP

data = json.load(open("data/contributions.json", encoding="utf-8"))
days = data["days"]
first = date.fromisoformat(days[0]["date"])
offset = (first.weekday() + 1) % 7  # GitHub weeks start on Sunday

cells, months, last_month = [], [], None
for i, d in enumerate(days):
    idx = i + offset
    week, row = idx // 7, idx % 7
    x, y = LEFT + week * STEP, TOP + row * STEP
    delay = round((week + row) * 0.025, 3)
    cells.append(f'<rect class="c" x="{x}" y="{y}" width="{BOX}" height="{BOX}" rx="3" '
                 f'fill="{PALETTE[min(d["level"], 4)]}" style="animation-delay:{delay}s">'
                 f'<title>{d["count"]} on {d["date"]}</title></rect>')
    m = d["date"][5:7]
    if row == 0 and m != last_month:
        name = date.fromisoformat(d["date"]).strftime("%b")
        months.append(f'<text x="{x}" y="18" class="t">{name}</text>')
        last_month = m

weeks = (len(days) + offset + 6) // 7
W = LEFT + weeks * STEP + 10
H = TOP + 7 * STEP + 42
labels = "".join(f'<text x="2" y="{TOP + r*STEP + 10}" class="t">{n}</text>'
                 for r, n in [(1, "Mon"), (3, "Wed"), (5, "Fri")])
legend_x = W - 150
legend = f'<text x="{legend_x-34}" y="{H-12}" class="t">Less</text>' + "".join(
    f'<rect x="{legend_x + i*17}" y="{H-22}" width="12" height="12" rx="3" fill="{c}"/>'
    for i, c in enumerate(PALETTE)) + f'<text x="{legend_x+90}" y="{H-12}" class="t">More</text>'
footer = (f'<text x="{LEFT}" y="{H-12}" class="t">{data["total"]:,} contributions in the last year '
          f'· streak {data["current_streak"]}d · longest {data["longest_streak"]}d</text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
.t{{font:11px ui-monospace,Menlo,Consolas,monospace;fill:#8b949e}}
.c{{opacity:0;animation:in .5s ease-out forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(-6px)}}to{{opacity:1;transform:none}}}}
</style>
<rect width="100%" height="100%" rx="8" fill="#0d1117"/>
{"".join(months)}{labels}
{"".join(cells)}
{footer}{legend}
</svg>'''
open("contrib-heatmap.svg", "w", encoding="utf-8").write(svg)
print(f"wrote contrib-heatmap.svg ({W}x{H})")