import os
import EditMP3
import FindFiles
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, ttk

MusicFolder = 'C:/Users/niksu/Music/Juice WRLD'
files = os.listdir(MusicFolder)

window = tk.Tk()
window.geometry("700x500")
window.resizable(width=False, height=False)
window.title("Mana Muzik")

#Frames
TopBarF = tk.Frame(window)
FolderList = tk.Frame(window)
cover = tk.Frame(window)
editor = tk.Frame(window)

TitleF = tk.Frame(editor)
ArtistF = tk.Frame(editor)
YearF = tk.Frame(editor)
CommentF = tk.Frame(editor)
AlbumF = tk.Frame(editor)
GenreF = tk.Frame(editor)

#TopBar
AutoB = tk.Label(TopBarF, text="Automation")
def AutoClick(event):
    messagebox.showinfo(
        message=f"AutoB"
    )
AutoB.bind("<Button-1>", AutoClick)

Divide = tk.Label(TopBarF, text="|")
DirectoryL = tk.Label(TopBarF, text="Music Directory:")
MusicDirectory = tk.StringVar()
DirectoryE = tk.Entry(TopBarF, bd=3, textvariable=MusicFolder)

ComfirmB = tk.Button(TopBarF, text ="✔")
def Comfirm(event):
    messagebox.showinfo(
        message=f"ComfirmB"
    )
ComfirmB.bind("<Button-1>", Comfirm)

InfoB = tk.Label(TopBarF, text="INFO")
def Info(event):
    messagebox.showinfo(
        message=f"InfoB"
    )
InfoB.bind("<Button-1>", Info)

#Folder List Select 
DropMenu = ttk.Combobox(FolderList)
def DropMenuSelect(event):
    selection = DropMenu.get()
    messagebox.showinfo(
        message=f"DropMenu {selection}"
    )
DropMenu['values'] = ("---","Juice WRLD", "Playboi Carti","XXXTENTACION")
DropMenu.current(0)
DropMenu.bind("<<ComboboxSelected>>", DropMenuSelect)

scrollbar = tk.Scrollbar(FolderList)
listbox = tk.Listbox(FolderList, width=50, yscrollcommand = scrollbar.set)
for file in files:
    listbox.insert(tk.END, file)
scrollbar.config(command = listbox.yview)

#Cover
image = Image.open("C:/Users/niksu/OneDrive/New folder/Attēli/img_2547.webp")
new_size = (300, 300)
image = image.resize(new_size)
photo = ImageTk.PhotoImage(image)
CoverImage = tk.Label(cover, image=photo, background="black")

#Editor
Title = tk.Label(TitleF, text="Title:")
TitleInput = tk.StringVar()
TitleE = tk.Entry(TitleF,bd=3,textvariable=TitleInput)

Artist = tk.Label(ArtistF, text="Artist:")
ArtistInput = tk.StringVar()
ArtistE = tk.Entry(ArtistF,bd=3,textvariable=ArtistInput)

Year = tk.Label(YearF, text="Year:")
YearInput = tk.StringVar()
YearE = tk.Entry(YearF,bd=3,textvariable=YearInput)

Comment = tk.Label(CommentF, text="Comment:")
CommentInput = tk.StringVar()
CommentE = tk.Entry(CommentF,bd=3,textvariable=CommentInput)

Album = tk.Label(AlbumF, text="Album:")
AlbumInput = tk.StringVar()
AlbumE = tk.Entry(AlbumF,bd=3,textvariable=AlbumInput)

Genre = tk.Label(GenreF, text="Genre:")
GenreInput = tk.StringVar()
GenreE = tk.Entry(GenreF,bd=3,textvariable=GenreInput)

SaveB = tk.Button(window, text ="Save")
def Save(event):
    messagebox.showinfo(
        message=f"SaveB"
    )
SaveB.bind("<Button-1>", Save)

#Layout
TopBarF.pack(side="top",fill="x")
AutoB.pack(side="left",fill="both")
Divide.pack(side="left",fill="both")
DirectoryL.pack(side="left",fill="both")
DirectoryE.pack(side="left",fill="both", expand=True)
ComfirmB.pack(side="left",fill="both")
InfoB.pack(side="left",fill="both")

FolderList.pack(side="left",fill="y")
DropMenu.pack(side="top",fill="x")
listbox.pack(side="left",fill="y")
scrollbar.pack( side = "left", fill = "y")

cover.pack(side="top")
CoverImage.pack(side="top",fill="both", expand=True)

editor.pack(side="top",fill="both", expand=True)

TitleF.pack(side="top",fill="x")
Title.pack(side="left")
TitleE.pack(side="left",fill="x",expand=True)

ArtistF.pack(side="top",fill="x")
Artist.pack(side="left")
ArtistE.pack(side="left",fill="x",expand=True)

YearF.pack(side="top",fill="x")
Year.pack(side="left")
YearE.pack(side="left",fill="x",expand=True)

CommentF.pack(side="top",fill="x")
Comment.pack(side="left")
CommentE.pack(side="left",fill="x",expand=True)

AlbumF.pack(side="top",fill="x")
Album.pack(side="left")
AlbumE.pack(side="left",fill="x",expand=True)

GenreF.pack(side="top",fill="x")
Genre.pack(side="left")
GenreE.pack(side="left",fill="x",expand=True)

SaveB.pack(side="right",fill="both",expand=True)

window.mainloop()

def Program():
    MusicFolder = 'C:/Users/niksu/Music/Juice WRLD' #FindFiles.GetDirectory()
    FindFiles.VerifyFiles(MusicFolder)