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
FolderListF = tk.Frame(window)
CoverF = tk.Frame(window)
EditorF = tk.Frame(window)

class TopBar:
    def __init__(self, parent):
        self.parent = parent

        self.AutoB = tk.Label(TopBarF, text="Automation")
        self.AutoB.bind("<Button-1>", self.AutoClick)

        self.Divide = tk.Label(TopBarF, text="|")
        self.ForlderDirL = tk.Label(TopBarF, text="Music Directory:")
        self.MusicForlderDir = tk.StringVar()
        self.ForlderDirE = tk.Entry(TopBarF,textvariable=self.MusicForlderDir)
        
        self.ComfirmB = tk.Button(TopBarF, text ="✔",bd=1)
        self.ComfirmB.bind("<Button-1>", self.Comfirm)

        self.InfoB = tk.Label(TopBarF, text="Tutorial/Info")
        self.InfoB.bind("<Button-1>", self.Info)

        self.AutoB.pack(side="left",fill="both")
        self.Divide.pack(side="left",fill="both")
        self.ForlderDirL.pack(side="left",fill="both")
        self.ForlderDirE.pack(side="left",fill="both", expand=True)
        self.ComfirmB.pack(side="left",fill="both")
        self.InfoB.pack(side="left",fill="both")

    def AutoClick(self, event):
        messagebox.showinfo(
            message=f"Coming soon! Lil Bibby soon!"
        )

    def GetForderDir(self):
        Entry = Path(self.ForlderDirE.get())
        if Entry.is_dir():
            ForlderDir = "c:/Users/niksu/Music" # ForlderDirE.get()
            if ForlderDir.startswith('"') and ForlderDir.endswith('"'):
                ForlderDir = ForlderDir[1:-1]
            return ForlderDir
        
    def Comfirm(self, event):
        Dir = self.GetForderDir()
        if ('/' in Dir) == True:
            FLClass.DropMenu['values'] = (Functions.GetMusicFolders(Dir))
    
    def Info(self, event):
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

class FolderList:
    def __init__(self, parent):
        self.parent = parent

        self.DropMenuF = tk.Frame(FolderListF)

        self.FolderL = tk.Label(self.DropMenuF, text="Forders:")
        self.DropMenu = ttk.Combobox(self.DropMenuF, state="readonly")
        self.DropMenu.bind("<<ComboboxSelected>>", self.DropMenuSelect)

        self.FLScrollbar = tk.Scrollbar(FolderListF)
        self.FLListbox = tk.Listbox(FolderListF, width=60, yscrollcommand = self.FLScrollbar.set)
        self.FLListbox.bind("<<ListboxSelect>>", self.ListboxSelected)

        self.DropMenuF.pack(side="top",fill="x")
        self.FolderL.pack(side="left")
        self.DropMenu.pack(side="top",fill="x")
        self.FLListbox.pack(side="left",fill="y")
        self.FLScrollbar.pack( side="left",fill="y")

    def DropMenuSelect(self, event):
        CurrentDir = TBClass.GetForderDir() + "/" + self.DropMenu.get()
        Contents = os.listdir(CurrentDir)
        self.ListboxUpdate(Contents)

    def GetSelectedIndex(self):
        SelectedIndex = self.FLListbox.curselection()
        if not SelectedIndex:
            return None
        else:
            return SelectedIndex
        
    def GetCurrentDir(self):
            CurrentDir = TBClass.GetForderDir() + "/" + self.DropMenu.get() + "/" + self.FLListbox.get(self.GetSelectedIndex())
            return CurrentDir
    
    def ListboxUpdate(self, Contents):
        self.FLListbox.delete(0, tk.END)
        for Content in Contents:
            self.FLListbox.insert(tk.END, Content)
        self.FLScrollbar.config(command = self.FLListbox.yview)

    def ListboxSelected(self, event):
        if self.DropMenu.get() == "":
            return
        else:
            EditorClass.FileField.FillEntry(EditorClass.GetFileN(self.FLListbox.get(self.GetSelectedIndex())))

            CoverClass.RefreshPathE()

            CurrentDir = self.GetCurrentDir()
            EditorClass.TitleField.FillEntry(MP3Info.GetTitle(CurrentDir))
            EditorClass.ArtistField.FillEntry(MP3Info.GetArtist(CurrentDir))
            CoverClass.FillCover(CurrentDir)
            EditorClass.AlbumField.FillEntry(MP3Info.GetAlbum(CurrentDir))
            EditorClass.TnField.FillEntry(MP3Info.GetTn(CurrentDir))
            EditorClass.GenreField.FillEntry(MP3Info.GetGenre(CurrentDir))
            EditorClass.YearField.FillEntry(MP3Info.GetYear(CurrentDir))
            EditorClass.CommentField.FillEntry(MP3Info.GetComment(CurrentDir))

