import os
import time

try:
    import PySimpleGUI as sg
    from pytube import YouTube, Playlist
    import re
except ImportError:
    os.system("pip install pysimplegui")
    os.system("pip install pytube")

def main():

    sg.theme('DarkAmber')

    layout = [  [sg.Text("Enter the URL"), sg.InputText()],
                [sg.Text("Enter the PATH"), sg.InputText()],
                [sg.Button("Ok"), sg.Button("Cancel")] ]

    window = sg.Window("YT to MP3", layout)

    while True:
        event, values  = window.read()

        if event == "Ok":
           window.close()
           break

        if event == sg.WIN_CLOSED or event == "Cancel":
           exit()

    window.close()

    if "playlist" in str(values[0]): # detects if you're trying to download a playlist

        playlist = Playlist(str(values[0]))

        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

        for url in playlist.video_urls:
            yt = YouTube(url)
            video = yt.streams.filter(only_audio=True).first()
            destination = str((values[1]))
            out_file = video.download(output_path=destination)

            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
    else:
        yt = YouTube(str(values[0]))
        video = yt.streams.filter(only_audio=True).first()
        destination = str((values[1]))
        out_file = video.download(output_path=destination)

        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

    newLayout = [ [sg.Text(f"The .mp3 is downloaded in {destination}")],
    [sg.Button("Exit")], [sg.Button("Download")] ]

    newWindow = sg.Window("Successfully Downloaded!", newLayout)

    while True:
        event, values  = newWindow.read()

        if event == "Exit":
           window.close()
           break

        if event == "Download":
           newWindow.close()
           main()

        if event == sg.WIN_CLOSED or event == "Cancel":
           exit()

    newWindow.close()

main()
