from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv

load_dotenv()

# 如果 .env 没填，这里手动输入
api_id = os.getenv("TG_API_ID") or input("请输入 API ID: ")
api_hash = os.getenv("TG_API_HASH") or input("请输入 API HASH: ")

with TelegramClient(StringSession(), int(api_id), api_hash) as client:
    print("\n请复制下面这一行 (TG_SESSION_STRING):")
    print("--------------------------------------------------")
    print(client.session.save())
    print("--------------------------------------------------")
    print("将此字符串填入 .env 文件或 GitHub Secrets")