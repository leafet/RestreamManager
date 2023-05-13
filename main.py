import os
import sys
import subprocess
import logging
from tkinter import *
from tkinter import ttk

logging.basicConfig(level=logging.INFO)
sys.path.append('../')
from obswebsocket import obsws, requests  # noqa: E402

root = Tk()
root.title("StreamManager")
root.geometry("650x200")
root.resizable(False, False)

root.title("Stream Manager")

style = ttk.Style()
style.configure('TButton', background='black')
style.configure('TButton', foreground='green')

host = "localhost"
port = 4455
password = "secret"

ws = obsws(host, port, password)

cwd = os.getcwd()


def runMonaserver():
    f = open("StartMonaserver.bat", "w")
    f.write(cwd[0].lower() + ": \n" + "cd " + cwd + "\n" + "MonaServer.exe")
    f.close()
    subprocess.Popen([cwd + r"\StartMonaserver.bat"])


def runObs():
    path = pathEntry.get()
    f = open("StartObs.bat", "w")
    f.write(path[0].lower() + ": \n" + "cd " + path + "\n" + "obs64.exe")
    f.close()
    subprocess.Popen([cwd + r"\StartObs.bat"])


def connectToWebSockets():
    ws.connect()


def beginStream():
    ws.call(requests.StartStream())


def runRestream():
    rtmplist = RTMPentry.get()
    rtmplist = rtmplist.split()
    newRTMPList = []
    for i in range(len(rtmplist)):
        currentRTMP = rtmplist[i]
        currentRTMP = "[f=flv]" + currentRTMP + "|"
        newRTMPList.append(currentRTMP)
    finalRTMPlist = "".join(newRTMPList)
    finalRTMPlist = finalRTMPlist[:-1]
    finalRTMPString = 'ffmpeg -i rtmp://localhost:1935/live/stream -c:v copy -c:a copy -map 0 -f tee "' + finalRTMPlist + '"'

    f = open("StartFfmpeg.bat", "w")
    f.write(cwd[0].lower() + ": \n" + "cd " + cwd + "\n" + finalRTMPString)
    f.close()
    subprocess.Popen([cwd + r"\StartFfmpeg.bat"])


def mainSequence():
    runObs()
    runMonaserver()
    connectToWebSockets()
    beginStream()
    runRestream()


def endAll():
    ws.call(requests.StopStream())
    os.system('taskkill /f /im MonaServer.exe')
    os.system('taskkill /f /im ffmpeg.exe')
    ws.disconnect()


mainBorder = ttk.Frame(root)
mainBorder.pack(padx=10, pady=10, fill='x', expand=True)

pathLabel = ttk.Label(mainBorder, text="Path to obs64.exe")
pathLabel.pack(fill="x", expand=True)

pathEntry = Entry(mainBorder)
pathEntry.pack(fill="x", expand=True)

ttk.Label(mainBorder, text="enter RTMP servers").pack(fill="x", expand=True)
RTMPentry = Entry(mainBorder)
RTMPentry.pack(fill="x", expand=True)

ttk.Button(mainBorder, text="StartStream", command=lambda: mainSequence()).pack(pady=5, fill="x")
ttk.Button(mainBorder, text="EndStream", command=lambda: endAll()).pack(pady=5, fill="x")

root.mainloop()
