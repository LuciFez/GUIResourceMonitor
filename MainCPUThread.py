import time
import MainGraph
import psutil
import Gui
import threading


def cpuThread(mainGraphCanvas, miniCPUsCanvasList, fullSpeedCPULabel, eachCoreLabelList):
    """
    Thread method used to update the CPU component.

    Checks if the CPU component should be displayed. This is the thread safety mechanism:
    it will finish the thread if the component has changed.

    If it should be displayed the:
    Deletes everything from the main canvas for the CPU component, the canvases for each
    phisical core of the CPU and the details frame of the CPU.
    Draw the details again for each canvas and frame.

    Call its self after waiting one second.
    """
    if MainGraph.cpu == True:

        """
        for thread in threading.enumerate():
            print(thread.name)
        """
        try:
            mainGraphCanvas.delete("all")
            drawGraphDetails(mainGraphCanvas, "CPU")

            if len(Gui.cpuPercentage) > 1:
                i = len(Gui.cpuPercentage) - 1
                fullSpeedCPULabel.config(text="CPU speed: " + str(Gui.cpuPercentage[i]))
                positionX = MainGraph.mainGraphDefaultWidth
                while (i > 1):
                    if len(Gui.cpuPercentage) > 30 and i < len(Gui.cpuPercentage) - 30:
                        break
                    mainGraphCanvas.create_line(positionX,
                                                MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                Gui.cpuPercentage[i],
                                                positionX - MainGraph.mainGraphDefaultWidth / 30,
                                                MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                Gui.cpuPercentage[i - 1],
                                                fill='#549401', width=2)
                    positionX -= MainGraph.mainGraphDefaultWidth / 30
                    i -= 1

            for miniCPU in miniCPUsCanvasList:
                miniCPU.delete("all")
                drawMiniCPUsDetails(miniCPU, miniCPUsCanvasList.index(miniCPU) + 1)
            for miniCPU in miniCPUsCanvasList:
                index = miniCPUsCanvasList.index(miniCPU)
                percentage = []
                for p in Gui.cpuPercentagePerCore:
                    percentage.append(p[index])
                    if Gui.cpuPercentagePerCore.index(p) == len(Gui.cpuPercentagePerCore) - 1:
                        eachCoreLabelList[index].config(text="Core " + str(index + 1) + " speed: " + str(p[index]))
                nbCPUs = psutil.cpu_count(logical=False)
                miniCPUHeight = MainGraph.mainGraphDefaultHeight / 2 - 10
                i = len(percentage) - 1
                positionX = MainGraph.mainGraphDefaultWidth / nbCPUs * 2 - 10
                while (i > 1):
                    if len(percentage) > 30 and i < len(percentage) - 30:
                        break
                    miniCPU.create_line(positionX,
                                        miniCPUHeight - miniCPUHeight / 100 *
                                        percentage[i],
                                        positionX - (MainGraph.mainGraphDefaultWidth / nbCPUs * 2 - 10) / 30,
                                        miniCPUHeight - miniCPUHeight / 100 *
                                        percentage[i - 1],
                                        fill='#549401', width=2)
                    positionX -= (MainGraph.mainGraphDefaultWidth / nbCPUs * 2 - 10) / 30
                    i -= 1
        except:
            pass
        time.sleep(1)
        cpuThread(mainGraphCanvas, miniCPUsCanvasList, fullSpeedCPULabel, eachCoreLabelList)
    else:
        print("Stopped the thread CPU")


def drawMiniCPUsDetails(cpu, index):
    """
    Creates the lines and numbers oriented horizontally which will indicate
    the usage percentage on the core graphs.
    """
    cpu.create_text((MainGraph.mainGraphDefaultHeight) - 25, 5, fill="#72B2D6", font="Times 6 italic bold",
                    text=f"CPU {index}")
    positionY = 0
    while positionY < (MainGraph.mainGraphDefaultHeight / 2 - 10):
        if positionY != 0 and positionY != MainGraph.mainGraphDefaultHeight:
            cpu.create_line(20, positionY, MainGraph.mainGraphDefaultWidth, positionY, fill='#E6F1F8')
            cpu.create_text(10, positionY, fill="#72B2D6", font="Times 6 italic bold",
                            text=str(int(100 - positionY / (MainGraph.mainGraphDefaultHeight / 2 - 10) * 100)))
        positionY += (MainGraph.mainGraphDefaultHeight / 2 - 10) / 10


def drawGraphDetails(graph, component):
    """
    Creates the lines and numbers oriented horizontally which will indicate
    the usage percentage on the main graph.
    """
    graph.create_text(MainGraph.mainGraphDefaultWidth - 35, 10, fill="#72B2D6", font="Times 10 italic bold",
                      text=f"{component} Usage")
    positionY = 0
    while positionY < MainGraph.mainGraphDefaultHeight:
        if positionY != 0 and positionY != MainGraph.mainGraphDefaultHeight:
            graph.create_line(30, positionY, MainGraph.mainGraphDefaultWidth, positionY, fill='#E6F1F8')
            graph.create_text(15, positionY, fill="#72B2D6", font="Times 10 italic bold",
                              text=str(int(100 - positionY / MainGraph.mainGraphDefaultHeight * 100)))
        positionY += MainGraph.mainGraphDefaultHeight / 10
