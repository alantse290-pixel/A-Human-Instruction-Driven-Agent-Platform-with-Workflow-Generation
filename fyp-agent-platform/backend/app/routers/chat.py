# 對話/指令 API
#建立一個專門處理「聊天（Chat）」功能的 API 路由模組。它定義了前端如何發送訊息給後端，以及後端如何呼叫 LLM（大型語言模型，如 ChatGPT）來產生回覆並傳回給前端。
#體現了後端開發中「關注點分離（Separation of Concerns）」的良好架構。

#***路由層只負責「接收請求」和「回傳結果，真正複雜的邏輯（例如如何與 OpenAI API 溝通、如何組合 Prompt）都交給 LLMService（服務層）去處理。***

from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_service import LLMService

#建立一個 FastAPI 的路由器實例 router，專門用於處理與聊天相關的 API 請求。
router = APIRouter()
llm_service = LLMService()

#定義了這個 API 接收與回傳的資料格式（JSON 結構）
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# 定義一個 POST API 端點 /send，當前端發送訊息到這個端點時，後端會呼叫 LLMService 的 chat 方法來取得回覆，然後將回覆包裝成 ChatResponse 回傳給前端。（結合 main.py 中的設定，完整網址會是 /api/chat/send）

@router.post("/send", response_model=ChatResponse)
# async/await讓伺服器在等待 AI 回覆的期間，繼續去處理其他使用者的請求，不會造成整個伺服器卡住：
async def send_message(request: ChatRequest):
    
    reply = await llm_service.chat(request.message)

    #將 AI 生成的文字包裝成剛剛定義的 Pydantic 模型並回傳給前端
    return ChatResponse(reply=reply)