import os
import EditMP3
import FindFiles
import tkinter as tk
from PIL import Image, ImageTk

MusicFolder = 'C:/Users/niksu/Music/Juice WRLD'
files = os.listdir(MusicFolder)

window = tk.Tk()
window.geometry("1000x700")
window.title("Mana Muzik")

#frames
TopBarF = tk.Frame(window)
FolderList = tk.Frame(window)
editor = tk.Frame(window)
info = tk.Frame(editor)
text = tk.Frame(editor)

#top bar
AutoB = tk.Label(TopBarF, text="Automation")
DirectoryL = tk.Label(TopBarF, text="Music Directory")
DirectoryE = tk.Entry(TopBarF, bd=3)
ComfirmB = tk.Button(TopBarF, text ="✔")
InfoB = tk.Label(TopBarF, text="INFO")



def AutoClick(event):
    print("c")

AutoB.bind("<Button-1>", AutoClick)


#listbox
listbox = tk.Listbox(FolderList, width=60)
for file in files:
    listbox.insert(tk.END, file)

#editbox
infobox = tk.Label(editor, text="x", bg="red")
infobox2 = tk.Label(editor, text="x", bg="blue")
infobox3 = tk.Label(editor, text="x", bg="black")

#cover
image = Image.open("C:/Users/niksu/OneDrive/New folder/Attēli/img_2547.webp")
new_size = (100, 100)
image = image.resize(new_size)
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(window, image=photo, background="green")

#layouy
TopBarF.pack(side="top",fill="x")

AutoB.pack(side="left",fill="both")
DirectoryL.pack(side="left",fill="both")
DirectoryE.pack(side="left",fill="both", expand=True)
ComfirmB.pack(side="left",fill="both")
InfoB.pack(side="left",fill="both")

FolderList = tk.Frame(window)

listbox.pack(side="left",fill="y")
#image_label.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=10, pady=10)

#infobox.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)
#infobox2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)
#editor.pack(fill=tk.BOTH, expand=True)


#resize
def on_window_resize(event):
    new_height = event.height // 10
    listbox.config(height=new_height)
    
window.bind("<Configure>", on_window_resize)

window.mainloop()

def Program():
    MusicFolder = 'C:/Users/niksu/Music/Juice WRLD' #FindFiles.GetDirectory()
    FindFiles.VerifyFiles(MusicFolder)
