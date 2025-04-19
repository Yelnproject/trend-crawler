# trend.py
import requests, csv, os
from datetime import datetime, timedelta

# ---- 1) 取得する日付 = 2 日前（UTC 基準） ------------------
day = datetime.utcnow() - timedelta(days=2)
y, m, d = day.strftime("%Y"), day.strftime("%m"), day.strftime("%d")
url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/ja.wikipedia/all-access/{y}/{m}/{d}"
print(f"Fetching: {url}")

res = requests.get(url)
res.raise_for_status()               # 200 以外なら例外で終了
data = res.json()

# ---- 2) CSV 出力（ファイルはリポジトリ直下に作成） ---------
csv_path = os.path.join(os.path.dirname(__file__), "trend.csv")
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["timestamp", "rank", "article", "views"])
    for art in data["items"][0]["articles"][:100]:
        w.writerow([
            datetime.utcnow().isoformat(timespec="seconds"),
            art["rank"], art["article"], art["views"]
        ])

print(f"✔ CSV written → {csv_path}")
