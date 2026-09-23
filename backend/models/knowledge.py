from sqlalchemy import Column, Integer, String, Text, Float
from database import Base

class KnowledgeItem(Base):
    __tablename__ = "knowledge_items"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    category = Column(String)
    embedding = Column(Text)
    create_ad = Column(String)