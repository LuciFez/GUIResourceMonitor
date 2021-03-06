import psutil
import threading
import MainCPUThread
import MainGPUThread
import MainRAMThread
import MainHDDThread
import MainNETThread
import Gui
import GPUtil
from tkinter import *
from psutil._common import bytes2human

"""
Declare the widely available variables hardware component.

The default main graph canvas width and height are set below.
"""

mainGraphDefaultWidth = 600
mainGraphDefaultHeight = 200

cpu = False
gpu = False
ram = False
hdd = False
net = False


class AppClass:
    """
    Class used for drawing the main frame of the application
    """

    def __init__(self, graph):
        """
        Draw the CPU at the start of the application
        """
        self.drawCPUGraph(graph)

    def drawCPUGraph(self, graph):
        """
        Creates the main canvas for the CPU component, the canvases for each phisical core of the CPU
        and the details frame of the CPU. Draw the details for each canvas.

        Starts a thread to update the canvases and the details of the CPU each second.
        """
        self.mainCPUGraph = Canvas(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white",
                                   highlightthickness=1, highlightbackground="#5CA6D0")
        self.mainCPUGraph.grid(row=0, column=0, padx=2)
        self.drawGraphDetails(self.mainCPUGraph, "CPU")

        self.miniCPUs = LabelFrame(graph, padx=0, pady=0, bd=0, highlightthickness=0, bg="white")
        self.miniCPUs.grid(row=1, column=0)
        self.miniCPUsRow1 = LabelFrame(self.miniCPUs, padx=0, pady=0, bd=0, highlightthickness=0, bg="white")
        self.miniCPUsRow1.grid(row=0, column=0)
        self.miniCPUsRow2 = LabelFrame(self.miniCPUs, padx=0, pady=0, bd=0, highlightthickness=0, bg="white")
        self.miniCPUsRow2.grid(row=1, column=0)
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

        cpuDetailsFrame = LabelFrame(graph, padx=0, pady=0, bd=0, highlightthickness=0, bg="white")
        cpuDetailsFrame.grid(row=2, column=0)
        self.speedFullCPU = Label(cpuDetailsFrame,
                                  text="CPU speed: " + str(Gui.cpuPercentage[len(Gui.cpuPercentage) - 1]), width=20,
                                  bg="white", bd=0, highlightthickness=0, anchor='w')
        self.speedFullCPU.grid(row=0, column=0)
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
            self.mainCPUGraph, self.miniCPUsList, self.speedFullCPU, self.speedList), daemon=True)
        self.cpuThread.start()

    def drawGPUGraph(self, graph):
        """
        If the machine has a GPU from NVIDIA the:
        Creates the main canvas for the GPU component and the details of the GPU.
        Draw the details for canvas.
        Starts a thread to update the canvases and the details of the GPU each second.
        Else:
        Draw advertisement to Nvidia
        """
        GPUs = GPUtil.getGPUs()
        if len(GPUs) > 0:
            self.gpuName = Label(graph, text=GPUs[0].name, bg="white", bd=0, font=("TkDefaultFont", 14))
            self.gpuName.grid(row=0, column=0)
            self.gpuCanvas = Canvas(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white",
                                    highlightthickness=1, highlightbackground="#5CA6D0")
            self.gpuCanvas.grid(row=1, column=0, padx=2, pady=2)

            self.gpuDetails = LabelFrame(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight,
                                         bg="white",
                                         bd=0, highlightthickness=0)
            self.gpuDetails.grid(row=2, column=0, pady=20)
            self.gpuTM = Label(self.gpuDetails, text="Total memory: " + str(GPUs[0].memoryTotal) + " MB", bg="white",
                               bd=0, anchor='w', font=("TkDefaultFont", 14))
            self.gpuTM.grid(row=0, column=0, pady=5)
            self.gpuAM = Label(self.gpuDetails, text="Available memory: " + str(GPUs[0].memoryFree) + " MB", bg="white",
                               bd=0, anchor='w', font=("TkDefaultFont", 14))
            self.gpuAM.grid(row=1, column=0, pady=5)
            self.gpuUM = Label(self.gpuDetails, text="Used memory: " + str(GPUs[0].memoryUsed) + " MB", bg="white",
                               bd=0, anchor='w', font=("TkDefaultFont", 14))
            self.gpuUM.grid(row=2, column=0, pady=5)
            self.gpuTemp = Label(self.gpuDetails, text="Temperature: " + str(GPUs[0].temperature) + " Celsius",
                                 bg="white", bd=0, anchor='w', font=("TkDefaultFont", 14))
            self.gpuTemp.grid(row=3, column=0, pady=5)

            self.drawGraphDetails(self.gpuCanvas, "GPU")

            self.gpuThread = threading.Thread(target=MainGPUThread.gpuThread,
                                              args=(self.gpuCanvas, self.gpuTM, self.gpuAM, self.gpuUM, self.gpuTemp),
                                              daemon=True)
            self.gpuThread.start()
        else:
            self.gpuStatus = Label(graph, text="Buy Nvidia", bg="white", bd=0, font=("TkDefaultFont", 32))
            self.gpuStatus.grid(row=0, column=0, padx=mainGraphDefaultWidth / 2 - 102, pady=mainGraphDefaultHeight / 2)

    def drawRAMGraph(self, graph):
        """
        Creates the main canvas for the RAM component, the canvas for the RAM bar
        and the details frame of the RAM. Draw the details for each canvas.

        Starts a thread to update the canvases and the details of the RAM each second.
        """
        self.mainRAMGraph = Canvas(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white",
                                   highlightthickness=1, highlightbackground="#5CA6D0")
        self.mainRAMGraph.grid(row=0, column=0, padx=2, pady=10)
        self.drawGraphDetails(self.mainRAMGraph, "RAM")

        self.chartRamLabel = LabelFrame(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white",
                                        bd=0, highlightthickness=0)
        self.chartRamLabel.grid(row=1, column=0)
        self.ramText = Label(self.chartRamLabel, text="Usage Bar", bg="white", bd=0)
        self.ramText.grid(row=0, column=0)
        self.ramBar = Canvas(self.chartRamLabel, width=mainGraphDefaultWidth - 100, height=mainGraphDefaultHeight / 7,
                             bg="white", highlightthickness=1, highlightbackground="#5CA6D0")
        self.ramBar.create_line((mainGraphDefaultWidth - 100) * (float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]) * 100 / (
                float(Gui.ramAvailable[len(Gui.ramAvailable) - 1][:-1]) + float(
            Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]))) / 100,
                                0,
                                (mainGraphDefaultWidth - 100) * (float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]) * 100 / (
                                        float(Gui.ramAvailable[len(Gui.ramAvailable) - 1][:-1]) + float(
                                    Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]))) / 100,
                                mainGraphDefaultHeight / 7 + 1,
                                fill='#549401', width=2)
        self.ramBar.create_rectangle(0, 0, (mainGraphDefaultWidth - 100) * (
                float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]) * 100 / (
                float(Gui.ramAvailable[len(Gui.ramAvailable) - 1][:-1]) + float(
            Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]))) / 100, mainGraphDefaultHeight / 7 + 1, fill='#EDF9EB')
        self.ramBar.create_text(40, mainGraphDefaultHeight / 14 + 1, fill="#549401", font="TkDefaultFont 8",
                                text=str(Gui.ramPercentage[len(Gui.ramPercentage) - 1]) + " % used")
        self.ramBar.grid(row=0, column=1, padx=7, pady=10)

        self.detailsRamLabel = LabelFrame(graph, bg="white", bd=0, highlightthickness=0)
        self.detailsRamLabel.grid(row=2, column=0)
        self.totalRam = Label(self.detailsRamLabel,
                              text="Total RAM: " + str(bytes2human(psutil.virtual_memory().total)), bg="white", bd=0)
        self.totalRam.grid(row=0, column=0, padx=20, pady=10)
        self.availableRam = Label(self.detailsRamLabel,
                                  text="Available RAM: " + str(Gui.ramAvailable[len(Gui.ramAvailable) - 1]), bg="white",
                                  bd=0)
        self.availableRam.grid(row=0, column=2, padx=20, pady=10)
        self.usedRam = Label(self.detailsRamLabel, text="Used RAM: " + str(Gui.ramUsed[len(Gui.ramUsed) - 1]),
                             bg="white", bd=0)
        self.usedRam.grid(row=0, column=1, padx=20, pady=10)

        self.ramThread = threading.Thread(target=MainRAMThread.ramThread, args=(
            self.mainRAMGraph, self.ramBar, self.totalRam, self.availableRam, self.usedRam, Gui.ramPercentage,
            Gui.ramAvailable, Gui.ramUsed), daemon=True)
        self.ramThread.start()

    def drawHDDGraph(self, graph):
        """
        Creates the main canvas for the HDD component and the canvases for each partition on the machine.
        Draw the details for each canvas.

        Starts a thread to update the canvases and the details of the HDD each second.
        """
        self.diskIOPerfect = Canvas(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white",
                                    highlightthickness=1, highlightbackground="#5CA6D0")
        self.diskIOPerfect.grid(row=0, column=0, padx=0, pady=0)
        self.diskIOPerfect.create_text(30, 8, fill="black", font="TkDefaultFont 8", text="Max speed")
        self.diskIOPerfect.create_text(30, mainGraphDefaultHeight - 8, fill="black", font="TkDefaultFont 8",
                                       text="Low speed")
        self.diskIOPerfect.create_text(30, 18, fill="blue", font="TkDefaultFont 8", text="MBps read")
        self.diskIOPerfect.create_text(36, 28, fill="#549401", font="TkDefaultFont 8", text="MBps written")

        self.barCanvas = Canvas(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white", bd=0,
                                highlightthickness=0)
        self.barCanvas.grid(row=1, column=0, padx=3, pady=3)
        Gui.hddPartitionNumber = len(psutil.disk_partitions(all=True))
        partitions = psutil.disk_partitions(all=True)
        for i in range(0, Gui.hddPartitionNumber):
            self.barCanvas.create_rectangle(70, mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1) - 20,
                                            mainGraphDefaultWidth - 20,
                                            mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1) + 20,
                                            outline="#549401")
            self.barCanvas.create_rectangle(71, mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1) - 19, (
                    Gui.hddUsed[len(Gui.hddUsed) - 1][i] * 100 / (
                    Gui.hddFree[len(Gui.hddFree) - 1][i] + Gui.hddUsed[len(Gui.hddUsed) - 1][i])) * (
                                                    mainGraphDefaultWidth - 90) / 100 + 70,
                                            mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1) + 19,
                                            fill="#EDF9EB", outline="#EDF9EB")
            self.barCanvas.create_text(120, mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1),
                                       fill="#549401", font="TkDefaultFont 10", text=str(
                    Gui.hddUsed[len(Gui.hddUsed) - 1][i] * 100 / (
                            Gui.hddFree[len(Gui.hddFree) - 1][i] + Gui.hddUsed[len(Gui.hddUsed) - 1][i]))[
                                                                                     :5] + "% used")
            self.barCanvas.create_text(40, mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1),
                                       fill="black", font="TkDefaultFont 12", text=str(partitions[i].device[:1]) + ":/")

        self.hddThread = threading.Thread(target=MainHDDThread.hddThread, args=(self.barCanvas, self.diskIOPerfect),
                                          daemon=True)
        self.hddThread.start()

    def drawNETGraph(self, graph):
        """
        Creates the main canvas for the NET component.

        Starts a thread to update the canvases and the details of the NET each second.
        """
        self.netIOCanvas = Canvas(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white",
                                  highlightthickness=1, highlightbackground="#5CA6D0")
        self.netIOCanvas.grid(row=0, column=0, padx=2, pady=2)
        self.netIOCanvas.create_text(30, 8, fill="black", font="TkDefaultFont 8", text="Max speed")
        self.netIOCanvas.create_text(30, mainGraphDefaultHeight - 8, fill="black", font="TkDefaultFont 8",
                                     text="Low speed")
        self.netIOCanvas.create_text(40, 18, fill="blue", font="TkDefaultFont 8", text="MBps received")
        self.netIOCanvas.create_text(29, 28, fill="#549401", font="TkDefaultFont 8", text="MBps sent")

        self.netThread = threading.Thread(target=MainNETThread.netThread, args=(self.netIOCanvas,), daemon=True)
        self.netThread.start()

    def drawMiniCPUsDetails(self, cpu, index):
        """
        Creates the lines and numbers oriented horizontally which will indicate
        the usage percentage on the core graphs.
        """
        cpu.create_text((mainGraphDefaultHeight) - 25, 5, fill="#72B2D6", font="Times 6 italic bold",
                        text=f"CPU {index}")
        positionY = 0
        while positionY < (mainGraphDefaultHeight / 2 - 10):
            if positionY != 0 and positionY != mainGraphDefaultHeight:
                cpu.create_line(20, positionY, mainGraphDefaultWidth, positionY, fill='#E6F1F8')
                # add the percent of the height
                cpu.create_text(10, positionY, fill="#72B2D6", font="Times 6 italic bold",
                                text=str(int(100 - positionY / (mainGraphDefaultHeight / 2 - 10) * 100)))
            positionY += (mainGraphDefaultHeight / 2 - 10) / 10

    def drawGraphDetails(self, graph, component):
        """
        Creates the lines and numbers oriented horizontally which will indicate
        the usage percentage on the main graph.
        """
        graph.create_text(mainGraphDefaultWidth - 35, 10, fill="#72B2D6", font="Times 10 italic bold",
                          text=f"{component} Usage")
        positionY = 0
        while positionY < mainGraphDefaultHeight:
            if positionY != 0 and positionY != mainGraphDefaultHeight:
                graph.create_line(30, positionY, mainGraphDefaultWidth, positionY, fill='#E6F1F8')
                graph.create_text(15, positionY, fill="#72B2D6", font="Times 10 italic bold",
                                  text=str(int(100 - positionY / mainGraphDefaultHeight * 100)))
            positionY += mainGraphDefaultHeight / 10
