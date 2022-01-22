import asyncio
import os
import sys
import json
import time
import ffmpeg
import subprocess
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

async def encode(filepath):
    basefilepath, extension = os.path.splitext(filepath)
    output_filepath = basefilepath + '.mp4'
    progress = output_directory + "/" + "progress.txt"
    with open(progress, 'w') as f:
      pass
  
    file_genertor_command = [
            "ffmpeg",
            "-hide_banner",
            "quiet",
            "-progress",
            progress,
            "-i",
            video_file,
            "-c:v",
            "h264",
            "-preset",
            "veryfast",
            "-crf",
            "26",
            "-c:a",
            "copy",
            "-map",
            "0",
            out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

def get_thumbnail(in_filename, path, ttl):
    out_filename = os.path.join(path, str(time.time()) + ".jpg")
    open(out_filename, 'a').close()
    try:
        (
            ffmpeg
            .input(in_filename, ss=ttl)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return out_filename
    except ffmpeg.Error as e:
      return None

def get_duration(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has('duration'):
      return metadata.get('duration').seconds
    else:
      return 0

def get_width_height(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has('width') and metadata.has('height'):
      return metadata.get("width"), metadata.get("height")
    else:
      return 1280, 720
