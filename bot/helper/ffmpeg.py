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
            filepath,
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
