import yt_dlp

def Audio(URL, path):
        
        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'outtmpl': f"{path}\\%(title)s",
            'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            }],
            'ignoreerrors' : True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(URL)