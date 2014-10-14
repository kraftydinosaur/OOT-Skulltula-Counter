import ctypes
from ctypes import *
from ctypes.wintypes import *
from threading import Thread
from Tkinter import *
from time import sleep

OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
CloseHandle = windll.kernel32.CloseHandle

PROC_READ = 0x10
SKULL_ADD = 0xA062E2


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
        memmove(ctypes.byref(val), buffer, ctypes.sizeof(val))
        return val.value
    else:
        return 0
    sleep(1)


buffer = c_char_p(b"")
val = c_ubyte()
bytesRead = c_long(0)
processHandle = OpenProcess(PROC_READ, False, findPID("mupen64"))


class App(Frame):

    def getConf(self):
        self.bgcolor = "#F31"

    def setup(self):
        root.config(bg=self.bgcolor)
        photo = PhotoImage(file="icon.gif")
        w = Label(root, image=photo)
        w.photo = photo
        w.pack()
        w.config(bg=self.bgcolor)
        self.skullCount = StringVar()
        textLab = Label(root, textvariable=self.skullCount)
        textLab.pack()
        textLab.config(bg=self.bgcolor)


    def update(self):
        self.skullCount.set(readByte(SKULL_ADD, processHandle))
        self.update_idletasks()
        self.after(100, self.update)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        #self.pack()
        self.getConf()
        self.setup()

root = Tk()
app = App(master=root)
app.update()
app.mainloop()
