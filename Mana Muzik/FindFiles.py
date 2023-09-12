import os

def GetDirectory():
    return input("Input the MP3 files directory.\n-> ")

def VerifyFiles(path):
    files = os.listdir(path)
    MP3Files = 0
    Files = 0
    for file in files:
        if not file.endswith(".mp3"):
            Files += 1
        else:
            MP3Files += 1
    return print(f"Folder has {MP3Files} MP3, {Files} other files.")
