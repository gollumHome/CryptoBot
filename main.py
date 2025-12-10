import asyncio
from config.settings import (
    TG_TARGET_GROUPS, DISCORD_TARGET_CHANNELS, TIME_WINDOW_HOURS,
    WEBHOOK_URL_TG, WEBHOOK_URL_DISCORD
)
from core.telegram_client import TgScraper
from core.discord_client import DiscordScraper  # 新增
from core.ai_engine import GeminiAnalyst
from core.notifier import WeChatNotifier


async def run_task():
    print(">>> 全渠道情报系统启动...")

    # 初始化所有组件
    tg_scraper = TgScraper()
    dc_scraper = DiscordScraper()  # 新增
    analyst = GeminiAnalyst()
    notifier = WeChatNotifier()

    # ==========================
    # 任务 1: 处理 Telegram
    # ==========================
    if TG_TARGET_GROUPS:
        print("\n--- 📡 开始处理 Telegram 群组 ---")
        try:
            for group in TG_TARGET_GROUPS:
                if not group['enabled']: continue
                print(f">>> [TG] 正在抓取: {group['name']}")

                # 拉取
                chat_log = await tg_scraper.fetch_messages(group['id'], hours=TIME_WINDOW_HOURS)
                if not chat_log:
                    print("    (无新消息)")
                    continue

                # 分析
                report = analyst.analyze(chat_log, group['name'], TIME_WINDOW_HOURS)

                # 推送 -> 传入 TG 专用的 Webhook
                notifier.send_report(group['name'], report, webhook_url=WEBHOOK_URL_TG)

                await asyncio.sleep(5)
        except Exception as e:
            print(f"TG 任务异常: {e}")
        finally:
            await tg_scraper.close()

    # ==========================
    # 任务 2: 处理 Discord
    # ==========================
    if DISCORD_TARGET_CHANNELS:
        print("\n--- 🎮 开始处理 Discord 频道 ---")
        try:
            for channel in DISCORD_TARGET_CHANNELS:
                if not channel['enabled']: continue
                print(f">>> [Discord] 正在抓取: {channel['name']}")

                # 拉取 (同步方法，不需要 await，但可以在 async 函数里调)
                chat_log = dc_scraper.fetch_messages(channel['id'], hours=TIME_WINDOW_HOURS)
                if not chat_log:
                    print("    (无新消息)")
                    continue

                # 分析
                report = analyst.analyze(chat_log, channel['name'], TIME_WINDOW_HOURS)

                # 推送 -> 传入 Discord 专用的 Webhook
                notifier.send_report(channel['name'], report, webhook_url=WEBHOOK_URL_DISCORD)

                await asyncio.sleep(5)
        except Exception as e:
            print(f"Discord 任务异常: {e}")

    print("\n>>> 所有任务执行完毕")


if __name__ == "__main__":
    asyncio.run(run_task())