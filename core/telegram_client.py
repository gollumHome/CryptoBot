import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from datetime import datetime, timedelta, timezone
# 引入配置
from config.settings import API_ID, API_HASH, SESSION_STRING, PROXY_URL, USE_MOCK_DATA


class TgScraper:
    def __init__(self):
        self.client = None
        # 只有在非 Mock 模式下才初始化客户端
        if not USE_MOCK_DATA:
            # 解析代理格式
            proxy_args = None
            if PROXY_URL:
                try:
                    from urllib.parse import urlparse
                    p = urlparse(PROXY_URL)
                    # Telethon 代理格式: (类型, 地址, 端口)
                    proxy_args = (p.scheme, p.hostname, p.port)
                except Exception:
                    print("⚠️ 代理地址格式解析失败，将直连")

            try:
                self.client = TelegramClient(
                    StringSession(SESSION_STRING),
                    API_ID,
                    API_HASH,
                    proxy=proxy_args
                )
            except Exception as e:
                print(f"⚠️ 客户端初始化失败 (Mock模式下可忽略): {e}")

    async def fetch_messages(self, chat_id, hours=6):
        """
        拉取消息。如果开启 Mock 模式，直接返回模拟数据。
        """
        # === MOCK 模式分支 ===
        if USE_MOCK_DATA:
            print(f"⚠️ [MOCK模式] 正在生成虚拟数据用于测试... (Target: {chat_id})")
            return self._generate_mock_data(chat_id)

        # === 真实 API 分支 ===
        if not self.client:
            return None

        await self.client.connect()

        if not await self.client.is_user_authorized():
            print("❌ Telegram Session 无效")
            return None

        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        messages_buffer = []

        try:
            entity = await self.client.get_entity(chat_id)
            async for message in self.client.iter_messages(entity, limit=None):
                if message.date < cutoff_time:
                    break
                if message.text:
                    sender = "Unknown"
                    if message.sender:
                        sender = getattr(message.sender, 'first_name', '') or \
                                 getattr(message.sender, 'title', 'Unknown')

                    # 简单清洗
                    clean_text = message.text[:500].replace('\n', ' ')
                    # 格式化时间
                    msg_time = message.date.astimezone(timezone(timedelta(hours=8))).strftime('%H:%M')
                    messages_buffer.append(f"[{msg_time}] {sender}: {clean_text}")

        except Exception as e:
            print(f"❌ 拉取失败 {chat_id}: {e}")
            return None

        return "\n".join(reversed(messages_buffer))

    async def close(self):
        if self.client:
            await self.client.disconnect()

    def _generate_mock_data(self, chat_id):
        """生成模拟的币圈聊天记录，用于测试 AI 分析能力"""
        # 这里模拟了一段包含 Alpha、噪音、FUD 和 风险提示的对话
        return """
[10:00] 老韭菜A: gm
[10:01] 潜水员B: gn,昨晚没睡好
[10:05] 冲土狗C: 兄弟们，Solana上那个新盘子 $PEPE2 好像要发空投了，刚才官方推特发了链接。
[10:06] 技术大佬D: @冲土狗C 别点那个链接，那是钓鱼网站！我看过合约了，权限没丢，owner能无限增发，典型的貔貅盘。
[10:10] 老韭菜A: 卧槽，差点冲了，感谢大佬。
[10:30] 宏观分析师E: 这两天 ETH 汇率有点回暖啊，V神刚才发文说要优化 Gas 费，感觉 Layer2 赛道要有动作。
[10:35] 潜水员B: 确实，我看 OP 和 ARB 都在涨。
[11:00] 消息灵通F: 报！Uniswap 好像有 governance proposal 要通过了，说是要开启 fee switch (费用开关)，UNI 代币可能要赋能了！
[11:02] 冲土狗C: 真假？赶紧抄底一点 UNI。
[11:05] 广告哥G: 专业承接合约审计，私聊我...
[11:10] 技术大佬D: 忽略楼上广告。对了，最近有个叫 Monad 的公链要在测试网发 NFT，建议去跑个节点，大概率大毛。教程链接: https://github.com/monad-node-guide
[11:20] 悲观者H: 别折腾了，大盘要崩，美联储下周还要加息，赶紧空仓保平安。
[11:25] 乐观者I: 楼上又在 FUD，牛市初期都是这样的，拿住就行。
"""