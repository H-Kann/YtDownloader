import yt_dlp

def Audio(URL):
        
        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'outtmpl': "\\Downloads\\%(title)s",
            'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(URL)