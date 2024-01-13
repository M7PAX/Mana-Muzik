import os

# MusicFolder ='C:/Users/niksu/Music'

def GetMusicFolders(Path):
    Contents = os.listdir(Path)
    MusicFolders = [item for item in Contents if os.path.isdir(os.path.join(Path, item))]
    return MusicFolders

def CheckFill(text):
    if text == None:
        text = ""
    return text

def FileChange(FilePath,NewFile):
    if FilePath and "/" in FilePath:
        last_slash_index = FilePath.rfind("/")
        Dir = FilePath[:last_slash_index]
    NewPath = os.path.join(Dir,NewFile+".mp3")
    os.rename(FilePath,NewPath)