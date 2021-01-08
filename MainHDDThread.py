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
        numberPartitions = len(psutil.disk_partitions(all=True))
        partitions = psutil.disk_partitions(all=True)
        for i in range(0, numberPartitions):
            barCanvas.create_rectangle(MainGraph.mainGraphDefaultWidth / (numberPartitions + 1) * (i + 1) - 20, 0,
                                            MainGraph.mainGraphDefaultWidth / (numberPartitions + 1) * (i + 1) + 20,
                                            MainGraph.mainGraphDefaultHeight + 100 - 20, outline="#549401")
            barCanvas.create_rectangle(MainGraph.mainGraphDefaultWidth / (numberPartitions + 1) * (i + 1) - 19,
                                            (MainGraph.mainGraphDefaultHeight + 100 - 20) - (MainGraph.mainGraphDefaultHeight + 100 - 20) * (
                                                        Gui.hddFree[len(Gui.hddFree) - 1][i] * 100 / (
                                                            Gui.hddFree[len(Gui.hddFree) - 1][i] +
                                                            Gui.hddUsed[len(Gui.hddUsed) - 1][i])) / 100
                                            , MainGraph.mainGraphDefaultWidth / (numberPartitions + 1) * (i + 1) + 19,
                                            MainGraph.mainGraphDefaultHeight + 100 - 21, fill="#EDF9EB", outline="#EDF9EB")
            barCanvas.create_text(MainGraph.mainGraphDefaultWidth / (numberPartitions + 1) * (i + 1),
                                       MainGraph.mainGraphDefaultHeight + 100 - 30, fill="#549401", font="TkDefaultFont 10", text=str(
                    Gui.hddFree[len(Gui.hddUsed) - 1][i] * 100 / (
                                Gui.hddFree[len(Gui.hddFree) - 1][i] + Gui.hddUsed[len(Gui.hddUsed) - 1][i]))[:5])
            barCanvas.create_text(MainGraph.mainGraphDefaultWidth / (numberPartitions + 1) * (i + 1),
                                       MainGraph.mainGraphDefaultHeight + 100 - 6, fill="black", font="TkDefaultFont 12",
                                       text=str(partitions[i].device[:1]))

        time.sleep(1)
        hddThread(barCanvas)
    else:
        print("Stopped the thread HDD")