import time
import MainGraph
import Gui


def netThread(netIOCanvas):
    #if the current component is NET
    if MainGraph.net == True:
        try:
            #delete everything from net canvas
            netIOCanvas.delete("all")

            #if there are 2 or more speeds captured for sending and receiving data
            if len(Gui.netReceived) > 1 and len(Gui.netSent)>1:

                # declare a list to calculate the speed of receive each second
                diffWriteList = []
                #itearate the bytes received by the system
                for index in range(0, len(Gui.netReceived) - 1):
                    if index == 0:
                        diffWriteList.append(1)
                    # if there is no byte sent between the previous second and the current one
                    elif Gui.netReceived[index+1] - Gui.netReceived[index] == 0:
                        #assign 1
                        diffWriteList.append(1)
                    else:
                        # assign the bytes received
                        diffWriteList.append(Gui.netReceived[index + 1] - Gui.netReceived[index])
                # declare a list to calculate the speed of sent each second
                diffReadList = []
                # itearate the bytes sent by the system
                for index in range(0, len(Gui.netSent) - 1):
                    if index ==0:
                        diffReadList.append(1)
                    # if there is no byte sent between the previous second and the current one
                    elif Gui.netSent[index + 1] - Gui.netSent[index] == 0:
                        # assign 1
                        diffReadList.append(1)
                    else:
                        # assign the bytes sent
                        diffReadList.append(Gui.netSent[index + 1] - Gui.netSent[index])

                #set i on the right
                i = len(diffWriteList)-1
                #set position x on the right side of thecanvas
                positionX = MainGraph.mainGraphDefaultWidth
                #while there are speeds in the list
                while i > 0:
                    #create line from the current speed to the previous one
                    # the height of the line is calculated by dividing the maximum speed reached yet by the current speed
                    netIOCanvas.create_line(positionX,
                                      MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * diffWriteList[i] * 100 / max(diffWriteList+diffReadList),
                                      positionX - MainGraph.mainGraphDefaultWidth / 30,
                                      MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * diffWriteList[i-1] * 100 / max(diffWriteList+diffReadList),
                                      fill='blue', width=1)
                    #if the current speed is the last one captured
                    if i == len(diffWriteList) - 1:
                        #if the current speed has not changed from the last second
                        if diffWriteList[i] == 1:
                            #calculate the speed
                            speed = diffWriteList[i] / 1024 / 1024
                            #put the speed on the screen
                            netIOCanvas.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                      MainGraph.mainGraphDefaultHeight - 10, fill="black",
                                                      font="TkDefaultFont 8", text="0.000000")
                        else:
                            #calculate the speed
                            speed = diffWriteList[i] / 1024 / 1024
                            #if 'e' appears in the speed value
                            if str(speed).find('e') != -1:
                                #put the speed on the canvas (to low to count)
                                netIOCanvas.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                        MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                        diffWriteList[i] * 100 / max(diffReadList + diffWriteList) - 10,
                                                        fill="black", font="TkDefaultFont 8", text="0.000000")
                            else:
                                #if the speed is greater then the max speed reached
                                if max(diffReadList + diffWriteList) / 2 < diffWriteList[i]:
                                    #put the speed on the canvas 26 below
                                    netIOCanvas.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                              MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                              diffWriteList[i] * 100 / max(diffReadList + diffWriteList) + 10,
                                                              fill="black", font="TkDefaultFont 8", text=str(speed)[:8])
                                else:
                                    #put the speed on the canvas 26 below
                                    netIOCanvas.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                              MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                              diffWriteList[i] * 100 / max(diffReadList + diffWriteList) - 10,
                                                              fill="black", font="TkDefaultFont 8", text=str(speed)[:8])
                    #decrease the x position
                    positionX -= MainGraph.mainGraphDefaultWidth / 30
                    #set i on the previous speed
                    i -= 1

                #same as above but for read speed
                i = len(diffReadList) - 1
                positionX = MainGraph.mainGraphDefaultWidth
                while i > 0:
                    netIOCanvas.create_line(positionX,
                                     MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * diffReadList[i] * 100 / max(diffWriteList+diffReadList),
                                     positionX - MainGraph.mainGraphDefaultWidth / 30,
                                     MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * diffReadList[i - 1] * 100 / max(diffWriteList+diffReadList),
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
                                                              diffReadList[i] * 100 / max(diffReadList + diffWriteList) + 10,
                                                              fill="black", font="TkDefaultFont 8", text=str(speed)[:8])
                                else:
                                    netIOCanvas.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                              MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                              diffReadList[i] * 100 / max(diffReadList + diffWriteList) - 10,
                                                              fill="black", font="TkDefaultFont 8", text=str(speed)[:8])

                    positionX -= MainGraph.mainGraphDefaultWidth / 30
                    i -= 1
            #set indicators for max speed, lowest speed, color of the lines based on the received/sent data
            netIOCanvas.create_text(30, 8, fill="black", font="TkDefaultFont 8", text="Max speed")
            netIOCanvas.create_text(30, MainGraph.mainGraphDefaultHeight - 8, fill="black", font="TkDefaultFont 8",
                                      text="Low speed")
            netIOCanvas.create_text(40, 18, fill="blue", font="TkDefaultFont 8", text="MBps received")
            netIOCanvas.create_text(29, 28, fill="#549401", font="TkDefaultFont 8", text="MBps sent")
            netIOCanvas.create_text(MainGraph.mainGraphDefaultWidth-15,9, fill="#72B2D6", font="Times 10 italic bold",text="NET")
        except:
            pass
        #sleep one second
        time.sleep(1)
        #recursive call for thread
        netThread(netIOCanvas)
    else:
        #component has changed, thread has to stop
        print("Stopped the thread NET")