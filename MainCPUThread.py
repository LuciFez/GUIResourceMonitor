import time
import MainGraph
import threading
import psutil


def cpuThread(mainGraphCanvas, miniCPUsCanvasList, fullSpeedCPULabel, eachCoreLabelList, speedList, speedListPerCPU):
    if MainGraph.cpu == True:

        """
        for checking threads
        print(speedList)
        for thread in threading.enumerate():
            print(thread.name)
        """

        mainGraphCanvas.delete("all")
        drawGraphDetails(mainGraphCanvas, "CPU")

        # draw graph usage lines
        if len(speedList) > 1:
            i = len(speedList) - 1
            fullSpeedCPULabel.config(text="CPU speed: " + str(speedList[i]))
            positionX = MainGraph.mainGraphDefaultWidth
            while (i > 1):
                if len(speedList) > 30 and i < len(speedList) - 30:
                    break
                mainGraphCanvas.create_line(positionX,
                                            MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                            speedList[i],
                                            positionX - MainGraph.mainGraphDefaultWidth / 30,
                                            MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                            speedList[i - 1],
                                            fill='#549401', width=2)
                positionX -= MainGraph.mainGraphDefaultWidth / 30
                i -= 1

        for miniCPU in miniCPUsCanvasList:
            miniCPU.delete("all")
            drawMiniCPUsDetails(miniCPU, miniCPUsCanvasList.index(miniCPU) + 1)

        for miniCPU in miniCPUsCanvasList:
            index = miniCPUsCanvasList.index(miniCPU)
            percentage = []
            for p in speedListPerCPU:
                percentage.append(p[index])
                if speedListPerCPU.index(p) == len(speedListPerCPU)-1:
                    eachCoreLabelList[index].config(text = "Core " + str(index+1) + " speed: "+str(p[index]))

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

        time.sleep(1)
        cpuThread(mainGraphCanvas, miniCPUsCanvasList, fullSpeedCPULabel, eachCoreLabelList, speedList, speedListPerCPU)
    else:
        print("Stopped the thread CPU")


def drawMiniCPUsDetails(cpu, index):
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
    graph.create_text(MainGraph.mainGraphDefaultWidth - 35, 10, fill="#72B2D6", font="Times 10 italic bold",
                      text=f"{component} Usage")
    positionY = 0
    while positionY < MainGraph.mainGraphDefaultHeight:
        if positionY != 0 and positionY != MainGraph.mainGraphDefaultHeight:
            graph.create_line(30, positionY, MainGraph.mainGraphDefaultWidth, positionY, fill='#E6F1F8')
            graph.create_text(15, positionY, fill="#72B2D6", font="Times 10 italic bold",
                              text=str(int(100 - positionY / MainGraph.mainGraphDefaultHeight * 100)))
        positionY += MainGraph.mainGraphDefaultHeight / 10
