import time
import MainGraph
import Gui
import psutil


def hddThread(barCanvas,diskIOPerfect):
    if MainGraph.hdd == True:
        barCanvas.delete("all")
        diskIOPerfect.delete("all")
        barCanvas.create_line(0, MainGraph.mainGraphDefaultWidth, MainGraph.mainGraphDefaultWidth, MainGraph.mainGraphDefaultHeight )
        partitions = psutil.disk_partitions(all=True)
        if (Gui.hddPartitionNumber == len(partitions)):
            for i in range(0, Gui.hddPartitionNumber):
                barCanvas.create_rectangle(70,
                                                MainGraph.mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1) - 20,
                                                MainGraph.mainGraphDefaultWidth - 20,
                                                MainGraph.mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1) + 20,
                                                outline="#549401")
                barCanvas.create_rectangle(71,
                                                MainGraph.mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1) - 19, (
                                                            Gui.hddUsed[len(Gui.hddUsed) - 1][i] * 100 / (
                                                                Gui.hddFree[len(Gui.hddFree) - 1][i] +
                                                                Gui.hddUsed[len(Gui.hddUsed) - 1][i])) * (
                                                            MainGraph.mainGraphDefaultWidth - 90) / 100 + 70,
                                                MainGraph.mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1) + 19,
                                                fill="#EDF9EB", outline="#EDF9EB")

                barCanvas.create_text(120, MainGraph.mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1),
                                           fill="#549401", font="TkDefaultFont 10", text=str(
                        Gui.hddUsed[len(Gui.hddUsed) - 1][i] * 100 / (
                                    Gui.hddFree[len(Gui.hddFree) - 1][i] + Gui.hddUsed[len(Gui.hddUsed) - 1][i]))[
                                                                                         :5] + "% used")
                barCanvas.create_text(40, MainGraph.mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1),
                                           fill="black", font="TkDefaultFont 12",
                                           text=str(partitions[i].device[:1]) + ":/")

            if len(Gui.diskWrite) > 1:
                i = len(Gui.diskWrite) - 1
                positionX = MainGraph.mainGraphDefaultWidth

                diffList = []
                for index in range(0,len(Gui.diskWrite)-1):
                    diffList.append(Gui.diskWrite[index+1][0]-Gui.diskWrite[index][0])

                while i > 1:
                    if len(Gui.diskWrite) > 30 and i < len(Gui.diskWrite) - 30:
                        break
                    diskIOPerfect.create_line(positionX,
                                      MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * ((Gui.diskWrite[i][0]-Gui.diskWrite[i-1][0])*100/max(diffList)),
                                      positionX - MainGraph.mainGraphDefaultWidth / 30,
                                      MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * ((Gui.diskWrite[i-1][0]-Gui.diskWrite[i-2][0])*100/max(diffList)),
                                      fill='#549401', width=2)
                    if (Gui.diskWrite[i][0]-Gui.diskWrite[i-1][0])/1000000 > max(diffList)/2:
                        diskIOPerfect.create_text(positionX-10,
                                          MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * ((Gui.diskWrite[i][0]-Gui.diskWrite[i-1][0])*100/max(diffList))+14,
                                          text= str((Gui.diskWrite[i][0]-Gui.diskWrite[i-1][0])/1000000)[:4])
                    else:
                        diskIOPerfect.create_text(positionX - 10,
                                          MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * ((Gui.diskWrite[i][0] - Gui.diskWrite[i - 1][0]) * 100 / max(diffList)) - 14,
                                          text=str((Gui.diskWrite[i][0] - Gui.diskWrite[i - 1][0]) / 1000000)[:4])
                    positionX -= MainGraph.mainGraphDefaultWidth / 30
                    i -= 1

                if len(Gui.diskRead) > 1:
                    i = len(Gui.diskRead) - 1
                    positionX = MainGraph.mainGraphDefaultWidth

                    diffList = []
                    for index in range(0, len(Gui.diskRead) - 1):
                        diffList.append(Gui.diskRead[index + 1][0] - Gui.diskRead[index][0])

                    while i > 1:
                        if len(Gui.diskRead) > 30 and i < len(Gui.diskRead) - 30:
                            break
                        diskIOPerfect.create_line(positionX,
                                                  MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * (
                                                              (Gui.diskRead[i][0] - Gui.diskRead[i - 1][
                                                                  0]) * 100 / max(diffList)),
                                                  positionX - MainGraph.mainGraphDefaultWidth / 30,
                                                  MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * (
                                                              (Gui.diskRead[i - 1][0] - Gui.diskRead[i - 2][
                                                                  0]) * 100 / max(diffList)),
                                                  fill='blue', width=2)
                        if (Gui.diskRead[i][0] - Gui.diskRead[i - 1][0]) / 1000000 > max(diffList) / 2:
                            diskIOPerfect.create_text(positionX - 10,
                                                      MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * (
                                                                  (Gui.diskRead[i][0] - Gui.diskRead[i - 1][
                                                                      0]) * 100 / max(diffList)) + 14,
                                                      text=str(
                                                          (Gui.diskRead[i][0] - Gui.diskRead[i - 1][0]) / 1000000)[
                                                           :4])
                        else:
                            diskIOPerfect.create_text(positionX - 10,
                                                      MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * (
                                                                  (Gui.diskRead[i][0] - Gui.diskRead[i - 1][
                                                                      0]) * 100 / max(diffList)) - 14,
                                                      text=str(
                                                          (Gui.diskRead[i][0] - Gui.diskRead[i - 1][0]) / 1000000)[
                                                           :4])
                        positionX -= MainGraph.mainGraphDefaultWidth / 30
                        i -= 1

                diskIOPerfect.create_text(30, 8, fill="black",font="TkDefaultFont 8", text="Max speed")
                diskIOPerfect.create_text(30, MainGraph.mainGraphDefaultHeight - 8, fill="black",font="TkDefaultFont 8", text="Low speed")
        else:
            barCanvas.create_text(MainGraph.mainGraphDefaultWidth/2,(MainGraph.mainGraphDefaultHeight)/2, fill="#549401", font="TkDefaultFont 16",text="Loading...")
            diskIOPerfect.config(highlightthickness=0, highlightbackground="#5CA6D0")
            time.sleep(1)
            diskIOPerfect.config(highlightthickness=1, highlightbackground="#5CA6D0")
            hddThread(barCanvas,diskIOPerfect)

        time.sleep(1)
        hddThread(barCanvas,diskIOPerfect)
    else:
        print("Stopped the thread HDD")