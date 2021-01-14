import os
import datetime
from tkinter import *


def drawGraph(component, parent):
    """
    Method that draws the new windows which will contain the graph.

    After creating the canvas and frame calls the correct drawing
    method based on the component we are displaying
    """
    drawing = Tk()
    drawing.title("GUI Resource Monitor")
    drawing.geometry("1280x720")
    drawing.configure(bg="white")
    drawing.resizable(False, False)

    canvas = Canvas(drawing, width=1240, height=620, bg="white", highlightthickness=1, highlightbackground="#5CA6D0")
    canvas.grid(row=0, column=0, padx=20, pady=20)
    done = Button(drawing, width=20, font="TkDefaultFont 16", command=lambda: leave(parent, drawing), text='Done')
    done.grid(row=1, column=0)

    if component[:3] == "cpu":
        drawCPU(component, canvas)
    elif component[:3] == "gpu":
        drawGPU(component, canvas)
    elif component[:3] == "ram":
        drawRAM(component, canvas)
    elif component[:3] == "hdd":
        drawHDD(component, canvas)
    elif component[:3] == "net":
        drawNET(component, canvas)
    drawing.mainloop()


def drawCPU(folder, canvas):
    """
    Reads the stored percentages from the saved file
    Calls the drawing percentage function
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    f = open(dir_path + "\\output\\" + folder + "\\" + folder + ".txt", "r")
    input = f.read()
    input = input[1:len(input) - 1]
    li = list(input.split(", "))
    for i in li:
        li[li.index(i)] = float(i)
    drawPercentage(li, canvas, "CPU", folder)


def drawGPU(folder, canvas):
    """
    Reads the stored percentages from the saved file
    Calls the drawing percentage function
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    f = open(dir_path + "\\output\\" + folder + "\\" + folder + ".txt", "r")
    input = f.read()
    input = input[1:len(input) - 1]
    li = list(input.split(", "))
    for i in li:
        li[li.index(i)] = float(i)

    drawPercentage(li, canvas, "GPU", folder)


def drawRAM(folder, canvas):
    """
    Reads the stored percentages from the saved file
    Calls the drawing percentage function
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    f = open(dir_path + "\\output\\" + folder + "\\" + folder + ".txt", "r")
    input = f.read()
    input = input[1:len(input) - 1]
    li = list(input.split(", "))
    for i in li:
        li[li.index(i)] = float(i)

    drawPercentage(li, canvas, "RAM", folder)


def drawHDD(folder, canvas):
    """
    Reads the stored percentages from the saved file
    Calls the draw smart graph function
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    f = open(dir_path + "\\output\\" + folder + "\\" + folder + ".txt", "r")
    input = f.read()
    input = input[1:len(input) - 1]
    readInput = input[1:input.find("<sep>") - 2]
    writeOutput = input[input.find("<sep>") + 7:len(input) - 1]
    readInputList = list(readInput.split("], ["))
    writeInputList = list(writeOutput.split("], ["))

    read = []
    write = []
    for i in readInputList:
        read.append(i[:i.find(',')])
    for i in writeInputList:
        write.append(i[:i.find(',')])
    for i in read:
        read[read.index(i)] = float(i)
    for i in write:
        write[write.index(i)] = float(i)

    finalRead = []
    for i in range(0, len(read)):
        if i == 0:
            finalRead.append(1)
        elif read[i] == read[i - 1]:
            finalRead.append(1)
        else:
            finalRead.append(read[i] - read[i - 1])
    finalWrite = []
    for i in range(0, len(write)):
        if i == 0:
            finalWrite.append(1)
        elif write[i] == write[i - 1]:
            finalWrite.append(1)
        else:
            finalWrite.append(write[i] - write[i - 1])

    drawSmartGraph(finalRead, finalWrite, canvas, "HDD", folder)


