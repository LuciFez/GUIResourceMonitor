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

        Gui.hddPercentage.append(percent)
        Gui.hddUsed.append(used)
        Gui.hddFree.append(free)

        io_counters = psutil.Process().io_counters()
        disk_io_counter = psutil.disk_io_counters()

        miniGraphUsageList.append((io_counters[2] + io_counters[3]) / (disk_io_counter[2]+disk_io_counter[3])*100)



    elif component == "NET":
        ...
    if len(miniGraphUsageList) > 1:
        i = len(miniGraphUsageList) - 1
        positionX = Gui.miniGraphDefaultWidth
        while (i > 1):
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
    Gui.drawMiniGraphsDetails(graph, component)
    miniGraphThread(graph, component, miniGraphUsageList)
