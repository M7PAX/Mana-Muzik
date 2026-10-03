import io
import MP3Info
import Functions
import customtkinter
import tkinter as tk
from tkinter import *
from PIL import Image
from customtkinter import *
from tkinter import messagebox

window = customtkinter.CTk()

window.geometry("780x780")
window.minsize(780, 780)
window.title("Mana Muzik")
try:
    window.iconbitmap("Images/Icon.ico")
except Exception:
    try:
        window.iconphoto(False, tk.PhotoImage(file="Images/Icon.png"))
    except Exception:
        pass

customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("dark")

current_theme = 0


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
        self.FolderDirE.bind("<Return>", lambda _: self.Confirm())
        self.FolderDirB = customtkinter.CTkButton(master=TopBarF, text="Open Folder", command=self.OpenFolderDirectory, width=10)

        self.ModeB = customtkinter.CTkButton(master=TopBarF, text="☀", command=self.ApplyTheme, width=30)
        self.InfoB = customtkinter.CTkButton(master=TopBarF, text="Tutorial/Info", command=Functions.Info, width=10)

        self.AutoB.pack(side="left", fill="both", padx=5, pady=5)
        self.FolderDirL.pack(side="left", fill="both")
        self.FolderDirE.pack(side="left", fill="x", expand=True)
        self.FolderDirB.pack(side="left", fill="x", padx=(1, 5), pady=5)

        self.ModeB.pack(side="left", fill="both", padx=(0, 5), pady=5)
        self.InfoB.pack(side="left", fill="both", padx=(0, 5), pady=5)

    def ApplyTheme(self):
        global current_theme
        current_theme = 0 if current_theme == 1 else 1
        if current_theme == 0:
            customtkinter.set_appearance_mode('dark')
            self.ModeB.configure(text="☀")
        else:
            customtkinter.set_appearance_mode('light')
            self.ModeB.configure(text="☾")

    def OpenFolderDirectory(self):
        FolderDirectory = tk.filedialog.askdirectory()
        if FolderDirectory:
            self.FolderDirE.delete(0, tk.END)
            self.FolderDirE.insert(0, FolderDirectory)
            self.Confirm()

    def GetFileDir(self):
        folder_dir = self.FolderDirE.get().strip()
        if folder_dir.startswith('"') and folder_dir.endswith('"'):
            folder_dir = folder_dir[1:-1]
        if folder_dir and os.path.isdir(folder_dir):
            return folder_dir
        return ""

    def Confirm(self):
        FLClass.CleanListBox()
        FLClass.DropMenu.set("")
        EditorClass.ClearEntry()

        directory = self.GetFileDir()
        if directory:
            folders = Functions.GetMusicFolders(directory)
            FLClass.DropMenu.configure(values=folders)
            FLClass.ResetCurrentDir()
            FLClass.ListBoxFill()


class FileList:
    def __init__(self, parent):
        self.parent = parent
        self.saved_name = ""
        self.current_dir = ""

        self.DropMenuF = customtkinter.CTkFrame(master=FileListF)

        self.FolderL = customtkinter.CTkLabel(master=self.DropMenuF, text="Folders:")
        self.DropMenu = customtkinter.CTkComboBox(master=self.DropMenuF, command=lambda _: (self.ResetCurrentDir(), self.ListBoxFill()), state="readonly", justify="center", values=[])
        self.ListBox = customtkinter.CTkScrollableFrame(master=FileListF, width=350)

        self.DropMenuF.pack(side="top", fill="x")
        self.FolderL.pack(side="left")
        self.DropMenu.pack(side="top", fill="x")
        self.ListBox.pack(side="left", fill="y")

    def CleanListBox(self):
        for widget in self.ListBox.winfo_children():
            widget.destroy()

    def GetFolderDir(self):
        base_dir = TBClass.GetFileDir()
        if not base_dir:
            return ""
        sub_folder = self.DropMenu.get().strip()
        if sub_folder:
            return os.path.join(base_dir, sub_folder)
        return base_dir

    def ResetCurrentDir(self):
        self.saved_name = ""
        self.current_dir = self.GetFolderDir()
        return self.current_dir

    def GetCurrentDir(self, name=None):
        folder_dir = self.GetFolderDir()
        if not folder_dir:
            return ""
        if name:
            self.saved_name = name
            self.current_dir = os.path.join(folder_dir, name)
        elif self.saved_name:
            self.current_dir = os.path.join(folder_dir, self.saved_name)
        else:
            self.current_dir = folder_dir
        return self.current_dir

    def ListBoxSelected(self):
        file_path = self.GetCurrentDir()
        if not file_path or not os.path.isfile(file_path):
            return

        EditorClass.FileField.FillEntry(Functions.GetFileName(self.saved_name))
        CoverClass.CoverE.delete(0, tk.END)

        EditorClass.TitleField.FillEntry(MP3Info.GetTitle(file_path))
        EditorClass.ArtistField.FillEntry(MP3Info.GetArtist(file_path))
        CoverClass.FillCover(file_path)
        EditorClass.AlbumField.FillEntry(MP3Info.GetAlbum(file_path))
        EditorClass.TnField.FillEntry(MP3Info.GetTn(file_path))
        EditorClass.GenreField.FillEntry(MP3Info.GetGenre(file_path))
        EditorClass.YearField.FillEntry(MP3Info.GetYear(file_path))
        EditorClass.CommentField.FillEntry(MP3Info.GetComment(file_path))

    def ListBoxFill(self):
        self.CleanListBox()
        folder_dir = self.GetFolderDir()
        if not folder_dir or not os.path.isdir(folder_dir):
            return

        try:
            contents = sorted(os.listdir(folder_dir))
        except Exception:
            return

        for content in contents:
            if content.lower().endswith(".mp3"):
                NameB = customtkinter.CTkButton(master=self.ListBox, text=content)
                NameB.pack(side="top", fill="x", padx=2, pady=2)
                name = content
                NameB.configure(command=lambda n=name: (self.GetCurrentDir(n), self.ListBoxSelected()))


