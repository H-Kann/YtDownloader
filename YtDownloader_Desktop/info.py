def progressHook(d, downLabel, progressbar):
    # Update label and progress bar with download progress
    if d['status'] == 'downloading':
        downloaded_percent = int((d["downloaded_bytes"]*100)/d["total_bytes"])
        downLabel.configure(text=f'Progress: {downloaded_percent}%')
        progressbar.set(downloaded_percent/100)

def processingHook(d, downLabel):
    # Show video processing progress
    if d['status'] == 'started':
        downLabel.configure(text='Processing Video...')
    elif d['status'] == 'finished':
        downLabel.configure(text='Processing Complete')