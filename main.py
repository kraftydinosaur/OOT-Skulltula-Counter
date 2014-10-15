from ctypes import *
from ctypes.wintypes import *
from Tkinter import *
import ConfigParser
import os.path
import tkMessageBox
import sys

OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
CloseHandle = windll.kernel32.CloseHandle


def findPID(search):
    """Finds Process that contains PROCNAME and returns pid"""
    import psutil
    for proc in psutil.process_iter():
        if search in str(proc.name):
            return proc.pid
    return None


def readByte(address, handle):
    """Reads byte at given address in given process handle and returns value"""
    if ReadProcessMemory(handle, address, buffer, 1, byref(bytesRead)):
        memmove(byref(val), buffer, sizeof(val))
        return val.value
    else:
        return 0


buffer = c_char_p(b"")
val = c_ubyte()
bytesRead = c_long(0)
processHandle = OpenProcess(0x10, False, findPID("mupen64"))


class App(Frame):

    def getConf(self):
        conf = ConfigParser.ConfigParser()
        try:
            if os.path.isfile("user.conf"):
                conf.read("user.conf")
            else:
                conf.read("default.conf")

            # Style
            self.bgcolor = conf.get("Style", "BackgroundColor")
            self.font = conf.get("Style", "Font")
            self.fontsize = conf.get("Style", "FontSize")
            self.fontcolor = conf.get("Style", "FontColor")
            bold = conf.get("Style", "Bold")
            self.pos = conf.get("Style", "Position")

            self.fontstyle = ""
            if bold:
                self.fontstyle = "bold"

            # Function
            self.updateInterval = conf.get("Function", "UpdateInterval")
            self.skullAdd = int(conf.get("Function", "SkullAddress"), 16)
        except:
            tkMessageBox.showerror("Error", "Error reading config file.")
            root.destroy()
            sys.exit()

    def setup(self):
        root.wm_title("OOT Skulltula Counter")
        root.config(bg=self.bgcolor)
        photo = PhotoImage(file="icon.gif")
        root.tk.call('wm', 'iconphoto', root._w, photo)
        w = Label(root, image=photo)
        w.photo = photo
        w.config(bg=self.bgcolor)
        self.skullCount = StringVar()
        textLab = Label(root, textvariable=self.skullCount,
                        font=(self.font, self.fontsize, self.fontstyle))
        textLab.config(bg=self.bgcolor, fg=self.fontcolor)

        w.pack(side=self.pos)
        textLab.pack(side=self.pos)

    def update(self):
        self.skullCount.set(readByte(self.skullAdd, processHandle))
        self.update_idletasks()
        self.after(self.updateInterval, self.update)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.getConf()
        self.setup()

root = Tk()
app = App(master=root)
app.update()
app.mainloop()
