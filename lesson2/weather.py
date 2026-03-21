import requests
import time

# 這裡我們偷偷用了一個專門為終端機設計的天氣網站 wttr.in
# 既然我們知道你現在在新北市板橋區，我們就把目標鎖定在 Banqiao (板橋)！
# 後面的 "?0" 是為了讓畫面乾淨一點，只顯示當前天氣，不要顯示到三天後。
url = "https://wttr.in/Banqiao?0"

print("📡 正在連線至氣象衛星，偷偷抓取板橋區的即時天氣...")

try:
    time.sleep(10)
    # 派出我們的隱形瀏覽器去這個網址抓資料
    response = requests.get(url)

    # 檢查是否成功 (在網路世界，狀態碼 200 代表「成功 OK」)
    if response.status_code == 200:
        print("✅ 抓取成功！以下是最新天氣狀況：\n")
        # 直接把網站回傳的文字印出來
        print(response.text)
    else:
        print(f"❌ 抓取失敗，伺服器回傳錯誤碼：{response.status_code}")

except Exception as e:
    print(f"⚠️ 發生錯誤：{e} (請檢查樹莓派是否有連上網路！)")