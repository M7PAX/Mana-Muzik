import io
import eyed3
import MP3Info
import Functions
import customtkinter
import tkinter as tk
from tkinter import *
from PIL import Image
from pathlib import Path
from customtkinter import *
from tkinter import messagebox

window = customtkinter.CTk()

window.geometry("780x780")
window.minsize(780, 780)
window.title("Mana Muzik")
window.iconbitmap("Images/Icon.ico")

customtkinter.set_default_color_theme("dark-blue")

current_theme = 0


# RANDOM FUN
def ApplyTheme():
    global current_theme
    current_theme = 0 if current_theme == 1 else 1
    if current_theme == 0:
        customtkinter.set_appearance_mode('dark')
    else:
        customtkinter.set_appearance_mode('light')


# Frames
TopBarF = customtkinter.CTkFrame(master=window)
FileListF = customtkinter.CTkFrame(master=window)
CoverF = customtkinter.CTkFrame(master=window)
EditorF = customtkinter.CTkFrame(master=window)


class TopBar:
    def __init__(self, parent):
        self.parent = parent

        self.AutoB = customtkinter.CTkButton(master=TopBarF, text="Automation", command=Functions.AutoClick, width=10)
        self.FolderDirL = customtkinter.CTkLabel(master=TopBarF, text="Music Directory:")
        self.MusicFolderDir = tk.StringVar()
        self.FolderDirE = customtkinter.CTkEntry(master=TopBarF, textvariable=self.MusicFolderDir)

        self.ConfirmB = customtkinter.CTkButton(master=TopBarF, text="✔", command=self.Confirm, width=2)
        self.ModeB = customtkinter.CTkButton(master=TopBarF, text="Theme", command=ApplyTheme, width=10)
        self.InfoB = customtkinter.CTkButton(master=TopBarF, text="Tutorial/Info", command=Functions.Info, width=10)

        self.AutoB.pack(side="left", fill="both", padx=5, pady=5)
        self.FolderDirL.pack(side="left", fill="both")
        self.FolderDirE.pack(side="left", fill="x", expand=True)
        self.ConfirmB.pack(side="left", fill="both", padx=(0, 5), pady=5)
        self.ModeB.pack(side="left", fill="both", padx=(0, 5), pady=5)
        self.InfoB.pack(side="left", fill="both", padx=(0, 5), pady=5)

    def GetFileDir(self):
        entry = Path(self.FolderDirE.get())
        if entry.is_dir():
            folder_dir = "c:/Users/niksu/Music"  # self.FolderDirE.get()
            if folder_dir.startswith('"') and folder_dir.endswith('"'):
                folder_dir = folder_dir[1:-1]
            return folder_dir

    def Confirm(self):
        FLClass.CleanListBox()
        FLClass.DropMenu.set("")
        EditorClass.ClearEntry()

        FLClass.GetCurrentDir("")
        FLClass.ListBoxFill()
        directory = self.GetFileDir()
        if '/' in directory:
            folders = Functions.GetMusicFolders(directory)
            FLClass.DropMenu.configure(values=folders)


class FileList:
    def __init__(self, parent):
        self.parent = parent
        self.saved_name = ""
        self.current_dir = ""

        self.DropMenuF = customtkinter.CTkFrame(master=FileListF)

        self.FolderL = customtkinter.CTkLabel(master=self.DropMenuF, text="Folders:")
        self.DropMenu = customtkinter.CTkComboBox(master=self.DropMenuF, command=lambda _: (self.GetCurrentDir(""), self.ListBoxFill()), state="readonly", justify="center", values=[])
        self.ListBox = customtkinter.CTkScrollableFrame(master=FileListF, width=350)

        self.DropMenuF.pack(side="top", fill="x")
        self.FolderL.pack(side="left")
        self.DropMenu.pack(side="top", fill="x")
        self.ListBox.pack(side="left", fill="y")

    def CleanListBox(self):
        for widget in self.ListBox.winfo_children():
            widget.destroy()

    def GetCurrentDir(self, name):
        if name != "":
            self.saved_name = name
            self.current_dir = TBClass.GetFileDir() + "/" + self.DropMenu.get() + "/" + self.saved_name
        elif self.DropMenu.get() == "":
            self.current_dir = TBClass.GetFileDir()
        elif self.DropMenu.get() != "":
            self.current_dir = TBClass.GetFileDir() + "/" + self.DropMenu.get()
        else:
            self.current_dir = TBClass.GetFileDir() + "/" + self.DropMenu.get() + "/" + self.saved_name

    def ListBoxSelected(self):
        EditorClass.FileField.FillEntry(Functions.GetFileName(self.saved_name))
        CoverClass.CoverE.delete(0, tk.END)

        EditorClass.TitleField.FillEntry(MP3Info.GetTitle(self.current_dir))
        EditorClass.ArtistField.FillEntry(MP3Info.GetArtist(self.current_dir))
        CoverClass.FillCover(self.current_dir)
        EditorClass.AlbumField.FillEntry(MP3Info.GetAlbum(self.current_dir))
        EditorClass.TnField.FillEntry(MP3Info.GetTn(self.current_dir))
        EditorClass.GenreField.FillEntry(MP3Info.GetGenre(self.current_dir))
        EditorClass.YearField.FillEntry(MP3Info.GetYear(self.current_dir))
        EditorClass.CommentField.FillEntry(MP3Info.GetComment(self.current_dir))

    def ListBoxFill(self):
        self.CleanListBox()

        contents = os.listdir(self.current_dir)
        for content in contents:
            if content.endswith(".mp3"):
                NameB = customtkinter.CTkButton(master=self.ListBox, text=content)
                NameB.pack(side="top", fill="x", padx=2, pady=2)
                name = NameB.cget("text")
                NameB.configure(command=lambda n=name: (self.GetCurrentDir(n), self.ListBoxSelected()))


