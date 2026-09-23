from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base
import models.conversation
import models.message
import models.knowledge
from api.chat import router as chat_router
from api.knowledge import router as knowledge_router
from api.stats import router as stats_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="智能客服管理系统", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(knowledge_router)
app.include_router(stats_router)

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

@app.get("/api/health")
async def health():
    return {"status": "ok"}
