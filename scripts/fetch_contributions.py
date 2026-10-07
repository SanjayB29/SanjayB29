from pathlib import Path
import json
import re
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

USERNAME = "SanjayB29"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = Path("data/contributions.json")

html = requests.get(
    URL,
    timeout=30,
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
).text

soup = BeautifulSoup(html, "html.parser")
days = []

for cell in soup.select("td.ContributionCalendar-day"):
    d = cell.get("data-date")
    level = cell.get("data-level")
    if d and level is not None:
        days.append({"date": d, "level": int(level)})

# GitHub can change classes/markup; fail loudly instead of committing a blank graph.
if not days:
    # Fallback to title text: "N contributions on YYYY-MM-DD"
    for cell in soup.select("td[data-date]"):
        d = cell.get("data-date")
        title = cell.get("title", "")
        m = re.search(r"(\d+) contribution", title)
        if d and m:
            n = int(m.group(1))
            level = 0 if n == 0 else min(5, 1 + n // 4)
            days.append({"date": d, "level": level})

if not days:
    raise RuntimeError("Could not find GitHub contribution cells. GitHub markup may have changed.")

days = sorted({x["date"]: x for x in days}.values(), key=lambda x: x["date"])

# Approximate counts from the level buckets when exact counts are not exposed.
level_counts = {i: sum(d["level"] == i for d in days) for i in range(6)}
total_estimated = sum(d["level"] for d in days)

OUT.write_text(json.dumps({
    "username": USERNAME,
    "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "days": days,
    "stats": {
        "days": len(days),
        "level_counts": level_counts,
        "activity_score": total_estimated,
    }
}, indent=2), encoding="utf-8")

print(f"Wrote {OUT} with {len(days)} days")