class Cover:
    def __init__(self, parent):
        self.parent = parent

        self.CoverEntryF = customtkinter.CTkFrame(master=CoverF)

        self.CoverInput = StringVar()
        self.CoverL = customtkinter.CTkLabel(master=self.CoverEntryF, text="Cover:", width=65)
        self.CoverE = customtkinter.CTkEntry(master=self.CoverEntryF, textvariable=self.CoverInput)
        self.CoverEntryB = customtkinter.CTkButton(master=self.CoverEntryF, text="X", command=self.CoverE.delete(0, tk.END), width=30)

        self.CoverImage = customtkinter.CTkLabel(master=CoverF, text="")
        self.CoverB = customtkinter.CTkButton(master=CoverF, text="X", command=self.CoverRemove)

        self.CoverReplacement = customtkinter.CTkLabel(CoverF, text="'COVER'", width=300, height=300)

        self.CoverEntryF.pack(side="bottom", fill="x")
        self.CoverReplacement.pack(side="top", pady=(10, 0))
        self.CoverB.pack(side="top", fill="x", expand=True, pady=(0, 10), padx=(50, 50))
        self.CoverL.pack(side="left")
        self.CoverE.pack(side="left", fill="x", expand=True, ipady=2)
        self.CoverEntryB.pack(side="right", padx=(0, 10))

    def FillCover(self, path):
        audio = eyed3.load(path)
        if audio.tag and audio.tag.images:
            for i in audio.tag.images:
                img = customtkinter.CTkImage(dark_image=Image.open(io.BytesIO(i.image_data)), size=(300, 300))
                self.CoverImage.configure(image=img)

            self.CoverReplacement.pack_forget()
            self.CoverB.pack_forget()
            self.CoverImage.pack(side="top", fill="both", expand=True, pady=(10, 0))
            self.CoverB.pack(side="top", fill="x", expand=True, pady=(0, 10), padx=(50, 50))
        else:
            self.CoverImage.pack_forget()
            self.CoverB.pack_forget()
            self.CoverReplacement.pack(side="top", pady=(10, 0))
            self.CoverB.pack(side="top", fill="x", expand=True, pady=(0, 10), padx=(50, 50))

    def CoverRemove(self):
        audio = eyed3.load(FLClass.GetCurrentDir(""))
        if audio.tag and audio.tag.images:
            result = messagebox.askquestion("Remove or Cancel", "Do you want to remove the current cover?")
            if result == 'yes':
                MP3Info.RemoveCover(FLClass.GetCurrentDir(""))
                self.CoverImage.pack_forget()
                self.CoverB.pack_forget()
                self.CoverReplacement.pack(side="top", pady=(10, 0))
                self.CoverB.pack(side="top", fill="x", expand=True, pady=(0, 10), padx=(50, 50))
        else:
            messagebox.showwarning(title="Invalid", message=f"There is no image to remove!")


# Editor
class EditorEntry:
    def __init__(self, parent, label_text):
        self.parent = parent

        self.EditorL = customtkinter.CTkLabel(master=parent, text=label_text, width=65)
        self.EditorInput = tk.StringVar()
        self.EditorE = customtkinter.CTkEntry(master=parent, textvariable=self.EditorInput)
        self.EditorB = customtkinter.CTkButton(master=parent, text="X", command=self.EditorE.delete(0, tk.END), width=30)

    def ClearEntry(self):
        self.EditorE.delete(0, tk.END)
        CoverClass.CoverE.delete(0, tk.END)

    def FillEntry(self, fill_text):
        self.ClearEntry()
        self.EditorE.insert(0, Functions.CheckFill(fill_text))


