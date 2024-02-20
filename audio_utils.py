import yt_dlp

async def get_audio_info(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'noplaylist': True,
        'ffmpeg_location': '/usr/bin/ffmpeg',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', 'Unknown Title')
        audio_url = info.get('url', None)
        return title, audio_url