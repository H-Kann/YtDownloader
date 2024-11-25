import customtkinter as ctk
import youtubeDownloader, onlyAudio
from contextMenu import ContextMenu
from threading import Thread
from tkinter import filedialog
from plyer import notification
from os.path import exists
from configparser import ConfigParser
from PIL import Image



ctk.set_appearance_mode("dark")
root = ctk.CTk(fg_color=("#F9FAFA", "#242424"))
root.title("YtDownloader")
root.iconbitmap('.\\YtDownloader.ico')
# Color palette
hoverColor1 = "#b90039"
hoverColor2 = "#ee2a42"
fgColor1 = ("#D8DADB", "#4a4d50")
fgColor2 = ("#f1f3f4", "#2b2b2b")
txtColor1 = ("black","white")

def progressNotification(title:str, message:str):

    # Display notification
    notification.notify(
        title = title,
        message = message,
        app_name='YTDownloader',
        app_icon = '.\\YtDownloader.ico',
    )
    
def thread():
    # Start thread to keep the progress bar running while downloading
    t1 = Thread(target = saveDir)
    t1.start()


def configIni()->str:
    # Save configuration
    path = filedialog.askdirectory()
    config = ConfigParser()
    config["DEFAULT"]= {
        "PATH" : path,
        "UI": switchVar.get(),
        }
    
    # Write to config.ini
    with open("config.ini", "w") as f:
        config.write(f)
    return path

def setDir(path:str):
    # Create the rest of the widgets after setting a download directory
    root.geometry("847x610")
    frame2 = ctk.CTkFrame(master = frame, fg_color="transparent")
    frame2.pack(pady =20, padx=(60,0), fill="both", expand = True)

    downloadDirectory = ctk.CTkLabel(master = frame2, font=("Roboto", 15), text="Download Directory: ")
    downloadDirectory.pack(side="left", padx=(10,10))

    dir = ctk.StringVar(value=path)
    downDir= ctk.CTkEntry(master = frame2, textvariable=dir, width=300, state="readonly", fg_color = fgColor2)
    downDir.pack(side="left")

    buttonChange = ctk.CTkButton(master = frame2, text = "Change Directory", command=lambda: changeDir(dir), fg_color=hoverColor2, hover_color = hoverColor1, text_color=txtColor1)
    buttonChange.pack(side="left", padx=(5,0))
    
def saveDir():
    if not exists(".\\config.ini"):
        # Create config.ini, save path and start download
        path = configIni()
        setDir(path)
        download(path)
    else:
        # Get path from config.ini and start download
        config = ConfigParser()
        config.read("config.ini")
        path = config["DEFAULT"]["PATH"]
        download(path)
        
def changeDir(dir:ctk.StringVar):
    # Change directory in config.ini and textbox 
    dir.set(value= configIni())

def download(path:str):
    # Get url, resolution and user option for SponsorBlock
    url = entry1.get()
    res = qualitySelect.get()
    sponsor = checkboxSponsor.get()

    # Check if the user chose only audio option
    if checkboxAudio.get() == 1:

        # Only Audio Download
        if(onlyAudio.Audio(url, path, downLabel, progressbar)):
            # Send Notification
            progressNotification('Download Progress', 'Download Complete!!!')
        else:
            progressNotification('Error', 'Download Failed')
    
        
    else:
        # Selected Quality Download
        if res != "Best Quality":
            if(youtubeDownloader.downloadWithRes(url, res, sponsor, path, downLabel, progressbar) == False):
                # Send Notification
                progressNotification('Download Failed', 'Resolution not available')

            else:
                # Send Notification
                progressNotification('Download Progress', 'Mp4 extension not found, Webm used instead')
                
        else:
            # Best Quality Download
            if(youtubeDownloader.downloadBestRes(url, sponsor, path, downLabel, progressbar)):
                 # Send Notification 
                progressNotification('Download Progress', 'Download Complete!!!')
            else:
                progressNotification('Error', 'Download Failed')

def changeColor(mode:str):
    # Change to light or dark mode
    ctk.set_appearance_mode(mode)
    UiSwitch.configure(text = mode.capitalize()+ " Mode")

def callChangeColor():
    # Check what mode the UI is on and change accordingly
    if switchVar.get() == "off":
        changeColor("light")
    else:
        changeColor("dark")

def changeUi():
    # Check if the UI is fully available
    if not exists(".\\config.ini"):
        callChangeColor()
    else:
        callChangeColor()
        editConfig()

def editConfig():
    # Change the mode choice in the configuration file
    config = ConfigParser()
    config.read(".\\config.ini")
    cnfFile = open(".\\config.ini", "w")
    config.set("DEFAULT", "UI", switchVar.get())
    config.write(cnfFile)
    cnfFile.close()


