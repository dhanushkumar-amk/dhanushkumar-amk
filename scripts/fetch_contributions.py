"""Fetch a public GitHub contribution calendar (no token needed).
Usage: python scripts/fetch_contributions.py YOUR_USERNAME
"""
import json, re, sys, os
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup

user = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GH_USER")
if not user:
    sys.exit("Usage: python scripts/fetch_contributions.py YOUR_USERNAME")

r = requests.get(f"https://github.com/users/{user}/contributions",
                 headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

# Counts live in <tool-tip for="cell-id">N contributions on ...</tool-tip>
counts = {}
for tip in soup.find_all("tool-tip"):
    m = re.match(r"(\d+|No) contribution", tip.get_text(strip=True))
    if m:
        counts[tip.get("for")] = 0 if m.group(1) == "No" else int(m.group(1))

days = []
for td in soup.select("td.ContributionCalendar-day"):
    if not td.get("data-date"):
        continue
    days.append({"date": td["data-date"],
                 "level": int(td.get("data-level", 0)),
                 "count": counts.get(td.get("id"), 0)})
days.sort(key=lambda d: d["date"])
if not days:
    sys.exit("No contribution cells found - GitHub's HTML may have changed.")

# Stats
total = sum(d["count"] for d in days)
best = max(days, key=lambda d: d["count"])
longest = cur = 0
for d in days:
    cur = cur + 1 if d["count"] > 0 else 0
    longest = max(longest, cur)
today = date.today().isoformat()
current = 0
for d in reversed([d for d in days if d["date"] <= today]):
    if d["count"] > 0:
        current += 1
    elif d["date"] == today:
        continue  # today may not have activity yet
    else:
        break

os.makedirs("data", exist_ok=True)
with open("data/contributions.json", "w") as f:
    json.dump({"user": user, "total": total, "current_streak": current,
               "longest_streak": longest, "best_day": best, "days": days}, f)
print(f"{user}: {total} contributions, streak {current}, longest {longest}")