import os
import time

print("Hello, 歡迎來到樹莓派的世界！")
print("正在讀取系統資訊...\n")

# 暫停 1 秒鐘製造一點儀式感
time.sleep(1)

# 使用樹莓派內建指令讀取 CPU 溫度
temp_output = os.popen("vcgencmd measure_temp").readline()

print("✅ 讀取成功！")
print(f"🌡️ 目前的 CPU 溫度是：{temp_output}")


while True:
    time.sleep(1)
    print("=== 🍓 樹莓派健康診斷儀表板 ===\n")

    # 1. 取得 CPU 溫度
    temp = os.popen("vcgencmd measure_temp").readline().strip()
    print(f"🌡️ 溫度：{temp.replace('temp=', '')}")

    # 2. 取得 CPU 頻率 (回傳的是 Hz，我們把它換算成 MHz 比較好懂)
    clock_raw = os.popen("vcgencmd measure_clock arm").readline()
    freq_hz = int(clock_raw.split("=")[1])
    print(f"⚡ 時脈：{freq_hz / 1000000} MHz")

    # 3. 檢查系統健康狀態碼 (Throttled)
    throttled = os.popen("vcgencmd get_throttled").readline().strip()
    print(f"⚠️ 狀態碼：{throttled.replace('throttled=', '')}")

    if "0x0" in throttled:
        print("   -> 🟢 狀態極佳：電壓穩定且無過熱！")
    else:
        print("   -> 🔴 注意：系統可能曾經發生供電不足或過熱降頻。")

    # 4. 查看記憶體使用量 (利用 Linux 指令與字串處理)
    ram_info = os.popen("free -h | grep Mem").readline().split()
    print(f"\n🧠 記憶體：已使用 {ram_info[2]} / 總共 {ram_info[1]}")
    print("===============================")