import sys
import threading
import MainGraph
from tkinter import *



defaultRootWidth = 740
defaultRootHeight = 560

miniGraphDefaultWidth = 120
miniGraphDefaultHeight = 100

mainGraphDefaultWidth = 600
mainGraphDefaultHeight = 500

component = "CPU"

def drawGraphDetails(graph):
    graph.create_text(mainGraphDefaultWidth-35, 10, fill="darkblue", font="Times 10 italic bold", text=f"{component} Usage")
    positionY = 0
    while positionY < mainGraphDefaultHeight:
        if positionY!=0 and positionY!= mainGraphDefaultHeight:
            graph.create_line(30,positionY,mainGraphDefaultWidth,positionY,fill='gray')
            graph.create_text(20, positionY, fill="darkblue", font="Times 10 italic bold", text=str(int(100-positionY / mainGraphDefaultHeight * 100)))
        positionY += mainGraphDefaultHeight/10

def drawMiniGraphsDetails(miniGraph,comp):
    miniGraph.create_text(miniGraphDefaultWidth - 10, 6, fill="darkblue", font="Times 6 italic bold",text=str(comp))
    positionY = 0
    while positionY < miniGraphDefaultHeight:
        if positionY != 0 and positionY != miniGraphDefaultHeight:
            miniGraph.create_line(20, positionY, miniGraphDefaultWidth, positionY, fill='gray')
            miniGraph.create_text(10, positionY, fill="darkblue", font="Times 6 italic bold",text=str(int(100 - positionY / miniGraphDefaultHeight * 100)))
        positionY += miniGraphDefaultHeight / 10

class Gui(Canvas):

    def __init__(self):
        self.root = Tk()
        self.root.title("GUI Resource Monitor")
        self.root.geometry(f"{defaultRootWidth}x{defaultRootHeight}")
    #menu
        self.menu = LabelFrame(self.root,padx=0,pady=0)
        self.menu.grid(row = 0, column = 0)
    #menu items
        self.open = Button(self.menu,text="Open",padx=0,pady=3)
        self.open.grid(row = 0, column = 0)
        self.save = Button(self.menu,text="Save",padx=0,pady=3)
        self.save.grid(row = 0, column = 1)
        self.exit = Button(self.menu,text="Exit",padx=0,pady=3, command = self.exit)
        self.exit.grid(row = 0, column = 2)
    #app
        self.app = LabelFrame(self.root,padx=0,pady=0)
        self.app.grid(row=1,column=0,padx=0,pady=0)

    #app component
        self.miniGraphs = LabelFrame(self.app,padx=0,pady=0)
        self.miniGraphs.grid(row = 0, column = 0, padx=0,pady=0)
    #minigraphs items
        self.cpu = Canvas(self.miniGraphs,width = miniGraphDefaultWidth,height = miniGraphDefaultHeight, bg = "white")
        self.cpu.grid(row = 0, column = 0)
        self.gpu = Canvas(self.miniGraphs,width = miniGraphDefaultWidth,height = miniGraphDefaultHeight, bg = "white")
        self.gpu.grid(row = 1, column = 0)
        self.ram = Canvas(self.miniGraphs,width = miniGraphDefaultWidth,height = miniGraphDefaultHeight, bg = "white")
        self.ram.grid(row = 2, column = 0)
        self.hdd = Canvas(self.miniGraphs,width = miniGraphDefaultWidth,height = miniGraphDefaultHeight, bg = "white")
        self.hdd.grid(row = 3, column = 0)
        self.net = Canvas(self.miniGraphs,width = miniGraphDefaultWidth,height = miniGraphDefaultHeight, bg = "white")
        self.net.grid(row = 4, column = 0)
    #app component
        self.graph = LabelFrame(self.app,padx=0,pady=0)
        self.graph.grid(row = 0, column = 1, padx = 0, pady = 0)
        self.mainGraph = Canvas(self.graph,width = mainGraphDefaultWidth,height = mainGraphDefaultHeight, bg = "white")
        self.mainGraph.grid(row = 0,column = 0)

        self.root.update()
        self.mainGraph.update()
        self.cpu.update()
        self.gpu.update()
        self.ram.update()
        self.hdd.update()
        self.net.update()

    def run(self):
        drawGraphDetails(self.mainGraph)
        drawMiniGraphsDetails(self.cpu,"CPU")
        drawMiniGraphsDetails(self.gpu,"GPU")
        drawMiniGraphsDetails(self.ram,"RAM")
        drawMiniGraphsDetails(self.hdd,"HDD")
        drawMiniGraphsDetails(self.net,"NET")

        self.cpuThread = threading.Thread(target=MainGraph.mainGraphThread, args=(self.mainGraph,), daemon=True)
        self.cpuThread.start()

        self.root.mainloop()

    def exit(self):
        sys.exit()