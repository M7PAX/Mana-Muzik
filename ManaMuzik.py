import os
import io
import eyed3
import MP3Info
import Functions
import tkinterDnD
import tkinter as tk
from tkinter import *
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import messagebox, ttk 

window = tkinterDnD.Tk()

window.geometry("780x680")
window.minsize(780,680)

Ico = Image.open("Images/Mana.jpg")
IcoPhoto = ImageTk.PhotoImage(Ico)
window.wm_iconphoto(False, IcoPhoto)

window.title("Mana Muzik")

#Frames
TopBarF = tk.Frame(window)
FolderList = tk.Frame(window)
DropMenuF = tk.Frame(FolderList)
Cover = tk.Frame(window)
Editor = tk.Frame(window)

CoverF = tk.Frame(Editor)
FileF = tk.Frame(Editor)
TitleF = tk.Frame(Editor)
ArtistF = tk.Frame(Editor)
AlbumF = tk.Frame(Editor)
TnF = tk.Frame(Editor)
GenreF = tk.Frame(Editor)
YearF = tk.Frame(Editor)
CommentF = tk.Frame(Editor)

#TopBar
AutoB = tk.Label(TopBarF, text="Automation")
def AutoClick(event):
    messagebox.showinfo(
        message=f"Coming soon! Lil Bibby soon!"
    )
AutoB.bind("<Button-1>", AutoClick)

Divide = tk.Label(TopBarF, text="|")
ForlderDirL = tk.Label(TopBarF, text="Music Directory:")
MusicForlderDir = tk.StringVar()
ForlderDirE = tk.Entry(TopBarF,textvariable=MusicForlderDir)

def GetForderDir():
    Entry = Path(ForlderDirE.get())
    if Entry.is_dir():
        ForlderDir = "c:/Users/niksu/Music" # ForlderDirE.get()
        if ForlderDir.startswith('"') and ForlderDir.endswith('"'):
            ForlderDir = ForlderDir[1:-1]
        return ForlderDir

ComfirmB = tk.Button(TopBarF, text ="✔",bd=1)
def Comfirm(event):
    Dir = GetForderDir()
    if ('/' in Dir) == True:
        DropMenu['values'] = (Functions.GetMusicFolders(Dir))
ComfirmB.bind("<Button-1>", Comfirm)

InfoB = tk.Label(TopBarF, text="Tutorial/Info")
def Info(event):
    messagebox.showinfo(title="Info",
        message=f"""Tutorial and Instructions

1. Locate the "Music Directory" option in the top bar and add a directory, which is folder with a folder of each artist or have a folder of youre mp3 files.
2. Use the "Folders" drop-down menu to select the specific folder you want to work with.
3. In the listbox, choose the desired song that you want to edit. Begin the editing process, making any changes needed. Be sure to save your modifications when done.
Note: To update the album cover, drag and drop an image file (only supporting jpg, jpeg, and png formats) into the blank space where the cover would be displayed.

IMPORTANT Actions That May Cause Issues:
Avoid copying, highlighting text, or using the "Tab" key in the editor, as these actions will prevent changes from being saved.

Bugs:
In case the cover change doesn't work correctly, try removing the existing cover and then attempt to set it again.

These guidelines should help you navigate through the program smoothly. If you encounter any other feel free to reach out to me on GitHub at M7PAX.
""")
InfoB.bind("<Button-1>", Info)

#Folder List Select 
FolderL = tk.Label(DropMenuF, text="Forders:")
DropMenu = ttk.Combobox(DropMenuF, state="readonly")
def DropMenuSelect(event):
    CurrentDir = GetForderDir() + "/" + DropMenu.get()
    Contents = os.listdir(CurrentDir)
    ListboxUpdate(Contents)
DropMenu.bind("<<ComboboxSelected>>", DropMenuSelect)

def GetSelectedIndex():
    SelectedIndex = Listbox.curselection()
    if not SelectedIndex:
        return None
    else:
        return SelectedIndex
