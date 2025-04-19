import requests
import csv
from datetime import datetime, timedelta

# 安定動作用：2日前を指定
safe_day = datetime.utcnow() - timedelta(days=50)
day_str = safe_day.strftime("%Y%m%d")



# Wikipedia API 呼び出し
url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/ja.wikipedia/all-access/{day_str}"
res = requests.get(url)
data = res.json()

# CSV出力
with open("trend.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "rank", "article", "views"])
    for article in data["items"][0]["articles"][:100]:
        writer.writerow([
            datetime.utcnow().isoformat(),
            article["rank"],
            article["article"],
            article["views"]
        ])
