from fastapi import FastAPI
from app.routers import chat

app = FastAPI(title="Kopilot")

versionAPI = "v1"
app.include_router(chat.router, prefix=f"/api/{versionAPI}/chat")