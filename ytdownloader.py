import os
from pytube import YouTube
import re

async def yt_to_mp3(video_url):
    print(f"Received video URL: {video_url}")
    try:
        video = YouTube(video_url)
        audio_stream = video.streams.filter(only_audio=True).first()
        if audio_stream is None:
            return "Hmm... I'm sorry, but I couldn't find an audio stream for the video."

        # Sanitize the file name
        filename = re.sub(r'[<>:"/\\|?*]', '', video.title) + ".mp3"
        audio_stream.download(filename=filename)

        output_filename = re.sub(r'[<>:"/\\|?*]', '', video.title) + "_converted.mp3"
        os.system(f'ffmpeg -i "{filename}" -b:a 320k "{output_filename}"')

        # Remove the original downloaded file
        os.remove(filename)

        return output_filename
    except Exception as e:
        return f"Oops! Failed to download the video: {str(e)}"