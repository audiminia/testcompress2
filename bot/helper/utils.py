import os
from bot import data, download_dir
from pyrogram.types import Message
from .ffmpeg import encode, get_thumbnail

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
        duration = get_duration(new_file)
        thumb = get_thumbnail(new_file, download_dir, duration / 4)
        width, height = get_width_height(new_file)
        msg.edit("```Uploading video...```")
        message.reply_video(new_file, thumb=thumb, caption=filename, duration=duration, width=width, height=height, parse_mode=None)
        os.remove(new_file)
        os.remove(thumb)
        msg.edit("```Video Encoded to x265```")
      else:
        msg.edit("```Something wents wrong while encoding your file. Make sure it is not already in HEVC format.```")
        os.remove(filepath)
    except Exception as e:
      msg.edit(f"```{e}```")
    on_task_complete()
