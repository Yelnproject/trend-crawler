import requests, csv
from datetime import datetime, timedelta

# まずは「2日前」をターゲット（必要ならリトライで日を遡る）
for back in range(2, 7):                 # 2〜6日前を試す
    day = datetime.utcnow() - timedelta(days=back)
    y, m, d = day.strftime("%Y"), day.strftime("%m"), day.strftime("%d")
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/ja.wikipedia/all-access/{y}/{m}/{d}"
    res = requests.get(url)
    if res.status_code == 200 and res.text.strip():
        print(f"✅ データ取得: {y}-{m}-{d}")
        data = res.json()
        break
else:
    print("⚠️ 有効な日付のデータが見つかりませんでした")
    exit(0)

# CSV 出力
with open("trend.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["timestamp", "rank", "article", "views"])
    for art in data["items"][0]["articles"][:100]:
        w.writerow([datetime.utcnow().isoformat(), art["rank"], art["article"], art["views"]])
