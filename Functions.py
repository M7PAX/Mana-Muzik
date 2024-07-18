import os
from PIL import Image


# MusicFolder ='C:/Users/niksu/Music'

def GetMusicFolders(path):
    contents = os.listdir(path)
    music_folders = [item for item in contents if os.path.isdir(os.path.join(path, item))]
    return music_folders


def CheckFill(text):
    if text is None:
        text = ""
    return text


def FileChange(file_path, new_file):
    if file_path and "/" in file_path:
        last_slash_index = file_path.rfind("/")
        direction = file_path[:last_slash_index]
    NewPath = os.path.join(direction, new_file + ".mp3")
    os.rename(file_path, NewPath)


def GetImgFormat(img_path):
    try:
        with Image.open(img_path) as img:
            return img.format.lower()
    except Exception as e:
        print(f"Error: {e}")
        return None
