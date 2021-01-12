import time
import MainGraph
import Gui
import psutil


def hddThread(barCanvas,diskIOPerfect):
    # if the current component is HDD
    if MainGraph.hdd == True:
        try:
            #delete everything from partition canvas
            barCanvas.delete("all")
            #delete everything from usage canvas
            diskIOPerfect.delete("all")

            #get the current partition number
            partitions = psutil.disk_partitions(all=True)
            #avoid timing issues when a drive is removed from system
            if (Gui.hddPartitionNumber == len(partitions)):

                # add label to indicate speed on the top of the canvas
                diskIOPerfect.create_text(30, 8, fill="black", font="TkDefaultFont 8", text="Max speed")
                #add label to indicate speed on the bottom of the canvas
                diskIOPerfect.create_text(30, MainGraph.mainGraphDefaultHeight - 8, fill="black", font="TkDefaultFont 8",
                                          text="Low speed")
                #add text and color to indicate the read line color
                diskIOPerfect.create_text(30, 18, fill="blue", font="TkDefaultFont 8", text="MBps read")
                #add text and color to indicate the write line color
                diskIOPerfect.create_text(36, 28, fill="#549401", font="TkDefaultFont 8", text="MBps written")
                #add text to display the component
                diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth - 14, 8, fill="#72B2D6",
                                          font="Times 10 italic bold", text="HDD")

                #for each partition
                for i in range(0, Gui.hddPartitionNumber):
                    #create the rectable for total memory available in the system for current partition
                    barCanvas.create_rectangle(70,
                                                    MainGraph.mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1) - 20,
                                                    MainGraph.mainGraphDefaultWidth - 20,
                                                    MainGraph.mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1) + 20,
                                                    outline="#549401")
                    #create the rectable for total memory used in the system for current partition
                    barCanvas.create_rectangle(71,
                                                    MainGraph.mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1) - 19, (
                                                                Gui.hddUsed[len(Gui.hddUsed) - 1][i] * 100 / (
                                                                    Gui.hddFree[len(Gui.hddFree) - 1][i] +
                                                                    Gui.hddUsed[len(Gui.hddUsed) - 1][i])) * (
                                                                MainGraph.mainGraphDefaultWidth - 90) / 100 + 70,
                                                    MainGraph.mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1) + 19,
                                                    fill="#EDF9EB", outline="#EDF9EB")
                    #display the percentage used for the current partition
                    barCanvas.create_text(120, MainGraph.mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1),
                                               fill="#549401", font="TkDefaultFont 10", text=str(
                            Gui.hddUsed[len(Gui.hddUsed) - 1][i] * 100 / (
                                        Gui.hddFree[len(Gui.hddFree) - 1][i] + Gui.hddUsed[len(Gui.hddUsed) - 1][i]))[
                                                                                             :5] + "% used")
                    #display the name of the current patition
                    barCanvas.create_text(40, MainGraph.mainGraphDefaultHeight / (Gui.hddPartitionNumber + 1) * (i + 1),
                                               fill="black", font="TkDefaultFont 12",
                                               text=str(partitions[i].device[:1]) + ":/")

                #if there are at least two speeds in the lists write and read
                if len(Gui.diskWrite) > 1 and len(Gui.diskRead) > 1:
                    #declare a list to calculate the speed of write each second
                    diffWriteList = []
                    #itearate the bytes written by the system
                    for index in range(0, len(Gui.diskWrite) - 1):
                        #if there is no byte written between the previous second and the current one
                        if Gui.diskWrite[index + 1][0] - Gui.diskWrite[index][0] == 0:
                            #assign 1
                            diffWriteList.append(1)
                        else:
                            #assign the bytes written
                            diffWriteList.append(Gui.diskWrite[index + 1][0] - Gui.diskWrite[index][0])

                    #declare a list to calculate the speed of read each second
                    diffReadList = []
                    #itearate the bytes read by the system
                    for index in range(0, len(Gui.diskRead) - 1):
                        #if there is no byte read between the previous second and the current one
                        if Gui.diskRead[index + 1][0] - Gui.diskRead[index][0] == 0:
                            #assign 1
                            diffReadList.append(1)
                        else:
                            #assign the bytes read
                            diffReadList.append(Gui.diskRead[index + 1][0] - Gui.diskRead[index][0])

                    #set i on the end of the written bytes by second list
                    i = len(diffWriteList) - 1
                    #set position x to the right side of the canvas
                    positionX = MainGraph.mainGraphDefaultWidth
                    #while we did not iterate over all the elements in the written list
                    while i > 0:
                        #create line from the previous speed to the current speed
                        #the height of the line is calculated by dividing the maximum speed reached yet by the current speed
                        diskIOPerfect.create_line(positionX,
                                          MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * (
                                                      diffWriteList[i] * 100 / max(diffReadList + diffWriteList)),
                                          positionX - MainGraph.mainGraphDefaultWidth / 30,
                                          MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * (
                                                      diffWriteList[i - 1] * 100 / max(diffReadList + diffWriteList)),
                                          fill='#549401', width=1)
                        #if the current speed iterated is the latest one captured
                        if i==len(diffWriteList)-1:
                            #if there is no difference from the previous speed captured
                            if diffWriteList[i] == 1:
                                #place the speed value to the left of it's position
                                diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                          MainGraph.mainGraphDefaultHeight - 10, fill="black",
                                                          font="TkDefaultFont 8", text="0.000000")
                            else:
                                #calculate the MBps value
                                speed = diffWriteList[i] / 1024 / 1024
                                #handle the 'e' expression of the speed (too low to be counted anyway)
                                if str(speed).find('e') != -1:
                                    #place the speed value to the left of it's position
                                    diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                            MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                            diffWriteList[i] * 100 / max(diffReadList + diffWriteList) - 10,
                                                            fill="black", font="TkDefaultFont 8", text="0.000000")
                                else:
                                    #if the speed is above 50% of the max speed
                                    if max(diffReadList + diffWriteList) / 2 < diffWriteList[i]:
                                        #place the speed value 26 pixels below it's pont
                                        diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth - 26,MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *diffWriteList[i] * 100 / max(diffReadList + diffWriteList) + 10, fill="black",font="TkDefaultFont 8", text=str(speed)[:8])
                                    else:
                                        #place the speed value 26 pixels above it's pont
                                        diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth - 26,MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *diffWriteList[i] * 100 / max(diffReadList + diffWriteList) - 10, fill="black",font="TkDefaultFont 8", text=str(speed)[:8])
                        #decrease the x position
                        positionX -= MainGraph.mainGraphDefaultWidth / 30
                        #set i on the previous speed captured
                        i -= 1


                    #set i on the end of the read bytes by second list
                    i = len(diffReadList) - 1
                    #set position x to the right side of the canvas
                    positionX = MainGraph.mainGraphDefaultWidth

                    #while we did not iterate over all the elements in the read list
                    while i > 0:
                        #create line from the previous speed to the current speed
                        #the height of the line is calculated by dividing the maximum speed reached yet by the current speed
                        diskIOPerfect.create_line(positionX,
                                          MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * diffReadList[
                                              i] * 100 / max(diffReadList + diffWriteList),
                                          positionX - MainGraph.mainGraphDefaultWidth / 30,
                                          MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * diffReadList[
                                              i - 1] * 100 / max(diffReadList + diffWriteList),
                                          fill='blue', width=1)

                        #if the current speed iterated is the latest one captured
                        if i==len(diffReadList)-1:
                            #if there is no difference from the previous speed captured
                            if diffReadList[i] == 1:
                                #place the speed value to the left of it's position
                                diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth-26, MainGraph.mainGraphDefaultHeight-10, fill="black", font="TkDefaultFont 8", text="0.000000")
                            else:
                                #calculate the MBps value
                                speed = diffReadList[i]/1024/1024
                                #handle the 'e' expression of the speed (too low to be counted anyway)
                                if str(speed).find('e') != -1:
                                    #place the speed value to the left of it's position
                                    diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth - 26,
                                                              MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 *
                                                              diffWriteList[i] * 100 / max(
                                                                  diffReadList + diffWriteList) - 10,
                                                              fill="black", font="TkDefaultFont 8", text="0.000000")
                                else:
                                    #if the speed is above 50% of the max speed
                                    if max(diffReadList + diffWriteList)/2 < diffReadList[i]:
                                        #place the speed value 26 pixels below it's pont
                                        diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth-26, MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * diffReadList[i] * 100 / max(diffReadList + diffWriteList)+10, fill="black", font="TkDefaultFont 8", text=str(speed)[:8])
                                    else:
                                        #place the speed value 26 pixels above it's pont
                                        diskIOPerfect.create_text(MainGraph.mainGraphDefaultWidth-26, MainGraph.mainGraphDefaultHeight - MainGraph.mainGraphDefaultHeight / 100 * diffReadList[i] * 100 / max(diffReadList + diffWriteList)-10, fill="black", font="TkDefaultFont 8", text=str(speed)[:8])

                        #decrease the x position
                        positionX -= MainGraph.mainGraphDefaultWidth / 30
                        #set i on the previous speed captured
                        i -= 1
            #timing issue when extracting a drive from the system
            else:
                try:
                    #delete everything from the bar canvas
                    barCanvas.delete("all")
                    #delete everything from the graph canvas
                    diskIOPerfect.delete("all")
                    #show loading spreed
                    barCanvas.create_text(MainGraph.mainGraphDefaultWidth / 2, (MainGraph.mainGraphDefaultHeight) / 2,
                                          fill="#549401", font="TkDefaultFont 16", text="Loading...")
                    #hide graph border while waiting
                    diskIOPerfect.config(highlightthickness=0, highlightbackground="#5CA6D0")
                    #sleep for 1 second
                    time.sleep(1)
                    #draw the graph border again
                    diskIOPerfect.config(highlightthickness=1, highlightbackground="#5CA6D0")
                    #recursive call of the thread
                    hddThread(barCanvas, diskIOPerfect)
                except:
                    pass
        #handle of drawing error because of timing issues
        except:
            try:
                #delete everything from the bar canvas
                barCanvas.delete("all")
                #delete everything from the graph canvas
                diskIOPerfect.delete("all")
                #show loading spreed
                barCanvas.create_text(MainGraph.mainGraphDefaultWidth / 2, (MainGraph.mainGraphDefaultHeight) / 2,
                                      fill="#549401", font="TkDefaultFont 16", text="Loading...")
                #hide graph border while waiting
                diskIOPerfect.config(highlightthickness=0, highlightbackground="#5CA6D0")
                #sleep for 1 second
                time.sleep(1)
                #draw the graph border again
                diskIOPerfect.config(highlightthickness=1, highlightbackground="#5CA6D0")
                # recursive call of the thread
                hddThread(barCanvas, diskIOPerfect)
            except:
                pass
        # sleep for 1 second
        time.sleep(1)
        # recursive call of the thread
        hddThread(barCanvas,diskIOPerfect)
    else:
        #stop the thread because the current component has changed
        print("Stopped the thread HDD")