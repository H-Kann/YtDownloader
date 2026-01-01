
<p align="center"><img src="https://github.com/H-Kann/YtDownloader/assets/100532697/7f0a95f6-9e90-4613-9a2c-94cdbf8a5bf6"/></p>

>[!IMPORTANT]
> There are two versions of this app, the web app and desktop versions.
> 
> The desktop version is in the releases section on the right, just download the latest version, install ffmpeg and the app.
>
> For advanced users: The dependencies that are needed located below.
</span>
<br>

# Features
- Download Youtube videos with the highest quality possible.
- Download high quality extracted audio from the videos.
- Download songs from Youtube Music.
- Sponsorblock integration.
- Light and Dark mode.
<br>

# Screenshots
![Dark](https://github.com/H-Kann/YtDownloader/assets/100532697/c8406894-b75d-454d-aca8-315f16f9c930)
![Light](https://github.com/H-Kann/YtDownloader/assets/100532697/18fb6480-4fb4-495a-a069-75c766748718)





# YtDownloader required package

## Ffmpeg
[Download ffmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z)

### Instructions to install FFmpeg
1. Extract the zip file 
2. Copy the contents of the extracted folder
3. Navigate to the root of the C drive
4. Make a new folder "ffmpeg"

5. Paste the contents of the extracted folder into it
6. Should look like this<br>
![Screenshot 2023-10-09 201442](https://github.com/H-Kann/YtDownloader/assets/100532697/c9cfd322-c2c9-447b-bbc1-fba001ba9359)

### Instructions to add Ffmpeg to Windows PATH
1. Go to start and search for "edit the system environment variables"
![sysVar_1](https://github.com/H-Kann/YtDownloader/assets/100532697/5d7db415-31fd-4c9f-9dd2-6fc670fc433f)

2. Go to the advanced tab
3. Click "Environment Variables" button<br>
![sysVar_2](https://github.com/H-Kann/YtDownloader/assets/100532697/13ff660c-99e0-40bb-8444-f9946f229c64)

4. Select Path from the list and click Edit<br>![sysVar_3](https://github.com/H-Kann/YtDownloader/assets/100532697/27fa7d07-1ba5-44c7-ace4-9651b2a9c2db)

5. Click New and paste the location of the bin folder, Should be something like this C:\ffmpeg\bin<br>![sysVar_4](https://github.com/H-Kann/YtDownloader/assets/100532697/994f4a1d-af27-4e35-b5b3-45321558b8c8)

6. Click Ok, Ok and Ok


## YtDownloader web app dependencies

## Flask
```bash
pip install flask
```
## yt_dlp
```bash
pip install -U "yt-dlp[default]"
```
## YtDownloader desktop dependencies

## yt_dlp
```bash
pip install -U "yt-dlp[default]"
```
## CustomTkinter
```bash
pip install customtkinter
```
