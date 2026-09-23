import asyncio
from services.llm_service import chat_with_llm

async def run():
    print("开始调用deepseek...")
    resp = await chat_with_llm([{"role":"user","content":"怎么退货？"}])
    print("返回结果：", resp)

if __name__ == "__main__":
    asyncio.run(run())
