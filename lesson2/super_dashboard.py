import os
import time
import requests

# 取得天氣的專屬函式
def get_weather():
    url = "https://wttr.in/Banqiao?0"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return f"❌ 天氣抓取失敗，錯誤碼：{response.status_code}"
    except Exception as e:
        return f"⚠️ 網路連線錯誤：{e}"

# 取得樹莓派健康的專屬函式
def get_pi_health():
    temp = os.popen("vcgencmd measure_temp").readline().strip().replace('temp=', '')
    
    clock_raw = os.popen("vcgencmd measure_clock arm").readline()
    freq_mhz = int(clock_raw.split("=")[1]) // 1000000
    
    throttled = os.popen("vcgencmd get_throttled").readline().strip().replace('throttled=', '')
    status = "🟢 狀態極佳" if "0x0" in throttled else "🔴 注意：可能供電不足或過熱"
    
    ram_info = os.popen("free -h | grep Mem").readline().split()
    ram_usage = f"已使用 {ram_info[2]} / 總共 {ram_info[1]}"
    
    # 將所有資訊排版成一段漂亮的文字
    return f"🌡️ 溫度：{temp}\n⚡ 時脈：{freq_mhz} MHz\n⚠️ 狀態：{throttled} ({status})\n🧠 記憶體：{ram_usage}"

# ================= 主程式開始 =================

while True:
    # 🌟 小魔術：清除終端機畫面 (Linux 指令 clear)
    os.system('clear')
    
    print("="*50)
    print("🌅 歡迎使用早晨專屬超級儀表板 🌅")
    print("="*50)
    
    print("\n🌤️ 【今日板橋區天氣預報】")
    print(get_weather())
    
    print("\n" + "="*50)
    print("🍓 【樹莓派即時健康診斷】")
    print(get_pi_health())
    print("="*50)
    
    # 顯示現在的時間，讓你知道畫面有沒有在動
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n🕒 最後更新時間：{current_time}")
    print("⏳ 下次更新：10 分鐘後... (按 Ctrl+C 即可離開)")
    
    # 🛑 暫停 600 秒 (10分鐘)，保護天氣網站的伺服器！
    time.sleep(600)