def GetCurrentDir():
        CurrentDir = GetForderDir() + "/" + DropMenu.get() + "/" + Listbox.get(GetSelectedIndex())
        return CurrentDir
def ListboxUpdate(Contents):
    Listbox.delete(0, tk.END)
    for Content in Contents:
        Listbox.insert(tk.END, Content)
    Scrollbar.config(command = Listbox.yview)

Scrollbar = tk.Scrollbar(FolderList)
Listbox = tk.Listbox(FolderList, width=60, yscrollcommand = Scrollbar.set)
def ListboxSelected(event):
    if DropMenu.get() == "":
        return
    else:
        FillFileE(Listbox.get(GetSelectedIndex()))
        CurrentDir = GetCurrentDir()
        RefreshPathE()
        FillTitleE(CurrentDir)
        FillArtistE(CurrentDir)
        FillCover(CurrentDir)
        FillAlbumE(CurrentDir)
        FillTnE(CurrentDir)
        FillGenreE(CurrentDir)
        FillYearE(CurrentDir)
        FillCommentE(CurrentDir)
Listbox.bind("<<ListboxSelect>>", ListboxSelected)

#Cover
ImgSize = (300, 300)
def FillCover(Path):
    audio = eyed3.load(Path)
    if audio.tag and audio.tag.images:
        for i in audio.tag.images: 
            img = ImageTk.PhotoImage(Image.open(io.BytesIO(i.image_data)).resize(ImgSize))
        CoverImage.image = img
        CoverImage.config(image=img)

        CoverDnD.pack_forget()
        CoverB.pack_forget()
        CoverImage.pack(side="top",fill="both",expand=True,pady=(10,0))
        CoverB.pack(side="top",fill="x",expand=True,pady=(0,10))
    else:
        CoverImage.pack_forget()
        CoverB.pack_forget()
        CoverDnD.pack(side="top",pady=(10,0))
        CoverB.pack(side="top",fill="x",expand=True,pady=(0,10))
CoverImage = tk.Label(Cover)

CoverB = tk.Button(Cover, text =" x ",bd=1)
def CoverRemove(event):
    audio = eyed3.load(GetCurrentDir())
    if audio.tag and audio.tag.images:
        if GetSelectedIndex() == None:
            return
        else:
            result = messagebox.askquestion("Remove or Cancel", "Do you want to remove the current cover?")
            if result == 'yes':
                MP3Info.RemoveCover(GetCurrentDir())
                CoverImage.pack_forget()
                CoverB.pack_forget()
                CoverDnD.pack(side="top",pady=(10,0))
                CoverB.pack(side="top",fill="x",expand=True,pady=(0,10))
            else:
                return
    else:
        messagebox.showwarning(title="Invalid",message=f"There is no image to remove!")
CoverB.bind("<Button-1>", CoverRemove)

CoverInput = StringVar()

def drop(event):
    CoverInput.set(event.data)

def drag_command(event):
    return (tkinterDnD.COPY, "DND_Text")

CoverL = tk.Label(CoverF,text="Cover:",width=8)
CoverE = Entry(CoverF,textvar=CoverInput)
CoverE.register_drop_target("*")
CoverE.bind("<<Drop>>", drop)
CoverE.register_drag_source("*")
CoverE.bind("<<DragInitCmd>>", drag_command)
CoverDnD = ttk.Label(Cover, ondrop=drop, ondragstart=drag_command,textvar=CoverInput,relief="solid",padding=142.4,width=3)

def RefreshPathE():
    CoverE.delete(0, tk.END)
PathB = tk.Button(CoverF, text=" x ",bd=1)
def RemovePath(event):
    CoverE.delete(0, tk.END)
PathB.bind("<Button-1>", RemovePath)

#Editor
def FillFileE(FillText):
    FileE.delete(0, tk.END)
    period = FillText.rfind(".")
    if period != -1:
        UpdatedText = FillText[:period]
    FileE.insert(0, UpdatedText)
FileL = tk.Label(FileF, text="File:", width=8)
FileInput = tk.StringVar()
FileE = tk.Entry(FileF,textvariable=FileInput)
FileB = tk.Button(FileF, text=" x ",bd=1)
def RemoveFile(event):
    FileE.delete(0, tk.END)
