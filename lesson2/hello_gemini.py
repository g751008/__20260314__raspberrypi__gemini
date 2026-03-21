from google import genai
from dotenv import load_dotenv


load_dotenv()
client = genai.Client()

print("🧠 正在透過網路連線至 Gemini AI 大腦，請稍候...\n")

question = "嗨！我是剛學會用樹莓派的小白，請用一句話、幽默一點的方式歡迎我加入寫程式的世界，並加上一個表情符號。"
print(f"👤 我問：{question}")

try:
    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=question
    )
    print("-" * 30)
    print(f"🤖 AI 答：{response.text}")
    print("-" * 30)

except Exception as e:
    print(f"❌ 呼叫失敗，請檢查 API Key 是否正確，或網路是否有問題。錯誤細節：{e}")