# file, title, artist, album, tn, genre, year, comment
class Editor(EditorEntry):
    def __init__(self, parent):
        super().__init__(parent, None)

        self.FileF = customtkinter.CTkFrame(master=EditorF)
        self.TitleF = customtkinter.CTkFrame(master=EditorF)
        self.ArtistF = customtkinter.CTkFrame(master=EditorF)
        self.AlbumF = customtkinter.CTkFrame(master=EditorF)
        self.TnF = customtkinter.CTkFrame(master=EditorF)
        self.GenreF = customtkinter.CTkFrame(master=EditorF)
        self.YearF = customtkinter.CTkFrame(master=EditorF)
        self.CommentF = customtkinter.CTkFrame(master=EditorF)

        self.FileField = EditorEntry(self.FileF, "File:")
        self.TitleField = EditorEntry(self.TitleF, "Title:")
        self.ArtistField = EditorEntry(self.ArtistF, "Artist:")
        self.AlbumField = EditorEntry(self.AlbumF, "Album:")
        self.TnField = EditorEntry(self.TnF, "TrackN:")
        self.GenreField = EditorEntry(self.GenreF, "Genre:")
        self.YearField = EditorEntry(self.YearF, "Year:")
        self.CommentField = EditorEntry(self.CommentF, "Comment:")

        self.SaveB = customtkinter.CTkButton(master=window, text="Save", command=self.Save)

        PackWidgets(self.FileF, self.FileField.EditorL, self.FileField.EditorE, self.FileField.EditorB)
        PackWidgets(self.TitleF, self.TitleField.EditorL, self.TitleField.EditorE, self.TitleField.EditorB)
        PackWidgets(self.ArtistF, self.ArtistField.EditorL, self.ArtistField.EditorE, self.ArtistField.EditorB)
        PackWidgets(self.AlbumF, self.AlbumField.EditorL, self.AlbumField.EditorE, self.AlbumField.EditorB)
        PackWidgets(self.TnF, self.TnField.EditorL, self.TnField.EditorE, self.TnField.EditorB)
        PackWidgets(self.GenreF, self.GenreField.EditorL, self.GenreField.EditorE, self.GenreField.EditorB)
        PackWidgets(self.YearF, self.YearField.EditorL, self.YearField.EditorE, self.YearField.EditorB)
        PackWidgets(self.CommentF, self.CommentField.EditorL, self.CommentField.EditorE, self.CommentField.EditorB)

        self.SaveB.pack(side="right", fill="both", expand=True)

    def Save(self):
        MP3Info.TitleChange(FLClass.GetCurrentDir(""), self.TitleField.EditorE.get())
        MP3Info.ArtistChange(FLClass.GetCurrentDir(""), self.ArtistField.EditorE.get())
        MP3Info.CoverChange(FLClass.GetCurrentDir(""), CoverClass.CoverE.get())
        MP3Info.AlbumChange(FLClass.GetCurrentDir(""), self.AlbumField.EditorE.get())
        MP3Info.TnChange(FLClass.GetCurrentDir(""), self.TnField.EditorE.get())
        MP3Info.GenreChange(FLClass.GetCurrentDir(""), self.GenreField.EditorE.get())
        MP3Info.YearChange(FLClass.GetCurrentDir(""), self.YearField.EditorE.get())
        MP3Info.CommentChange(FLClass.GetCurrentDir(""), self.CommentField.EditorE.get())

        file_name = self.FileField.EditorE.get()
        Functions.FileChange(FLClass.GetCurrentDir(""), file_name)
        FLClass.GetCurrentDir(Functions.GetDirectoryFile(file_name + ".mp3"))
        FLClass.ListBoxFill()


def PackWidgets(WidgetFrame, WidgetLabel, WidgetEntry, WidgetButton, pady=(5, 0)):
    WidgetFrame.pack(side="top", fill="x", pady=pady)
    WidgetLabel.pack(side="left")
    WidgetEntry.pack(side="left", fill="x", expand=True, ipady=2)
    WidgetButton.pack(side="right", padx=(0, 10))


TopBarF.pack(side="top", fill="x")
FileListF.pack(side="left", fill="y")
CoverF.pack(side="top", fill="x", pady=10)
EditorF.pack(side="top", fill="both", expand=True)

if __name__ == "__main__":
    TBClass = TopBar(window)
    FLClass = FileList(window)
    CoverClass = Cover(window)
    EditorClass = Editor(window)
    window.mainloop()
