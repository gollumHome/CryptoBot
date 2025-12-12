# core/telegram_client.py

from telethon import TelegramClient
from telethon.sessions import StringSession
from datetime import datetime, timedelta, timezone
from config.settings import TG_SESSION_STRING, PROXY_URL, USE_MOCK_DATA


class TgScraper:
    # ==========================================
    # 🔥 核心修改：直接内置 Telegram 官方安卓 Key
    # 这样你就不用去网页申请了，可以直接跑通
    # ==========================================
    OFFICIAL_API_ID = 6
    OFFICIAL_API_HASH = 'eb06d4abfb49dc3eeb1aeb98ae0f581e'

    def __init__(self):
        self.client = None

        # MOCK 模式下不需要初始化客户端
        if USE_MOCK_DATA:
            return

        # 检查 Session String 是否存在
        if not TG_SESSION_STRING:
            print("❌ 错误: 未找到 TG_SESSION_STRING。请先运行 get_session.py 获取。")
            return

        # 解析代理 (保留你原有的逻辑)
        proxy_args = None
        if PROXY_URL:
            try:
                from urllib.parse import urlparse
                p = urlparse(PROXY_URL)
                proxy_args = (p.scheme, p.hostname, p.port)
            except Exception:
                print("⚠️ 代理地址格式解析失败，将直连")

        try:
            # 初始化客户端 (使用 Session String + 官方 Key)
            self.client = TelegramClient(
                StringSession(TG_SESSION_STRING),
                self.OFFICIAL_API_ID,
                self.OFFICIAL_API_HASH,
                proxy=proxy_args
            )
        except Exception as e:
            print(f"⚠️ 客户端初始化失败: {e}")

    async def fetch_messages(self, chat_id, hours=6):
        """
        拉取消息。
        chat_id: 可以是整数 ID (如 -100xxx) 或 用户名 (如 'bitcoin')
        """
        # === MOCK 模式 ===
        if USE_MOCK_DATA:
            print(f"⚠️ [MOCK] 生成测试数据... (Target: {chat_id})")
            return self._generate_mock_data(chat_id)

        # === 真实模式 ===
        if not self.client:
            print("❌ 客户端未就绪，无法拉取")
            return None

        try:
            # 确保连接
            if not self.client.is_connected():
                await self.client.connect()

            # 校验登录状态
            if not await self.client.is_user_authorized():
                print("❌ Session 失效或未登录")
                return None

            # 转换 ID (如果是字符串形式的数字，转为 int)
            try:
                if isinstance(chat_id, str) and chat_id.startswith("-100"):
                    chat_id = int(chat_id)
            except ValueError:
                pass

            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
            messages_buffer = []

            # 获取实体 (群组/频道)
            entity = await self.client.get_entity(chat_id)

            # 遍历消息
            async for message in self.client.iter_messages(entity, limit=None):
                # 时间截止判断
                if message.date < cutoff_time:
                    break

                # 过滤有效文本
                if message.text and not message.action:
                    sender = "Unknown"
                    if message.sender:
                        # 尝试获取发送者名称
                        sender = getattr(message.sender, 'first_name', '') or \
                                 getattr(message.sender, 'title', 'Unknown')

                    # 简单清洗
                    clean_text = message.text[:800].replace('\n', ' ')

                    # 格式化时间 (转为东八区显示)
                    msg_time = message.date.astimezone(timezone(timedelta(hours=8))).strftime('%m-%d %H:%M')

                    messages_buffer.append(f"[{msg_time}] {sender}: {clean_text}")

            print(f"✅ [TG] {entity.title if hasattr(entity, 'title') else chat_id} 拉取完成: {len(messages_buffer)} 条")

        except Exception as e:
            print(f"❌ 拉取失败 {chat_id}: {e}")
            return None

        if not messages_buffer:
            return None

        # 反转列表，按时间正序返回
        return "\n".join(reversed(messages_buffer))

    async def close(self):
        if self.client:
            await self.client.disconnect()

    def _generate_mock_data(self, chat_id):
        # 你的 Mock 数据保持不变
        return """
[10:00] 老韭菜A: gm
[10:05] 冲土狗C: $PEPE2 要发空投了。
[10:06] 技术大佬D: 别点，那是钓鱼。
"""