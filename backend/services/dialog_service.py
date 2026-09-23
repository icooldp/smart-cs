from services.rag_service import search_knowledge
from services.llm_service import chat_with_llm
from config import CONFIDENCE_THRESHOLD


async def get_reply(user_query: str, history_list: list, knowledge) -> dict:
    """
    返回格式要匹配上层chat.py调用：
    return {
        "reply": str,
        "confidence": float,
        "need_transfer": bool
    }
    """
    docs = await search_knowledge(user_query)

    confidence = 0.0
    context = "没有匹配到知识库资料，请以智能客服身份友好回答用户。"

    if docs:
        confidence = docs[0]["score"]
        if confidence >= CONFIDENCE_THRESHOLD:
            context = "\n".join([item["content"] for item in docs])

    system_prompt = f"你是业务智能客服，优先参考下面参考资料回答用户问题。参考资料：{context}"

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history_list)
    messages.append({"role": "user", "content": user_query})

    llm_reply = await chat_with_llm(messages)

    # 置信度低于阈值标记转人工；但依然返回大模型回答，不直接截断
    need_transfer = confidence < CONFIDENCE_THRESHOLD

    return {
        "reply": llm_reply,
        "confidence": confidence,
        "need_transfer": need_transfer
    }
