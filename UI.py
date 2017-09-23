from tkinter import *
from PIL import ImageTk, Image
#import vtk


class UI:
    def __init__(self, master):
        self.master = master
        master.title("CEESIM Visualizer")
        self.antennas = Button(master, text="Import Antennas")
        self.mod = Button(master, text="Modify Antennas")
        self.planes = Button(master, text="Planes")
        self.wireframe = Button(master, text="Wireframe On/Off")
        self.canvas = Canvas()
        self.antennas.grid(row=0, column=5, sticky="ENWS")
        self.mod.grid(row=1, column=5, sticky="ENWS")
        self.planes.grid(row=2, column=5, sticky="ENWS")
        self.wireframe.grid(row=3, column=5, sticky="ENWS")
        self.path = "f22.jpg"
        self.plane = ImageTk.PhotoImage(Image.open(self.path))
        self.label = Label(master, image = self.plane)
        self.label.image = self.plane
        self.label.grid(row=0, column=0, rowspan=4, columnspan=4)
        
         """ x,y,z coords """
        self.xcoord = Label(master, text = "X-coordinates")
        self.ycoord = Label(master, text = "Y-coordinates")
        self.zcoord = Label(master, text = "Z-coordinates")

        self.xentry = Entry(master)
        self.yentry = Entry(master)
        self.zentry = Entry(master)
        
        self.xcoord.grid(row = 4, column = 0)
        self.ycoord.grid(row = 4, column = 1)
        self.zcoord.grid(row = 4, column = 2)

        self.xentry.grid(row = 5, column = 0)
        self.yentry.grid(row = 5, column = 1)
        self.zentry.grid(row = 5, column = 2) 



root = Tk()
myUI = UI(root)
root.mainloop()
