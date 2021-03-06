import time
import MainGraph
import Gui


def netThread(netIOCanvas):
    """
    Thread method used to update the NET component.

    Checks if the NET component should be displayed. This is the thread safety mechanism:
    it will finish the thread if the component has changed.

    If it should be displayed the:
    Deletes everything from the main canvas for the NET component.
    Draw the details again.

    Call its self after waiting one second.
    """
    if MainGraph.net == True:
        try:
            netIOCanvas.delete("all")

            if len(Gui.netReceived) > 1 and len(Gui.netSent) > 1:

                diffWriteList = []
                for index in range(0, len(Gui.netReceived) - 1):
                    if index == 0:
                        diffWriteList.append(1)
                    elif Gui.netReceived[index + 1] - Gui.netReceived[index] == 0:
                        diffWriteList.append(1)
                    else:
                        diffWriteList.append(Gui.netReceived[index + 1] - Gui.netReceived[index])
                diffReadList = []
                for index in range(0, len(Gui.netSent) - 1):
                    if index == 0:
                        diffReadList.append(1)
                    elif Gui.netSent[index + 1] - Gui.netSent[index] == 0:
                        diffReadList.append(1)
                    else:
                        diffReadList.append(Gui.netSent[index + 1] - Gui.netSent[index])

                i = len(diffWriteList) - 1
                positionX = MainGraph.mainGraphDefaultWidth
                while i > 0:
                    netIOCanvas.create_line(positionX,
                                            MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                            diffWriteList[i] * 100 / max(diffWriteList + diffReadList),
                                            positionX - MainGraph.mainGraphDefaultWidth / 30,
                                            MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                            diffWriteList[i - 1] * 100 / max(diffWriteList + diffReadList),
                                            fill='blue', width=1)
                    if i == len(diffWriteList) - 1:
                        if diffWriteList[i] == 1:
                            speed = diffWriteList[i] / 1024 / 1024
                            netIOCanvas.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                    MainGraph.mainGraphDefaultHeight - 10, fill="black",
                                                    font="TkDefaultFont 8", text="0.000000")
                        else:
                            speed = diffWriteList[i] / 1024 / 1024
                            if str(speed).find('e') != -1:
                                netIOCanvas.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                        MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                        diffWriteList[i] * 100 / max(diffReadList + diffWriteList) - 10,
                                                        fill="black", font="TkDefaultFont 8", text="0.000000")
                            else:
                                if max(diffReadList + diffWriteList) / 2 < diffWriteList[i]:
                                    netIOCanvas.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                            MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                            diffWriteList[i] * 100 / max(
                                                                diffReadList + diffWriteList) + 10,
                                                            fill="black", font="TkDefaultFont 8", text=str(speed)[:8])
                                else:
                                    netIOCanvas.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                            MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                            diffWriteList[i] * 100 / max(
                                                                diffReadList + diffWriteList) - 10,
                                                            fill="black", font="TkDefaultFont 8", text=str(speed)[:8])
                    positionX -= MainGraph.mainGraphDefaultWidth / 30
                    i -= 1

                i = len(diffReadList) - 1
                positionX = MainGraph.mainGraphDefaultWidth
                while i > 0:
                    netIOCanvas.create_line(positionX,
                                            MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                            diffReadList[i] * 100 / max(diffWriteList + diffReadList),
                                            positionX - MainGraph.mainGraphDefaultWidth / 30,
                                            MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                            diffReadList[i - 1] * 100 / max(diffWriteList + diffReadList),
                                            fill='#549401', width=1)

                    if i == len(diffReadList) - 1:
                        if diffReadList[i] == 1:
                            netIOCanvas.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                    MainGraph.mainGraphDefaultHeight - 10, fill="black",
                                                    font="TkDefaultFont 8", text="0.000000")
                        else:
                            speed = diffReadList[i] / 1024 / 1024
                            if str(speed).find('e') != -1:
                                netIOCanvas.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                        MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                        diffWriteList[i] * 100 / max(diffReadList + diffWriteList) - 10,
                                                        fill="black", font="TkDefaultFont 8", text="0.000000")
                            else:
                                if max(diffReadList + diffWriteList) / 2 < diffReadList[i]:
                                    netIOCanvas.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                            MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                            diffReadList[i] * 100 / max(
                                                                diffReadList + diffWriteList) + 10,
                                                            fill="black", font="TkDefaultFont 8", text=str(speed)[:8])
                                else:
                                    netIOCanvas.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                            MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                            diffReadList[i] * 100 / max(
                                                                diffReadList + diffWriteList) - 10,
                                                            fill="black", font="TkDefaultFont 8", text=str(speed)[:8])

                    positionX -= MainGraph.mainGraphDefaultWidth / 30
                    i -= 1
            netIOCanvas.create_text(30, 8, fill="black", font="TkDefaultFont 8", text="Max speed")
            netIOCanvas.create_text(30, MainGraph.mainGraphDefaultHeight - 8, fill="black", font="TkDefaultFont 8",
                                    text="Low speed")
            netIOCanvas.create_text(40, 18, fill="blue", font="TkDefaultFont 8", text="MBps received")
            netIOCanvas.create_text(29, 28, fill="#549401", font="TkDefaultFont 8", text="MBps sent")
            netIOCanvas.create_text(MainGraph.mainGraphDefaultWidth - 15, 9, fill="#72B2D6",
                                    font="Times 10 italic bold", text="NET")
        except:
            pass

        time.sleep(1)
        netThread(netIOCanvas)
    else:
        print("Stopped the thread NET")
