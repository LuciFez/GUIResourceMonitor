import time
import MainGraph
import Gui
import threading
import psutil
from psutil._common import bytes2human


def hddThread(barCanvas):
    if MainGraph.hdd == True:
        barCanvas.delete("all")

        barCanvas.create_line(0, MainGraph.mainGraphDefaultWidth, MainGraph.mainGraphDefaultWidth, MainGraph.mainGraphDefaultHeight + 100)
        partitions = psutil.disk_partitions(all=True)
        if (Gui.hddPartitionNumber == len(partitions)):
            for i in range(0, Gui.hddPartitionNumber):

                barCanvas.create_rectangle(MainGraph.mainGraphDefaultWidth / (Gui.hddPartitionNumber + 1) * (i + 1) - 19,
                                           (MainGraph.mainGraphDefaultHeight + 100 - 20) - (MainGraph.mainGraphDefaultHeight + 100 - 20) * (
                                                Gui.hddUsed[len(Gui.hddFree) - 1][i] * 100 / (
                                                Gui.hddFree[len(Gui.hddFree) - 1][i] +
                                                Gui.hddUsed[len(Gui.hddUsed) - 1][i])) / 100
                                                , MainGraph.mainGraphDefaultWidth / (Gui.hddPartitionNumber + 1) * (i + 1) + 19,
                                                MainGraph.mainGraphDefaultHeight + 100 - 21, fill="#EDF9EB", outline="#EDF9EB")
                barCanvas.create_rectangle(
                    MainGraph.mainGraphDefaultWidth / (Gui.hddPartitionNumber + 1) * (i + 1) - 20, 0,
                    MainGraph.mainGraphDefaultWidth / (Gui.hddPartitionNumber + 1) * (i + 1) + 20,
                    MainGraph.mainGraphDefaultHeight + 100 - 20, outline="#549401")

                barCanvas.create_text(MainGraph.mainGraphDefaultWidth / (Gui.hddPartitionNumber + 1) * (i + 1),MainGraph.mainGraphDefaultHeight + 100 - 30, fill="#549401", font="TkDefaultFont 10", text=str(Gui.hddUsed[len(Gui.hddUsed) - 1][i] * 100 / (Gui.hddFree[len(Gui.hddFree) - 1][i] + Gui.hddUsed[len(Gui.hddUsed) - 1][i]))[:5])
                barCanvas.create_text(MainGraph.mainGraphDefaultWidth / (Gui.hddPartitionNumber + 1) * (i + 1),MainGraph.mainGraphDefaultHeight + 100 - 6, fill="black", font="TkDefaultFont 12",text=str(partitions[i].device[:1]).lower()+":/")
                barCanvas.create_text(MainGraph.mainGraphDefaultWidth / (Gui.hddPartitionNumber + 1) * (i + 1)-42,MainGraph.mainGraphDefaultHeight + 100 - 30, fill="black", font="TkDefaultFont 10",text="Usage: ")
        else:
            barCanvas.create_text(MainGraph.mainGraphDefaultWidth/2,(MainGraph.mainGraphDefaultHeight+100)/2, fill="#549401", font="TkDefaultFont 16",text="Loading...")
            time.sleep(1)
            hddThread(barCanvas)

        time.sleep(1)
        hddThread(barCanvas)
    else:
        print("Stopped the thread HDD")