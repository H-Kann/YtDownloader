import customtkinter as ctk
import youtubeDownloader, onlyAudio
from threading import Thread
from tkinter import filedialog
from plyer import notification
from os.path import exists
from configparser import ConfigParser


ctk.set_appearance_mode("dark")

root = ctk.CTk()


def progressNotification(title:str, message:str):
    progressbar.stop()

    notification.notify(
        title = title,
        message = message,
        app_name='YTDownloader',
    )


def thread():
    # Start thread to keep the progress bar running while downloading
    t1 = Thread(target = saveDir)
    t1.start()


def configIni()->str:
    # save configuration to file
    path = filedialog.askdirectory()
    config = ConfigParser()
    config["DEFAULT"]= {
        "PATH" : path,
        }
    
    with open("config.ini", "w") as f:
        config.write(f)
    return path


def setDir(path:str):

    frame2 = ctk.CTkFrame(master = frame, fg_color="transparent")
    frame2.pack(pady =20, padx=60, fill="both", expand = True)

    downloadDirectory = ctk.CTkLabel(master = frame2, font=("Roboto", 15), text="Download Directory: ")
    downloadDirectory.pack(side="left", padx=(10,10))

    dir = ctk.StringVar(value=path)
    downDir= ctk.CTkEntry(master = frame2, textvariable=dir, width=300, state="readonly")
    downDir.pack(side="left")

    
    buttonChange = ctk.CTkButton(master = frame2, text = "Change Dir", command=lambda: changeDir(dir), fg_color="#ee2a42", hover_color = "#b90039")
    buttonChange.pack(side="left", padx=(5,0))

def saveDir():
    # Check if configuration file exists
    if not exists(".\\config.ini"):

        path = configIni()
        
        setDir(path)
        download(path)

    else:
        config = ConfigParser()
        config.read("config.ini")
        path = config["DEFAULT"]["PATH"]
        download(path)
        
def changeDir(dir:ctk.StringVar):
    dir.set(value= configIni())

def download(path:str):

    
    progressbar.configure(mode='indeterminate')
    progressbar.start()
    
    # Get url, resolution and user option for SponsorBlock
    url = entry1.get()
    res = qualitySelect.get()
    sponsor = checkboxSponsor.get()

    # Check if the user choose only audio option
    if checkboxAudio.get() == 1:

        # Only Audio Download
        onlyAudio.Audio(url, path)

        progressbar.configure(mode='determinate')
        progressbar.set(1)

        # Send Notification
        progressNotification('Download Progress', 'Download Complete!!!')
    
        
    else:
        # Selected Quality Download
        if res != "Best Quality":

            if(youtubeDownloader.downloadWithRes(url, res, sponsor, path) == False):
                
                progressbar.stop()

                # Send Notification
                progressNotification('Download Failed', 'Resolution not available')

            else:
                progressbar.configure(mode='determinate')
                progressbar.set(1)

                # Send Notification
                progressNotification('Download Progress', 'Download Complete!!!')
                
        else:
            # Best Quality Download
            youtubeDownloader.downloadBestRes(url, sponsor, path)

            progressbar.configure(mode='determinate')
            progressbar.set(1)

            # Send Notification 
            progressNotification('Download Progress', 'Download Complete!!!')

  
# CustomTkinter Widgets
frame = ctk.CTkFrame(master = root)
frame.pack(pady =20, padx=60, fill="both", expand = True)

label = ctk.CTkLabel(master = frame, text = "Youtube Downloader", font = ("Roboto", 24))
label.pack(pady = 12, padx = 10)

entry1 = ctk.CTkEntry(master = frame, placeholder_text="Enter URL...", width=500)
entry1.pack(pady = 12, padx = 10)

qualities= ["Best Quality", "4K", "1440p", "1080p", "720p", "480p", "360p", "144p"]
qualitySelect = ctk.CTkComboBox(master = frame, values=qualities, border_color = "#ee2a42", button_color = "#ee2a42")
qualitySelect.pack(pady = 12, padx = 10)


buttonDownload = ctk.CTkButton(master = frame, text = "Download", command=thread, fg_color="#ee2a42", hover_color = "#b90039")
buttonDownload.pack(pady = 12, padx = 10)

checkboxAudio = ctk.CTkCheckBox(master = frame, text = "Audio only", fg_color="#ee2a42", hover_color = "#b90039")
checkboxAudio.pack(pady=20)

checkboxSponsor = ctk.CTkCheckBox(master = frame, text = "Use SponsorBlock", fg_color="#ee2a42", hover_color = "#b90039")
checkboxSponsor.pack(padx=(34,0))

progressbar = ctk.CTkProgressBar(master=frame, orientation="horizontal", progress_color="#ee2a42", mode="indeterminate")
progressbar.pack(pady=20)

if exists(".\\config.ini"):

    config = ConfigParser()
    config.read("config.ini")
    path = config["DEFAULT"]["PATH"]
    root.geometry("847x485")
    setDir(path)

root.mainloop()