import yt_dlp

def Audio(URL, path, downLabel, progressbar):

    def progressHook(d):
        if d['status'] == 'downloading':
            downloaded_percent = int((d["downloaded_bytes"]*100)/d["total_bytes"])
            downLabel.configure(text=f'Progress: {downloaded_percent}%')
            progressbar.set(downloaded_percent/100)

    def processingHook(d):
        if d['status'] == 'started':
            downLabel.configure(text='Processing Video...')
        elif d['status'] == 'finished':
            downLabel.configure(text='Processing Complete')

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': f"{path}\\%(title)s",
        'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
        }],
        'ignoreerrors' : True,
        'progress_hooks':[progressHook],
        'postprocessor_hooks': [processingHook],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(URL)