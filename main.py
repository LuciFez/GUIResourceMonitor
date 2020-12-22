from tkinter import *


def initializer():
    root = Tk()

#menu
    menu = LabelFrame(root,padx=0,pady=0)
    menu.grid(row = 0, column = 0,padx=0,pady=0)
    open = Button(menu,text="Open")
    open.grid(row = 0, column = 0)
    save = Button(menu,text="Save")
    save.grid(row = 0, column = 1)
    exit = Button(menu,text="Exit")
    exit.grid(row = 0, column = 2)

#app
    app = LabelFrame(root,padx=0,pady=0)
    app.grid(row=1,column=0,padx=0,pady=0)

    miniGraphs = LabelFrame(app,padx=0,pady=0)
    miniGraphs.grid(row = 0, column = 0, padx=0,pady=0)

    cpu = Button(miniGraphs,text="CPU")
    cpu.grid(row = 0, column = 0)
    gpu = Button(miniGraphs,text="GPU")
    gpu.grid(row = 1, column = 0)
    ram = Button(miniGraphs,text="RAM")
    ram.grid(row = 2, column = 0)
    hdd = Button(miniGraphs,text="HDD")
    hdd.grid(row = 3, column = 0)
    net = Button(miniGraphs,text="Net")
    net.grid(row = 4, column = 0)

    graph = LabelFrame(app,padx=0,pady=0)
    graph.grid(row = 0, column = 1, padx = 0, pady = 0)
    a = Button(graph,text = "Exemplu")
    a.grid(row = 0,column = 0)

    root.mainloop()

if __name__ == '__main__':
    initializer()