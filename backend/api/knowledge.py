from fastapi import APIRouter, Depends, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json
from database import get_db
from models.knowledge import KnowledgeItem
from services.rag_service import _text_to_embedding

router = APIRouter(prefix="/api/knowledge", tags=["知识库"])

class KnowledgeCreate(BaseModel):
    question: str
    answer: str
    category: str = "默认"

@router.post("/add")
async def add_knowledge(item: KnowledgeCreate, db: Session = Depends(get_db)):
    embedding = _text_to_embedding(item.question + item.answer)
    record = KnowledgeItem(
        question=item.question,
        answer=item.answer,
        category=item.category,
        embedding=json.dumps(embedding)
    )
    db.add(record)
    db.commit()
    return {"msg": "添加成功", "id": record.id}

@router.get("/list")
async def list_knowledge(db: Session = Depends(get_db)):
    items = db.query(KnowledgeItem).all()
    return [{"id": i.id, "question": i.question, "answer": i.answer, "category": i.category} for i in items]

@router.delete("/{kid}")
async def delete_knowledge(kid: int, db: Session = Depends(get_db)):
    item = db.query(KnowledgeItem).filter(KnowledgeItem.id == kid).first()
    if item:
        db.delete(item)
        db.commit()
    return {"msg": "已删除"}

@router.post("/import")
async def import_faq(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    data = json.loads(content)
    count = 0
    for item in data:
        embedding = _text_to_embedding(item["question"] + item["answer"])
        record = KnowledgeItem(
            question=item["question"],
            answer=item["answer"],
            category=item.get("category", "导入"),
            embedding=json.dumps(embedding)
        )
        db.add(record)
        count += 1
    db.commit()
    return {"msg": f"成功导入 {count} 条"}
