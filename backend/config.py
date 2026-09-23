from dotenv import load_dotenv
import os

# 加载backend目录的.env配置文件
load_dotenv()

# LLM通用配置
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-flash")

# DeepSeek配置 【不带/v1】
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# 通义千问dashscope
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")

# Ollama本地大模型
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

# RAG知识库检索配置
RAG_SIM_THRESHOLD = float(os.getenv("RAG_SIM_THRESHOLD", 0.6))
TOP_K = int(os.getenv("TOP_K", 2))
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.01))

# 数据库连接串，默认sqlite本地文件
DB_URL = os.getenv("DB_URL", "sqlite:///./smartcs.db")
