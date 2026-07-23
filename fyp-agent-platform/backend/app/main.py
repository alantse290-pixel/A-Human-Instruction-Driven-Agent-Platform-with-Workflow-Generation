# FastAPI 入口
#用 FastAPI 框架來建立一個網頁伺服器，負責初始化應用程式、設定安全性（CORS）、整合各個功能模組的路由，以及提供一個基本的狀態檢查接口。


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import workflow, chat

app = FastAPI(title="Agent Platform", version="0.1.0")

# 允許前端跨域存取
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 預設埠
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflow.router, prefix="/api/workflow", tags=["workflow"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Agent Platform API is running"}