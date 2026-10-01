from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.projects import router as projects_router
from app.api.conversations import router as conversations_router
from app.api.approvals import router as approvals_router


app = FastAPI(
    title="CodeForge AI",
    description="Local AI coding agent powered by Gemini",
    version="1.0.0",
)


app.include_router(chat_router)
app.include_router(projects_router)
app.include_router(conversations_router)
app.include_router(approvals_router)
