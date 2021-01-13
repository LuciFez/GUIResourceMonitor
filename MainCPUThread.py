import time
import MainGraph
import psutil
import Gui
import threading


def cpuThread(mainGraphCanvas, miniCPUsCanvasList, fullSpeedCPULabel, eachCoreLabelList):
    #check if the thread should be alive
    if MainGraph.cpu == True:

        """
        for thread in threading.enumerate():
            print(thread.name)
        """
        try:
            #delete everything from the main graph canvas
            mainGraphCanvas.delete("all")
            #draw details on main graph canvas
            drawGraphDetails(mainGraphCanvas, "CPU")

            # if there are two or more percentages saved on the list
            if len(Gui.cpuPercentage) > 1:
                #seve the list length
                i = len(Gui.cpuPercentage) - 1
                #add graph description
                fullSpeedCPULabel.config(text="CPU speed: " + str(Gui.cpuPercentage[i]))
                #set the x position to the right of the graph
                positionX = MainGraph.mainGraphDefaultWidth
                #while there are precentages in the list
                while (i > 1):
                    #check to see if we exceeded the 30 seconds limit of the graph
                    if len(Gui.cpuPercentage) > 30 and i < len(Gui.cpuPercentage) - 30:
                        break
                    #draw line from the current i position to the i-1 position in the list
                    #draws the lines from the latest cpu perentage captured to the previous one
                    mainGraphCanvas.create_line(positionX,
                                                MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                Gui.cpuPercentage[i],
                                                positionX - MainGraph.mainGraphDefaultWidth / 30,
                                                MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                Gui.cpuPercentage[i - 1],
                                                fill='#549401', width=2)
                    #change the x position for the previous cpu percentage captured
                    positionX -= MainGraph.mainGraphDefaultWidth / 30
                    #set i to the previous cpu percentage captured
                    i -= 1

            for miniCPU in miniCPUsCanvasList:
                #delete everthing in the mini cpus
                miniCPU.delete("all")
                #add details to them
                drawMiniCPUsDetails(miniCPU, miniCPUsCanvasList.index(miniCPU) + 1)

            #iterate over the mini cpus
            for miniCPU in miniCPUsCanvasList:
                #get the index of the current cpu
                index = miniCPUsCanvasList.index(miniCPU)
                percentage = []
                for p in Gui.cpuPercentagePerCore:
                    #add the percentage of the current core at the p second to the list
                    percentage.append(p[index])
                    #saves the latest captured core percentage
                    if Gui.cpuPercentagePerCore.index(p) == len(Gui.cpuPercentagePerCore)-1:
                        eachCoreLabelList[index].config(text = "Core " + str(index+1) + " speed: "+str(p[index]))
                #get number of cores
                nbCPUs = psutil.cpu_count(logical=False)
                #set the height of the core
                miniCPUHeight = MainGraph.mainGraphDefaultHeight / 2 - 10
                #save the size of the list of percentage of the current core
                i = len(percentage) - 1
                #set the width of the core
                positionX = MainGraph.mainGraphDefaultWidth / nbCPUs * 2 - 10
                #while there are percentages
                while (i > 1):
                    #if we itarate over 30 seconds/percentages
                    if len(percentage) > 30 and i < len(percentage) - 30:
                        break
                    #draw line from the current percentage to the previous one
                    miniCPU.create_line(positionX,
                                        miniCPUHeight - miniCPUHeight / 100 *
                                        percentage[i],
                                        positionX - (MainGraph.mainGraphDefaultWidth / nbCPUs * 2 - 10) / 30,
                                        miniCPUHeight - miniCPUHeight / 100 *
                                        percentage[i - 1],
                                        fill='#549401', width=2)
                    #set x position for the previous percentage
                    positionX -= (MainGraph.mainGraphDefaultWidth / nbCPUs * 2 - 10) / 30
                    #set i to the previous percentage
                    i -= 1
        except:
            pass
        #sleep one second
        time.sleep(1)
        #recursive call of the thread
        cpuThread(mainGraphCanvas, miniCPUsCanvasList, fullSpeedCPULabel, eachCoreLabelList)
    else:
        #component has changed, thread will close
        print("Stopped the thread CPU")

#same as the MainGraph.drawMiniCpuDetails
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
