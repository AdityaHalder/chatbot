import asyncio, logging, os, sys

from os import getenv
from dotenv import load_dotenv
from typing import Union, List, Pattern
from pyrogram import Client, filters, idle
from logging.handlers import RotatingFileHandler
from motor.motor_asyncio import AsyncIOMotorClient


logging.basicConfig(
    format="[%(name)s]:: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    handlers=[
        RotatingFileHandler("logs.txt", maxBytes=(1024 * 1024 * 5), backupCount=10),
        logging.StreamHandler(),
    ],
)

logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

logs = logging.getLogger()
loop = asyncio.get_event_loop()


if os.path.exists("Config.env"):
    load_dotenv("Config.env")

API_ID = int(getenv("API_ID", 0))
API_HASH = getenv("API_HASH", None)
BOT_TOKEN = getenv("BOT_TOKEN", None)
MONGO_DB_URL = getenv("MONGO_DB_URL", None)
OWNER_ID = int(getenv("OWNER_ID", 0))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", 0))
START_IMAGE_URL = getenv("START_IMAGE_URL", None)


def cdx(commands: Union[str, List[str]]):
    return filters.command(commands, ["/", "!", "."])

def cdz(commands: Union[str, List[str]]):
    return filters.command(commands, ["", "/", "!", "."])

def rgx(pattern: Union[str, Pattern]):
    return filters.regex(pattern)


bot = Client(
    name="adixd",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

mdb = AsyncIOMotorClient(MONGO_DB_URL).test







async def main():
    






@bot.on_message(filters.command("start") & filters.private)
async def start_message_private(client, message):
    user_id = message.from_user.id
    mention = message.from_user.mention
    caption = f"""**✅ Hello, {mention},

❍  I am an advanced & powerful
ai chat bot powered by open ai, I
can help you if you need.

❍  You can add me in your chat,
i can chat with known/unknown
chat members in your chat.**"""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🥀 Add Me In Your Chat ✨",
                    url=f"https://t.me/{bot.me.username}?startgroup=true",
                )
            ]
        ]
    )
    return await message.reply_text(text=caption, reply_markup=buttons)





if __name__ == "__main__":
    loop.run_until_complete(main())

