import customtkinter as ctk
import youtubeDownloader, onlyAudio
from threading import Thread
from tkinter import filedialog
from plyer import notification
from os.path import exists
from configparser import ConfigParser


ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("YtDownloader")
root.iconbitmap('.\YtDownloader.ico')

def progressNotification(title:str, message:str):
    progressbar.stop()

    notification.notify(
        title = title,
        message = message,
        app_name='YTDownloader',
        app_icon = '.\YtDownloader.ico',
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
        "UI": switchVar.get(),
        }
    
    with open("config.ini", "w") as f:
        config.write(f)
    return path


def setDir(path:str):
    root.geometry("847x600")
    frame2 = ctk.CTkFrame(master = frame, fg_color="transparent")
    frame2.pack(pady =20, padx=(60,0), fill="both", expand = True)

    downloadDirectory = ctk.CTkLabel(master = frame2, font=("Roboto", 15), text="Download Directory: ")
    downloadDirectory.pack(side="left", padx=(10,10))

    dir = ctk.StringVar(value=path)
    downDir= ctk.CTkEntry(master = frame2, textvariable=dir, width=300, state="readonly")
    downDir.pack(side="left")

    buttonChange = ctk.CTkButton(master = frame2, text = "Change Directory", command=lambda: changeDir(dir), fg_color="#ee2a42", hover_color = "#b90039", text_color=("black", "white"))
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
    
    # Get url, resolution and user option for SponsorBlock
    url = entry1.get()
    res = qualitySelect.get()
    sponsor = checkboxSponsor.get()

    # Check if the user choose only audio option
    if checkboxAudio.get() == 1:

        # Only Audio Download
        onlyAudio.Audio(url, path, downLabel, progressbar)

        # Send Notification
        progressNotification('Download Progress', 'Download Complete!!!')
    
        
    else:
        # Selected Quality Download
        if res != "Best Quality":

            if(youtubeDownloader.downloadWithRes(url, res, sponsor, path, downLabel, progressbar) == False):

                # Send Notification
                progressNotification('Download Failed', 'Resolution not available')

            else:

                # Send Notification
                progressNotification('Download Progress', 'Download Complete!!!')
                
        else:
            # Best Quality Download
            youtubeDownloader.downloadBestRes(url, sponsor, path, downLabel, progressbar)

            # Send Notification 
            progressNotification('Download Progress', 'Download Complete!!!')

def changeColor(switchLabel:str, frameColor:str, mode:str, windowColor:str, progressColor:str):

    UiSwitch.configure(text = switchLabel)
    frame.configure(fg_color = frameColor)
    ctk.set_appearance_mode(mode)
    root.configure(fg_color = windowColor)
    progressbar.configure(fg_color = progressColor)

def callChangeColor():
    if switchVar.get() == "off":
        changeColor("Light Mode", "#f1f3f4", "light", "#F9FAFA", "#D8DADB")
    else:
        changeColor("Dark Mode", "#2b2b2b", "dark", "#242424", "#4a4d50")

def changeUi():
    if not exists(".\\config.ini"):
        callChangeColor()
    else:
        callChangeColor()
        editConfig()

def editConfig():
    # Edit configuration to file
    config = ConfigParser()
    config.read(".\\config.ini")
    cnfFile = open(".\\config.ini", "w")
    config.set("DEFAULT", "UI", switchVar.get())
    config.write(cnfFile)
    cnfFile.close()

        
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


buttonDownload = ctk.CTkButton(master = frame, text = "Download", command=thread, fg_color="#ee2a42", hover_color = "#b90039", text_color=("black", "white"))
buttonDownload.pack(pady = 12, padx = 10)

checkboxAudio = ctk.CTkCheckBox(master = frame, text = "Audio only", fg_color="#ee2a42", hover_color = "#b90039")
checkboxAudio.pack(pady=20)

checkboxSponsor = ctk.CTkCheckBox(master = frame, text = "Use SponsorBlock", fg_color="#ee2a42", hover_color = "#b90039")
checkboxSponsor.pack(padx=(35,0))

progressbar = ctk.CTkProgressBar(master=frame, orientation="horizontal", progress_color="#ee2a42")
progressbar.set(0)
progressbar.pack(pady=20)

downLabel = ctk.CTkLabel(master = frame, text='')
downLabel.pack()

if exists(".\\config.ini"):
    config = ConfigParser()
    config.read("config.ini")
    path = config["DEFAULT"]["PATH"]
    if config["DEFAULT"]["UI"] == "off":
        switchVar = ctk.StringVar(value="off")
        UiSwitch = ctk.CTkSwitch(master = frame, progress_color="#ee2a42", onvalue="on", offvalue="off", text="Dark Mode", variable=switchVar, command=changeUi)
        UiSwitch.pack(pady=20)
        changeColor("Light Mode", "#f1f3f4", "light", "#F9FAFA", "#D8DADB")
    else:
        switchVar = ctk.StringVar(value="on")
        UiSwitch = ctk.CTkSwitch(master = frame, progress_color="#ee2a42", onvalue="on", offvalue="off", text="Dark Mode", variable=switchVar, command=changeUi)
        UiSwitch.pack(pady=20)
        changeColor("Dark Mode", "#2b2b2b", "dark", "#242424", "#4a4d50")

    root.geometry("847x600")
    setDir(path)
else:
    switchVar = ctk.StringVar(value="on")
    UiSwitch = ctk.CTkSwitch(master = frame, progress_color="#ee2a42", onvalue="on", offvalue="off", text="Dark Mode", variable=switchVar, command=changeUi)
    UiSwitch.pack(pady=20)



root.mainloop()