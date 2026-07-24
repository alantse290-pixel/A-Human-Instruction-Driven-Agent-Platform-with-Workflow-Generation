# LLM 調用封裝
#服務層 Service Layer， 將與 OpenAI API 互動的複雜邏輯「封裝（Encapsulate）」
import re
import json
from openai import AsyncOpenAI
from ..config import settings



# LLMService 類別負責與 OpenAI API 互動，提供兩個主要功能：
# 1. chat: 接收使用者訊息，並回傳 AI 的回覆。
# 2. generate_json: 接收使用者訊息和系統提示
class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        )
        self.model = settings.openai_model

    # chat 方法負責與 OpenAI 的 chat.completions API 互動，接收使用者訊息和可選的系統提示，並回傳 AI 的回覆。
    async def chat(self, user_message: str, system_prompt: str = None) -> str:
        messages = []

        #如果有提供 system_prompt，則將其加入訊息列表中，作為系統角色的訊息，這有助於引導 AI 的回覆風格或內容。
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})

        #呼叫 OpenAI 的 chat.completions API，使用指定的模型和訊息列表來生成回覆。temperature 設定為 0.7，這意味著生成的回覆會有一定的隨機性和創造性。
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
        )
        #回傳 AI 生成的文字內容，這是從 API 回應中提取的第一個選項的訊息內容。
        return response.choices[0].message.content

    # generate_json 方法專門用於生成 JSON 輸出，接收使用者訊息和系統提示，並回傳 AI 生成的 JSON 字串。這個方法使用較低的 temperature（0.3），以確保生成的 JSON 結構更穩定和一致。
    async def generate_json(self, user_message: str, system_prompt: str) -> str:
        """專門用於生成 JSON 輸出的方法"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,  # JSON 生成用較低 temperature
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content

    def _extract_json(self, text: str) -> str:
        """從可能包含 markdown 標記的回覆中擷取 JSON"""
        # 嘗試找 ```json ... ``` 區塊
        match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
        if match:
            return match.group(1).strip()

        # 嘗試找第一個 { ... } 區塊
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return match.group(0).strip()

        # 都找不到就原樣回傳，讓上層處理錯誤
        return text