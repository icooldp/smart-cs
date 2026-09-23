from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
from models.conversation import Conversation
from models.message import Message

router = APIRouter(prefix="/api/stats", tags=["统计"])

@router.get("/overview")
async def overview(db: Session = Depends(get_db)):
    total_convs = db.query(func.count(Conversation.id)).scalar() or 0
    active_convs = db.query(func.count(Conversation.id)).filter(Conversation.status == "active").scalar() or 0
    transferred = db.query(func.count(Conversation.id)).filter(Conversation.status == "transferred").scalar() or 0
    total_messages = db.query(func.count(Message.id)).scalar() or 0
    auto_resolve = total_convs - transferred if total_convs > 0 else 0
    auto_rate = round(auto_resolve / total_convs * 100, 1) if total_convs else 0

    return {
        "total_conversations": total_convs,
        "active_conversations": active_convs,
        "transferred_count": transferred,
        "total_messages": total_messages,
        "auto_resolve_rate": f"{auto_rate}%",
    }
