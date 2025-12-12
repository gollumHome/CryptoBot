import asyncio
import qrcode
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError  # 引入新异常处理

# ================= 配置 =================
# 1. 代理 (你的端口是 10809)
PROXY = ('http', '127.0.0.1', 10809)

# 2. 官方 Key
API_ID = 6
API_HASH = 'eb06d4abfb49dc3eeb1aeb98ae0f581e'


# =======================================

async def main():
    print(f"🌍 正在连接 Telegram 服务器 (Proxy: {PROXY})...")

    client = TelegramClient(StringSession(), API_ID, API_HASH, proxy=PROXY)
    await client.connect()

    if not await client.is_user_authorized():
        print("🔄 正在请求登录二维码...")

        qr_login = await client.qr_login()

        # 打印二维码
        print("\n请用手机 Telegram 扫描下方二维码：")
        print("(设置 -> 设备 -> 连接桌面设备)")
        print("=========================================")
        qr = qrcode.QRCode()
        qr.add_data(qr_login.url)
        qr.print_ascii(invert=True)
        print("=========================================\n")

        try:
            # 等待扫码确认
            print("⏳ 等待扫码中...")
            await qr_login.wait()

        except SessionPasswordNeededError:
            # 🔥 核心修改：捕获两步验证错误
            print("\n🔐 检测到两步验证 (2FA) 已开启！")
            print("这是你设置的【云端密码】(Cloud Password)，不是手机验证码。")

            # 让用户输入密码
            pwd = input("请输入你的 2FA 密码: ")

            # 提交密码
            await client.sign_in(password=pwd)

    # 登录成功
    print("\n✅ 登录成功！")
    print("👇 请复制下方 Session String 填入 .env 文件：")
    print("-" * 60)
    print(client.session.save())
    print("-" * 60)

    await client.disconnect()


if __name__ == '__main__':
    asyncio.run(main())