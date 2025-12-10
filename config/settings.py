import os
from dotenv import load_dotenv

load_dotenv()

# --- 环境判断 & 代理 ---
IS_RUNNING_ON_GITHUB = os.getenv("GITHUB_ACTIONS") == "true"
PROXY_URL = None if IS_RUNNING_ON_GITHUB else os.getenv("HTTP_PROXY")

# --- 基础配置 ---
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "False").lower() == "true"
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
TIME_WINDOW_HOURS = 6

# --- Telegram 配置 ---
TG_API_ID = int(os.getenv("TG_API_ID", 0))
TG_API_HASH = os.getenv("TG_API_HASH", "")
TG_SESSION_STRING = os.getenv("TG_SESSION_STRING", "")
# TG 专用 Webhook
WEBHOOK_URL_TG = os.getenv("WECHAT_WEBHOOK_TG", "")

TG_TARGET_GROUPS = [
    {"id": "ethereum_cn", "name": "TG-ETH中文", "enabled": True},
    # {"id": -100123456, "name": "TG-某VIP群", "enabled": True},
]

# --- Discord 配置 (新增) ---
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
# Discord 专用 Webhook
WEBHOOK_URL_DISCORD = os.getenv("WECHAT_WEBHOOK_DISCORD", "")

DISCORD_TARGET_CHANNELS = [
    # id 必须是数字 (Channel ID)，不是 Server ID
    # {"id": 123456789012345678, "name": "DC-项目公告", "enabled": True},
    # {"id": 987654321098765432, "name": "DC-中文区", "enabled": True},
]

# --- 通用 Prompt (可复用) ---
CRYPTO_PROMPT_TEMPLATE = """
【角色设定】
你是一名资深的 Web3/加密货币行业研究员。

【分析目标】
以下是来源 "{group_name}" 过去 {hours} 小时的聊天记录。请提炼情报。

【分析要求】
1. **Alpha 挖掘**: 新项目、Token、空投、白名单。
2. **情绪分析**: 市场多空情绪。
3. **风险预警**: Rug Pull、黑客攻击。
4. **过滤噪音**: 忽略 GM/GN、表情包、机器人指令。
5. **如果没有重要信息**: 输出“无重要 Alpha 或市场动态”。

【输出格式 (Markdown)】
### 📊 情绪
- ...
### 🚀 Alpha & 机会
- ...
### ⚠️ 风险
- ...
### 💡 摘要
- ...

【原始记录】:
{chat_history}
"""