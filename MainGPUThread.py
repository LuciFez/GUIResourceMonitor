import time
import MainGraph
import GPUtil
import Gui

def gpuThread(gpuCanvas, gpuTM, gpuAM, gpuUM, gpuTemp):
    #check if the current component displayed is the GPU
    if MainGraph.gpu == True:
        """
        for checking threads
        print(speedList)
        for thread in threading.enumerate():
            print(thread.name)
        """
        try:
            #delete everthing from gpu main graph canvas
            gpuCanvas.delete("all")
            #draw details to the graph
            drawGraphDetails(gpuCanvas, "GPU")
            #declaration of GPUtil
            GPUs = GPUtil.getGPUs()
            #set total memory
            gpuTM.config(text="Total memory: " + str(GPUs[0].memoryTotal) + " MB")
            #set total memory available
            gpuAM.config(text="Available memory: " + str(GPUs[0].memoryFree) + " MB")
            #set total memory used
            gpuUM.config(text="Used memory: " + str(GPUs[0].memoryUsed) + " MB")
            #set current temperature
            gpuTemp.config(text="Temperature: " + str(GPUs[0].temperature) + " Celsius")

            #if there are more the one gpu percentages captured
            if len(Gui.gpuPercentage) > 1:
                #get the size of the list with the percentages
                i = len(Gui.gpuPercentage) - 1
                #set the x position to the right of the cavas
                positionX = MainGraph.mainGraphDefaultWidth
                #while there are still percentages to be displayed
                while (i > 1):
                    #if we already surpassed the 30 seconds of the graph
                    if len(Gui.gpuPercentage) > 30 and i < len(Gui.gpuPercentage) - 30:
                        break
                    #create line from the current percentage to the previous percentage
                    gpuCanvas.create_line(positionX,
                                                MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                Gui.gpuPercentage[i],
                                                positionX - MainGraph.mainGraphDefaultWidth / 30,
                                                MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                Gui.gpuPercentage[i - 1],
                                                fill='#549401', width=2)
                    #set the x position for the previous percentage
                    positionX -= MainGraph.mainGraphDefaultWidth / 30
                    #set i to the previous second/percentage
                    i -= 1
        except:
            pass
        #wait 1 second to update the graph
        time.sleep(1)
        #recursive call for thread
        gpuThread(gpuCanvas, gpuTM, gpuAM, gpuUM, gpuTemp)
    else:
        #stop the thread
        print("Stopped the thread GPU")

#same as the MainGraph.drawGraphDetails
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