def do_popup(event, frame):
    # Open the popup menu 
    try: frame.popup(event.x_root, event.y_root)
    finally: frame.grab_release()
        
def copy_text():
        # Copy text operation
        frame.clipboard_clear()
        
        try: frame.clipboard_append(entry1.get())
        except: pass
    
def cut_text():
    # Cut text operation
    copy_text()
    try: entry1.delete(ctk.SEL_FIRST, ctk.SEL_LAST)
    except: pass

def paste():
    try:
        entry1.insert(entry1.index('insert'), root.clipboard_get())
    except: pass

def paste_text():
    # paste text operation
    if entry1.select_present():
        entry1.delete(0, 'end')
        paste()
    else:
        paste()


def changeSwitchText(switchVar):
    UiSwitch.configure(variable=switchVar)
    UiSwitch.pack(pady=20)

# CustomTkinter Widgets
frame = ctk.CTkFrame(master = root, fg_color=fgColor2)
frame.pack(pady =20, padx=60, fill="both", expand = True)

logo = ctk.CTkImage(light_image=Image.open(".\\Logo.png"), dark_image=Image.open(".\\Logo.png"), size=(300,90))
label = ctk.CTkLabel(master = frame, image=logo, text="", font = ("Roboto", 24))
label.pack(pady = 12, padx = 10)


entry1 = ctk.CTkEntry(master = frame, placeholder_text="Enter URL...", width=500, fg_color = fgColor2)
entry1.pack(pady = 12, padx = 10)


float_window = ContextMenu(master = frame)
entry1.bind("<Button-3>", lambda event :do_popup(event, float_window))

ctxMenuButton = ctk.CTkButton(float_window.frameMenu, text="Copy", text_color=txtColor1, fg_color="transparent", hover_color=hoverColor2, command = copy_text)
ctxMenuButton.pack(expand=True, fill="x", padx=10, pady=(10,0))

ctxMenuButton2 = ctk.CTkButton(float_window.frameMenu, text="Paste", text_color=txtColor1, fg_color="transparent", hover_color=hoverColor2, command = paste_text)
ctxMenuButton2.pack(expand=True, fill="x", padx=10, pady=(5,0))

ctxMenuButton3 = ctk.CTkButton(float_window.frameMenu, text="Cut", text_color=txtColor1, fg_color="transparent", hover_color=hoverColor2, command = cut_text)
ctxMenuButton3.pack(expand=True, fill="x", padx=10, pady=(5,10))



qualities= ["Best Quality", "4K", "1440p", "1080p", "720p", "480p", "360p", "144p"]
qualitySelect = ctk.CTkOptionMenu(master = frame, values=qualities, button_color = hoverColor2, button_hover_color = hoverColor1, fg_color = fgColor1, text_color=txtColor1, dropdown_hover_color = hoverColor2, corner_radius = 7, dropdown_text_color=txtColor1)
qualitySelect.pack(pady = 12, padx = 10)


buttonDownload = ctk.CTkButton(master = frame, text = "Download", command=thread, fg_color=hoverColor2, hover_color = hoverColor1, text_color=txtColor1)
buttonDownload.pack(pady = 12, padx = 10)

checkboxAudio = ctk.CTkCheckBox(master = frame, text = "Audio only", fg_color=hoverColor2, hover_color = hoverColor1)
checkboxAudio.pack(pady=20)

checkboxSponsor = ctk.CTkCheckBox(master = frame, text = "Use SponsorBlock", fg_color=hoverColor2, hover_color = hoverColor1)
checkboxSponsor.pack(padx=(35,0))

progressbar = ctk.CTkProgressBar(master=frame, orientation="horizontal", progress_color=hoverColor2, fg_color=fgColor1)
progressbar.set(0)
progressbar.pack(pady=20)

downLabel = ctk.CTkLabel(master = frame, text='')
downLabel.pack()

if exists(".\\config.ini"):
    # Loading user preferences saved in the configuration file
    config = ConfigParser()
    config.read("config.ini")
    path = config["DEFAULT"]["PATH"]

    UiSwitch = ctk.CTkSwitch(master = frame, progress_color=hoverColor2, onvalue="on", offvalue="off", fg_color=fgColor1, command=changeUi)
    
    if config["DEFAULT"]["UI"] == "off":
        switchVar = ctk.StringVar(value = "off")
        changeSwitchText(switchVar)
        changeColor("light")

    else:
        switchVar = ctk.StringVar(value = "on")
        changeSwitchText(switchVar)
        changeColor("dark")

    root.geometry("847x600")
    setDir(path)
else:
    switchVar = ctk.StringVar(value="on")
    UiSwitch = ctk.CTkSwitch(master = frame, progress_color=hoverColor2, onvalue="on", offvalue="off", text="Dark Mode", variable=switchVar, command=changeUi)
    UiSwitch.pack(pady=20)

# Run the app
root.mainloop()