class Cover:
    def __init__(self, parent):
        self.parent = parent

        self.ImgSize = (300, 300)

        self.CoverEntryF = tk.Frame(CoverF)

        self.CoverInput = StringVar()
        self.CoverL = tk.Label(self.CoverEntryF,text="Cover:",width=8)
        self.CoverE = Entry(self.CoverEntryF,textvar=self.CoverInput)
        self.CoverPathB = tk.Button(self.CoverEntryF, text=" x ",bd=1)
        self.CoverPathB.bind("<Button-1>", self.RemovePath)

        self.CoverImage = tk.Label(CoverF)
        self.CoverB = tk.Button(CoverF, text =" x ",bd=1)
        self.CoverB.bind("<Button-1>", self.CoverRemove)
        self.CoverE.register_drop_target("*")
        self.CoverE.bind("<<Drop>>", self.drop)
        self.CoverE.register_drag_source("*")
        self.CoverE.bind("<<DragInitCmd>>", self.drag_command)
        self.CoverDnD = ttk.Label(CoverF, ondrop=self.drop, ondragstart=self.drag_command,textvar=self.CoverInput,relief="solid",padding=142.4,width=3)

        self.CoverEntryF.pack(side="bottom",fill="x")
        self.CoverDnD.pack(side="top",pady=(10,0))
        self.CoverB.pack(side="top",fill="x",expand=True,pady=(0,10),padx=(47,47))
        self.CoverL.pack(side="left")
        self.CoverE.pack(side="left",fill="x",expand=True,ipady=2)
        self.CoverPathB.pack(side="right",padx=(0,10))

    def FillCover(self, Path):
        audio = eyed3.load(Path)
        if audio.tag and audio.tag.images:
            for i in audio.tag.images: 
                img = ImageTk.PhotoImage(Image.open(io.BytesIO(i.image_data)).resize(self.ImgSize))
            self.CoverImage.image = img
            self.CoverImage.config(image=img)

            self.CoverDnD.pack_forget()
            self.CoverB.pack_forget()
            self.CoverImage.pack(side="top",fill="both",expand=True,pady=(10,0))
            self.CoverB.pack(side="top",fill="x",expand=True,pady=(0,10),padx=(47,47))
        else:
            self.CoverImage.pack_forget()
            self.CoverB.pack_forget()
            self.CoverDnD.pack(side="top",pady=(10,0))
            self.CoverB.pack(side="top",fill="x",expand=True,pady=(0,10),padx=(47,47))

    def CoverRemove(self, event):
        if FLClass.GetSelectedIndex() == None:
            return
        else:
            audio = eyed3.load(FLClass.GetCurrentDir())
            if audio.tag and audio.tag.images:
                if FLClass.GetSelectedIndex() == None:
                    return
                else:
                    result = messagebox.askquestion("Remove or Cancel", "Do you want to remove the current cover?")
                    if result == 'yes':
                        MP3Info.RemoveCover(FLClass.GetCurrentDir())
                        self.CoverImage.pack_forget()
                        self.CoverB.pack_forget()
                        self.CoverDnD.pack(side="top",pady=(10,0))
                        self.CoverB.pack(side="top",fill="x",expand=True,pady=(0,10),padx=(47,47))
                    else:
                        return
            else:
                messagebox.showwarning(title="Invalid",message=f"There is no image to remove!")

    def drop(self, event):
        self.CoverInput.set(event.data)

    def drag_command(self, event):
        return (tkinterDnD.COPY, "DND_Text")
    
    def RefreshPathE(self):
        self.CoverE.delete(0, tk.END)

    def RemovePath(self, event):
        self.CoverE.delete(0, tk.END)

#Editor
class EditorEntrys:
    def __init__(self, parent, LabelText):
        self.parent = parent

        self.EditorL = tk.Label(parent, text=LabelText, width=8)
        self.EditorInput = tk.StringVar()
        self.EditorE = tk.Entry(parent, textvariable=self.EditorInput)
        self.EditorB = tk.Button(parent, text=" x ", bd=1)
        self.EditorB.bind("<Button-1>", self.RemoveEntry)

    def FillEntry(self, FillText):
        self.EditorE.delete(0, tk.END)
        self.EditorE.insert(0, Functions.CheckFill(FillText))

    def RemoveEntry(self, event):
        self.EditorE.delete(0, tk.END)

