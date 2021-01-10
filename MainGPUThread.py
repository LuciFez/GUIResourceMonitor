import time
import MainGraph
import GPUtil
import Gui

def gpuThread(gpuCanvas, gpuTM, gpuAM, gpuUM, gpuTemp):
    if MainGraph.gpu == True:
        """
        for checking threads
        print(speedList)
        for thread in threading.enumerate():
            print(thread.name)
        """
        try:
            gpuCanvas.delete("all")

            drawGraphDetails(gpuCanvas, "GPU")

            GPUs = GPUtil.getGPUs()
            gpuTM.config(text="Total memory: " + str(GPUs[0].memoryTotal) + " MB")
            gpuAM.config(text="Available memory: " + str(GPUs[0].memoryFree) + " MB")
            gpuUM.config(text="Used memory: " + str(GPUs[0].memoryUsed) + " MB")
            gpuTemp.config(text="Temperature: " + str(GPUs[0].temperature) + " Celsius")

            if len(Gui.gpuPercentage) > 1:
                i = len(Gui.gpuPercentage) - 1
                positionX = MainGraph.mainGraphDefaultWidth
                while (i > 1):
                    if len(Gui.gpuPercentage) > 30 and i < len(Gui.gpuPercentage) - 30:
                        break
                    gpuCanvas.create_line(positionX,
                                                MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                Gui.gpuPercentage[i],
                                                positionX - MainGraph.mainGraphDefaultWidth / 30,
                                                MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                Gui.gpuPercentage[i - 1],
                                                fill='#549401', width=2)
                    positionX -= MainGraph.mainGraphDefaultWidth / 30
                    i -= 1
        except:
            pass
        time.sleep(1)
        gpuThread(gpuCanvas, gpuTM, gpuAM, gpuUM, gpuTemp)
    else:
        print("Stopped the thread GPU")


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
