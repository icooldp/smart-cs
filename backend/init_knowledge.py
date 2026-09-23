import json
from database import engine, SessionLocal, Base
from models.knowledge import KnowledgeItem
from services.rag_service import _text_to_embedding

FAQ_DATA = [
    {"question": "你们的营业时间是什么？", "answer": "我们的营业时间是周一至周五 9:00-18:00，周末 10:00-17:00。", "category": "基本信息"},
    {"question": "怎么退货？", "answer": "支持7天无理由退货。请在订单页面申请退货，客服审核后安排上门取件。", "category": "售后服务"},
    {"question": "运费怎么算？", "answer": "订单满99元包邮，未满99元收取8元运费。", "category": "物流"},
    {"question": "怎么修改收货地址？", "answer": "在订单发货前，可在「我的订单」中修改地址。发货后请联系客服处理。", "category": "订单"},
    {"question": "支持哪些支付方式？", "answer": "支持微信支付、支付宝、银行卡、花呗分期。", "category": "支付"},
    {"question": "多久能收到货？", "answer": "一般3-5个工作日到货，偏远地区5-7个工作日。", "category": "物流"},
    {"question": "怎么开发票？", "answer": "在订单详情页点击「申请发票」，可开电子普票或增值税专票。", "category": "财务"},
    {"question": "会员有什么权益？", "answer": "会员享受95折优惠、生日礼券、优先客服通道。", "category": "会员"},
]

def init():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.query(KnowledgeItem).delete()
    db.commit()
    count = 0
    for item in FAQ_DATA:
        embedding = _text_to_embedding(item["question"] + item["answer"])
        record = KnowledgeItem(
            question=item["question"],
            answer=item["answer"],
            category=item["category"],
            embedding=json.dumps(embedding)
        )
        db.add(record)
        count += 1
    db.commit()
    db.close()
    print(f"✅ 知识库初始化完成，共 {count} 条")

if __name__ == "__main__":
    init()
