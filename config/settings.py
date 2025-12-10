import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# --- 环境判断 ---
# GitHub Actions 运行时会自动注入这个变量
IS_RUNNING_ON_GITHUB = os.getenv("GITHUB_ACTIONS") == "true"

# --- 智能代理设置 ---
if IS_RUNNING_ON_GITHUB:
    # 如果在 GitHub Actions 跑，强制关闭代理 (云端直连 TG/Google 极快)
    PROXY_URL = None
    print(">>> 环境检测: GitHub Actions (不使用代理)")
else:
    # 本地开发：读取 .env 里的 HTTP_PROXY
    PROXY_URL = os.getenv("HTTP_PROXY")
    if PROXY_URL:
        print(f">>> 环境检测: 本地开发 (使用代理: {PROXY_URL})")
    else:
        print(">>> 环境检测: 本地开发 (无代理配置)")

# --- 基础配置 ---
# 如果开启 Mock 模式，这些 ID 可以随便填，不会报错
API_ID = int(os.getenv("TG_API_ID", 0))
API_HASH = os.getenv("TG_API_HASH", "")
SESSION_STRING = os.getenv("TG_SESSION_STRING", "")
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
WEBHOOK_URL = os.getenv("WECHAT_WEBHOOK", "")

# --- 业务开关 ---
# 如果为 True，则不连接 Telegram，直接返回假数据
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "False").lower() == "true"

TIME_WINDOW_HOURS = 6

TARGET_GROUPS = [
    # 模拟模式下，ID 随便填
    {"id": "mock_group_alpha", "name": "模拟-Alpha猎手群", "enabled": True},
    {"id": "mock_group_general", "name": "模拟-宏观吹水群", "enabled": True},
]

# --- Prompt (保持不变) ---
CRYPTO_PROMPT_TEMPLATE = """
【角色设定】
你是一名资深的 Web3/加密货币行业研究员。

【分析目标】
以下是群组 "{group_name}" 的聊天记录。请提炼出具有交易价值或研究价值的情报。

【分析要求】
1. **Alpha 挖掘**: 关注新项目、潜力 Token、空投教程、白名单。
2. **情绪分析**: 分析对大盘或特定赛道的看法（要有逻辑支持，忽略无脑喊单）。
3. **风险预警**: 提取黑客攻击、Rug Pull、合约漏洞信息。
4. **过滤噪音**: 忽略 GM/GN、表情包、闲聊。
5. **如果没有重要信息**: 输出“本周期内无重要 Alpha 或市场动态”。

【输出格式 (Markdown)】
### 📊 市场/赛道情绪
- ...
### 🚀 Alpha & 机会
- ...
### ⚠️ 风险 & 争议
- ...
### 💡 重点摘要
- ...

【聊天记录】:
{chat_history}
"""