# trend.py
import requests, csv, os
from datetime import datetime, timedelta

# ---------- 1) 直近で必ずデータがある日を探す（2〜6日前） ----------
for back in range(2, 7):
    day = datetime.utcnow() - timedelta(days=back)
    y, m, d = day.strftime("%Y"), day.strftime("%m"), day.strftime("%d")
    url = (f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/"
           f"ja.wikipedia/all-access/{y}/{m}/{d}")
    res = requests.get(url)
    if res.status_code == 200 and res.text.strip():
        print(f"✅ data found: {y}-{m}-{d}")
        data = res.json()
        break
else:
    print("⚠ No valid data, exit.")
    raise SystemExit(0)

# ---------- 2) trend.csv をスクリプトと同じ階層に書き出し ----------
csv_path = os.path.join(os.path.dirname(__file__), "trend.csv")
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["timestamp", "rank", "article", "views"])
    for art in data["items"][0]["articles"][:100]:
        w.writerow([
            datetime.utcnow().isoformat(timespec="seconds"),
            art["rank"], art["article"], art["views"]
        ])

print(f"📦 CSV written -> {csv_path}")
