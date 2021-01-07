from tkinter import *
import psutil
import threading
import MainCPUThread
import MainRAMThread
import Gui
from psutil._common import bytes2human

mainGraphDefaultWidth = 600
mainGraphDefaultHeight = 200

cpu = False
gpu = False
ram = False
hdd = False
net = False


class AppClass:
    def __init__(self, graph):
        self.drawCPUGraph(graph)

    def drawCPUGraph(self, graph):
        # big graph
        self.mainCPUGraph = Canvas(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white",
                                   highlightthickness=1, highlightbackground="#5CA6D0")
        self.mainCPUGraph.grid(row=0, column=0)
        self.drawGraphDetails(self.mainCPUGraph, "CPU")

        # containter mini graphs
        self.miniCPUs = LabelFrame(graph, padx=0, pady=0, bd=0, highlightthickness=0, bg="white")
        self.miniCPUs.grid(row=1, column=0)

        # mini graphs Canvas
        self.miniCPUsRow1 = LabelFrame(self.miniCPUs, padx=0, pady=0, bd=0, highlightthickness=0, bg="white")
        self.miniCPUsRow1.grid(row=0, column=0)
        # mini graphs info
        self.miniCPUsRow2 = LabelFrame(self.miniCPUs, padx=0, pady=0, bd=0, highlightthickness=0, bg="white")
        self.miniCPUsRow2.grid(row=1, column=0)

        # draw mini graphs Canvas
        nbCPUs = psutil.cpu_count(logical=False)
        self.miniCPUsList = []
        for index in range(0, nbCPUs):
            if index > nbCPUs / 2 - 1:
                row2 = Canvas(self.miniCPUsRow2, width=mainGraphDefaultWidth / nbCPUs * 2 - 10,
                              height=mainGraphDefaultHeight / 2 - 10, bg="white", bd=0, highlightthickness=1,
                              highlightbackground="#5CA6D0")
                row2.grid(row=1, column=int(index - nbCPUs / 2), padx=5, pady=5)
                self.miniCPUsList.append(row2)
                self.drawMiniCPUsDetails(row2, index + 1)
            else:
                row1 = Canvas(self.miniCPUsRow1, width=mainGraphDefaultWidth / nbCPUs * 2 - 10,
                              height=mainGraphDefaultHeight / 2 - 10, bg="white", bd=0, highlightthickness=1,
                              highlightbackground="#5CA6D0")
                row1.grid(row=0, column=int(index), padx=5, pady=5)
                self.miniCPUsList.append(row1)
                self.drawMiniCPUsDetails(row1, index + 1)

        # full CPU info
        cpuDetailsFrame = LabelFrame(graph, padx=0, pady=0, bd=0, highlightthickness=0, bg="white")
        cpuDetailsFrame.grid(row=2, column=0)
        self.speedFullCPU = Label(cpuDetailsFrame,
                                  text="CPU speed: " + str(Gui.cpuPercentage[len(Gui.cpuPercentage) - 1]), width=20,
                                  bg="white", bd=0, highlightthickness=0, anchor='w')
        self.speedFullCPU.grid(row=0, column=0)

        # each core speed info
        self.speedList = []
        for index in range(0, nbCPUs):
            if index > nbCPUs / 2 - 1:
                speed = Label(cpuDetailsFrame, text="Core " + str(index + 1) + " speed: " + str(
                    Gui.cpuPercentagePerCore[len(Gui.cpuPercentagePerCore) - 1][index]), width=20, bg="white", bd=0,
                              highlightthickness=0,
                              padx=10, pady=5, anchor='w')
                speed.grid(row=2, column=int(index - nbCPUs / 2))
                self.speedList.append(speed)
            else:
                speed = Label(cpuDetailsFrame, text="Core " + str(index + 1) + " speed: " + str(
                    Gui.cpuPercentagePerCore[len(Gui.cpuPercentagePerCore) - 1][index]), width=20, bg="white", bd=0,
                              highlightthickness=0,
                              padx=10, pady=5, anchor='w')
                speed.grid(row=1, column=int(index))
                self.speedList.append(speed)

        self.cpuThread = threading.Thread(target=MainCPUThread.cpuThread, args=(
            self.mainCPUGraph, self.miniCPUsList, self.speedFullCPU, self.speedList, Gui.cpuPercentage,
            Gui.cpuPercentagePerCore), daemon=True)
        self.cpuThread.start()

    def drawGPUGraph(self, graph, text):
        ...

    def drawRAMGraph(self, graph):
        # Big Ram Graph
        self.mainRAMGraph = Canvas(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white",
                                   highlightthickness=1, highlightbackground="#5CA6D0")
        self.mainRAMGraph.grid(row=0, column=0, padx=2, pady=10)
        self.drawGraphDetails(self.mainRAMGraph, "RAM")

        # chart Ram label
        self.chartRamLabel = LabelFrame(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white",
                                        bd=0, highlightthickness=0)
        self.chartRamLabel.grid(row=1, column=0)
        # chart text
        self.ramText = Label(self.chartRamLabel, text="Usage Bar", bg="white", bd=0)
        self.ramText.grid(row=0, column=0)
        # chart
        self.ramBar = Canvas(self.chartRamLabel, width=mainGraphDefaultWidth - 100, height=mainGraphDefaultHeight / 7,
                             bg="white", highlightthickness=1, highlightbackground="#5CA6D0")

        self.ramBar.create_line((mainGraphDefaultWidth - 100) * (float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]) * 100 / (float(Gui.ramAvailable[len(Gui.ramAvailable) - 1][:-1]) + float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]))) / 100,
                                0,
                                (mainGraphDefaultWidth - 100) * (float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]) * 100 / (float(Gui.ramAvailable[len(Gui.ramAvailable) - 1][:-1]) + float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]))) / 100,
                                mainGraphDefaultHeight / 7 + 1,
                                fill='#549401', width=2)
        self.ramBar.create_rectangle(0,0,(mainGraphDefaultWidth - 100) * (float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]) * 100 / (float(Gui.ramAvailable[len(Gui.ramAvailable) - 1][:-1]) + float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]))) / 100,mainGraphDefaultHeight / 7 + 1,fill='#EDF9EB')
        self.ramBar.create_text(40,mainGraphDefaultHeight / 14+1,fill="#549401",font="TkDefaultFont 8",text=str(Gui.ramPercentage[len(Gui.ramPercentage)-1])+" % used")
        self.ramBar.grid(row=0, column=1, padx=7, pady=10)
        # details label
        self.detailsRamLabel = LabelFrame(graph, bg="white",
                                          bd=0, highlightthickness=0)
        self.detailsRamLabel.grid(row=2, column=0)
        # total ram
        self.totalRam = Label(self.detailsRamLabel,
                              text="Total RAM: " + str(bytes2human(psutil.virtual_memory().total)), bg="white", bd=0)
        self.totalRam.grid(row=0, column=0, padx=20, pady=10)
        # available ram
        self.availableRam = Label(self.detailsRamLabel,
                                  text="Available RAM: " + str(Gui.ramAvailable[len(Gui.ramAvailable) - 1]), bg="white",
                                  bd=0)
        self.availableRam.grid(row=0, column=2, padx=20, pady=10)
        # used ram
        self.usedRam = Label(self.detailsRamLabel, text="Used RAM: " + str(Gui.ramUsed[len(Gui.ramUsed) - 1]),
                             bg="white", bd=0)
        self.usedRam.grid(row=0, column=1, padx=20, pady=10)

        self.ramThread = threading.Thread(target=MainRAMThread.ramThread, args=(
            self.mainRAMGraph, self.ramBar, self.totalRam, self.availableRam, self.usedRam, Gui.ramPercentage,
            Gui.ramAvailable, Gui.ramUsed), daemon=True)
        self.ramThread.start()


    def drawHDDGraph(self, graph, text):
        ...

    def drawNETGraph(self, graph, text):
        ...

    def drawMiniCPUsDetails(self, cpu, index):
        cpu.create_text((mainGraphDefaultHeight) - 25, 5, fill="#72B2D6", font="Times 6 italic bold",
                        text=f"CPU {index}")
        positionY = 0
        while positionY < (mainGraphDefaultHeight / 2 - 10):
            if positionY != 0 and positionY != mainGraphDefaultHeight:
                cpu.create_line(20, positionY, mainGraphDefaultWidth, positionY, fill='#E6F1F8')
                cpu.create_text(10, positionY, fill="#72B2D6", font="Times 6 italic bold",
                                text=str(int(100 - positionY / (mainGraphDefaultHeight / 2 - 10) * 100)))
            positionY += (mainGraphDefaultHeight / 2 - 10) / 10

    def drawGraphDetails(self, graph, component):
        graph.create_text(mainGraphDefaultWidth - 35, 10, fill="#72B2D6", font="Times 10 italic bold",
                          text=f"{component} Usage")
        positionY = 0
        while positionY < mainGraphDefaultHeight:
            if positionY != 0 and positionY != mainGraphDefaultHeight:
                graph.create_line(30, positionY, mainGraphDefaultWidth, positionY, fill='#E6F1F8')
                graph.create_text(15, positionY, fill="#72B2D6", font="Times 10 italic bold",
                                  text=str(int(100 - positionY / mainGraphDefaultHeight * 100)))
            positionY += mainGraphDefaultHeight / 10
