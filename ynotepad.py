import tkinter
import os, sys, ctypes
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *

class Notepad:
    root = Tk()
    root.iconphoto( False, PhotoImage(file = 'notepad.png'))
    root.geometry('1366x768')
    # Support for HiDPI
    if sys.platform.startswith("win"):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        root.tk.call('tk', 'scaling', ScaleFactor / 75)


    # Set main window
    Width = 300
    Height = 300
    TextArea = Text(root)
    menu = Menu(root)
    file_menu = Menu(menu, tearoff = 0)
    edit_menu = Menu(menu, tearoff = 0)
    help_menu = Menu(menu, tearoff = 0)
    scroll_bar = Scrollbar(TextArea)
    file = None
    file2 = None

    def __init__(self, **kwargs):
        self.root.config(menu = self.menu)
        # Set text area size
        try:
            self.Width = kwargs['width']
        except KeyError:
            pass
        try:
            self.Height = kwargs['height']
        except KeyError:
            pass
        # Set window title
        self.root.title("yNotepad")

        self.root.grid_rowconfigure(0, weight = 1)
        self.root.grid_columnconfigure(0, weight = 1)

        # Add controls (widget)
        self.TextArea.grid(sticky = N + E + S + W)

        # Add command
        self.file_menu.add_command(label = "New", command = self.newfile)
        self.file_menu.add_command(label = "Open", command = self.openfile)
        self.file_menu.add_command(label = "Save", command = self.savefile)
        self.file_menu.add_separator()
        self.file_menu.add_command(label = "Quit", command = self.quit)
        self.menu.add_cascade(label = "File", menu = self.file_menu)
        self.edit_menu.add_command(label = "Cut", command = self.cut)
        self.edit_menu.add_command(label = "Copy", command = self.copy)
        self.edit_menu.add_command(label = "Paste", command = self.paste)
        self.edit_menu.add_command(label = "Clear", command = self.clear)
        self.menu.add_cascade(label = "Edit", menu = self.edit_menu)
        self.help_menu.add_command(label = "About", command = self.about)
        self.menu.add_cascade(label = "Help", menu = self.help_menu)
        self.root.config(menu = self.menu)
        self.scroll_bar.pack(side = RIGHT, fill = Y)
        self.scroll_bar.config(command = self.TextArea.yview)
        self.TextArea.config(yscrollcommand = self.scroll_bar.set)

    def quit(self):
        self.root.destroy()

    def about(self):
        showinfo("About", "yNotepad v1.0.0 \n by Yihang Xiao")

    def openfile(self):
        self.file = askopenfilename(defaultextension = ".txt",
                                    filetypes = [("All Files", "*.*"),
                                                 ("Text Documents", "*.txt")])
        if self.file == "":
            self.file = None
        else:
            self.root.title(os.path.basename(self.file))
            self.TextArea.delete(1.0, END)
            file = open(self.file, "r")
            self.TextArea.insert(1.0, file.read())
            file.close()

    def newfile(self):
        self.root.title("Untitled")
        self.file = None
        self.TextArea.delete(1.0, END)

    def savefile(self):
        if self.file == None:
            self.file = asksaveasfilename(initialfile = 'Untitled.txt',
                                          defaultextension = ".txt",
                                          filetypes = [("All Files", "*.*"),
                                                       ("Text Documents",
                                                        "*.txt")])
            if self.file == "":
                self.file = None
            else:
                file = open(self.file, "w")
                file.write(self.TextArea.get(1.0, END))
                file.close()

                self.root.title(os.path.basename(self.file))
        else:
            file = open(self.file, "w")
            file.write(self.TextArea.get(1.0, END))
            file.close()

    def cut(self):
        self.TextArea.event_generate("<<Cut>>")

    def copy(self):
        self.TextArea.event_generate("<<Copy>>")

    def paste(self):
        self.TextArea.event_generate("<<Paste>>")

    def clear(self):
        self.TextArea.delete(1.0, "end")


    # def search(self):
    #     self.root.tag_remove("match", "1.0", 'end')
    #     count = 0; pos = "1.0"
    #     needle = string.get()
    #     if needle:
    #         while True:
    #             pos = self.notePad.search(needle, pos, nocase=num.get(), stopindex='end')
    #             if not pos:
    #                 break
    #             lastpos = f'{pos}+{len(needle)}c'
    #             self.notePad.tag_add("match", pos, lastpos)
    #             count += 1; pos = lastpos
    #         self.notePad.tag_configure('match', background = 'yellow')
    #         et.focus_set()
    #         find.title(f"{count}个被匹配")

    def run(self):
        self.root.mainloop()


notepad = Notepad(width = 600, height = 400)
notepad.run()