def drawNET(folder, canvas):
    """
    Reads the stored percentages from the saved file
    Calls the draw smart graph function
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    f = open(dir_path + "\\output\\" + folder + "\\" + folder + ".txt", "r")
    input = f.read()
    input = input[1:len(input) - 1]
    readInput = input[:input.find("]<sep>[")]
    writeOutput = input[input.find("]<sep>[") + 7:len(input)]

    read = list(readInput.split(", "))
    write = list(writeOutput.split(", "))
    for i in read:
        read[read.index(i)] = float(i)
    for i in write:
        write[write.index(i)] = float(i)

    finalRead = []
    for i in range(0, len(read)):
        if i == 0:
            finalRead.append(1)
        elif read[i] == read[i - 1]:
            finalRead.append(1)
        else:
            finalRead.append(read[i] - read[i - 1])
    finalWrite = []
    for i in range(0, len(write)):
        if i == 0:
            finalWrite.append(1)
        elif write[i] == write[i - 1]:
            finalWrite.append(1)
        else:
            finalWrite.append(write[i] - write[i - 1])

    drawSmartGraph(finalWrite, finalRead, canvas, "NET", folder)


def drawPercentage(li, canvas, component, folder):
    """
    Function used to display the CPU, GPU and RAM graphs.
    Adds the details for the percentages on the graph and then adds the percentages on the graph.
    """
    canvas.create_text(1240 - 60, 20, fill="#72B2D6", font="Times 16 italic bold",
                       text=f"{component} Usage")
    positionY = 0
    while positionY < 620:
        if positionY != 0 and positionY != 620:
            canvas.create_line(30, positionY, 1240, positionY, fill='#E6F1F8')
            canvas.create_text(15, positionY, fill="#72B2D6", font="Times 10 italic bold",
                               text=str(int(100 - positionY / 620 * 100)))
        positionY += 620 / 10

    i = len(li) - 1
    positionX = 1240
    while (i > 0):
        canvas.create_line(positionX,
                           620 - 620 / 100 *
                           li[i],
                           positionX - 1240 / (len(li) - 1),
                           620 - 620 / 100 *
                           li[i - 1],
                           fill='#549401', width=2)
        if len(li) < 60:
            if i == len(li) - 1:
                canvas.create_text(positionX - 12, 620 - 620 / 100 * li[i], fill='black', text=li[i])
                if len(li) - 1 == 1:
                    canvas.create_text(positionX - 1240 / (len(li) - 1) + 12, 620 - 620 / 100 * li[i - 1], fill='black',
                                       text=li[i - 1])
            elif i == 1:
                canvas.create_text(positionX, 620 - 620 / 100 * li[i], fill='black', text=li[i])
                canvas.create_text(positionX - 1240 / (len(li) - 1) + 12, 620 - 620 / 100 * li[i - 1], fill='black',
                                   text=li[i - 1])
            else:
                canvas.create_text(positionX, 620 - 620 / 100 * li[i], fill='black', text=li[i])
        positionX -= 1240 / (len(li) - 1)
        i -= 1

    diff = datetime.datetime.strptime(
        str(folder[len(folder) - 6:len(folder) - 4]) + ":" + str(folder[len(folder) - 4:len(folder) - 2]) + ":" + str(
            folder[len(folder) - 2:]), '%H:%M:%S') - datetime.timedelta(seconds=int(len(li) - 1))

    canvas.create_text(1215, 610, fill='black', text=str(folder[len(folder) - 6:len(folder) - 4]) + ":" + str(
        folder[len(folder) - 4:len(folder) - 2]) + ":" + str(folder[len(folder) - 2:]))
    canvas.create_text(30, 610, fill='black', text=str(diff)[len(str(diff)) - 8:])


def drawSmartGraph(read, write, canvas, component, folder):
    """
    Function used to display the GPU and HDD graphs.
    Adds the details on the graph and based on the max from the lists read and write
    adds the lines at the correct height on the graph based on percentage from the max.
    """
    i = len(read) - 1
    positionX = 1240
    while (i > 0):
        canvas.create_line(positionX,
                           620 - 620 / 100 *
                           read[i] * 100 / max(read + write),
                           positionX - 1240 / (len(read) - 1),
                           620 - 620 / 100 *
                           read[i - 1] * 100 / max(read + write),
                           fill='blue', width=2)
        positionX -= 1240 / (len(read) - 1)
        i -= 1

    i = len(write) - 1
    positionX = 1240
    while (i > 0):
        canvas.create_line(positionX,
                           620 - 620 / 100 *
                           write[i] * 100 / max(read + write),
                           positionX - 1240 / (len(write) - 1),
                           620 - 620 / 100 *
                           write[i - 1] * 100 / max(read + write),
                           fill='#549401', width=2)
        positionX -= 1240 / (len(write) - 1)
        i -= 1

    m = max(read + write)
    canvas.create_line(45, 310, 1240, 310, fill='#E6F1F8')
    canvas.create_text(30, 310, fill="#72B2D6", font="Times 10 italic bold",
                       text=str(m / 2 / 1024 / 1024)[:8])

    canvas.create_line(45, 155, 1240, 155, fill='#E6F1F8')
    canvas.create_text(30, 155, fill="#72B2D6", font="Times 10 italic bold",
                       text=str(m * 3 / 4 / 1024 / 1024)[:8])

    canvas.create_line(45, 465, 1240, 465, fill='#E6F1F8')
    canvas.create_text(30, 465, fill="#72B2D6", font="Times 10 italic bold",
                       text=str(m / 4 / 1024 / 1024)[:8])

    diff = datetime.datetime.strptime(
        str(folder[len(folder) - 6:len(folder) - 4]) + ":" + str(folder[len(folder) - 4:len(folder) - 2]) + ":" + str(
            folder[len(folder) - 2:]), '%H:%M:%S') - datetime.timedelta(seconds=int(len(read) - 1))

    canvas.create_text(1210, 20, fill='black', text=str(folder[len(folder) - 6:len(folder) - 4]) + ":" + str(
        folder[len(folder) - 4:len(folder) - 2]) + ":" + str(folder[len(folder) - 2:]))
    canvas.create_text(30, 20, fill='black', text=str(diff)[len(str(diff)) - 8:])
    canvas.create_text(37, 40, fill='blue', text="MBps read")
    canvas.create_text(44, 60, fill='#549401', text="MBps written")

    canvas.create_text(1100, 20, fill="#72B2D6", font="Times 16 italic bold",
                       text=f"{component} Usage")


def leave(parent, drawing):
    """
    Leave function to close the window.
    Calls the main application leave function and then restores the functionality of its buttons.
    """
    parent.leave()
    parent.open.config(state="normal")
    parent.save.config(state="normal")
    parent.exit.config(state="normal")
    # mapps the canvas to the corresponding click function
    parent.cpu.bind("<Button-1>", lambda event: parent.showCPU(event, graph=parent.graph))
    parent.gpu.bind("<Button-1>", lambda event: parent.showGPU(event, graph=parent.graph))
    parent.ram.bind("<Button-1>", lambda event: parent.showRAM(event, graph=parent.graph))
    parent.hdd.bind("<Button-1>", lambda event: parent.showHDD(event, graph=parent.graph))
    parent.net.bind("<Button-1>", lambda event: parent.showNET(event, graph=parent.graph))
    drawing.destroy()
