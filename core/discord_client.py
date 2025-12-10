import requests
import datetime
from datetime import timezone, timedelta
from config.settings import DISCORD_TOKEN, PROXY_URL, USE_MOCK_DATA


class DiscordScraper:
    def __init__(self):
        self.base_url = "https://discord.com/api/v10"
        self.headers = {
            "Authorization": f"Bot {DISCORD_TOKEN}",
            "Content-Type": "application/json"
        }

        # 处理代理
        self.proxies = None
        if PROXY_URL and not USE_MOCK_DATA:
            self.proxies = {
                "http": PROXY_URL,
                "https": PROXY_URL
            }

    def fetch_messages(self, channel_id, hours=6):
        """拉取 Discord 频道历史消息"""

        # === Mock 模式 ===
        if USE_MOCK_DATA:
            print(f"⚠️ [Discord Mock] 生成虚拟数据: {channel_id}")
            return self._generate_mock_data()

        # === 真实请求 ===
        if not DISCORD_TOKEN:
            print("❌ Discord Token 未配置")
            return None

        # 计算时间窗口 (Discord API 不支持按时间筛选，只能按 limit 拉取后在本地筛选)
        # 策略：拉取最近 100 条 (通常够 6 小时了，不够再加 limit)
        url = f"{self.base_url}/channels/{channel_id}/messages"
        params = {"limit": 100}

        try:
            resp = requests.get(url, headers=self.headers, params=params, proxies=self.proxies, timeout=10)

            if resp.status_code == 403:
                print(f"❌ 权限不足 (403): 请确保机器人已加入服务器并开启 'Read Message History' 权限。")
                return None
            elif resp.status_code != 200:
                print(f"❌ Discord API 错误: {resp.status_code} - {resp.text}")
                return None

            messages = resp.json()
            if not messages:
                return None

            # 筛选时间
            cutoff_time = datetime.datetime.now(timezone.utc) - timedelta(hours=hours)
            buffer = []

            for msg in messages:
                # Discord 时间格式: 2023-10-27T10:00:00.000000+00:00
                msg_time_str = msg['timestamp']
                msg_dt = datetime.datetime.fromisoformat(msg_time_str)

                if msg_dt < cutoff_time:
                    continue  # 消息太旧

                content = msg.get('content', '')
                if not content:
                    continue

                author = msg['author']['username']

                # 转北京时间展示
                cn_time = msg_dt.astimezone(timezone(timedelta(hours=8))).strftime('%H:%M')
                buffer.append(f"[{cn_time}] {author}: {content}")

            if not buffer:
                return None

            # API 返回是倒序的（最新在前），我们需要正序给 AI
            return "\n".join(reversed(buffer))

        except Exception as e:
            print(f"❌ Discord 连接失败: {e}")
            return None

    def _generate_mock_data(self):
        return """
[10:00] Mod_Alice: Verify your wallet in #verify-channel.
[10:05] Degen_Bob: Anyone saw the announcement? Mint price is 0.05 ETH.
[10:10] Degen_Charlie: Looks expensive for a bear market.
[11:00] Dev_Dave: We are delaying the mint by 2 hours due to a frontend bug.
[11:05] Degen_Bob: FUD! Is it a rug?
[12:00] Whale_Eve: Picking up some cheap floor sweeps.
"""