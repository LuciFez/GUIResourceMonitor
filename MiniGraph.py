import psutil
import time
import Gui
import GPUtil
from psutil._common import bytes2human


def miniGraphThread(graph, component, miniGraphUsageList):
    """
    Method used as a thread to collect each second information about the components of the machine.

    After the data is stored, it will draw for the corresponding mini graph for the current component
    the details and the graph lines with the percentage used on the component

    It will wait one second and it will call recursively for the same component to collect data again

    *** No thread mechanism for stopping created. This thread should run until the application is closed.
    """
    if component == "CPU":
        miniGraphUsageList.append(psutil.cpu_percent())
        Gui.cpuPercentagePerCore.append(psutil.cpu_percent(percpu=True))
        Gui.cpuPercentage = miniGraphUsageList
    elif component == "GPU":
        GPUs = GPUtil.getGPUs()
        if len(GPUs) > 0:
            Gui.gpuManufacturer = True
            Gui.gpuPercentage.append(GPUs[0].memoryUtil * 100)

    elif component == "RAM":
        miniGraphUsageList.append(psutil.virtual_memory().percent)
        Gui.ramPercentage.append(psutil.virtual_memory().percent)
        Gui.ramAvailable.append(bytes2human(psutil.virtual_memory().available))
        Gui.ramUsed.append(bytes2human(psutil.virtual_memory().used))

    elif component == "HDD":
        Gui.hddPartitionNumber = len(psutil.disk_partitions(all=True))
        percent = []
        used = []
        free = []
        availableSpace = 0
        usedSpace = 0
        for p in psutil.disk_partitions(all=True):
            details = psutil.disk_usage(p.device)
            percent.append(details.percent)
            used.append(details.used / 1024 / 1024 / 1024)
            free.append(details.free / 1024 / 1024 / 1024)
            usedSpace += details.used / 1024 / 1024 / 1024
            availableSpace += details.free / 1024 / 1024 / 1024
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
        miniGraphUsageList.append(usedSpace * 100 / (usedSpace + availableSpace))

    elif component == "NET":
        netIO = psutil.net_io_counters(pernic=False, nowrap=True)
        Gui.netSent.append(netIO[0])
        Gui.netReceived.append(netIO[1])

    if component == "HDD":
        if len(Gui.diskWrite) > 1 and len(Gui.diskRead) > 1:
            diffWriteList = []
            for index in range(0, len(Gui.diskWrite) - 1):
                if index == 0:
                    diffWriteList.append(1)
                elif Gui.diskWrite[index + 1][0] - Gui.diskWrite[index][0] == 0:
                    diffWriteList.append(1)
                else:
                    diffWriteList.append(Gui.diskWrite[index + 1][0] - Gui.diskWrite[index][0])
            diffReadList = []

            for index in range(0, len(Gui.diskRead) - 1):
                if index == 0:
                    diffReadList.append(1)
                elif Gui.diskRead[index + 1][0] - Gui.diskRead[index][0] == 0:
                    diffReadList.append(1)
                else:
                    diffReadList.append(Gui.diskRead[index + 1][0] - Gui.diskRead[index][0])

            i = len(diffWriteList) - 1
            positionX = Gui.miniGraphDefaultWidth
            while i > 0:
                graph.create_line(positionX,
                                  Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 * (
                                          diffWriteList[i] * 100 / max(diffReadList + diffWriteList)),
                                  positionX - Gui.miniGraphDefaultWidth / 30,
                                  Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 * (
                                          diffWriteList[i - 1] * 100 / max(diffReadList + diffWriteList)),
                                  fill='#549401', width=1)
                positionX -= Gui.miniGraphDefaultWidth / 30
                i -= 1

            i = len(diffReadList) - 1
            positionX = Gui.miniGraphDefaultWidth

            while i > 0:
                graph.create_line(positionX,
                                  Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 * diffReadList[
                                      i] * 100 / max(diffReadList + diffWriteList),
                                  positionX - Gui.miniGraphDefaultWidth / 30,
                                  Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 * diffReadList[
                                      i - 1] * 100 / max(diffReadList + diffWriteList),
                                  fill='blue', width=1)
                positionX -= Gui.miniGraphDefaultWidth / 30
                i -= 1
        graph.create_text(Gui.miniGraphDefaultWidth - 10, 6, fill="#72B2D6", font="Times 6 italic bold", text="HDD")

    elif component == "NET":
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
            positionX = Gui.miniGraphDefaultWidth
            while i > 0:
                graph.create_line(positionX,
                                  Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 * diffWriteList[
                                      i] * 100 / max(diffWriteList + diffReadList),
                                  positionX - Gui.miniGraphDefaultWidth / 30,
                                  Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 * diffWriteList[
                                      i - 1] * 100 / max(diffWriteList + diffReadList),
                                  fill='blue', width=1)
                positionX -= Gui.miniGraphDefaultWidth / 30
                i -= 1
            i = len(diffReadList) - 1
            positionX = Gui.miniGraphDefaultWidth
            while i > 0:
                graph.create_line(positionX,
                                  Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 * diffReadList[
                                      i] * 100 / max(diffWriteList + diffReadList),
                                  positionX - Gui.miniGraphDefaultWidth / 30,
                                  Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 * diffReadList[
                                      i - 1] * 100 / max(diffWriteList + diffReadList),
                                  fill='#549401', width=1)
                positionX -= Gui.miniGraphDefaultWidth / 30
                i -= 1
        graph.create_text(Gui.miniGraphDefaultWidth - 10, 6, fill="#72B2D6", font="Times 6 italic bold", text="NET")

    elif component == "GPU":
        if Gui.gpuManufacturer == True:
            if len(Gui.gpuPercentage) > 1:
                i = len(Gui.gpuPercentage) - 1
                positionX = Gui.miniGraphDefaultWidth
                while i > 1:
                    if len(miniGraphUsageList) > 30 and i < len(miniGraphUsageList) - 30:
                        break
                    graph.create_line(positionX,
                                      Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 *
                                      Gui.gpuPercentage[i],
                                      positionX - Gui.miniGraphDefaultWidth / 30,
                                      Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 *
                                      Gui.gpuPercentage[i - 1],
                                      fill='red', width=2)
                    positionX -= Gui.miniGraphDefaultWidth / 30
                    i -= 1
        else:
            graph.delete("all")
            graph.create_text(Gui.miniGraphDefaultWidth / 2, Gui.miniGraphDefaultHeight / 2, fill="#72B2D6",
                              font="Times 8 italic bold", text="Buy Nvidia")
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
                                  Gui.miniGraphDefaultHeight - Gui.miniGraphDefaultHeight / 100 * miniGraphUsageList[
                                      i - 1],
                                  fill='red', width=2)
                positionX -= Gui.miniGraphDefaultWidth / 30
                i -= 1

    time.sleep(1)
    graph.delete("all")
    if component in {"CPU", "RAM"}:
        Gui.drawMiniGraphsDetails(graph, component)
    elif component == "GPU" and Gui.gpuManufacturer == True:
        Gui.drawMiniGraphsDetails(graph, component)
    miniGraphThread(graph, component, miniGraphUsageList)