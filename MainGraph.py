from tkinter import *

mainGraphDefaultWidth = 600
mainGraphDefaultHeight = 500

def onOpen(graph):
    mainGraph = Canvas(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white")
    mainGraph.grid(row=0,column=0)
    drawGraphDetails(mainGraph,"CPU")


def drawGraphDetails(graph,component):
    graph.create_text(mainGraphDefaultWidth-35, 10, fill="darkblue", font="Times 10 italic bold", text=f"{component} Usage")
    positionY = 0
    while positionY < mainGraphDefaultHeight:
        if positionY!=0 and positionY!= mainGraphDefaultHeight:
            graph.create_line(30,positionY,mainGraphDefaultWidth,positionY,fill='gray')
            graph.create_text(20, positionY, fill="darkblue", font="Times 10 italic bold", text=str(int(100-positionY / mainGraphDefaultHeight * 100)))
        positionY += mainGraphDefaultHeight/10

def drawCPUGraph(graph,text):
    mainGraph = Canvas(graph, width=mainGraphDefaultWidth, height=mainGraphDefaultHeight, bg="white")
    mainGraph.grid(row=0, column=0)
    drawGraphDetails(mainGraph, text)

"""
def mainGraphThread(graph,component):
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
 Gui.drawGraphDetails(graph,component)
 mainGraphThread(graph,component)"""