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