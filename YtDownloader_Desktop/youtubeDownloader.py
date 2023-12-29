import yt_dlp


def downloadBestRes(URL, sponsor, path, downLabel, progressbar):
    
    def format_selector(ctx):
        
            # Sorting format best to worst
            formats = ctx.get('formats')[::-1]
            
            # Getting video without audio
            best_video = next(f for f in formats
                            if f['vcodec'] != 'none' and f['acodec'] == 'none')

            # Finding compatible audio extension
            audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]


            # Geting audio without video
            best_audio = next(f for f in formats if (
                f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))


            # These are the minimum required fields for a merged format
            yield {
                'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
                'ext': best_video['ext'],
                'requested_formats': [best_video, best_audio],
                # Must be + separated list of protocols
                'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
            }

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

            
    if (sponsor):
        
        ydl_opts = {
            'format': format_selector,
            'outtmpl': f"{path}\\%(title)s",
            'postprocessors': 
                [
                    {  
                        'key': 'SponsorBlock',
                        'categories': ['sponsor', 'intro', 'outro', 'selfpromo', 'preview', 'filler', 'interaction']
                    },
                    {
                        'key': 'ModifyChapters', 
                        'remove_sponsor_segments': ['sponsor', 'intro', 'outro', 'selfpromo', 'preview', 'filler', 'interaction']
                    }
                ],
                'progress_hooks':[progressHook],
                'postprocessor_hooks': [processingHook],
        }
    else:
        
        ydl_opts = {
            'format': format_selector,
            'outtmpl': f"{path}\\%(title)s",
            'progress_hooks':[progressHook],
            'postprocessor_hooks': [processingHook],
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(URL)
        return True


def downloadWithRes(URL, res, sponsor, path, downLabel, progressbar):
    # Cleaning
    if res == '4K':
        newRes = '2160p'
    #else:
        #newres = res.replace("p", "")

    def checkRes(URL, newRes):

        ydl_opts1  = {
            "quiet": "true"
        }
        with yt_dlp.YoutubeDL(ydl_opts1) as y:
           video_info = y.extract_info(URL, download = False)

        
        formats = video_info['formats'][::-1]

        # Checking if the format is supported in the video
        for f in formats:
            if newRes in f['format']:
                found = True
                return found
            

    def format_selector(ctx):
        
            # Sorting format best to worst
            formats = ctx.get('formats')[::-1]
            
            # Getting video without audio
            best_video = next(f for f in formats
                            if f['vcodec'] != 'none' and f['acodec'] == 'none' and res in f['format'])

            # Finding compatible audio extension
            audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]

            # Geting audio without video
            best_audio = next(f for f in formats if (
                f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))


            # These are the minimum required fields for a merged format
            yield {
                'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
                'ext': best_video['ext'],
                'requested_formats': [best_video, best_audio],
                # Must be + separated list of protocols
                'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
            }

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

    if (checkRes(URL, res)):
        
        if(sponsor):
            ydl_opts = {
                'format': format_selector,
                'outtmpl': f"{path}\\%(title)s",
                'postprocessors': 
                [
                    {  
                        'key': 'SponsorBlock',
                        'categories': ['sponsor', 'intro', 'outro', 'selfpromo', 'preview', 'filler', 'interaction']
                    },
                    {
                        'key': 'ModifyChapters', 
                        'remove_sponsor_segments': ['sponsor', 'intro', 'outro', 'selfpromo', 'preview', 'filler', 'interaction']
                    }
                ],
                'progress_hooks':[progressHook],
                'postprocessor_hooks': [processingHook],
            }
        
        else:
             ydl_opts = {
                'format': format_selector,
                'outtmpl': f"{path}\\%(title)s",
                'progress_hooks':[progressHook],
                'postprocessor_hooks': [processingHook],
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(URL)
            return True
    else:
        return False
    

    


    