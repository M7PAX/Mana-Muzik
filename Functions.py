import os
from PIL import Image
from tkinter import messagebox


# MusicFolder ='C:/Users/niksu/Music'

def AutoClick():
    messagebox.showinfo(
        message=f"Coming soon! Lil Bibby soon!"
    )


def Info():
    messagebox.showinfo(title="Info",
                        message=f"""
Tutorial and Instructions

1. Locate the "Music Directory" option in the top bar and add a directory, which is folder with a folder of each 
artist or have a folder of your mp3 files. 2. Use the "Folders" drop-down menu to select the specific folder you 
want to work with. 3. In the listbox, choose the desired song that you want to edit. Begin the editing process, 
making any changes needed. Be sure to save your modifications when done. Note: To update the album cover, 
drag and drop an image file (only supporting jpg, jpeg, and png formats) into the blank space where the cover would be displayed.

Bugs:
In case the cover change doesn't work correctly, try removing the existing cover and then attempt to set it again.

These guidelines should help you navigate through the program smoothly. If you encounter any other feel free to reach out to me on GitHub at M7PAX. 
""")


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
        slash = file_path.rfind("/")
        directory = file_path[:slash]
    NewPath = os.path.join(directory, new_file + ".mp3")
    os.rename(file_path, NewPath)


def GetImgFormat(img_path):
    try:
        with Image.open(img_path) as img:
            return img.format.lower()
    except Exception as e:
        print(f"Error: {e}")
        return None


def GetFileName(fill_text):
    period = fill_text.rfind(".")
    if period != -1:
        fill_text = fill_text[:period]

    return fill_text


def GetDirectoryFile(fill_text):
    last_slash_index = fill_text.rfind('/')
    return fill_text[last_slash_index + 1:]
