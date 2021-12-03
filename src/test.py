import os
from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest

client = TelegramClient(
    os.environ.get("session_name", "replier"),
    os.environ.get("telegram_api_id"),
    os.environ.get("telegram_api_hash"),
    proxy=None
)

with client:
    async def getUser():
        full = await client(GetFullUserRequest("khanghou"))
        print(full)

    getUser()