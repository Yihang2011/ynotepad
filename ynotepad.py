#coding:utf-8


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
    label = Label(root, anchor = W)
    label.pack(side = BOTTOM, fill = X)
    menu = Menu(root)
    file_menu = Menu(menu, tearoff = 0)
    edit_menu = Menu(menu, tearoff = 0)
    help_menu = Menu(menu, tearoff = 0)
    scroll_bar = Scrollbar(TextArea)
    file = None
    file2 = None

    def __init__(self, **kwargs):
        self.root.config(menu = self.menu)
        self.TextArea.focus()
        self.TextArea.bind('<<TextModified>>', self.on_modify)
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
        self.TextArea.pack(side = TOP, fill = BOTH, expand = True)

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

    def _proxy(self, command, *args):
        if command == 'get' and (args[0] == 'sel.first' and args[1] == 'sel.last') and not self.tag_ranges('sel'):
            return
        if command == 'delete' and (args[0] == 'sel.first' and args[1] == 'sel.last') and not self.tag_ranges('sel'):
            return
        cmd = (self._orig, command) + args
        result = self.call(cmd)
        if command in ('insert', 'delete', 'replace'):
            self.event_generate('<<TextModified>>')
        return result

    def run(self):
        self.root.mainloop()

    def on_modify(event):
        chars = event.widget.get('0.0', 'end')
        label.configure(text='%s chars' % len(chars))
        print(chars)

notepad = Notepad(width = 600, height = 400)
notepad.run()
