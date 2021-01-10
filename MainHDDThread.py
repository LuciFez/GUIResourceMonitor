import time
import MainGraph
import Gui
import psutil


def hddThread(barCanvas,diskIOPerfect):
    if MainGraph.hdd == True:
        barCanvas.delete("all")
        diskIOPerfect.delete("all")
        partitions = psutil.disk_partitions(all=True)
        if (Gui.hddPartitionNumber == len(partitions)):
            diskIOPerfect.create_text(30, 8, fill="black", font="TkDefaultFont 8", text="Max speed")
            diskIOPerfect.create_text(30, MainGraph.mainGraphDefaultHeight - 8, fill="black", font="TkDefaultFont 8",
                                      text="Low speed")
            diskIOPerfect.create_text(30, 18, fill="blue", font="TkDefaultFont 8", text="MBps read")
            diskIOPerfect.create_text(36, 28, fill="#549401", font="TkDefaultFont 8", text="MBps written")
            diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth - 14, 8, fill="#72B2D6",
                                      font="Times 10 italic bold", text="HDD")

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

            if len(Gui.diskWrite) > 1 and len(Gui.diskRead) > 1:
                diffWriteList = []
                for index in range(0, len(Gui.diskWrite) - 1):
                    if Gui.diskWrite[index + 1][0] - Gui.diskWrite[index][0] == 0:
                        diffWriteList.append(1)
                    else:
                        diffWriteList.append(Gui.diskWrite[index + 1][0] - Gui.diskWrite[index][0])

                diffReadList = []
                for index in range(0, len(Gui.diskRead) - 1):
                    if Gui.diskRead[index + 1][0] - Gui.diskRead[index][0] == 0:
                        diffReadList.append(1)
                    else:
                        diffReadList.append(Gui.diskRead[index + 1][0] - Gui.diskRead[index][0])

                i = len(diffWriteList) - 1
                positionX = MainGraph.mainGraphDefaultWidth

                while i > 0:
                    diskIOPerfect.create_line(positionX,
                                      MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * (
                                                  diffWriteList[i] * 100 / max(diffReadList + diffWriteList)),
                                      positionX - MainGraph.mainGraphDefaultWidth / 30,
                                      MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * (
                                                  diffWriteList[i - 1] * 100 / max(diffReadList + diffWriteList)),
                                      fill='#549401', width=1)

                    if i==len(diffWriteList)-1:
                        if diffWriteList[i] == 1:
                            diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                      MainGraph.mainGraphDefaultHeight - 10, fill="black",
                                                      font="TkDefaultFont 8", text="0.000000")
                        else:
                            speed = diffWriteList[i] / 1024 / 1024
                            if str(speed).find('e') != -1:
                                diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                        MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                        diffWriteList[i] * 100 / max(diffReadList + diffWriteList) - 10,
                                                        fill="black", font="TkDefaultFont 8", text="0.000000")
                            else:
                                if max(diffReadList + diffWriteList) / 2 < diffWriteList[i]:
                                    diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth - 26,MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *diffWriteList[i] * 100 / max(diffReadList + diffWriteList) + 10, fill="black",font="TkDefaultFont 8", text=str(speed)[:8])
                                else:
                                    diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth - 26,MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *diffWriteList[i] * 100 / max(diffReadList + diffWriteList) - 10, fill="black",font="TkDefaultFont 8", text=str(speed)[:8])

                    positionX -= MainGraph.mainGraphDefaultWidth / 30
                    i -= 1

                i = len(diffReadList) - 1
                positionX = MainGraph.mainGraphDefaultWidth

                while i > 0:
                    diskIOPerfect.create_line(positionX,
                                      MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * diffReadList[
                                          i] * 100 / max(diffReadList + diffWriteList),
                                      positionX - MainGraph.mainGraphDefaultWidth / 30,
                                      MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * diffReadList[
                                          i - 1] * 100 / max(diffReadList + diffWriteList),
                                      fill='blue', width=1)

                    if i==len(diffReadList)-1:
                        if diffReadList[i] == 1:
                            diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth-26, MainGraph.mainGraphDefaultHeight-10, fill="black", font="TkDefaultFont 8", text="0.000000")
                        else:
                            speed = diffReadList[i]/1024/1024
                            if str(speed).find('e') != -1:
                                diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                          MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                          diffWriteList[i] * 100 / max(
                                                              diffReadList + diffWriteList) - 10,
                                                          fill="black", font="TkDefaultFont 8", text="0.000000")
                            else:
                                if max(diffReadList + diffWriteList)/2 < diffReadList[i]:
                                    diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth-26, MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * diffReadList[i] * 100 / max(diffReadList + diffWriteList)+10, fill="black", font="TkDefaultFont 8", text=str(speed)[:8])
                                else:
                                    diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth-26, MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * diffReadList[i] * 100 / max(diffReadList + diffWriteList)-10, fill="black", font="TkDefaultFont 8", text=str(speed)[:8])

                    positionX -= MainGraph.mainGraphDefaultWidth / 30
                    i -= 1
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