import os
from dotenv import load_dotenv

load_dotenv()

# --- 环境判断 & 代理 ---
IS_RUNNING_ON_GITHUB = os.getenv("GITHUB_ACTIONS") == "true"
# 如果在本地运行且需要代理，确保 .env 里填了 HTTP_PROXY (如 http://127.0.0.1:7890)
PROXY_URL = None if IS_RUNNING_ON_GITHUB else os.getenv("HTTP_PROXY")

# --- 基础配置 ---
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "False").lower() == "true"
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
TIME_WINDOW_HOURS = 6

# --- Telegram 配置 ---
# 【重要】API_ID 和 HASH 已移除，改为在 core/telegram_client.py 中内置官方安卓 Key
# 这里只需要 Session String 用于登录验证
TG_SESSION_STRING = os.getenv("TG_SESSION_STRING", "")

# TG 专用 Webhook (用于推送到微信/钉钉/飞书等)
WEBHOOK_URL_TG = os.getenv("WECHAT_WEBHOOK_TG", "")

TG_TARGET_GROUPS = [
    # 示例1: 公开群 (使用用户名)
    {"id": "ethereum_cn", "name": "TG-ETH中文", "enabled": True},

    # 示例2: 私密群 (必须使用数字 ID，以 -100 开头)
    # {"id": -1001234567890, "name": "某VIP内幕群", "enabled": True},
]

# --- Discord 配置 ---
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
# Discord 专用 Webhook
WEBHOOK_URL_DISCORD = os.getenv("WECHAT_WEBHOOK_DISCORD", "")

DISCORD_TARGET_CHANNELS = [
    # Discord 必须使用 Channel ID (数字)
    # {"id": 123456789012345678, "name": "DC-项目公告", "enabled": True},
]

# --- 通用 Prompt (可复用) ---
CRYPTO_PROMPT_TEMPLATE = """
【角色设定】
你是一名资深的 Web3/加密货币行业研究员。

【分析目标】
以下是来源 "{group_name}" 过去 {hours} 小时的聊天记录。请提炼情报。

【分析要求】
1. **Alpha 挖掘**: 重点关注新项目、Token 合约、空投机会、白名单信息。
2. **情绪分析**: 简述市场是贪婪还是恐慌。
3. **风险预警**: 识别 Rug Pull、貔貅盘、钓鱼链接或黑客攻击信息。
4. **过滤噪音**: 忽略 GM/GN、表情包、互喷和机器人指令。
5. **如果没有重要信息**: 直接输出“无重要 Alpha 或市场动态”。

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