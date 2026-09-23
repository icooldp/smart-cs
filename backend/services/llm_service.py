import httpx
from config import *


async def chat_with_llm(messages: list, temperature=0.7) -> str:
    provider = LLM_PROVIDER
    try:
        print(f"===== LLM provider={provider}, messages={messages}")
        if provider == "deepseek":
            return await _call_deepseek(messages, temperature)
        elif provider == "dashscope":
            return await _call_dashscope(messages, temperature)
        elif provider == "ollama":
            return await _call_ollama(messages, temperature)
        else:
            return "抱歉，AI服务暂时不可用，请转人工客服。"
    except Exception as e:
        print(f"#####【LLM调用异常】ERROR: {str(e)}")
        return "抱歉，这个问题我暂时无法准确回答。正在为您转接人工客服，请稍候..."


async def _call_deepseek(messages, temperature):
    async with httpx.AsyncClient(timeout=15) as client:
        url = f"{DEEPSEEK_BASE_URL}/chat/completions"
        print(f"----- deepseek POST url={url}, key_len={len(DEEPSEEK_API_KEY)}")
        resp = await client.post(
            url,
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
            json={
                "model": LLM_MODEL,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 1024,
                "stream": False
            }
        )
        print(f"----- deepseek status={resp.status_code}, text={resp.text[:500]}")
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


async def _call_dashscope(messages, temperature):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            headers={"Authorization": f"Bearer {DASHSCOPE_API_KEY}"},
            json={
                "model": "qwen-plus",
                "messages": messages,
                "temperature": temperature
            }
        )
        print(f"----- dashscope status={resp.status_code}, text={resp.text[:500]}")
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


async def _call_ollama(messages, temperature):
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": "qwen2.5:7b",
                "messages": messages,
                "options": {"temperature": temperature},
                "stream": False
            }
        )
        print(f"----- ollama status={resp.status_code}, text={resp.text[:500]}")
        resp.raise_for_status()
        data = resp.json()
        return data["message"]["content"]
