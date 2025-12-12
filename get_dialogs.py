import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# ==========================================
# 1. 你的 Session String (确保是刚才生成的，没有任何空格)
# 我直接把你刚才贴出来的填进去了
SESSION_STRING = '1BVtsOIQBuwySQdPeQtMJbH5vVhdm4vQV5M09TPgwv4A7ycERwB5aKlDft2pezr9y4_l3B5HYN9okVcnQpqWnswLK7U4MlRIT4W-u8XGzsA6WauYO1WT_mxFINNIdBc0egBsEijDiNHeCUcLqwvJ27kaZGsgzsrzHv09TRTiEan09y7H1ggMvcYbrzhK5Y2EGsAlTKIGWRi1T7BeHH94sEHpXVJQ2_BOA2jVmCqR6O5Zcwhy-PqfmRiAKqPLK4for4zP0gcYtUuZFyVY3yMCqwJr7uevKVJ6CT2w7UXQOL1akkKIEzxsk1F52DUKNyRXuJBjm2FJ6pboZB0O9Q-77hvKX0Xl4K00='

# 2. 官方 Key
API_ID = 6
API_HASH = 'eb06d4abfb49dc3eeb1aeb98ae0f581e'

# 3. 代理 (确保端口 10809 是对的)
PROXY = ('http', '127.0.0.1', 10809)


# ==========================================

async def main():
    print(f"🌍 [1/3] 正在通过代理 {PROXY} 连接 Telegram...")

    # 强制去除可能存在的空格
    clean_session = SESSION_STRING.strip()

    # 初始化
    client = TelegramClient(StringSession(clean_session), API_ID, API_HASH, proxy=PROXY)

    try:
        # 使用 connect() 而不是 start()，这样不会触发交互式登录
        await client.connect()
    except Exception as e:
        print(f"❌ 连接服务器失败: {e}")
        return

    print("🔍 [2/3] 正在验证 Session 有效性...")

    # 核心检查：到底登录没登录？
    if not await client.is_user_authorized():
        print("\n❌ 严重错误：Session 无效或已过期！")
        print("原因可能是：")
        print("1. 生成 Session 的 IP 和现在运行的 IP 变动太大，被 TG 踢下线了。")
        print("2. Session 字符串在复制时缺失了字符。")
        print("3. 这个 Session 已经被用过了（有时 Session 是一次性的）。")
        print("\n👉 解决办法：请重新运行 get_session_qr.py 重新扫码生成一个新的！")
        return

    print("✅ 登录验证通过！我是：" + (await client.get_me()).first_name)
    print("\n📜 [3/3] 正在获取群组列表...\n")
    print("=" * 60)

    # 获取列表
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            safe_title = dialog.title.replace('"', "'").replace('\n', ' ')
            # 打印结果
            print(f'{{"id": {dialog.id}, "name": "{safe_title}", "enabled": True}},')

    print("=" * 60)


if __name__ == '__main__':
    asyncio.run(main())