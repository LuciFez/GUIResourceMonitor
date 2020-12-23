import psutil
import time
import Gui

mainGraphUsageList = []

def mainGraphThread(graph):
    mainGraphUsageList.append(psutil.cpu_percent())
    print(mainGraphUsageList[len(mainGraphUsageList) - 1])
    if len(mainGraphUsageList)>1:
        i = len(mainGraphUsageList)-1
        positionX=Gui.mainGraphDefaultWidth
        while(i>1):
            if len(mainGraphUsageList)>30 and i < len(mainGraphUsageList)-30:
                break
            graph.create_line(positionX, Gui.mainGraphDefaultHeight - Gui.mainGraphDefaultHeight/100 * mainGraphUsageList[i],
                              positionX-Gui.mainGraphDefaultWidth/30,Gui.mainGraphDefaultHeight - Gui.mainGraphDefaultHeight/100 * mainGraphUsageList[i-1],fill='#73e02f',width=3)
            positionX -= Gui.mainGraphDefaultWidth/30
            i-= 1
        graph.create_text(Gui.mainGraphDefaultWidth-35, 20, fill="darkblue", font="Times 10 italic bold", text=str(mainGraphUsageList[len(mainGraphUsageList)-1]))
    time.sleep(1)
    graph.delete("all")
    Gui.drawGraphDetails(graph)
    mainGraphThread(graph)