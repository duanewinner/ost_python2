#!/usr/local/bin/python3

from tkinter import *

ALL = N+S+E+W

class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master.rowconfigure(0, weight = 1)
        self.master.columnconfigure(0, weight = 1)
        self.grid(sticky=ALL)

        for r in range(2):
            if r == 0:
                color="#8499ac"
            else:
                color="#aeb9c4"
            self.rowconfigure(r, weight=1, minsize=50)
            f = Label(self, text="Frame {0}".format(r+1), bg=color)
            f.grid(row=r, column=0, rowspan=1, columnspan=2, sticky=ALL)

        f = Label(self, text="Frame 3", bg="#a5a5a5")
        f.grid(row=0, column=2, rowspan=2, columnspan=4, sticky=ALL)
        
        for c in range(5):
            self.columnconfigure(c, weight=1)
            Button(self, text="Button {0}".format(c+1)).grid(row=5, column=c, sticky=E+W)

root=Tk()
app=Application(master=root)
app.mainloop()

