from flask import Flask, render_template, request
import re
from youtubeDownloader import downloadWithRes, downloadBestRes
from onlyAudio import Audio

app= Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('Home.html')

@app.route("/downloadAudio", methods = ["GET", "POST"])
def downloadAudio():
    message = ''
    errorType = 0
    if request.method == 'POST' and 'audio_url' in request.form:
            youtubeUrl = request.form["audio_url"]
            if(youtubeUrl):
                validateVideoUrl = (
                r'(https?://)?(www\.)?'
                '(youtube|youtu|youtube-nocookie)\.(com|be)/'
                '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
                
                validVideoUrl = re.match(validateVideoUrl, youtubeUrl)
                if validVideoUrl:
                    URL = youtubeUrl
                    Audio(URL)    
                    message = 'Audio Downloaded Successfully!!!'
                    errorType = 1
                else:
                    message = 'Enter a valid URL'
                    errorType = 0
            else:
                message = 'Enter Youtube Video URL.. '
                errorType = 0
    return render_template('youtube_Audio.html', message = message, errorType = errorType)


@app.route("/downloadVideo", methods= ["GET", "POST"])
def downloadVideo():
    message = ''
    errorType = 0
    if request.method == 'POST' and 'video_url' in request.form:
        youtubeUrl = request.form["video_url"]
        if(youtubeUrl):
            validateVideoUrl = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
            
            validVideoUrl = re.match(validateVideoUrl, youtubeUrl)
            
            if validVideoUrl:

                URL = youtubeUrl
                res = request.form.get('format')
                sponsor = request.form.get('sponsor')

                if (res != 'Best'):

                    if(downloadWithRes(URL, res, sponsor) == True):
                        message = 'Video Downloaded Successfully!!!'
                        errorType = 1
                    else:
                        message = 'Video Resolution Not Available'
                        errorType = 0
                else:

                    if(downloadBestRes(URL, sponsor) == True):
                        message = 'Video Downloaded Successfully!!!'
                        errorType = 1
                    else:
                        message = 'Video Resolution Not Available'
                        errorType = 0
            else:
                message = 'Enter a valid URL'
                errorType = 0
        else:
            message = 'Enter Youtube Video URL.. '
            errorType = 0
    return render_template('youtube_Video.html', message = message, errorType = errorType)

if __name__ == "__main__":
    app.run()