import time
import MainGraph
import Gui
import psutil
from psutil._common import bytes2human


def ramThread(mainRAMGraph, ramBar, totalRam, availableRam, usedRam, ramPercentage,ramAvailable, ramUsed):
    #check if the current component is the RAM
    if MainGraph.ram == True:
        """
        for thread in threading.enumerate():
            print(thread.name)
        """

        try:
            #deleta everthing from the ram canvas
            mainRAMGraph.delete("all")
            #add details to ram Canvas
            drawGraphDetails(mainRAMGraph, "RAM")
            #if there are for then one ram percentages captured
            if len(ramPercentage) > 1:
                #set i on as the size of the list with the ram percentages
                i = len(ramPercentage) - 1
                #set the position on the right side of the canvas
                positionX = MainGraph.mainGraphDefaultWidth
                #while there are still percentages
                while (i > 1):
                    #if we exceeded the limit of the 30 seconds of the main RAM graph
                    if len(ramPercentage) > 30 and i < len(ramPercentage) - 30:
                        break
                    #draw line from the current percentage of used ram to the previous one
                    mainRAMGraph.create_line(positionX,
                                                MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                ramPercentage[i],
                                                positionX - MainGraph.mainGraphDefaultWidth / 30,
                                                MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                ramPercentage[i - 1],
                                                fill='#549401', width=2)
                    #set the x position to the previous ram percentage captured
                    positionX -= MainGraph.mainGraphDefaultWidth / 30
                    #set i to the previous percentage index
                    i -= 1

            #delete everything from the RAM bar
            ramBar.delete("all")
            #create line to separate the used from the available ram percentage
            ramBar.create_line((MainGraph.mainGraphDefaultWidth - 100) * (float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]) * 100 / (float(Gui.ramAvailable[len(Gui.ramAvailable) - 1][:-1]) + float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]))) / 100,
                                0,
                                (MainGraph.mainGraphDefaultWidth - 100) * (float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]) * 100 / (float(Gui.ramAvailable[len(Gui.ramAvailable) - 1][:-1]) + float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]))) / 100,
                                MainGraph.mainGraphDefaultHeight / 7 + 1,
                                fill='#549401', width=2)

            # draw the usage color over the ram bar
            ramBar.create_rectangle(0, 0, (MainGraph.mainGraphDefaultWidth - 100) * (float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]) * 100 / (float(Gui.ramAvailable[len(Gui.ramAvailable) - 1][:-1]) + float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]))) / 100, MainGraph.mainGraphDefaultHeight / 7 + 1, fill='#EDF9EB')
            #add percentage over the ram bar
            ramBar.create_text(40, MainGraph.mainGraphDefaultHeight / 14 + 1, fill="#549401", font="TkDefaultFont 8",text=str(Gui.ramPercentage[len(Gui.ramPercentage) - 1]) + " % used")

            #modify the total ram usage label
            totalRam.config(text="Total RAM: " + str(bytes2human(psutil.virtual_memory().total)))
            #modify the total available ram usage label
            availableRam.config(text="Available RAM: " + str(Gui.ramAvailable[len(Gui.ramAvailable) - 1]))
            #modify the total used ram usage label
            usedRam.config(text="Used RAM: " + str(Gui.ramUsed[len(Gui.ramUsed) - 1]))
        except:
            pass
        #sleep for one second
        time.sleep(1)
        #recursive call for the ram thread
        ramThread(mainRAMGraph, ramBar, totalRam, availableRam, usedRam, ramPercentage,ramAvailable, ramUsed)
    else:
        print("Stopped the thread RAM")

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
