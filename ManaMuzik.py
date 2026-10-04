import io
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import customtkinter
from customtkinter import *
import Functions
import MP3Info
from PIL import Image

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

# Consistent Red Color for all "X" buttons
DANGER_RED = ("#c0392b", "#992d22")
DANGER_RED_HOVER = ("#962d22", "#78231b")

# Frames
TopBarF = customtkinter.CTkFrame(master=window, corner_radius=0)
FileListF = customtkinter.CTkFrame(master=window, corner_radius=8)
CoverF = customtkinter.CTkFrame(master=window, corner_radius=8)
EditorF = customtkinter.CTkFrame(master=window, corner_radius=8)


class TopBar:

  def __init__(self, parent):
    self.parent = parent

    self.AutoB = customtkinter.CTkButton(
        master=TopBarF,
        text="Automation",
        command=Functions.AutoClick,
        width=85,
        height=30,
        corner_radius=6,
    )
    self.FolderDirL = customtkinter.CTkLabel(
        master=TopBarF, text="Music Directory:"
    )
    self.MusicFolderDir = tk.StringVar()
    self.FolderDirE = customtkinter.CTkEntry(
        master=TopBarF,
        textvariable=self.MusicFolderDir,
        placeholder_text="Music Directory...",
        corner_radius=6,
        height=30,
    )
    self.FolderDirE.bind("<Return>", lambda _: self.Confirm())
    self.FolderDirE.bind(
        "<Double-Button-1>", lambda _: self.OpenCurrentFolderInExplorer()
    )
    self.FolderDirB = customtkinter.CTkButton(
        master=TopBarF,
        text="Open Folder",
        command=self.OpenFolderDirectory,
        width=92,
        height=30,
        corner_radius=6,
    )

    self.ModeB = customtkinter.CTkButton(
        master=TopBarF,
        text="☀",
        command=self.ApplyTheme,
        width=32,
        height=30,
        corner_radius=6,
    )
    self.InfoB = customtkinter.CTkButton(
        master=TopBarF,
        text="Tutorial/Info",
        command=Functions.Info,
        width=82,
        height=30,
        corner_radius=6,
    )

    self.AutoB.pack(side="left", fill="none", padx=(10, 6), pady=8)
    self.FolderDirL.pack(side="left", fill="none", padx=(0, 6), pady=8)
    self.FolderDirE.pack(side="left", fill="x", expand=True, padx=(0, 6), pady=8)
    self.FolderDirB.pack(side="left", fill="none", padx=(0, 6), pady=8)

    self.ModeB.pack(side="left", fill="none", padx=(0, 6), pady=8)
    self.InfoB.pack(side="left", fill="none", padx=(0, 10), pady=8)

  def ApplyTheme(self):
    global current_theme
    current_theme = 0 if current_theme == 1 else 1
    if current_theme == 0:
      customtkinter.set_appearance_mode("dark")
      self.ModeB.configure(text="☀")
    else:
      customtkinter.set_appearance_mode("light")
      self.ModeB.configure(text="☾")

  def OpenFolderDirectory(self):
    current = self.GetFileDir()
    FolderDirectory = Functions.SystemAskDirectory(
        title="Select Music Directory", initialdir=current
    )
    if FolderDirectory:
      self.FolderDirE.delete(0, tk.END)
      self.FolderDirE.insert(0, FolderDirectory)
      self.Confirm()

  def OpenCurrentFolderInExplorer(self):
    directory = self.GetFileDir()
    if directory:
      Functions.OpenInSystemExplorer(directory)

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
    self.track_buttons = {}

    self.DropMenuF = customtkinter.CTkFrame(
        master=FileListF, fg_color="transparent"
    )

    self.FolderL = customtkinter.CTkLabel(master=self.DropMenuF, text="Folders:")
    self.DropMenu = customtkinter.CTkComboBox(
        master=self.DropMenuF,
        command=lambda _: (self.ResetCurrentDir(), self.ListBoxFill()),
        state="readonly",
        justify="center",
        corner_radius=6,
        values=[],
    )
    self.ListBox = customtkinter.CTkScrollableFrame(
        master=FileListF, width=340, corner_radius=6
    )

    self.DropMenuF.pack(side="top", fill="x", padx=10, pady=(10, 8))
    self.FolderL.pack(side="left", padx=(0, 8))
    self.DropMenu.pack(side="left", fill="x", expand=True)
    self.ListBox.pack(
        side="left", fill="both", expand=True, padx=8, pady=(0, 8)
    )

  def CleanListBox(self):
    self.track_buttons.clear()
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

  def SelectTrack(self, selected_name):
    """Highlights only the selected track in blue, keeping other tracks dark."""
    for filename, btn in self.track_buttons.items():
      if filename == selected_name:
        btn.configure(
            fg_color=("#1f538d", "#14375e"),
            hover_color=("#14375e", "#0f2845"),
            text_color="#ffffff",
        )
      else:
        btn.configure(
            fg_color=("#2b2b2b", "#242424"),
            hover_color=("#3a3a3a", "#2e2e2e"),
            text_color="#d0d0d0",
        )

  def ShowTrackContextMenu(self, event, track_name):
    self.GetCurrentDir(track_name)
    self.ListBoxSelected()
    menu = tk.Menu(self.ListBox, tearoff=0)
    menu.add_command(
        label="Open in System File Explorer",
        command=lambda: Functions.OpenInSystemExplorer(self.GetCurrentDir()),
    )
    menu.tk_popup(event.x_root, event.y_root)

  def ListBoxSelected(self):
    file_path = self.GetCurrentDir()
    if not file_path or not os.path.isfile(file_path):
      return

    self.SelectTrack(self.saved_name)

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
        name = content
        is_selected = name == self.saved_name
        btn_fg = (
            ("#1f538d", "#14375e") if is_selected else ("#2b2b2b", "#242424")
        )
        btn_hover = (
            ("#14375e", "#0f2845") if is_selected else ("#3a3a3a", "#2e2e2e")
        )
        btn_txt = "#ffffff" if is_selected else "#d0d0d0"

        NameB = customtkinter.CTkButton(
            master=self.ListBox,
            text=f"♫  {name}",
            anchor="w",
            height=32,
            corner_radius=6,
            fg_color=btn_fg,
            hover_color=btn_hover,
            text_color=btn_txt,
        )
        NameB.pack(side="top", fill="x", padx=3, pady=2)
        NameB.configure(
            command=lambda n=name: (
                self.GetCurrentDir(n),
                self.ListBoxSelected(),
            )
        )
        NameB.bind(
            "<Button-3>",
            lambda event, n=name: self.ShowTrackContextMenu(event, n),
        )
        self.track_buttons[name] = NameB


