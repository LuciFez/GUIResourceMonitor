import psutil
import time
import Gui


def miniGraphThread(graph, component, miniGraphUsageList):
    if component == "CPU":
        miniGraphUsageList.append(psutil.cpu_percent())
        Gui.cpuPercentage = miniGraphUsageList
    elif component == "GPU":
        ...
    elif component == "RAM":
        miniGraphUsageList.append(psutil.virtual_memory().percent)
        Gui.ramPercentage = miniGraphUsageList
    elif component == "HDD":
        # used disk percent
        # print(psutil.disk_usage('/').percent)
        # print(psutil.disk_io_counters().read_bytes," ----- ",psutil.disk_io_counters().write_bytes)
        ...
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
                              fill='#73e02f', width=2)
            positionX -= Gui.miniGraphDefaultWidth / 30
            i -= 1
    time.sleep(1)
    graph.delete("all")
    Gui.drawMiniGraphsDetails(graph, component)
    miniGraphThread(graph, component, miniGraphUsageList)
