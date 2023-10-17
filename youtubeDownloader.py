import yt_dlp


def downloadBestRes(URL, sponsor):

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


    if(sponsor == 'True'):
         
        ydl_opts = {
            'format': format_selector,
            'outtmpl': "\\Downloads\\%(title)s",
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
                ]
        }
    else:
        
        ydl_opts = {
            'format': format_selector,
            'outtmpl': "\\Downloads\\%(title)s",
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(URL)

    return True


def downloadWithRes(URL, res, sponsor):
    
    def checkRes(URL, res):

        ydl_opts1  = {
            "quiet": "true"
        }
        with yt_dlp.YoutubeDL(ydl_opts1) as y:
           video_info = y.extract_info(URL, download = False)

        
        formats = video_info['formats']

        # Checking if the format is supported in the video
        for f in formats:
            if res in f['format']:
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


    if (checkRes(URL, res)):

        if(sponsor == 'True'):
             
            ydl_opts = {
                'format': format_selector,
                'outtmpl': "\\Downloads\\%(title)s",
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
                ]
            }
        
        else:
            ydl_opts = {
                'format': format_selector,
                'outtmpl': "\\Downloads\\%(title)s",
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(URL)
            return True
    else:
        return False
    

    


    