class Cover:

  def __init__(self, parent):
    self.parent = parent

    self.CoverEntryF = customtkinter.CTkFrame(
        master=CoverF, fg_color="transparent"
    )
    self.CoverButtonF = customtkinter.CTkFrame(
        master=CoverF, fg_color="transparent"
    )

    self.CoverInput = StringVar()
    self.CoverL = customtkinter.CTkLabel(
        master=self.CoverEntryF, text="Cover:", width=70, anchor="w"
    )
    self.CoverE = customtkinter.CTkEntry(
        master=self.CoverEntryF, textvariable=self.CoverInput, corner_radius=6
    )
    self.CoverEntryB = customtkinter.CTkButton(
        master=self.CoverEntryF,
        text="✕",
        command=lambda: self.CoverE.delete(0, tk.END),
        width=28,
        height=28,
        corner_radius=6,
        fg_color=DANGER_RED,
        hover_color=DANGER_RED_HOVER,
        text_color="#ffffff",
    )

    self.CoverImage = customtkinter.CTkLabel(master=CoverF, text="")
    self.CoverB = customtkinter.CTkButton(
        master=self.CoverButtonF,
        text="✕",
        command=self.CoverRemove,
        width=28,
        height=28,
        corner_radius=6,
        fg_color=DANGER_RED,
        hover_color=DANGER_RED_HOVER,
        text_color="#ffffff",
    )

    self.CoverReplacement = customtkinter.CTkLabel(
        CoverF,
        text="'COVER'",
        width=300,
        height=260,
        fg_color=("#141414", "#121212"),
        corner_radius=8,
        text_color=("#666666", "#666666"),
        font=("Segoe UI", 16, "bold"),
    )

    self.FileB = customtkinter.CTkButton(
        master=self.CoverButtonF,
        text="Open Cover",
        command=self.OpenFileCover,
        height=28,
        corner_radius=6,
        fg_color=("#1f538d", "#1f538d"),
        hover_color=("#14375e", "#14375e"),
    )

    self.CoverReplacement.pack(side="top", pady=(10, 8))
    self.CoverButtonF.pack(side="top", fill="x", padx=10, pady=(0, 8))
    self.FileB.pack(side="left", fill="x", expand=True, padx=(0, 6))
    self.CoverB.pack(side="right")

    self.CoverL.pack(side="left")
    self.CoverE.pack(side="left", fill="x", expand=True, padx=(5, 5), ipady=2)
    self.CoverEntryB.pack(side="right")

    # Only show CoverEntryF when user has selected/entered a file for the cover
    self.CoverInput.trace_add("write", self.OnCoverInputChange)

  def OnCoverInputChange(self, *args):
    if self.CoverInput.get().strip():
      if not self.CoverEntryF.winfo_ismapped():
        self.CoverEntryF.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
    else:
      if self.CoverEntryF.winfo_ismapped():
        self.CoverEntryF.pack_forget()

  def OpenFileCover(self):
    current = FLClass.GetCurrentDir()
    initial_dir = (
        os.path.dirname(current)
        if current and os.path.exists(current)
        else TBClass.GetFileDir()
    )
    CoverDirectory = Functions.SystemAskOpenFile(
        title="Select Cover Image",
        initialdir=initial_dir,
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.webp *.bmp *.gif"),
            ("All Files", "*.*"),
        ],
    )
    if CoverDirectory:
      self.CoverE.delete(0, tk.END)
      self.CoverE.insert(0, CoverDirectory)

  def CoverPackForget(self):
    self.CoverButtonF.pack_forget()
    self.CoverB.pack_forget()
    self.FileB.pack_forget()

  def CoverPack(self):
    self.CoverButtonF.pack(side="top", fill="x", padx=10, pady=(0, 8))
    self.FileB.pack(side="left", fill="x", expand=True, padx=(0, 6))
    self.CoverB.pack(side="right")

  def FillCover(self, path):
    cover_data = MP3Info.GetCoverData(path)
    if cover_data:
      try:
        img = customtkinter.CTkImage(
            dark_image=Image.open(io.BytesIO(cover_data)), size=(300, 260)
        )
        self.CoverImage.configure(image=img)

        self.CoverReplacement.pack_forget()
        self.CoverPackForget()

        self.CoverImage.pack(side="top", pady=(10, 8))
        self.CoverPack()
        return
      except Exception as e:
        print(f"Error loading cover image: {e}")

    self.CoverImage.pack_forget()
    self.CoverPackForget()

    self.CoverReplacement.pack(side="top", pady=(10, 8))
    self.CoverPack()

  def CoverRemove(self):
    file_path = FLClass.GetCurrentDir()
    if not file_path or not os.path.isfile(file_path):
      messagebox.showwarning(title="Invalid", message="No MP3 file selected!")
      return
    if MP3Info.HasCover(file_path):
      result = messagebox.askquestion(
          "Remove or Cancel", "Do you want to remove the current cover?"
      )
      if result == "yes":
        MP3Info.RemoveCover(file_path)
        self.CoverImage.pack_forget()
        self.CoverReplacement.pack(side="top", pady=(10, 8))
        self.CoverE.delete(0, tk.END)
    else:
      messagebox.showwarning(
          title="Invalid", message="There is no image to remove!"
      )


