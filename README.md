# Smart‑CS 智能客服系统

> 基于 FastAPI \+ RAG \+ 大模型的私有化智能客服演示项目，支持知识库问答、多轮对话、置信度判断、自动标记转人工、会话持久化。
>
>

## ✨ 功能特性

- ✅ FastAPI 后端接口，RESTful API，支持跨域

- ✅ RAG 知识库检索，基于相似度匹配业务资料

- ✅ 多模型兼容：DeepSeek API / 通义千问 DashScope / Ollama 本地大模型

- ✅ 多轮对话上下文记忆，会话持久化存储 SQLite

- ✅ 置信度阈值控制：低置信标记转人工（UI 弹窗提示，不阻断 AI 回答）

- ✅ 会话、消息数据库持久化，查询历史聊天记录

- ✅ 简单静态前端页面，直接浏览器访问即可体验

- ✅ 异常捕获兜底，大模型调用失败自动返回转人工提示

## 📁 项目目录结构

```Plain Text
smart-cs
├── backend                 # 后端 FastAPI
│   ├── api                 # 接口路由
│   │   ├── chat.py         # 对话接口
│   │   ├── knowledge.py    # 知识库管理接口
│   │   └── stats.py        # 统计接口
│   ├── models              # SQLAlchemy ORM 数据库模型
│   │   ├── conversation.py # 会话模型
│   │   ├── knowledge.py   # 知识库条目模型
│   │   └── message.py      # 聊天消息模型
│   ├── services            # 业务服务层
│   │   ├── dialog_service.py  # 对话核心逻辑
│   │   ├── llm_service.py     # 大模型调用封装
│   │   └── rag_service.py     # RAG向量检索服务
│   ├── .env                # 环境配置文件（密钥、模型参数）
│   ├── config.py           # 全局配置读取
│   ├── database.py        # 数据库连接
│   ├── init_knowledge.py  # 知识库初始化脚本
│   ├── main.py            # FastAPI程序入口
│   ├── requirements.txt  # Python依赖
│   └── debug_llm.py       # LLM单独调试脚本
└── frontend                # 简单网页前端页面
```

## 🛠️ 环境依赖

Python \>=3\.11

### 安装依赖

```powershell
cd backend
python -m venv venv
# Windows激活虚拟环境
venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

`requirements.txt`参考：

```txt
fastapi
uvicorn[standard]
sqlalchemy
pydantic
python-dotenv
httpx
```

## ⚙️ 配置文件 backend/\.env

```env
# LLM 服务商选择：deepseek / dashscope / ollama
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-xxx
DEEPSEEK_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-flash

# 阿里云通义千问
DASHSCOPE_API_KEY=

# Ollama本地模型
OLLAMA_BASE_URL=http://127.0.0.1:11434

# RAG检索参数
RAG_SIM_THRESHOLD=0.6
TOP_K=2
CONFIDENCE_THRESHOLD=0.6

# Sqlite数据库
DB_URL=sqlite:///./smartcs.db
```

> ⚠️ 注意：不要把`.env`提交到 git，里面包含 API 密钥。
>
>

## 🚀 启动运行

### 1、启动后端服务

```powershell
cd backend
venv\Scripts\Activate.ps1
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- 后端接口文档地址： [http://127\.0\.0\.1:8000/docs](http://127.0.0.1:8000/docs)

- 前端页面： [http://127\.0\.0\.1:8000/index\.html](http://127.0.0.1:8000/index.html)

### 2、单独调试大模型接口（跳过 web 服务，定位调用问题）

```powershell
cd backend
python debug_llm.py
```

## 📖 业务流程

1. 用户在前端发送问题

2. `api/chat/send`接口：查询 / 创建会话，读取历史聊天记录

3. `dialog_service.py`

    - 调用 RAG 检索知识库，拿到匹配文档与相似度分数

    - 根据`CONFIDENCE_THRESHOLD`判断置信度

    - 组装 System 提示词 \+ 历史对话 \+ 当前用户提问

    - 调用`llm_service`请求大模型

4. 返回结果字典：`{"reply":回答文本,"confidence":置信分数,"need_transfer":是否转人工标记}`

5. 聊天消息写入 SQLite 数据库；前端收到`need_transfer=True`弹出转人工提示 UI

6. 大模型网络 / 接口异常：返回兜底转人工字符串给前端

> 逻辑特点：置信度不足**只是标记转人工标识**，依然输出 AI 回答；只有 LLM 调用抛出异常才直接返回兜底文案。
>
>

## 🔌 API 接口说明

|接口|方法|说明|
|---|---|---|
|`/api/chat/send`|POST|发送聊天消息，返回 AI 回复、置信度、转人工标记|
|`/api/chat/history/{conversation_id}`|GET|获取指定会话全部历史消息|
|`/docs`|GET|FastAPI 自动生成 Swagger 接口文档|

## 🐛 常见问题

1. **DeepSeek 接口超时 ConnectTimeout**

> Windows 国内网络直连 deepseek 容易超时。
> 方案 A：切换`LLM_PROVIDER=ollama`使用本地 Ollama 模型测试业务；
> 方案 B：为 httpx 客户端配置网络代理。
>
>

2. `get_reply() takes 1 positional argument but 3 were given`

> dialog\\\[\_service\.py\]\(\_service\.py\) 函数入参需要和 \[chat\.py\]\(chat\.py\) 调用参数保持一致。
>
>

3. `string indices must be integers`

> dialog\_service 需要返回 dict 字典，不能直接返回字符串。
>
>

4. Uvicorn reload 模式日志看不到日志

> 项目内全部使用`print()`打印调试信息，reload 模式 print 会输出控制台。
>
>

## 📝 后续扩展方向

1. 完善知识库后台管理页面（新增、编辑、删除知识库条目）

2. 接入向量数据库（Chroma / Milvus）替换简易 RAG 检索

3. 增加会话管理后台，查看转人工会话列表

4. 支持流式 SSE 输出打字机效果

5. 接入真实人工客服对接模块

## 📮 联系信息

- 项目官网：[**icoolkj\.com**](https://icoolkj.com)

- 业务邮箱：[icoolkj@163\.com](mailto:icoolkj@163.com)

- QQ 邮箱：[594047667@qq\.com](mailto:594047667@qq.com)

## 📄 版权声明

```Plain Text
Copyright © 2026 icoolkj.com All Rights Reserved.
本项目仅供技术学习、研究演示使用。
未经作者许可，禁止用于商业产品、二次分发以及闭源商用场景。
如需要商用授权，请通过上方联系方式进行咨询。
```

---

### 配套 \.gitignore（可选，直接保存为`.gitignore`放在项目根目录 `smart-cs/.gitignore`）

```gitignore
# Python 虚拟环境
venv/
*.pyc
__pycache__/
*.pyo
*.pyd

# 环境密钥配置
backend/.env

# Sqlite数据库文件
*.db
*.sqlite3

# IDE
.idea/
.vscode/
*.swp
*.swo

# 日志
*.log
```
