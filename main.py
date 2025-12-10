import asyncio
# 只导入配置参数，不导入模板
from config.settings import TARGET_GROUPS, TIME_WINDOW_HOURS
from core.telegram_client import TgScraper
from core.ai_engine import GeminiAnalyst
from core.notifier import WeChatNotifier


async def run_task():
    print(">>> 系统启动...")

    # 初始化
    scraper = TgScraper()
    analyst = GeminiAnalyst()
    notifier = WeChatNotifier()

    try:
        for group in TARGET_GROUPS:
            if not group['enabled']:
                continue

            print(f"--- 处理群组: {group['name']} ---")

            # 1. 获取数据
            chat_log = await scraper.fetch_messages(group['id'], hours=TIME_WINDOW_HOURS)
            if not chat_log:
                print("   跳过: 无新消息")
                continue

            # 2. 调用分析 (内部会自动读取 settings.py 里的 Prompt)
            report = analyst.analyze(chat_log, group['name'], TIME_WINDOW_HOURS)

            # 3. 发送通知
            notifier.send_report(group['name'], report)

            # 随机延时防封
            await asyncio.sleep(5)

    finally:
        await scraper.close()
        print(">>> 任务完成")


if __name__ == "__main__":
    asyncio.run(run_task())