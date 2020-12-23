from tkinter import *
import threading
import time
import psutil
import sys

cpuUsage = []

def drawGraphTitleMain(graph):
    graph.create_text(graph.winfo_width()-35, 10, fill="darkblue", font="Times 10 italic bold", text="CPU Usage")
    positionY = 0
    while positionY < 500:
        graph.create_line(0,positionY,600,positionY,fill='gray')
        graph.create_text(15, positionY-10, fill="darkblue", font="Times 10 italic bold", text=str(100-positionY/5))
        positionY += 50

def cpuThread(graph):
    cpuUsage.append(psutil.cpu_percent())

    if len(cpuUsage)>1:
        i = len(cpuUsage)-1
        positionX=600
        while(i>1):
            if len(cpuUsage)>30 and i < len(cpuUsage)-30:
                break
            graph.create_line(positionX,500 - 5 * cpuUsage[i],positionX-20,500 - 5 * cpuUsage[i-1],fill='#73e02f',width=3)
            positionX -= 20
            i-= 1
        graph.create_text(graph.winfo_width()-35, 20, fill="darkblue", font="Times 10 italic bold", text=str(cpuUsage[len(cpuUsage)-1]))
    time.sleep(1)
    graph.delete("all")
    drawGraphTitleMain(graph)
    cpuThread(graph)

class Gui(Canvas):

    def __init__(self):
        self.root = Tk()
        self.root.title("GUI Resource Monitor")
        self.root.geometry("740x560")

    #menu
        self.menu = LabelFrame(self.root,padx=0,pady=0)
        self.menu.grid(row = 0, column = 0)
    #menu items
        self.open = Button(self.menu,text="Open",padx=0,pady=3)
        self.open.grid(row = 0, column = 0)
        self.save = Button(self.menu,text="Save",padx=0,pady=3)
        self.save.grid(row = 0, column = 1)
        self.exit = Button(self.menu,text="Exit",padx=0,pady=3, command = self.exit)
        self.exit.grid(row = 0, column = 2)

    #app
        self.app = LabelFrame(self.root,padx=0,pady=0)
        self.app.grid(row=1,column=0,padx=0,pady=0)

    #app component
        self.miniGraphs = LabelFrame(self.app,padx=0,pady=0)
        self.miniGraphs.grid(row = 0, column = 0, padx=0,pady=0)
    #minigraphs items
        self.cpu = Canvas(self.miniGraphs,width = 120,height = 100, bg = "white")
        self.cpu.grid(row = 0, column = 0)
        self.gpu = Canvas(self.miniGraphs,width = 120,height = 100, bg = "white")
        self.gpu.grid(row = 1, column = 0)
        self.ram = Canvas(self.miniGraphs,width = 120,height = 100, bg = "white")
        self.ram.grid(row = 2, column = 0)
        self.hdd = Canvas(self.miniGraphs,width = 120,height = 100, bg = "white")
        self.hdd.grid(row = 3, column = 0)
        self.net = Canvas(self.miniGraphs,width = 120,height = 100, bg = "white")
        self.net.grid(row = 4, column = 0)
    #app component
        self.graph = LabelFrame(self.app,padx=0,pady=0)
        self.graph.grid(row = 0, column = 1, padx = 0, pady = 0)
        self.mainGraph = Canvas(self.graph,width = 600,height = 500, bg = "white")
        self.mainGraph.grid(row = 0,column = 0)


        self.root.update()
        self.mainGraph.update()
        self.cpu.update()
        self.gpu.update()
        self.ram.update()
        self.hdd.update()
        self.net.update()

    def run(self):
        drawGraphTitleMain(self.mainGraph)
        self.cpuThread = threading.Thread(target=cpuThread,args=(self.mainGraph,), daemon=True)
        self.cpuThread.start()

        self.root.mainloop()

    def exit(self):
        sys.exit()