import json, math, jieba
from collections import Counter
from database import SessionLocal
from models.knowledge import KnowledgeItem
from config import TOP_K

def _text_to_embedding(text: str) -> list:
    words = list(jieba.cut(text.lower()))
    counter = Counter(words)
    vocab_size = 5000
    vec = [0] * vocab_size
    for word, freq in counter.items():
        idx = hash(word) % vocab_size
        vec[idx] += freq
    norm = math.sqrt(sum(x ** 2 for x in vec)) or 1
    return [x / norm for x in vec]

def _cosine_similarity(a: list, b: list) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x ** 2 for x in a)) or 1
    norm_b = math.sqrt(sum(x ** 2 for x in b)) or 1
    return dot / (norm_a * norm_b)

async def search_knowledge(query: str, top_k: int = TOP_K) -> list:
    db = SessionLocal()
    try:
        items = db.query(KnowledgeItem).all()
        if not items:
            return []
        query_vec = _text_to_embedding(query)
        results = []
        for item in items:
            item_vec = json.loads(item.embedding) if item.embedding else []
            if not item_vec:
                item_vec = _text_to_embedding(item.question + item.answer)
            score = _cosine_similarity(query_vec, item_vec)
            results.append({
                "question": item.question,
                "answer": item.answer,
                "category": item.category,
                "score": round(score, 4)
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
    finally:
        db.close()
