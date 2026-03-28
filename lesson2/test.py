"""
title: Example Filter
author: open-webui
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 0.1

這是一個 Open WebUI 的 Filter（過濾器）範例。
Filter 可以在訊息送出前（inlet）和收到回應後（outlet）進行攔截與處理。
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    """
    Filter 類別：Open WebUI 的過濾器插件主體。
    負責在對話流程的入口與出口進行攔截、驗證或修改資料。
    """

    class Valves(BaseModel):
        """
        Valves（管理員設定）：由管理員設定的全域參數。
        這些設定會套用到所有使用者。
        """
        priority: int = Field(
            default=0, description="過濾器的執行優先順序，數字越小越優先。"
        )
        max_turns: int = Field(
            default=8, description="管理員設定的最大對話輪數上限。"
        )
        pass

    class UserValves(BaseModel):
        """
        UserValves（使用者設定）：每位使用者可自行調整的參數。
        這些設定只影響該使用者自己。
        """
        max_turns: int = Field(
            default=4, description="使用者自己設定的最大對話輪數上限。"
        )
        pass

    def __init__(self):
        """
        初始化 Filter 實例。
        建立 Valves 設定物件，讓管理員的設定值生效。

        備註：若要啟用自訂檔案處理邏輯，可取消下方 self.file_handler = True 的註解，
        這會讓 WebUI 把檔案相關操作交由本 class 的方法處理，而非使用預設流程。
        """
        # self.file_handler = True  # 啟用後，WebUI 會將檔案處理交由本 class 負責

        # 初始化管理員設定（Valves），使用預設值建立設定物件
        self.valves = self.Valves()
        pass

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        inlet（入口攔截器）：在使用者訊息送往 AI 模型之前執行。
        可用來驗證輸入、修改請求內容，或在不符合條件時拋出例外中止請求。

        參數：
            body: 請求的完整內容，包含對話訊息等資料。
            __user__: 目前使用者的資訊，包含角色（role）與個人設定（valves）。

        回傳：
            處理後的 body（可能已被修改）。
        """
        # 印出除錯資訊，方便開發時追蹤執行狀況
        print(f"inlet:{__name__}")
        print(f"inlet:body:{body}")
        print(f"inlet:user:{__user__}")
        print("輸入inlet")
        # 取得使用者最新輸入的訊息內容並印出
        messages = body.get("messages", [])
        if messages:
            last_user_message = next(
                (m["content"] for m in reversed(messages) if m.get("role") == "user"),
                None
            )
            print(f"使用者輸入內容：{last_user_message}")


        # 只對 "user" 和 "admin" 角色進行對話輪數限制檢查
        if __user__.get("role", "admin") in ["user", "admin"]:
            messages = body.get("messages", [])  # 取得目前的對話訊息列表

            # 取使用者設定與管理員設定中較小的值，作為實際上限
            # 確保使用者無法超過管理員設定的全域上限
            max_turns = min(__user__["valves"].max_turns, self.valves.max_turns)

            # 若對話輪數超過上限，拋出例外，中止本次請求
            if len(messages) > max_turns:
                raise Exception(
                    f"已超過對話輪數限制。最大輪數：{max_turns}"
                )

        return body  # 回傳（可能已修改的）請求內容

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # """
        # outlet（出口攔截器）：在 AI 模型回應之後、回傳給使用者之前執行。
        # 可用來修改回應內容、記錄日誌或進行額外的分析處理。

        # 參數：
        #     body: AI 模型回應的完整內容。
        #     __user__: 目前使用者的資訊。

        # 回傳：
        #     處理後的 body（可能已被修改）。
        # """
        # # 印出除錯資訊
        # print(f"outlet:{__name__}")
        # print(f"outlet:body:{body}")
        # print(f"outlet:user:{__user__}")
        # print("輸出outlet")        
        # messages = body.get("messages", [])
        # if messages:
        #     last_assistant_message = next(
        #         (m["content"] for m in reversed(messages) if m.get("role") == "assistant"),
        #         None
        #     )
        #     print(f"模型輸出內容：{last_assistant_message}")
        
        # # 取得使用者最後輸入的內容
        # messages = body.get("messages", [])
        # user_input = ""
        # assistant_output = ""

        # for msg in reversed(messages):
        #     if msg.get("role") == "assistant" and not assistant_output:
        #         assistant_output = msg.get("content", "")
        #     elif msg.get("role") == "user" and not user_input:
        #         user_input = msg.get("content", "")
        #     if user_input and assistant_output:
        #         break

        # print("使用者最後輸入:", user_input)   
        # print("模型最後輸出:", assistant_output)

        # # 永遠將輸出覆蓋為 Hello! World!
        # for msg in messages:
        #     if msg.get("role") == "assistant":
        #         msg["content"] = "Hello! 徐國堂!💕"

        messages = body.get("messages", [])
        for msg in reversed(messages):
            if msg.get("role") == "assistant":
                msg["content"] = msg.get("content", "") + "\n\n天天開心"
                break

        return body  # 回傳（可能已修改的）回應內容
