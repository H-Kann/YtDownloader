import yt_dlp
from info import progressHook, processingHook, checkErrorCode
def Audio(URL, path, downLabel, progressbar):

    # yt_dlp options
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': f"{path}\\%(title)s",
        'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        }],
        'ignoreerrors' : True,
        'progress_hooks':[lambda d: progressHook(d, downLabel, progressbar)],
        'postprocessor_hooks': [lambda d: processingHook(d, downLabel)],
        'extractor_args':{'youtube': {'skip': ['dash']}}
    }
    # Start download with chosen options
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        errorcode = ydl.download(URL)
        if (checkErrorCode(errorcode)):
            return True
        else:
            return False