class Cover:
    def __init__(self, parent):
        self.parent = parent

        self.CoverEntryF = customtkinter.CTkFrame(master=CoverF)
        self.CoverButtonF = customtkinter.CTkFrame(master=CoverF)

        self.CoverInput = StringVar()
        self.CoverL = customtkinter.CTkLabel(master=self.CoverEntryF, text="Cover:", width=65)
        self.CoverE = customtkinter.CTkEntry(master=self.CoverEntryF, textvariable=self.CoverInput)
        self.CoverEntryB = customtkinter.CTkButton(master=self.CoverEntryF, text="X", command=lambda: self.CoverE.delete(0, tk.END), width=30)

        self.CoverImage = customtkinter.CTkLabel(master=CoverF, text="")
        self.CoverB = customtkinter.CTkButton(master=self.CoverButtonF, text="X", command=self.CoverRemove)

        self.CoverReplacement = customtkinter.CTkLabel(CoverF, text="'COVER'", width=300, height=300)

        self.FileB = customtkinter.CTkButton(master=self.CoverButtonF, text="Open Cover", command=self.OpenFileCover)

        self.CoverEntryF.pack(side="bottom", fill="x")
        self.CoverReplacement.pack(side="top", pady=(10, 0))

        self.CoverButtonF.pack(side="top", fill="x", expand=True, pady=(0, 10), padx=(50, 50))
        self.FileB.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.CoverB.pack(side="left", fill="x", expand=True)

        self.CoverL.pack(side="left")
        self.CoverE.pack(side="left", fill="x", expand=True, ipady=2)
        self.CoverEntryB.pack(side="right", padx=(0, 10))

    def OpenFileCover(self):
        CoverDirectory = tk.filedialog.askopenfilename()
        if CoverDirectory:
            self.CoverE.delete(0, tk.END)
            self.CoverE.insert(0, CoverDirectory)

    def CoverPackForget(self):
        self.CoverButtonF.pack_forget()
        self.CoverB.pack_forget()
        self.FileB.pack_forget()

    def CoverPack(self):
        self.CoverButtonF.pack(side="top", fill="x", expand=True, pady=(0, 10), padx=(50, 50))
        self.FileB.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.CoverB.pack(side="left", fill="x", expand=True)

    def FillCover(self, path):
        cover_data = MP3Info.GetCoverData(path)
        if cover_data:
            try:
                img = customtkinter.CTkImage(dark_image=Image.open(io.BytesIO(cover_data)), size=(300, 300))
                self.CoverImage.configure(image=img)

                self.CoverReplacement.pack_forget()
                self.CoverPackForget()

                self.CoverImage.pack(side="top", fill="both", expand=True, pady=(10, 0))
                self.CoverPack()
                return
            except Exception as e:
                print(f"Error loading cover image: {e}")

        self.CoverImage.pack_forget()
        self.CoverPackForget()

        self.CoverReplacement.pack(side="top", pady=(10, 0))
        self.CoverPack()

    def CoverRemove(self):
        file_path = FLClass.GetCurrentDir()
        if not file_path or not os.path.isfile(file_path):
            messagebox.showwarning(title="Invalid", message="No MP3 file selected!")
            return
        if MP3Info.HasCover(file_path):
            result = messagebox.askquestion("Remove or Cancel", "Do you want to remove the current cover?")
            if result == 'yes':
                MP3Info.RemoveCover(file_path)
                self.CoverImage.pack_forget()
                self.CoverB.pack_forget()
                self.CoverReplacement.pack(side="top", pady=(10, 0))
                self.CoverB.pack(side="top", fill="x", expand=True, pady=(0, 10), padx=(50, 50))
        else:
            messagebox.showwarning(title="Invalid", message="There is no image to remove!")


# Editor
class EditorEntry:
    def __init__(self, parent, label_text):
        self.parent = parent

        self.EditorL = customtkinter.CTkLabel(master=parent, text=label_text, width=65)
        self.EditorInput = tk.StringVar()
        self.EditorE = customtkinter.CTkEntry(master=parent, textvariable=self.EditorInput)
        self.EditorB = customtkinter.CTkButton(master=parent, text="X", command=lambda: self.EditorE.delete(0, tk.END), width=30)

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
        file_path = FLClass.GetCurrentDir()
        if not file_path or not os.path.isfile(file_path):
            messagebox.showwarning(title="Invalid", message="No MP3 file selected to save!")
            return

        MP3Info.TitleChange(file_path, self.TitleField.EditorE.get())
        MP3Info.ArtistChange(file_path, self.ArtistField.EditorE.get())
        MP3Info.CoverChange(file_path, CoverClass.CoverE.get())
        MP3Info.AlbumChange(file_path, self.AlbumField.EditorE.get())
        MP3Info.TnChange(file_path, self.TnField.EditorE.get())
        MP3Info.GenreChange(file_path, self.GenreField.EditorE.get())
        MP3Info.YearChange(file_path, self.YearField.EditorE.get())
        MP3Info.CommentChange(file_path, self.CommentField.EditorE.get())

        file_name = self.FileField.EditorE.get().strip()
        if file_name and file_name != Functions.GetFileName(FLClass.saved_name):
            Functions.FileChange(file_path, file_name)
            FLClass.GetCurrentDir(file_name + ".mp3")
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
