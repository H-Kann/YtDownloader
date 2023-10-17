import customtkinter as ctk
import youtubeDownloader, onlyAudio


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.geometry("800x350")



def download():
    

    URL = entry1.get()
    res = qualitySelect.get()
    sponsor = checkboxSponsor.get()

    if checkboxAudio.get() == 1:
        # Only Audio Download
        onlyAudio.Audio(URL)
        downloadLabel.configure(text = "Download Complete!!!")
       
        
    else:
        # Selected Quality Download
        if res != "Best Quality":

            if(youtubeDownloader.downloadWithRes(URL, res, sponsor) == False):
                downloadLabel.configure(text = "Resolution not available")
            else:
                downloadLabel.configure(text = "Download Complete!!!")
                
        else:
            # Best Quality Download
            youtubeDownloader.downloadBestRes(URL)
            downloadLabel.configure(text = "Download Complete!!!")
            
            
frame = ctk.CTkFrame(master = root)
frame.pack(pady =20, padx=60, fill="both", expand = True)

label = ctk.CTkLabel(master = frame, text = "Youtube Downloader", font = ("Roboto", 24))
label.pack(pady = 12, padx = 10)

entry1 = ctk.CTkEntry(master = frame, placeholder_text="Enter URL...", width=500)
entry1.pack(pady = 12, padx = 10)

qualities= ["Best Quality", "4K", "1440p", "1080p", "720p", "480p", "360p", "144p"]
qualitySelect = ctk.CTkComboBox(master = frame, values=qualities, border_color = "#ee2a42", button_color = "#ee2a42")
qualitySelect.pack(pady = 12, padx = 10)

button = ctk.CTkButton(master = frame, text = "Download", command=download, fg_color="#ee2a42", hover_color = "#b90039")
button.pack(pady = 12, padx = 10)

checkboxAudio = ctk.CTkCheckBox(master = frame, text = "Audio only", fg_color="#ee2a42", hover_color = "#b90039")
checkboxAudio.pack(pady = 12, padx = (220,0) ,side = 'left')

checkboxSponsor = ctk.CTkCheckBox(master = frame, text = "Use SponsorBlock", fg_color="#ee2a42", hover_color = "#b90039")
checkboxSponsor.pack(pady = 12, padx = (0,150), side = 'right')

downloadLabel = ctk.CTkLabel(master = frame, text = "")
downloadLabel.pack(pady = 12)



root.mainloop()