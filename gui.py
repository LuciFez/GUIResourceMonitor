import threading
import MainGraph
import MiniGraph
from tkinter import *
import os
from PIL import Image
from datetime import datetime
import DrawGraph

defaultRootWidth = 734
defaultRootHeight = 550

miniGraphDefaultWidth = 120
miniGraphDefaultHeight = 100

cpuPercentage = []
cpuPercentagePerCore = []

gpuPercentage = []
gpuManufacturer = False

ramPercentage = []
ramAvailable = []
ramUsed = []

hddPartitionNumber = -1
diskRead = []
diskWrite = []
hddUsed = []
hddFree = []

netPercentage = []
netSent = []
netReceived = []


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
        self.root.resizable(False, False)

        # menu
        self.menu = LabelFrame(self.root, padx=0, pady=0)
        self.menu.grid(row=0, column=0)
        self.menu.configure(bg="white")
        self.open = Button(self.menu, text="Open",width=10, padx=0, pady=3, command=self.open)
        self.open.grid(row=0, column=0)
        self.save = Button(self.menu, text="Save",width=10, padx=0, pady=3, command=self.save)
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
            self.mainGraph.drawGPUGraph(graph)

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
            self.mainGraph.drawNETGraph(graph)

    def run(self):
        drawMiniGraphsDetails(self.cpu, "CPU")
        drawMiniGraphsDetails(self.gpu, "GPU")
        drawMiniGraphsDetails(self.ram, "RAM")

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

    def save(self):

        self.open.config(state="disabled")
        self.save.config(state="disabled")
        self.exit.config(state="disabled")

        self.cpu.bind("<Button-1>", lambda event: self.doNothing(event))
        self.gpu.bind("<Button-1>", lambda event: self.doNothing(event))
        self.ram.bind("<Button-1>", lambda event: self.doNothing(event))
        self.hdd.bind("<Button-1>", lambda event: self.doNothing(event))
        self.net.bind("<Button-1>", lambda event: self.doNothing(event))

        now = datetime.now()
        dt = now.strftime("%Y-%m-%dT%H%M%S")

        dir_path = os.path.dirname(os.path.realpath(__file__))

        if MainGraph.cpu == True:
            folder = dir_path + "\\output\\" + str("cpu_") + str(dt)
            try:
                os.mkdir(folder, 0o755)
                self.mainGraph.mainCPUGraph.postscript(file=folder + "\\cpu_" + str(dt) + ".ps", colormode='color')
                psimage = Image.open(folder + "\\cpu_" + str(dt) + ".ps")
                psimage.save(folder + "\\cpu_" + str(dt) + ".jpeg",dpi=(600,600))
                psimage.save(folder + "\\cpu_" + str(dt) + ".pdf",dpi=(600,600))
                textFile = open(folder + "\\cpu_" + str(dt) + ".txt", "w+")
                textFile.write(str(cpuPercentage))
                textFile.close()
            except:
                pass

        elif MainGraph.gpu == True:
            folder = dir_path + "\\output\\" + str("gpu_") + str(dt)
            try:
                os.mkdir(folder, 0o755)
                self.mainGraph.gpuCanvas.postscript(file=folder + "\\gpu_" + str(dt) + ".ps", colormode='color')
                psimage = Image.open(folder + "\\gpu_" + str(dt) + ".ps")
                psimage.save(folder + "\\gpu_" + str(dt) + ".jpeg",dpi=(600,600))
                psimage.save(folder + "\\gpu_" + str(dt) + ".pdf",dpi=(600,600))
                textFile = open(folder + "\\gpu_" + str(dt) + ".txt", "w+")
                textFile.write(str(gpuPercentage))
                textFile.close()
            except:
                pass

        elif MainGraph.ram == True:
            folder = dir_path + "\\output\\" + str("ram_") + str(dt)
            try:
                os.mkdir(folder, 0o755)
                self.mainGraph.mainRAMGraph.postscript(file=folder + "\\ram_" + str(dt) + ".ps", colormode='color')
                psimage = Image.open(folder + "\\ram_" + str(dt) + ".ps")
                psimage.save(folder + "\\ram_" + str(dt) + ".jpeg",dpi=(600,600))
                psimage.save(folder + "\\ram_" + str(dt) + ".pdf",dpi=(600,600))
                textFile = open(folder + "\\ram_" + str(dt) + ".txt", "w+")
                textFile.write(str(ramPercentage))
                textFile.close()
            except:
                pass

        elif MainGraph.hdd == True:
            folder = dir_path + "\\output\\" + str("hdd_") + str(dt)
            try:
                os.mkdir(folder, 0o755)
                self.mainGraph.diskIOPerfect.postscript(file=folder + "\\hdd_" + str(dt) + ".ps", colormode='color')
                psimage = Image.open(folder + "\\hdd_" + str(dt) + ".ps")
                psimage.save(folder + "\\hdd_" + str(dt) + ".jpeg",dpi=(600,600))
                psimage.save(folder + "\\hdd_" + str(dt) + ".pdf",dpi=(600,600))
                textFile = open(folder + "\\hdd_" + str(dt) + ".txt", "w+")
                textFile.write(str(diskRead))
                textFile.write('<sep>')
                textFile.write(str(diskWrite))
                textFile.close()
            except:
                pass

        elif MainGraph.net == True:
            folder = dir_path + "\\output\\" + str("net_") + str(dt)
            try:
                os.mkdir(folder, 0o755)
            except:
                pass
            self.mainGraph.netIOCanvas.postscript(file=folder + "\\net_" + str(dt) + ".ps", colormode='color')
            psimage = Image.open(folder + "\\net_" + str(dt) + ".ps")
            psimage.save(folder + "\\net_" + str(dt) + ".jpeg",dpi=(600,600))
            psimage.save(folder + "\\net_" + str(dt) + ".pdf",dpi=(600,600))
            textFile = open(folder + "\\net_" + str(dt) + ".txt", "w+")
            textFile.write(str(netSent))
            textFile.write('<sep>')
            textFile.write(str(netReceived))
            textFile.close()


        self.popup = Tk()
        self.popup.wm_title("Saved")
        label = Label(self.popup,text="Image has been saved")
        label.pack(side="top")
        ok = Button(self.popup,text="OK",command = self.leave)
        ok.pack()

        self.popup.mainloop()

    def leave(self):
        self.popup.destroy()
        self.open.config(state="normal")
        self.save.config(state="normal")
        self.exit.config(state="normal")

        self.cpu.bind("<Button-1>", lambda event: self.showCPU(event, graph=self.graph))
        self.gpu.bind("<Button-1>", lambda event: self.showGPU(event, graph=self.graph))
        self.ram.bind("<Button-1>", lambda event: self.showRAM(event, graph=self.graph))
        self.hdd.bind("<Button-1>", lambda event: self.showHDD(event, graph=self.graph))
        self.net.bind("<Button-1>", lambda event: self.showNET(event, graph=self.graph))

    def open(self):
        self.choice = -1
        self.open.config(state="disabled")
        self.save.config(state="disabled")
        self.exit.config(state="disabled")

        self.cpu.bind("<Button-1>", lambda event: self.doNothing(event))
        self.gpu.bind("<Button-1>", lambda event: self.doNothing(event))
        self.ram.bind("<Button-1>", lambda event: self.doNothing(event))
        self.hdd.bind("<Button-1>", lambda event: self.doNothing(event))
        self.net.bind("<Button-1>", lambda event: self.doNothing(event))

        self.popup = Tk()
        self.popup.geometry("300x300")
        self.popup.wm_title("Graph View")
        dir_path = os.path.dirname(os.path.realpath(__file__))

        folders = []
        self.listB = Listbox(self.popup,width = 25, font = "TkDefaultFont 14")
        i=0
        for subdir, dirs, files in os.walk(dir_path + "\\output\\"):
            if len(subdir[subdir.rfind('\\')+1:]) > 1:
                folders.append(subdir[subdir.rfind('\\')+1:])
                self.listB.insert(i,subdir[subdir.rfind('\\')+1:])
                i += 1
        self.listB.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.listB.bind("<<ListboxSelect>>", lambda event: self.choose())

        bFrame = LabelFrame(self.popup)
        bFrame.grid(row=1,column = 0)

        back = Button(bFrame,width = 12, text="back", command=self.leave)
        back.grid(row=0,column=0)
        showG = Button(bFrame,width = 12, text="Show Graph", command=self.show)
        showG.grid(row=0,column=1)

    def choose(self):
        self.choice = self.listB.get(self.listB.curselection()[0])

    def show(self):
        if self.choice!=-1:
            DrawGraph.drawGraph(self.choice)
            self.leave()
        else:
            ...

    def doNothing(self,event):
        ...

    def exit(self):
        sys.exit()

