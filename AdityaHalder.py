import asyncio, logging, os, sys

from os import getenv
from dotenv import load_dotenv
from typing import Union, List, Pattern
from judini import CodeGPTPlus
from pyrogram import Client, filters, idle
from pyrogram.enums import ChatAction
from pyrogram.types import (
    ChatPermissions,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
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
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)


logs = logging.getLogger()
loop = asyncio.get_event_loop()


if os.path.exists("Config.env"):
    load_dotenv("Config.env")

API_ID = int(getenv("API_ID", 0))
API_HASH = getenv("API_HASH", None)
BOT_TOKEN = getenv("BOT_TOKEN", None)
MONGO_DB_URL = getenv("MONGO_DB_URL", None)
CODEGPT_API_KEY = getenv("CODEGPT_API_KEY", None)
CODEGPT_ORG_ID = getenv("CODEGPT_ORG_ID", None)
CODEGPT_AGENT_ID = getenv("CODEGPT_AGENT_ID", None)
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
    if API_ID == 0:
        logs.info("'API_ID' - Not Found !!")
        sys.exit()
    if not API_HASH:
        logs.info("'API_HASH' - Not Found !!")
        sys.exit()
    if not BOT_TOKEN:
        logs.info("'BOT_TOKEN' - Not Found !!")
        sys.exit()
    if not MONGO_DB_URL:
        logs.info("'MONGO_DB_URL' - Not Found !!")
        # sys.exit()
    if not CODEGPT_API_KEY:
        logs.info("'CODEGPT_API_KEY' - Not Found !!")
        sys.exit()
    if not CODEGPT_ORG_ID:
        logs.info("'CODEGPT_ORG_ID' - Not Found !!")
        sys.exit()
    if not CODEGPT_AGENT_ID:
        logs.info("'CODEGPT_AGENT_ID' - Not Found !!")
        sys.exit()
    if OWNER_ID == 0:
        logs.info("'OWNER_ID' - Not Found !!")
        sys.exit()
    if LOG_GROUP_ID == 0:
        logs.info("'LOG_GROUP_ID' - Not Found !!")
        sys.exit()
    if not START_IMAGE_URL:
        logs.info("'START_IMAGE_URL' - Not Found !!")
        # sys.exit()
    for file in os.listdir():
        if file.endswith(".session"):
            os.remove(file)
    for file in os.listdir():
        if file.endswith(".session-journal"):
            os.remove(file)
    try:
        await bot.start()
        try:
            await bot.send_message(
                LOG_GROUP_ID, "**✅ Now, I am Alive❗**"
            )
        except Exception:
            logs.info(f"🚫 Failed to access log group !!\n⚠️ Reason: {e}")
            sys.exit()
        logs.info("✅ Bot Started❗")
        await idle()
    except Exception as e:
        logs.info(f"🚫 Failed to start bot !!\n⚠️ Reason: {e}")
        sys.exit()
    
codegpt = CodeGPTPlus(
    api_key=CODEGPT_API_KEY, org_id=CODEGPT_ORG_ID
)

async def chat_with_gpt(query):
    messages = [
        {
            "role": "user", "content": query
        }
    ]
    chat = codegpt.chat_completion(
        agent_id=CODEGPT_AGENT_ID, messages=messages
    )
    return chat


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


@bot.on_message(cdx(["caesar", "cipher"]) & filters.private)
async def caesar_cipher_private(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "**⚠️ Give me a some text to convert❗...**"
        )
    aux = await message.reply_text("**🔄 Converting ✨...**")
    query = message.text.split(None, 1)[1]
    strings = "!\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    output_text = ""
    for s in query:
        x = strings.split(s)[1]
        lenth_x = len(x)
        if lenth_x > 2:
            o_text = x[2]
        elif lenth_x == 0:
            o_text = strings[2]

        elif lenth_x == 1:
            o_text = strings[1]

        elif lenth_x == 2:
            o_text = strings[0]
        output_text = output_text + o_text
    return await aux.edit(f"**🐬 Converted text:**\n```output\n{output_text}```")






@bot.on_message(filters.text & ~filters.bot)
async def start_chat_(client, message):
    if not message.command:
        if message.from_user:
            user_id = message.from_user.id
        elif message.sender_chat:
            user_id = message.sender_chat.id
        if message.reply_to_message:
            if message.reply_to_message.from_user:
                if (
                    message.reply_to_message.from_user.id != bot.me.id
                    and message.reply_to_message.from_user.id != user_id
                ):
                    return
            if message.reply_to_message.sender_chat:
                if message.reply_to_message.sender_chat.id != user_id:
                    return
        try:
            chat_id = message.chat.id
            await bot.send_chat_action(chat_id, ChatAction.TYPING)
            try:
                response = await chat_with_gpt(message.text)
                return await message.reply_text(response)
            except Exception as e:
                logs.info(f"🚫 Error: {e}")
                return await message.reply_text("🤭")
        except Exception:
            return
        




if __name__ == "__main__":
    loop.run_until_complete(main())

