from pyrogram import Client, filters
from pyrogram.types import Message,CallbackQuery
import requests
import json
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

import dotenv
import logging
from os import getenv

dotenv.load_dotenv('config.env')

logging.basicConfig(level=logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.INFO)

client_id= getenv("CLIENT_ID")
access_token= getenv("CLIENT_TOKEN")

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
  await run_code(app, message)

if __name__ == "__main__":
    bot.run()
  
