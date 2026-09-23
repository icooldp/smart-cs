from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models.conversation import Conversation
from models.message import Message
from services.dialog_service import get_reply
from services.rag_service import search_knowledge

router = APIRouter(prefix="/api/chat", tags=["对话"])

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    confidence: float
    need_transfer: bool
    conversation_id: int

@router.post("/send", response_model=ChatResponse)
async def send_message(req: ChatRequest, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(
        Conversation.user_id == req.user_id,
        Conversation.status == "active"
    ).first()

    if not conv:
        conv = Conversation(user_id=req.user_id, status="active")
        db.add(conv)
        db.commit()
        db.refresh(conv)

    user_msg = Message(conversation_id=conv.id, role="user", content=req.message)
    db.add(user_msg)
    db.commit()

    history = db.query(Message).filter(
        Message.conversation_id == conv.id
    ).order_by(Message.id).all()
    history_list = [{"role": m.role, "content": m.content} for m in history[:-1]]

    knowledge = await search_knowledge(req.message)
    result = await get_reply(req.message, history_list, knowledge)

    bot_msg = Message(conversation_id=conv.id, role="assistant", content=result["reply"])
    db.add(bot_msg)

    if result["need_transfer"]:
        conv.status = "transferred"
        conv.confidence = result["confidence"]

    db.commit()

    return ChatResponse(
        reply=result["reply"],
        confidence=result["confidence"],
        need_transfer=result["need_transfer"],
        conversation_id=conv.id
    )

@router.get("/history/{conversation_id}")
async def get_history(conversation_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.id).all()
    return [{"role": m.role, "content": m.content, "time": str(m.created_at)} for m in messages]
