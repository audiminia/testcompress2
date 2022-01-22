import os
from bot import data, download_dir
from pyrogram.types import Message
from .ffmpeg import encode

def on_task_complete():
    del data[0]
    if len(data) > 0:
      add_task(data[0])

def add_task(message: Message):
    try:
      msg = message.reply_text("```Downloading video...```", quote=True)
      filepath = message.download(file_name=download_dir)
      msg.edit("```Encoding video...```")
      new_file = encode(filepath)
      if new_file:
        msg.edit("```Video Encoded, getting metadata...```")

        msg.edit("```Uploading video...```")
        message.reply_document(new_file, caption=filename)
        os.remove(new_file)
        os.remove(thumb)
        msg.edit("```Video Encoded to x264```")
      else:
        msg.edit("```Something wents wrong while encoding your file. Make sure it is not already in HEVC format.```")
        os.remove(filepath)
    except Exception as e:
      msg.edit(f"```{e}```")
    on_task_complete()
