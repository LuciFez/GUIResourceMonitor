import time
import MainGraph
import Gui
import threading
import psutil
from psutil._common import bytes2human


def ramThread(mainRAMGraph, ramBar, totalRam, availableRam, usedRam, ramPercentage,ramAvailable, ramUsed):
    if MainGraph.ram == True:

        """
        for thread in threading.enumerate():
            print(thread.name)
        """


        mainRAMGraph.delete("all")
        drawGraphDetails(mainRAMGraph, "RAM")

        # draw graph usage lines
        if len(ramPercentage) > 1:
            i = len(ramPercentage) - 1
            positionX = MainGraph.mainGraphDefaultWidth
            while (i > 1):
                if len(ramPercentage) > 30 and i < len(ramPercentage) - 30:
                    break
                mainRAMGraph.create_line(positionX,
                                            MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                            ramPercentage[i],
                                            positionX - MainGraph.mainGraphDefaultWidth / 30,
                                            MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                            ramPercentage[i - 1],
                                            fill='#549401', width=2)
                positionX -= MainGraph.mainGraphDefaultWidth / 30
                i -= 1

        ramBar.delete("all")
        ramBar.create_line((MainGraph.mainGraphDefaultWidth - 100) * (float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]) * 100 / (float(Gui.ramAvailable[len(Gui.ramAvailable) - 1][:-1]) + float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]))) / 100,
                            0,
                            (MainGraph.mainGraphDefaultWidth - 100) * (float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]) * 100 / (float(Gui.ramAvailable[len(Gui.ramAvailable) - 1][:-1]) + float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]))) / 100,
                            MainGraph.mainGraphDefaultHeight / 7 + 1,
                            fill='#549401', width=2)
        ramBar.create_rectangle(0, 0, (MainGraph.mainGraphDefaultWidth - 100) * (float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]) * 100 / (float(Gui.ramAvailable[len(Gui.ramAvailable) - 1][:-1]) + float(Gui.ramUsed[len(Gui.ramUsed) - 1][:-1]))) / 100, MainGraph.mainGraphDefaultHeight / 7 + 1, fill='#EDF9EB')
        ramBar.create_text(40, MainGraph.mainGraphDefaultHeight / 14 + 1, fill="#549401", font="TkDefaultFont 8",text=str(Gui.ramPercentage[len(Gui.ramPercentage) - 1]) + " % used")

        totalRam.config(text="Total RAM: " + str(bytes2human(psutil.virtual_memory().total)))
        availableRam.config(text="Available RAM: " + str(Gui.ramAvailable[len(Gui.ramAvailable) - 1]))
        usedRam.config(text="Used RAM: " + str(Gui.ramUsed[len(Gui.ramUsed) - 1]))

        time.sleep(1)
        ramThread(mainRAMGraph, ramBar, totalRam, availableRam, usedRam, ramPercentage,ramAvailable, ramUsed)
    else:
        print("Stopped the thread RAM")

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
