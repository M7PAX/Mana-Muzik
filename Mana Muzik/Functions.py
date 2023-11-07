import os

MusicFolder ='C:/Users/niksu/Music'

def GetMusicFolders(Directory):
    contents = os.listdir(Directory)
    MusicFolders = [item for item in contents if os.path.isdir(os.path.join(Directory, item))]
    return MusicFolders

