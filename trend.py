# trend.py  ── Wikipedia 日本語版トレンド (2日前) → trend.csv

import requests, csv, os
from datetime import datetime, timedelta, UTC   # Python 3.11 以降

# ---------- 設定 ----------
DAYS_BACK = 2                                    # 何日前を取るか
USER_AGENT = "TrendCrawler/0.1 (+https://github.com/<YOUR_NAME>/trend-crawler)"

# ---------- 1) URL生成 ----------
day = datetime.now(UTC) - timedelta(days=DAYS_BACK)
y, m, d = day.strftime("%Y"), day.strftime("%m"), day.strftime("%d")
url = (
    "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/"
    f"ja.wikipedia/all-access/{y}/{m}/{d}"
)
print(f"Fetching: {url}")

# ---------- 2) API呼び出し ----------
res = requests.get(url, headers={"User-Agent": Yelnproject}, timeout=30)
res.raise_for_status()                            # 200以外で例外
data = res.json()

# ---------- 3) CSV出力 ----------
csv_path = os.path.join(os.path.dirname(__file__), "trend.csv")
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["timestamp", "rank", "article", "views"])
    for art in data["items"][0]["articles"][:100]:
        w.writerow([
            datetime.now(UTC).isoformat(timespec="seconds"),
            art["rank"], art["article"], art["views"]
        ])

print(f"✔ CSV written → {csv_path}")
