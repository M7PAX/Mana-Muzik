import os
import MP3Info
import Functions
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import messagebox, ttk

# Directory = 'c:/'
#Contents = os.listdir(Directory)

window = tk.Tk()
window.geometry("800x600")#700x550
window.resizable(width=False, height=False)
window.title("Mana Muzik")

#Frames
TopBarF = tk.Frame(window)
FolderList = tk.Frame(window)
DropMenuF = tk.Frame(FolderList)
cover = tk.Frame(window)
editor = tk.Frame(window)

FileF = tk.Frame(editor)
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
DirectoryE = tk.Entry(TopBarF, bd=3)#textvariable=Directory

def CurrentDirectory():
    Entry = Path(DirectoryE.get())
    if Entry.is_dir():
        Directory = "/home/mipax/Music"#DirectoryE.get() c:/Users/niksu/Music
        return Directory

ComfirmB = tk.Button(TopBarF, text ="✔")
def Comfirm(event):
    Directory = CurrentDirectory()
    DropMenu['values'] = (Functions.GetMusicFolders(Directory))

ComfirmB.bind("<Button-1>", Comfirm)

InfoB = tk.Label(TopBarF, text="INFO")
def Info(event):
    messagebox.showinfo(
        message=f"InfoB"
    )
InfoB.bind("<Button-1>", Info)

#Folder List Select 
FolderL = tk.Label(DropMenuF, text="Forder:")
DropMenu = ttk.Combobox(DropMenuF, state="readonly")
def DropMenuSelect(event):
    CurrentDir = CurrentDirectory() + "/" + DropMenu.get()
    Contents = os.listdir(CurrentDir)
    ListboxUpdate(Contents)
DropMenu.bind("<<ComboboxSelected>>", DropMenuSelect)

Scrollbar = tk.Scrollbar(FolderList)
Listbox = tk.Listbox(FolderList, width=50, yscrollcommand = Scrollbar.set)
def ListboxSelect(SelectedText):
    CurrentDir = CurrentDirectory() + "/" + SelectedText
    return CurrentDir
def ListboxUpdate(Contents):
    Listbox.delete(0, tk.END)
    for Content in Contents:
        Listbox.insert(tk.END, Content)
    Scrollbar.config(command = Listbox.yview)
def ListboxSelected(event):
    SelectedIndex = Listbox.curselection()
    SelectedText = Listbox.get(SelectedIndex)
    FillFileE(SelectedText)
    CurrentDir = ListboxSelect(SelectedText)
    #FillTitleE()
    print(MP3Info.GetTitle(CurrentDir))
    ListboxSelect(SelectedText)
Listbox.bind("<<ListboxSelect>>", ListboxSelected)

#Cover
image = Image.open("/home/mipax/Pictures/uzinanimegirl.jpg")#C:/Users/niksu/OneDrive/New folder/Attēli/img_2547.webp
new_size = (300, 300)
image = image.resize(new_size)
photo = ImageTk.PhotoImage(image)
CoverImage = tk.Label(cover, image=photo, background="black")

#Editor
def FillFileE(FillText):
    FileE.delete(0, tk.END)
    period = FillText.rfind(".")
    if period != -1:
        UpdatedText = FillText[:period]
    FileE.insert(0, UpdatedText)
FileL = tk.Label(FileF, text="File:", width=8)
FileInput = tk.StringVar()
FileE = tk.Entry(FileF,bd=3,textvariable=FileInput)

def FillTitleE(FillText):
    TitleE.delete(0, tk.END)
    TitleE.insert(0, FillText)
TitleL = tk.Label(TitleF, text="Title:", width=8)
TitleInput = tk.StringVar()
TitleE = tk.Entry(TitleF,bd=3,textvariable=TitleInput)

ArtistL = tk.Label(ArtistF, text="Artist:", width=8)
ArtistInput = tk.StringVar()
ArtistE = tk.Entry(ArtistF,bd=3,textvariable=ArtistInput)

YearL = tk.Label(YearF, text="Year:", width=8)
YearInput = tk.StringVar()
YearE = tk.Entry(YearF,bd=3,textvariable=YearInput)

AlbumL = tk.Label(AlbumF, text="Album:", width=8)
AlbumInput = tk.StringVar()
AlbumE = tk.Entry(AlbumF,bd=3,textvariable=AlbumInput)

GenreL = tk.Label(GenreF, text="Genre:", width=8)
GenreInput = tk.StringVar()
GenreE = tk.Entry(GenreF,bd=3,textvariable=GenreInput)

CommentL = tk.Label(CommentF, text="Comment:", width=8)
CommentInput = tk.StringVar()
CommentE = tk.Entry(CommentF,bd=3,textvariable=CommentInput)

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
DropMenuF.pack(side="top",fill="x")
FolderL.pack(side="left")
DropMenu.pack(side="top",fill="x")
Listbox.pack(side="left",fill="y")
Scrollbar.pack( side="left",fill="y")

cover.pack(side="top")
CoverImage.pack(side="top",fill="both",expand=True,pady=(10,10))

editor.pack(side="top",fill="both",expand=True)

FileF.pack(side="top",fill="x")
FileL.pack(side="left")
FileE.pack(side="left",fill="x",expand=True,padx=(0,10))

TitleF.pack(side="top",fill="x")
TitleL.pack(side="left")
TitleE.pack(side="left",fill="x",expand=True,padx=(0,10))

ArtistF.pack(side="top",fill="x")
ArtistL.pack(side="left")
ArtistE.pack(side="left",fill="x",expand=True,padx=(0,10))

YearF.pack(side="top",fill="x")
YearL.pack(side="left")
YearE.pack(side="left",fill="x",expand=True,padx=(0,10))

AlbumF.pack(side="top",fill="x")
AlbumL.pack(side="left")
AlbumE.pack(side="left",fill="x",expand=True,padx=(0,10))

GenreF.pack(side="top",fill="x")
GenreL.pack(side="left")
GenreE.pack(side="left",fill="x",expand=True,padx=(0,10))

CommentF.pack(side="top",fill="x")
CommentL.pack(side="left")
CommentE.pack(side="left",fill="x",expand=True,padx=(0,10))

SaveB.pack(side="right",fill="both",expand=True)

window.mainloop()