FileB.bind("<Button-1>", RemoveFile)

def FillTitleE(Path):
    TitleE.delete(0, tk.END)
    FillText = MP3Info.GetTitle(Path)
    TitleE.insert(0,Functions.CheckFill(FillText))
TitleL = tk.Label(TitleF, text="Title:", width=8)
TitleInput = tk.StringVar()
TitleE = tk.Entry(TitleF,textvariable=TitleInput)
TitleB = tk.Button(TitleF, text=" x ",bd=1)
def RemoveTitle(event):
    TitleE.delete(0, tk.END)
TitleB.bind("<Button-1>", RemoveTitle)

def FillArtistE(Path):
    ArtistE.delete(0, tk.END)
    FillText = MP3Info.GetArtist(Path)
    ArtistE.insert(0,Functions.CheckFill(FillText))
ArtistL = tk.Label(ArtistF, text="Artist:", width=8)
ArtistInput = tk.StringVar()
ArtistE = tk.Entry(ArtistF,textvariable=ArtistInput)
ArtistB = tk.Button(ArtistF, text=" x ",bd=1)
def RemoveArtist(event):
    ArtistE.delete(0, tk.END)
ArtistB.bind("<Button-1>", RemoveArtist)

def FillAlbumE(Path):
    AlbumE.delete(0, tk.END)
    FillText = MP3Info.GetAlbum(Path)
    AlbumE.insert(0,Functions.CheckFill(FillText))
AlbumL = tk.Label(AlbumF, text="Album:", width=8)
AlbumInput = tk.StringVar()
AlbumE = tk.Entry(AlbumF,textvariable=AlbumInput)
AlbumB = tk.Button(AlbumF, text=" x ",bd=1)
def RemoveAlbum(event):
    AlbumE.delete(0, tk.END)
AlbumB.bind("<Button-1>", RemoveAlbum)

def FillTnE(Path):
    TnE.delete(0, tk.END)
    FillText = MP3Info.GetTN(Path)
    TnE.insert(0,Functions.CheckFill(FillText))
TnL = tk.Label(TnF, text="TrackN:", width=8)
TnInput = tk.StringVar()
TnE = tk.Entry(TnF,textvariable=TnInput)
TnB = tk.Button(TnF, text=" x ",bd=1)
def RemoveTn(event):
    TnE.delete(0, tk.END)
TnB.bind("<Button-1>", RemoveTn)

def FillGenreE(Path):
    GenreE.delete(0, tk.END)
    FillText = MP3Info.GetGenre(Path)
    GenreE.insert(0,Functions.CheckFill(FillText))
GenreL = tk.Label(GenreF, text="Genre:", width=8)
GenreInput = tk.StringVar()
GenreE = tk.Entry(GenreF,textvariable=GenreInput)
GenreB = tk.Button(GenreF, text=" x ",bd=1)
def RemoveGenre(event):
    GenreE.delete(0, tk.END)
GenreB.bind("<Button-1>", RemoveGenre)

def FillYearE(Path):
    YearE.delete(0, tk.END)
    FillText = MP3Info.GetYear(Path)
    YearE.insert(0,Functions.CheckFill(FillText))
YearL = tk.Label(YearF, text="Year:", width=8)
YearInput = tk.StringVar()
YearE = tk.Entry(YearF,textvariable=YearInput)
YearB = tk.Button(YearF, text=" x ",bd=1)
def RemoveYear(event):
    YearE.delete(0, tk.END)
YearB.bind("<Button-1>", RemoveYear)

def FillCommentE(Path):
    CommentE.delete(0, tk.END)
    FillText = MP3Info.GetComment(Path)
    CommentE.insert(0,Functions.CheckFill(FillText))
CommentL = tk.Label(CommentF, text="Comment:", width=8)
CommentInput = tk.StringVar()
CommentE = tk.Entry(CommentF,textvariable=CommentInput)
CommentB = tk.Button(CommentF, text=" x ",bd=1)
def RemoveComment(event):
    CommentE.delete(0, tk.END)
