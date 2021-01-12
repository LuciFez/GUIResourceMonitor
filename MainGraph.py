from tkinter import *
import psutil
import threading
import MainCPUThread
import MainGPUThread
import MainRAMThread
import MainHDDThread
import MainNETThread
import Gui
from psutil._common import bytes2human
import GPUtil

mainGraphDefaultWidth = 600
mainGraphDefaultHeight = 200

cpu = False
gpu = False
ram = False
hdd = False
net = False


class AppClass:
    def __init__(self, graph):
        #draw the current graph based on the current component
        self.drawCPUGraph(graph)

    #draw the cpu component
    def drawCPUGraph(self, graph):
        #declaration of the Main graph of the CPU component
        self.mainCPUGraph = Canvas(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white",
                                   highlightthickness=1, highlightbackground="#5CA6D0")
        self.mainCPUGraph.grid(row=0, column=0,padx=2)
        #draw details for the main CPU graph
        self.drawGraphDetails(self.mainCPUGraph, "CPU")

        # declare frame for each core of the CPU
        self.miniCPUs = LabelFrame(graph, padx=0, pady=0, bd=0, highlightthickness=0, bg="white")
        self.miniCPUs.grid(row=1, column=0)

        # declare frame for first row of the CPU
        self.miniCPUsRow1 = LabelFrame(self.miniCPUs, padx=0, pady=0, bd=0, highlightthickness=0, bg="white")
        self.miniCPUsRow1.grid(row=0, column=0)
        # declare frame for second row of the CPU
        self.miniCPUsRow2 = LabelFrame(self.miniCPUs, padx=0, pady=0, bd=0, highlightthickness=0, bg="white")
        self.miniCPUsRow2.grid(row=1, column=0)

        # save the number of cores the CPU has
        nbCPUs = psutil.cpu_count(logical=False)
        #declare the list in which we will save references to each core canvas
        self.miniCPUsList = []
        for index in range(0, nbCPUs):
            #check if we iterate through the second half of the cores of CPU
            if index > nbCPUs / 2 - 1:
                #declare Canvas for the current core
                row2 = Canvas(self.miniCPUsRow2, width=mainGraphDefaultWidth / nbCPUs * 2 - 10,
                              height=mainGraphDefaultHeight / 2 - 10, bg="white", bd=0, highlightthickness=1,
                              highlightbackground="#5CA6D0")
                row2.grid(row=1, column=int(index - nbCPUs / 2), padx=5, pady=5)
                #append it to the list of Canvas
                self.miniCPUsList.append(row2)
                #draw details for this canvas
                self.drawMiniCPUsDetails(row2, index + 1)
            #we are in the first half of the cores of CPU
            else:
                #declare Canvas for the current core
                row1 = Canvas(self.miniCPUsRow1, width=mainGraphDefaultWidth / nbCPUs * 2 - 10,
                              height=mainGraphDefaultHeight / 2 - 10, bg="white", bd=0, highlightthickness=1,
                              highlightbackground="#5CA6D0")
                row1.grid(row=0, column=int(index), padx=5, pady=5)
                #append it to the list of Canvas
                self.miniCPUsList.append(row1)
                #draw details for this canvas
                self.drawMiniCPUsDetails(row1, index + 1)

        # add frame for details about CPU
        cpuDetailsFrame = LabelFrame(graph, padx=0, pady=0, bd=0, highlightthickness=0, bg="white")
        cpuDetailsFrame.grid(row=2, column=0)
        self.speedFullCPU = Label(cpuDetailsFrame,
                                  text="CPU speed: " + str(Gui.cpuPercentage[len(Gui.cpuPercentage) - 1]), width=20,
                                  bg="white", bd=0, highlightthickness=0, anchor='w')
        self.speedFullCPU.grid(row=0, column=0)

        # declare list for each core speed
        self.speedList = []
        for index in range(0, nbCPUs):
            #check if we are on the second half of the cores
            if index > nbCPUs / 2 - 1:
                #declare label for the current core
                speed = Label(cpuDetailsFrame, text="Core " + str(index + 1) + " speed: " + str(
                    Gui.cpuPercentagePerCore[len(Gui.cpuPercentagePerCore) - 1][index]), width=20, bg="white", bd=0,
                              highlightthickness=0,
                              padx=10, pady=5, anchor='w')
                speed.grid(row=2, column=int(index - nbCPUs / 2))
                #add core to list
                self.speedList.append(speed)
            #we are in the first half of the cores
            else:
                #declare label for the current core
                speed = Label(cpuDetailsFrame, text="Core " + str(index + 1) + " speed: " + str(
                    Gui.cpuPercentagePerCore[len(Gui.cpuPercentagePerCore) - 1][index]), width=20, bg="white", bd=0,
                              highlightthickness=0,
                              padx=10, pady=5, anchor='w')
                #add core to list
                speed.grid(row=1, column=int(index))
                self.speedList.append(speed)

        #declare thread for the main CPU graph and send the necessary widgets that will be updated
        self.cpuThread = threading.Thread(target=MainCPUThread.cpuThread, args=(
            self.mainCPUGraph, self.miniCPUsList, self.speedFullCPU, self.speedList), daemon=True)
        self.cpuThread.start()

    #draw the gpu component
    def drawGPUGraph(self, graph):
        #get GPU
        GPUs = GPUtil.getGPUs()
        #if there is a nvidia GPU installed
        if len(GPUs) > 0:
            #display GPU name
            self.gpuName = Label(graph, text=GPUs[0].name, bg="white", bd=0,font=("TkDefaultFont", 14))
            self.gpuName.grid(row=0, column=0)
            #declaration of GPU main graph canvas
            self.gpuCanvas = Canvas(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white",
                                      highlightthickness=1, highlightbackground="#5CA6D0")
            self.gpuCanvas.grid(row=1, column=0, padx=2, pady=2)
            #declaration of GPU details frame
            self.gpuDetails = LabelFrame(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight,
                                            bg="white",
                                            bd=0, highlightthickness=0)
            self.gpuDetails.grid(row=2, column=0,pady=20)
            #add details to frame
            self.gpuTM = Label(self.gpuDetails, text="Total memory: "+str(GPUs[0].memoryTotal)+" MB", bg="white", bd=0,anchor='w',font=("TkDefaultFont", 14))
            self.gpuTM.grid(row=0, column=0,pady=5)
            self.gpuAM = Label(self.gpuDetails, text="Available memory: "+str(GPUs[0].memoryFree)+" MB", bg="white", bd=0,anchor='w',font=("TkDefaultFont", 14))
            self.gpuAM.grid(row=1, column=0,pady=5)
            self.gpuUM = Label(self.gpuDetails, text="Used memory: "+str(GPUs[0].memoryUsed)+" MB", bg="white", bd=0,anchor='w',font=("TkDefaultFont", 14))
            self.gpuUM.grid(row=2, column=0,pady=5)
            self.gpuTemp = Label(self.gpuDetails, text="Temperature: "+str(GPUs[0].temperature)+" Celsius", bg="white", bd=0,anchor='w',font=("TkDefaultFont", 14))
            self.gpuTemp.grid(row=3, column=0,pady=5)
            #draw details to main graph of GPU
            self.drawGraphDetails(self.gpuCanvas, "GPU")
            #declaration of GPU thread
            self.gpuThread = threading.Thread(target=MainGPUThread.gpuThread, args=(self.gpuCanvas, self.gpuTM, self.gpuAM, self.gpuUM, self.gpuTemp), daemon=True)
            #start GPU thread
            self.gpuThread.start()
        else:
            #display advertisement for Nvidia
            self.gpuStatus = Label(graph, text="Buy Nvidia", bg="white", bd=0,font=("TkDefaultFont", 32))
            self.gpuStatus.grid(row=0,column=0,padx=mainGraphDefaultWidth/2-102,pady=mainGraphDefaultHeight/2)

    #draw the ram component
    def drawRAMGraph(self, graph):
        #declare main RAM graph
        self.mainRAMGraph = Canvas(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white",
                                   highlightthickness=1, highlightbackground="#5CA6D0")
        self.mainRAMGraph.grid(row=0, column=0, padx=2, pady=10)
        #draw details for the main graph
        self.drawGraphDetails(self.mainRAMGraph, "RAM")

        #declare frame for the RAM chart
        self.chartRamLabel = LabelFrame(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white",
                                        bd=0, highlightthickness=0)
        self.chartRamLabel.grid(row=1, column=0)
        #declare RAM usage bar name label
        self.ramText = Label(self.chartRamLabel, text="Usage Bar", bg="white", bd=0)
        self.ramText.grid(row=0, column=0)
        #declare RAM bar
        self.ramBar = Canvas(self.chartRamLabel, width=mainGraphDefaultWidth - 100, height=mainGraphDefaultHeight / 7,
                             bg="white", highlightthickness=1, highlightbackground="#5CA6D0")
        #create delimiter for the current used RAM
        self.ramBar.create_line((mainGraphDefaultWidth - 100) * (float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]) * 100 / (float(Gui.ramAvailable[len(Gui.ramAvailable) - 1][:-1]) + float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]))) / 100,
                                0,
                                (mainGraphDefaultWidth - 100) * (float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]) * 100 / (float(Gui.ramAvailable[len(Gui.ramAvailable) - 1][:-1]) + float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]))) / 100,
                                mainGraphDefaultHeight / 7 + 1,
                                fill='#549401', width=2)
        #draw the usage color over the ram bar
        self.ramBar.create_rectangle(0,0,(mainGraphDefaultWidth - 100) * (float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]) * 100 / (float(Gui.ramAvailable[len(Gui.ramAvailable) - 1][:-1]) + float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]))) / 100,mainGraphDefaultHeight / 7 + 1,fill='#EDF9EB')
        #add percentage over the ram bar
        self.ramBar.create_text(40,mainGraphDefaultHeight / 14+1,fill="#549401",font="TkDefaultFont 8",text=str(Gui.ramPercentage[len(Gui.ramPercentage)-1])+" % used")
        self.ramBar.grid(row=0, column=1, padx=7, pady=10)

        #declare the details label
        self.detailsRamLabel = LabelFrame(graph, bg="white",bd=0, highlightthickness=0)
        self.detailsRamLabel.grid(row=2, column=0)
        #declare the total ram label
        self.totalRam = Label(self.detailsRamLabel,text="Total RAM: " + str(bytes2human(psutil.virtual_memory().total)), bg="white", bd=0)
        self.totalRam.grid(row=0, column=0, padx=20, pady=10)
        #declare the total ram available label
        self.availableRam = Label(self.detailsRamLabel,text="Available RAM: " + str(Gui.ramAvailable[len(Gui.ramAvailable) - 1]), bg="white",bd=0)
        self.availableRam.grid(row=0, column=2, padx=20, pady=10)
        #declare the total ram used label
        self.usedRam = Label(self.detailsRamLabel, text="Used RAM: " + str(Gui.ramUsed[len(Gui.ramUsed) - 1]),bg="white", bd=0)
        self.usedRam.grid(row=0, column=1, padx=20, pady=10)

        #declare the ram thread
        self.ramThread = threading.Thread(target=MainRAMThread.ramThread, args=(
            self.mainRAMGraph, self.ramBar, self.totalRam, self.availableRam, self.usedRam, Gui.ramPercentage,
            Gui.ramAvailable, Gui.ramUsed), daemon=True)
        #start the ram thread
        self.ramThread.start()

    #draw the hdd component
    def drawHDDGraph(self, graph):
        #declaration of hdd canvas
        self.diskIOPerfect = Canvas(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white",
                                    highlightthickness=1, highlightbackground="#5CA6D0")
        self.diskIOPerfect.grid(row=0, column=0, padx=0, pady=0)
        #add label to indicate speed on the top of the canvas
        self.diskIOPerfect.create_text(30, 8, fill="black", font="TkDefaultFont 8", text="Max speed")
        #add label to indicate speed on the bottom of the canvas
        self.diskIOPerfect.create_text(30, mainGraphDefaultHeight - 8, fill="black", font="TkDefaultFont 8",
                                       text="Low speed")
        #add text and color to indicate the read line color
        self.diskIOPerfect.create_text(30, 18, fill="blue", font="TkDefaultFont 8", text="MBps read")
        #add text and color to indicate the write line color
        self.diskIOPerfect.create_text(36, 28, fill="#549401", font="TkDefaultFont 8", text="MBps written")

        #add cavas to display the drives
        self.barCanvas = Canvas(graph,width=mainGraphDefaultWidth,height=mainGraphDefaultHeight, bg="white", bd=0, highlightthickness=0)
        self.barCanvas.grid(row=1,column=0,padx=3,pady=3)

        #get the number of partitions in the system
        Gui.hddPartitionNumber = len(psutil.disk_partitions(all=True))
        partitions = psutil.disk_partitions(all=True)
        #for each partition in the system
        for i in range(0,Gui.hddPartitionNumber):
            #draw rectangle in the canvas for partition i
            self.barCanvas.create_rectangle(70, mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1) - 20,mainGraphDefaultWidth - 20,mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1) + 20,outline="#549401")
            #draw rectangle in the canvas for usage of partition i
            self.barCanvas.create_rectangle(71, mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1) - 19,(Gui.hddUsed[len(Gui.hddUsed) - 1][i] * 100 / (Gui.hddFree[len(Gui.hddFree) - 1][i] + Gui.hddUsed[len(Gui.hddUsed) - 1][i]))*(mainGraphDefaultWidth - 90)/100 + 70, mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1) + 19,fill="#EDF9EB", outline="#EDF9EB")
            #set label with the percentage used of partition i
            self.barCanvas.create_text(120,mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1), fill="#549401", font="TkDefaultFont 10", text=str(Gui.hddUsed[len(Gui.hddUsed) - 1][i] * 100 / (Gui.hddFree[len(Gui.hddFree) - 1][i] + Gui.hddUsed[len(Gui.hddUsed) - 1][i]))[:5]+ "% used")
            #set label with the name of the partition
            self.barCanvas.create_text(40,mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1), fill="black", font="TkDefaultFont 12",text=str(partitions[i].device[:1])+":/")

        #declare thread to display real time the HDD usage
        self.hddThread = threading.Thread(target=MainHDDThread.hddThread, args=(self.barCanvas, self.diskIOPerfect),daemon=True)
        #start thread to display real time the HDD usage
        self.hddThread.start()

    #draw the net component
    def drawNETGraph(self, graph):
        #declaration of main net canvas graph
        self.netIOCanvas= Canvas(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white",
                                    highlightthickness=1, highlightbackground="#5CA6D0")
        self.netIOCanvas.grid(row=0, column=0, padx=2, pady=2)
        #set text for max speed on top of the canvas
        self.netIOCanvas.create_text(30, 8, fill="black", font="TkDefaultFont 8", text="Max speed")
        #set text for min speed on top of the canvas
        self.netIOCanvas.create_text(30, mainGraphDefaultHeight - 8, fill="black", font="TkDefaultFont 8",text="Low speed")

        #create text to indicate the received MBps
        self.netIOCanvas.create_text(40, 18, fill="blue", font="TkDefaultFont 8", text="MBps received")
        #create text to indicate the sent MBps
        self.netIOCanvas.create_text(29, 28, fill="#549401", font="TkDefaultFont 8", text="MBps sent")

        #declared thread for internet
        self.netThread = threading.Thread(target=MainNETThread.netThread, args=(self.netIOCanvas,), daemon=True)
        #start thread for internet
        self.netThread.start()

    #draw the details for the small graphs on the right side of the app
    def drawMiniCPUsDetails(self, cpu, index):
        #set component
        cpu.create_text((mainGraphDefaultHeight) - 25, 5, fill="#72B2D6", font="Times 6 italic bold",
                        text=f"CPU {index}")
        #set height to the top of the canvas
        positionY = 0
        #while the height has not reched the bottom of the mini canvas
        while positionY < (mainGraphDefaultHeight / 2 - 10):
            #do not show/draw anything for 100 percent and 0 percent
            if positionY != 0 and positionY != mainGraphDefaultHeight:
                #create line for the current percent of the height (from 10 to 10 percent increase)
                cpu.create_line(20, positionY, mainGraphDefaultWidth, positionY, fill='#E6F1F8')
                #add the percent of the height
                cpu.create_text(10, positionY, fill="#72B2D6", font="Times 6 italic bold",
                                text=str(int(100 - positionY / (mainGraphDefaultHeight / 2 - 10) * 100)))
            positionY += (mainGraphDefaultHeight / 2 - 10) / 10

    #same as above but for bigger graphs
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