from pyrogram import Client, filters
from pyrogram.types import Message,CallbackQuery
import requests
import json
from datetime import datetime
import random
from bot.helper.pyeval import run_code

import dotenv
import logging
from os import getenv

dotenv.load_dotenv('config.env')

logging.basicConfig(level=logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.INFO)

sudo_users = list(set(int(x) for x in os.environ.get("SUDO_USERS").split()))

bot = Client(
    name='yamato_bot',
    api_id=getenv("API_ID"),
    api_hash=getenv("API_HASH"),
    bot_token=getenv("BOT_TOKEN")
)

@bot.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    await message.reply("Hello, this bot can send game info and character info. Send /help to get more info.")

@bot.on_message(filters.user(sudo_users) & filters.incoming & filters.command('eval'))
async def eval(bot, message):
  await run_code(bot, message)

if __name__ == "__main__":
    bot.run()
