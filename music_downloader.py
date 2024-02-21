# music_downloader.py

import random
import yt_dlp

def generate_random_filename():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=10))

def download_music(url: str, temp_music_folder: str):

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'~/MusicBot/Temp_Music/{generate_random_filename()}',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            return filename + '.mp3', info_dict['title']
    except Exception as e:
        raise RuntimeError(f"Произошла ошибка при скачивании трека: {e}")
