import sys
import threading
import MainGraph
import MiniGraph
from tkinter import *

defaultRootWidth = 740
defaultRootHeight = 560

miniGraphDefaultWidth = 120
miniGraphDefaultHeight = 100

cpuPercentage = []
gpuPercentage = []
ramPercentage = []
hddPercentage = []
netPercentage = []


def drawMiniGraphsDetails(miniGraph, component):
    miniGraph.create_text(miniGraphDefaultWidth - 10, 6, fill="darkblue", font="Times 6 italic bold",
                          text=str(component))
    positionY = 0
    while positionY < miniGraphDefaultHeight:
        if positionY != 0 and positionY != miniGraphDefaultHeight:
            miniGraph.create_line(20, positionY, miniGraphDefaultWidth, positionY, fill='gray')
            miniGraph.create_text(10, positionY, fill="darkblue", font="Times 6 italic bold",
                                  text=str(int(100 - positionY / miniGraphDefaultHeight * 100)))
        positionY += miniGraphDefaultHeight / 10


def showCPU(event, graph):
    for widget in graph.winfo_children():
        widget.destroy()
    print(cpuPercentage)
    MainGraph.drawCPUGraph(graph, "AAA")


def showGPU(event):
    print("GPU")
    MainGraph.drawGraphDetails(MainGraph.mainGraph, "GPU")


def showRAM(event):
    print(ramPercentage)
    MainGraph.drawGraphDetails(MainGraph.mainGraph, "RAM")


def showHDD(event):
    print("HDD")
    MainGraph.drawGraphDetails(MainGraph.mainGraph, "HDD")


def showNET(event):
    print("NET")
    MainGraph.drawGraphDetails(MainGraph.mainGraph, "NET")


class Gui(Canvas):

    def __init__(self):
        self.root = Tk()
        self.root.title("GUI Resource Monitor")
        self.root.geometry(f"{defaultRootWidth}x{defaultRootHeight}")
        # menu
        self.menu = LabelFrame(self.root, padx=0, pady=0)
        self.menu.grid(row=0, column=0)
        self.open = Button(self.menu, text="Open", padx=0, pady=3)
        self.open.grid(row=0, column=0)
        self.save = Button(self.menu, text="Save", padx=0, pady=3)
        self.save.grid(row=0, column=1)
        self.exit = Button(self.menu, text="Exit", padx=0, pady=3, command=self.exit)
        self.exit.grid(row=0, column=2)

        # app
        self.app = LabelFrame(self.root, padx=0, pady=0)
        self.app.grid(row=1, column=0, padx=0, pady=0)

        # app mini graphs
        self.miniGraphs = LabelFrame(self.app, padx=0, pady=0)
        self.miniGraphs.grid(row=0, column=0, padx=0, pady=0)

        self.cpu = Canvas(self.miniGraphs, width=miniGraphDefaultWidth, height=miniGraphDefaultHeight, bg="white")
        self.cpu.grid(row=0, column=1)

        self.gpu = Canvas(self.miniGraphs, width=miniGraphDefaultWidth, height=miniGraphDefaultHeight, bg="white")
        self.gpu.grid(row=1, column=1)

        self.ram = Canvas(self.miniGraphs, width=miniGraphDefaultWidth, height=miniGraphDefaultHeight, bg="white")
        self.ram.grid(row=2, column=1)

        self.hdd = Canvas(self.miniGraphs, width=miniGraphDefaultWidth, height=miniGraphDefaultHeight, bg="white")
        self.hdd.grid(row=3, column=1)

        self.net = Canvas(self.miniGraphs, width=miniGraphDefaultWidth, height=miniGraphDefaultHeight, bg="white")
        self.net.grid(row=4, column=1)

        # app main Graph
        self.graph = LabelFrame(self.app, padx=0, pady=0)
        self.graph.grid(row=0, column=1, padx=0, pady=0)

        self.cpu.bind("<Button-1>", lambda event: showCPU(event, graph=self.graph))
        self.gpu.bind("<Button-1>", showGPU)
        self.ram.bind("<Button-1>", showRAM)
        self.hdd.bind("<Button-1>", showHDD)
        self.net.bind("<Button-1>", showNET)

        self.root.update()
        self.cpu.update()
        self.gpu.update()
        self.ram.update()
        self.hdd.update()
        self.net.update()

    def run(self):
        MainGraph.onOpen(self.graph)

        drawMiniGraphsDetails(self.cpu, "CPU")
        drawMiniGraphsDetails(self.gpu, "GPU")
        drawMiniGraphsDetails(self.ram, "RAM")
        drawMiniGraphsDetails(self.hdd, "HDD")
        drawMiniGraphsDetails(self.net, "NET")

        self.cpuThread = threading.Thread(target=MiniGraph.miniGraphThread, args=(self.cpu, "CPU", [],), daemon=True)
        self.cpuThread.start()
        self.cpu1Thread = threading.Thread(target=MiniGraph.miniGraphThread, args=(self.gpu, "GPU", [],), daemon=True)
        self.cpu1Thread.start()
        self.cpu2Thread = threading.Thread(target=MiniGraph.miniGraphThread, args=(self.ram, "RAM", [],), daemon=True)
        self.cpu2Thread.start()
        self.cpu3Thread = threading.Thread(target=MiniGraph.miniGraphThread, args=(self.hdd, "HDD", [],), daemon=True)
        self.cpu3Thread.start()
        self.cpu4Thread = threading.Thread(target=MiniGraph.miniGraphThread, args=(self.net, "NET", [],), daemon=True)
        self.cpu4Thread.start()

        self.root.mainloop()

    def exit(self):
        sys.exit()
