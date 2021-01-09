import psutil
import time
import Gui
from psutil._common import bytes2human

def miniGraphThread(graph, component, miniGraphUsageList):
    if component == "CPU":
        miniGraphUsageList.append(psutil.cpu_percent())
        Gui.cpuPercentagePerCore.append(psutil.cpu_percent(percpu=True))
        Gui.cpuPercentage = miniGraphUsageList
    elif component == "GPU":
        ...
    elif component == "RAM":
        miniGraphUsageList.append(psutil.virtual_memory().percent)
        Gui.ramPercentage.append(psutil.virtual_memory().percent)
        Gui.ramAvailable.append(bytes2human(psutil.virtual_memory().available))
        Gui.ramUsed.append(bytes2human(psutil.virtual_memory().used))
    elif component == "HDD":
        Gui.hddPartitionNumber = len(psutil.disk_partitions(all=True))
        percent = []
        used = []
        free= []
        availableSpace = 0
        usedSpace = 0
        for p in psutil.disk_partitions(all = True):
            details = psutil.disk_usage(p.device)
            percent.append(details.percent)
            used.append(details.used/1024/1024/1024)
            free.append(details.free/1024/1024/1024)
            usedSpace += details.used/1024/1024/1024
            availableSpace += details.free/1024/1024/1024

        Gui.hddUsed.append(used)
        Gui.hddFree.append(free)

        ioCounter = psutil.disk_io_counters(perdisk=True, nowrap=True)
        readList = []
        writeList = []
        for i in ioCounter:
            readList.append(ioCounter[i][2])
            writeList.append(ioCounter[i][3])

        Gui.diskRead.append(readList)
        Gui.diskWrite.append(writeList)
        a = (readList[0]-Gui.diskRead[len(Gui.diskRead)-2][0])/1000000
        b = (writeList[0]-Gui.diskWrite[len(Gui.diskWrite)-2][0])/1000000
        #print("read: "+str(a)+" write: "+str(b))
        miniGraphUsageList.append(usedSpace*100/(usedSpace+availableSpace))



    elif component == "NET":
        ...

    if component == "HDD":
        if len(Gui.diskWrite) > 1:
            i = len(Gui.diskWrite) - 1
            positionX = Gui.miniGraphDefaultWidth

            diffList = []
            for index in range(0,len(Gui.diskWrite)-1):
                diffList.append(Gui.diskWrite[index+1][0]-Gui.diskWrite[index][0])

            while i > 1:
                if len(Gui.diskWrite) > 30 and i < len(Gui.diskWrite) - 30:
                    break
                graph.create_line(positionX,
                                  Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 * ((Gui.diskWrite[i][0]-Gui.diskWrite[i-1][0])*100/max(diffList)),
                                  positionX - Gui.miniGraphDefaultWidth / 30,
                                  Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 * ((Gui.diskWrite[i-1][0]-Gui.diskWrite[i-2][0])*100/max(diffList)),
                                  fill='#549401', width=1)
                positionX -= Gui.miniGraphDefaultWidth / 30
                i -= 1

            i = len(Gui.diskRead) - 1
            positionX = Gui.miniGraphDefaultWidth

            diffList = []
            for index in range(0, len(Gui.diskRead) - 1):
                diffList.append(Gui.diskRead[index + 1][0] - Gui.diskRead[index][0])
            while i > 1:
                if len(Gui.diskRead) > 30 and i < len(Gui.diskRead) - 30:
                    break
                graph.create_line(positionX,
                                  Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 * ((Gui.diskRead[i][0]-Gui.diskRead[i-1][0])*100/max(diffList)),
                                  positionX - Gui.miniGraphDefaultWidth / 30,
                                  Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 * ((Gui.diskRead[i-1][0]-Gui.diskRead[i-2][0])*100/max(diffList)),
                                  fill='blue', width=1)
                positionX -= Gui.miniGraphDefaultWidth / 30
                i -= 1
    elif component == "NET":
        ...
    else:
        if len(miniGraphUsageList) > 1:
            i = len(miniGraphUsageList) - 1
            positionX = Gui.miniGraphDefaultWidth
            while i > 1:
                if len(miniGraphUsageList) > 30 and i < len(miniGraphUsageList) - 30:
                    break
                graph.create_line(positionX,
                                  Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 * miniGraphUsageList[i],
                                  positionX - Gui.miniGraphDefaultWidth / 30,
                                  Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 * miniGraphUsageList[i - 1],
                                  fill='#549401', width=2)
                positionX -= Gui.miniGraphDefaultWidth / 30
                i -= 1

    time.sleep(1)
    graph.delete("all")
    if component in {"CPU","GPU","RAM"}:
        Gui.drawMiniGraphsDetails(graph, component)
    miniGraphThread(graph, component, miniGraphUsageList)