# Editor
class EditorEntry:

  def __init__(self, parent, label_text):
    self.parent = parent

    self.EditorL = customtkinter.CTkLabel(
        master=parent, text=label_text, width=70, anchor="w"
    )
    self.EditorInput = tk.StringVar()
    self.EditorE = customtkinter.CTkEntry(
        master=parent, textvariable=self.EditorInput, corner_radius=6
    )
    self.EditorB = customtkinter.CTkButton(
        master=parent,
        text="✕",
        command=lambda: self.EditorE.delete(0, tk.END),
        width=28,
        height=28,
        corner_radius=6,
        fg_color=DANGER_RED,
        hover_color=DANGER_RED_HOVER,
        text_color="#ffffff",
    )

  def ClearEntry(self):
    self.EditorE.delete(0, tk.END)
    CoverClass.CoverE.delete(0, tk.END)

  def FillEntry(self, fill_text):
    self.ClearEntry()
    self.EditorE.insert(0, Functions.CheckFill(fill_text))


class Editor(EditorEntry):

  def __init__(self, parent):
    super().__init__(parent, None)

    self.FileF = customtkinter.CTkFrame(master=EditorF, fg_color="transparent")
    self.TitleF = customtkinter.CTkFrame(master=EditorF, fg_color="transparent")
    self.ArtistF = customtkinter.CTkFrame(
        master=EditorF, fg_color="transparent"
    )
    self.AlbumF = customtkinter.CTkFrame(master=EditorF, fg_color="transparent")
    self.TnF = customtkinter.CTkFrame(master=EditorF, fg_color="transparent")
    self.GenreF = customtkinter.CTkFrame(master=EditorF, fg_color="transparent")
    self.YearF = customtkinter.CTkFrame(master=EditorF, fg_color="transparent")
    self.CommentF = customtkinter.CTkFrame(
        master=EditorF, fg_color="transparent"
    )

    self.FileField = EditorEntry(self.FileF, "File:")
    self.TitleField = EditorEntry(self.TitleF, "Title:")
    self.ArtistField = EditorEntry(self.ArtistF, "Artist:")
    self.AlbumField = EditorEntry(self.AlbumF, "Album:")
    self.TnField = EditorEntry(self.TnF, "TrackN:")
    self.GenreField = EditorEntry(self.GenreF, "Genre:")
    self.YearField = EditorEntry(self.YearF, "Year:")
    self.CommentField = EditorEntry(self.CommentF, "Comment:")

    PackWidgets(
        self.FileF,
        self.FileField.EditorL,
        self.FileField.EditorE,
        self.FileField.EditorB,
    )
    PackWidgets(
        self.TitleF,
        self.TitleField.EditorL,
        self.TitleField.EditorE,
        self.TitleField.EditorB,
    )
    PackWidgets(
        self.ArtistF,
        self.ArtistField.EditorL,
        self.ArtistField.EditorE,
        self.ArtistField.EditorB,
    )
    PackWidgets(
        self.AlbumF,
        self.AlbumField.EditorL,
        self.AlbumField.EditorE,
        self.AlbumField.EditorB,
    )
    PackWidgets(
        self.TnF,
        self.TnField.EditorL,
        self.TnField.EditorE,
        self.TnField.EditorB,
    )
    PackWidgets(
        self.GenreF,
        self.GenreField.EditorL,
        self.GenreField.EditorE,
        self.GenreField.EditorB,
    )
    PackWidgets(
        self.YearF,
        self.YearField.EditorL,
        self.YearField.EditorE,
        self.YearField.EditorB,
    )
    PackWidgets(
        self.CommentF,
        self.CommentField.EditorL,
        self.CommentField.EditorE,
        self.CommentField.EditorB,
    )

    self.SaveB = customtkinter.CTkButton(
        master=EditorF,
        text="Save",
        command=self.Save,
        width=160,
        height=34,
        corner_radius=6,
        fg_color=("#1f538d", "#1f538d"),
        hover_color=("#14375e", "#14375e"),
    )
    self.SaveB.pack(side="bottom", anchor="e", padx=10, pady=(6, 8))

  def Save(self):
    file_path = FLClass.GetCurrentDir()
    if not file_path or not os.path.isfile(file_path):
      messagebox.showwarning(
          title="Invalid", message="No MP3 file selected to save!"
      )
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


def PackWidgets(
    WidgetFrame, WidgetLabel, WidgetEntry, WidgetButton, pady=(2, 2)
):
  WidgetFrame.pack(side="top", fill="x", padx=10, pady=pady)
  WidgetLabel.pack(side="left")
  WidgetEntry.pack(side="left", fill="x", expand=True, padx=(5, 5), ipady=2)
  WidgetButton.pack(side="right")


TopBarF.pack(side="top", fill="x", padx=0, pady=(0, 0))
FileListF.pack(side="left", fill="y", padx=(8, 4), pady=(8, 8))
CoverF.pack(side="top", fill="x", padx=(4, 8), pady=(8, 4))
EditorF.pack(side="top", fill="both", expand=True, padx=(4, 8), pady=(4, 8))

if __name__ == "__main__":
  TBClass = TopBar(window)
  FLClass = FileList(window)
  CoverClass = Cover(window)
  EditorClass = Editor(window)
  window.mainloop()
