# FastAPI 入口
#用 FastAPI 框架來建立一個網頁伺服器，負責初始化應用程式、設定安全性（CORS）、整合各個功能模組的路由，以及提供一個基本的狀態檢查接口。


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import workflow, chat

#建立一個 FastAPI 的應用程式實例 app。
app = FastAPI(title="Agent Platform", version="0.1.0")

#  設定 CORS（跨來源資源共用）,允許前端跨域存取,解決前後端分離開發時常見的「跨域問題（CORS）」
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 預設埠,明確允許來自 Vite 前端開發伺服器的請求
    allow_credentials=True,
    #允許所有的 HTTP 方法（GET, POST, PUT, DELETE 等）和所有的標頭（Headers），方便開發:
    allow_methods=["*"],
    allow_headers=["*"],
)

#將不同功能的 API 拆分到不同的檔案中管理，然後在這裡統一註冊到主程式:
app.include_router(workflow.router, prefix="/api/workflow", tags=["workflow"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

#建立健康檢查（Health Check）端點, 提供一個最基礎的根目錄 (/) API。
#開發測試：當你啟動伺服器後，打開瀏覽器輸入 http://localhost:8000/，如果看到這串 JSON 回應，就代表你的後端伺服器已經成功啟動且正常運作。
#部署監控：在雲端部署（如 AWS, GCP, 或是 Docker 容器）時，系統通常需要一個簡單的網址來定期檢查伺服器是否還活著（存活探針 Liveness Probe），這個端點就非常適合做這件事。
@app.get("/")
def health_check():
    return {"status": "ok", "message": "Agent Platform API is running"}