CommentB.bind("<Button-1>", RemoveComment)

SaveB = tk.Button(window, text ="Save",bd=1)
def Save(event):
    if GetSelectedIndex() == None:
        return
    else:
        MP3Info.TitleChange(GetCurrentDir(),TitleE.get())
        MP3Info.ArtistChange(GetCurrentDir(),ArtistE.get())
        MP3Info.CoverChange(GetCurrentDir(),CoverE.get())
        MP3Info.AlbumChange(GetCurrentDir(),AlbumE.get())
        MP3Info.TnChange(GetCurrentDir(),TnE.get())
        MP3Info.GenreChange(GetCurrentDir(),GenreE.get())
        MP3Info.YearChange(GetCurrentDir(),YearE.get())
        MP3Info.CommentChange(GetCurrentDir(),CommentE.get())
        Functions.FileChange(GetCurrentDir(),FileE.get())
SaveB.bind("<Button-1>", Save)

#LAYOUT
#Topbar
TopBarF.pack(side="top",fill="x")
AutoB.pack(side="left",fill="both")
Divide.pack(side="left",fill="both")
ForlderDirL.pack(side="left",fill="both")
ForlderDirE.pack(side="left",fill="both", expand=True)
ComfirmB.pack(side="left",fill="both")
InfoB.pack(side="left",fill="both")

#Listbox
FolderList.pack(side="left",fill="y")
DropMenuF.pack(side="top",fill="x")
FolderL.pack(side="left")
DropMenu.pack(side="top",fill="x")
Listbox.pack(side="left",fill="y")
Scrollbar.pack( side="left",fill="y")

#Editor
Cover.pack(side="top")
CoverDnD.pack(side="top",pady=(10,0))
CoverB.pack(side="top",fill="x",expand=True,pady=(0,10))

Editor.pack(side="top",fill="both",expand=True)

CoverF.pack(side="top",fill="x",pady=10)
CoverL.pack(side="left")
CoverE.pack(side="left",fill="x",expand=True,ipady=2)
PathB.pack(side="right",padx=(0,10))

#file, title, artist, album, tn, genre, year, comment
FileF.pack(side="top",fill="x")
FileL.pack(side="left")
FileE.pack(side="left",fill="x",expand=True,ipady=2)
FileB.pack(side="right",padx=(0,10))

TitleF.pack(side="top",fill="x",pady=(5,0))
TitleL.pack(side="left")
TitleE.pack(side="left",fill="x",expand=True,ipady=2)
TitleB.pack(side="right",padx=(0,10))

ArtistF.pack(side="top",fill="x",pady=(5,0))
ArtistL.pack(side="left")
ArtistE.pack(side="left",fill="x",expand=True,ipady=2)
ArtistB.pack(side="right",padx=(0,10))

AlbumF.pack(side="top",fill="x",pady=(5,0))
AlbumL.pack(side="left")
AlbumE.pack(side="left",fill="x",expand=True,ipady=2)
AlbumB.pack(side="right",padx=(0,10))

TnF.pack(side="top",fill="x",pady=(5,0))
TnL.pack(side="left")
TnE.pack(side="left",fill="x",expand=True,ipady=2)
TnB.pack(side="right",padx=(0,10))

GenreF.pack(side="top",fill="x",pady=(5,0))
GenreL.pack(side="left")
GenreE.pack(side="left",fill="x",expand=True,ipady=2)
GenreB.pack(side="right",padx=(0,10))

YearF.pack(side="top",fill="x",pady=(5,0))
YearL.pack(side="left")
YearE.pack(side="left",fill="x",expand=True,ipady=2)
YearB.pack(side="right",padx=(0,10))

CommentF.pack(side="top",fill="x",pady=(5,0))
CommentL.pack(side="left")
CommentE.pack(side="left",fill="x",expand=True,ipady=2)
CommentB.pack(side="right",padx=(0,10))

SaveB.pack(side="right",fill="both",expand=True)

window.mainloop()