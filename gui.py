import sys
import time
import threading
import MainGraph
import MiniGraph
from tkinter import *

defaultRootWidth = 734
defaultRootHeight = 550

miniGraphDefaultWidth = 120
miniGraphDefaultHeight = 100

cpuPercentage = []
cpuPercentagePerCore = []

gpuPercentage = []

ramPercentage = []
ramAvailable = []
ramUsed = []

hddPercentage = []
netPercentage = []


def drawMiniGraphsDetails(miniGraph, component):
    miniGraph.create_text(miniGraphDefaultWidth - 10, 6, fill="#72B2D6", font="Times 6 italic bold",
                          text=str(component))
    positionY = 0
    while positionY < miniGraphDefaultHeight:
        if positionY != 0 and positionY != miniGraphDefaultHeight:
            miniGraph.create_line(20, positionY, miniGraphDefaultWidth, positionY, fill='#E6F1F8')
            miniGraph.create_text(10, positionY, fill="#72B2D6", font="Times 6 italic bold",
                                  text=str(int(100 - positionY / miniGraphDefaultHeight * 100)))
        positionY += miniGraphDefaultHeight / 10


class Gui(Canvas):

    def __init__(self):
        self.root = Tk()
        self.root.title("GUI Resource Monitor")
        self.root.geometry(f"{defaultRootWidth}x{defaultRootHeight}")
        self.root.configure(bg="white")

        # menu
        self.menu = LabelFrame(self.root, padx=0, pady=0)
        self.menu.grid(row=0, column=0)
        self.menu.configure(bg="white")
        self.open = Button(self.menu, text="Open",width=10, padx=0, pady=3)
        self.open.grid(row=0, column=0)
        self.save = Button(self.menu, text="Save",width=10, padx=0, pady=3)
        self.save.grid(row=0, column=1)
        self.exit = Button(self.menu, text="Exit",width=10, padx=0, pady=3, command=self.exit)
        self.exit.grid(row=0, column=2)

        # app
        self.app = LabelFrame(self.root, padx=0, pady=0)
        self.app.grid(row=1, column=0, padx=0, pady=0)
        self.app.configure(bg="white")

        # app mini graphs
        self.miniGraphs = LabelFrame(self.app, padx=0, pady=0, bd=0, highlightthickness=0)
        self.miniGraphs.grid(row=0, column=0, padx=0, pady=0)
        self.miniGraphs.configure(bg="white")

        self.cpu = Canvas(self.miniGraphs, width=miniGraphDefaultWidth, height=miniGraphDefaultHeight, bg="white",
                          highlightthickness=1, highlightbackground="#5CA6D0")
        self.cpu.grid(row=0, column=1)

        self.gpu = Canvas(self.miniGraphs, width=miniGraphDefaultWidth, height=miniGraphDefaultHeight, bg="white",
                          highlightthickness=1, highlightbackground="#5CA6D0")
        self.gpu.grid(row=1, column=1)

        self.ram = Canvas(self.miniGraphs, width=miniGraphDefaultWidth, height=miniGraphDefaultHeight, bg="white",
                          highlightthickness=1, highlightbackground="#5CA6D0")
        self.ram.grid(row=2, column=1)

        self.hdd = Canvas(self.miniGraphs, width=miniGraphDefaultWidth, height=miniGraphDefaultHeight, bg="white",
                          highlightthickness=1, highlightbackground="#5CA6D0")
        self.hdd.grid(row=3, column=1)

        self.net = Canvas(self.miniGraphs, width=miniGraphDefaultWidth, height=miniGraphDefaultHeight, bg="white",
                          highlightthickness=1, highlightbackground="#5CA6D0")
        self.net.grid(row=4, column=1)

        self.cpu.bind("<Button-1>", lambda event: self.showCPU(event, graph=self.graph))
        self.gpu.bind("<Button-1>", lambda event: self.showGPU(event, graph=self.graph))
        self.ram.bind("<Button-1>", lambda event: self.showRAM(event, graph=self.graph))
        self.hdd.bind("<Button-1>", lambda event: self.showHDD(event, graph=self.graph))
        self.net.bind("<Button-1>", lambda event: self.showNET(event, graph=self.graph))

        # app main Graph
        self.graph = LabelFrame(self.app, padx=0, pady=0, bd=0, highlightthickness=0, bg="white")
        self.graph.grid(row=0, column=1, padx=0, pady=0)

        self.root.update()
        self.cpu.update()
        self.gpu.update()
        self.ram.update()
        self.hdd.update()
        self.net.update()

    def showCPU(self, event, graph):
        if self.previousComponent is self.cpu:
            print("Aceeasi Componenta")
        else:
            self.previousComponent.configure(highlightthickness=1, highlightbackground="#5CA6D0")
            self.cpu.configure(highlightthickness=2, highlightbackground="#AD58C6")
            if self.previousComponent is self.gpu:
                MainGraph.gpu = False
            if self.previousComponent is self.ram:
                MainGraph.ram = False
            if self.previousComponent is self.hdd:
                MainGraph.hdd = False
            if self.previousComponent is self.net:
                MainGraph.net = False
            MainGraph.cpu=True
            self.previousComponent = self.cpu
            for widget in graph.winfo_children():
                widget.destroy()
            self.mainGraph.drawCPUGraph(graph)

    def showGPU(self, event, graph):
        if self.previousComponent is self.gpu:
            print("Aceeasi Componenta")
        else:
            self.previousComponent.configure(highlightthickness=1, highlightbackground="#5CA6D0")
            self.gpu.configure(highlightthickness=2, highlightbackground="#AD58C6")
            if self.previousComponent is self.cpu:
                MainGraph.cpu = False
            if self.previousComponent is self.ram:
                MainGraph.ram = False
            if self.previousComponent is self.hdd:
                MainGraph.hdd = False
            if self.previousComponent is self.net:
                MainGraph.net = False
            MainGraph.gpu=True
            self.previousComponent = self.gpu
            for widget in graph.winfo_children():
                widget.destroy()
            self.mainGraph.drawCPUGraph(graph)

    def showRAM(self, event, graph):
        if self.previousComponent is self.ram:
            print("Aceeasi Componenta")
        else:
            self.previousComponent.configure(highlightthickness=1, highlightbackground="#5CA6D0")
            self.ram.configure(highlightthickness=2, highlightbackground="#AD58C6")
            if self.previousComponent is self.gpu:
                MainGraph.gpu = False
            if self.previousComponent is self.cpu:
                MainGraph.cpu = False
            if self.previousComponent is self.hdd:
                MainGraph.hdd = False
            if self.previousComponent is self.net:
                MainGraph.net = False
            MainGraph.ram=True
            self.previousComponent = self.ram
            for widget in graph.winfo_children():
                widget.destroy()
            self.mainGraph.drawRAMGraph(graph)

    def showHDD(self, event, graph):
        if self.previousComponent is self.hdd:
            print("Aceeasi Componenta")
        else:
            self.previousComponent.configure(highlightthickness=1, highlightbackground="#5CA6D0")
            self.hdd.configure(highlightthickness=2, highlightbackground="#AD58C6")
            if self.previousComponent is self.gpu:
                MainGraph.gpu = False
            if self.previousComponent is self.ram:
                MainGraph.ram = False
            if self.previousComponent is self.cpu:
                MainGraph.cpu = False
            if self.previousComponent is self.net:
                MainGraph.net = False
            MainGraph.hdd=True
            self.previousComponent = self.hdd
            for widget in graph.winfo_children():
                widget.destroy()
            self.mainGraph.drawHDDGraph(graph)

    def showNET(self, event, graph):
        if self.previousComponent is self.net:
            print("Aceeasi Componenta")
        else:
            self.previousComponent.configure(highlightthickness=1, highlightbackground="#5CA6D0")
            self.net.configure(highlightthickness=2, highlightbackground="#AD58C6")

            #change the graph when the tab is changed
            if self.previousComponent is self.gpu:
                MainGraph.gpu = False
            if self.previousComponent is self.ram:
                MainGraph.ram = False
            if self.previousComponent is self.hdd:
                MainGraph.hdd = False
            if self.previousComponent is self.cpu:
                MainGraph.cpu = False
            MainGraph.net=True
            self.previousComponent = self.net
            for widget in graph.winfo_children():
                widget.destroy()
            self.mainGraph.drawCPUGraph(graph)

    def run(self):

        drawMiniGraphsDetails(self.cpu, "CPU")
        drawMiniGraphsDetails(self.gpu, "GPU")
        drawMiniGraphsDetails(self.ram, "RAM")
        drawMiniGraphsDetails(self.hdd, "HDD")
        drawMiniGraphsDetails(self.net, "NET")

        self.cpuThread = threading.Thread(target=MiniGraph.miniGraphThread, args=(self.cpu, "CPU", [],), daemon=True)
        self.cpuThread.start()
        self.gpuThread = threading.Thread(target=MiniGraph.miniGraphThread, args=(self.gpu, "GPU", [],), daemon=True)
        self.gpuThread.start()
        self.ramThread = threading.Thread(target=MiniGraph.miniGraphThread, args=(self.ram, "RAM", [],), daemon=True)
        self.ramThread.start()
        self.hddThread = threading.Thread(target=MiniGraph.miniGraphThread, args=(self.hdd, "HDD", [],), daemon=True)
        self.hddThread.start()
        self.netThread = threading.Thread(target=MiniGraph.miniGraphThread, args=(self.net, "NET", [],), daemon=True)
        self.netThread.start()

        # set the thread at the start of the application to be the CPU one
        MainGraph.cpu = True
        MainGraph.gpu = False
        MainGraph.ram = False
        MainGraph.hdd = False
        MainGraph.net = False
        self.previousComponent = self.cpu
        self.cpu.configure(highlightthickness=2, highlightbackground="#AD58C6")
        self.mainGraph = MainGraph.AppClass(self.graph)

        self.root.mainloop()

    def exit(self):
        sys.exit()