#file, title, artist, album, tn, genre, year, comment
class Editor(EditorEntrys):
    def __init__(self, parent):
        super().__init__(parent, None)

        self.FileF = tk.Frame(EditorF)
        self.TitleF = tk.Frame(EditorF)
        self.ArtistF = tk.Frame(EditorF)
        self.AlbumF = tk.Frame(EditorF)
        self.TnF = tk.Frame(EditorF)
        self.GenreF = tk.Frame(EditorF)
        self.YearF = tk.Frame(EditorF)
        self.CommentF = tk.Frame(EditorF)

        self.FileField = EditorEntrys(self.FileF, "File:")
        self.TitleField = EditorEntrys(self.TitleF, "Title:")
        self.ArtistField = EditorEntrys(self.ArtistF, "Artist:")
        self.AlbumField = EditorEntrys(self.AlbumF, "Album:")
        self.TnField = EditorEntrys(self.TnF, "TrackN:")
        self.GenreField = EditorEntrys(self.GenreF, "Genre:")
        self.YearField = EditorEntrys(self.YearF, "Year:")
        self.CommentField = EditorEntrys(self.CommentF, "Comment:")

        self.SaveB = tk.Button(window, text ="Save",bd=1)
        self.SaveB.bind("<Button-1>", self.Save)

        PackWidgets(self.FileF, self.FileField.EditorL, self.FileField.EditorE, self.FileField.EditorB,(0,0)) #pady=(0,0)
        PackWidgets(self.TitleF, self.TitleField.EditorL, self.TitleField.EditorE, self.TitleField.EditorB)
        PackWidgets(self.ArtistF, self.ArtistField.EditorL, self.ArtistField.EditorE, self.ArtistField.EditorB)
        PackWidgets(self.AlbumF, self.AlbumField.EditorL, self.AlbumField.EditorE, self.AlbumField.EditorB)
        PackWidgets(self.TnF, self.TnField.EditorL, self.TnField.EditorE, self.TnField.EditorB)
        PackWidgets(self.GenreF, self.GenreField.EditorL, self.GenreField.EditorE, self.GenreField.EditorB)
        PackWidgets(self.YearF, self.YearField.EditorL, self.YearField.EditorE, self.YearField.EditorB)
        PackWidgets(self.CommentF, self.CommentField.EditorL, self.CommentField.EditorE, self.CommentField.EditorB)

        self.SaveB.pack(side="right",fill="both",expand=True)

    def GetFileN(self, FillText):
        self.Period = FillText.rfind(".")
        if self.Period != -1:
            return FillText[:self.Period]

    def Save(self, event):
        if FLClass.GetSelectedIndex() == None:
            return
        else:
            MP3Info.TitleChange(FLClass.GetCurrentDir(),self.TitleField.EditorE.get())
            MP3Info.ArtistChange(FLClass.GetCurrentDir(),self.ArtistField.EditorE.get())
            MP3Info.CoverChange(FLClass.GetCurrentDir(),CoverClass.CoverE.get())
            MP3Info.AlbumChange(FLClass.GetCurrentDir(),self.AlbumField.EditorE.get())
            MP3Info.TnChange(FLClass.GetCurrentDir(),self.TnField.EditorE.get())
            MP3Info.GenreChange(FLClass.GetCurrentDir(),self.GenreField.EditorE.get())
            MP3Info.YearChange(FLClass.GetCurrentDir(),self.YearField.EditorE.get())
            MP3Info.CommentChange(FLClass.GetCurrentDir(),self.CommentField.EditorE.get())
            Functions.FileChange(FLClass.GetCurrentDir(),self.FileField.EditorE.get())

def PackWidgets(WidgetFrame, WidgetLabel, WidgetEntry, WidgetButton, pady=(5,0)):
    WidgetFrame.pack(side="top", fill="x", pady=pady)
    WidgetLabel.pack(side="left")
    WidgetEntry.pack(side="left", fill="x", expand=True, ipady=2)
    WidgetButton.pack(side="right", padx=(0,10))

TopBarF.pack(side="top",fill="x")
FolderListF.pack(side="left",fill="y")
CoverF.pack(side="top",fill="x",pady=10)
EditorF.pack(side="top",fill="both",expand=True)

if __name__ == "__main__":
    TBClass = TopBar(window)
    FLClass = FolderList(window)
    CoverClass = Cover(window)
    EditorClass = Editor(window)
    window.mainloop()