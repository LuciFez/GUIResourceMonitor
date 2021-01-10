import os


def drawGraph(component):
    if component[:3] == "cpu":
        drawCPU(component)
    elif component[:3] == "gpu":
        drawGPU(component)
    elif component[:3] == "ram":
        drawRAM(component)
    elif component[:3] == "hdd":
        drawHDD(component)
    elif component[:3] == "net":
        drawNET(component)


def drawCPU(folder):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    f = open(dir_path + "\\output\\"+folder+"\\"+folder+".txt", "r")
    input = f.read()
    input = input[1:len(input)-1]
    li = list(input.split(", "))
    for i in li:
        print(i)


def drawGPU(folder):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    f = open(dir_path + "\\output\\" + folder + "\\" + folder + ".txt", "r")
    input = f.read()
    input = input[1:len(input) - 1]
    li = list(input.split(", "))
    for i in li:
        print(i)


def drawRAM(folder):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    f = open(dir_path + "\\output\\" + folder + "\\" + folder + ".txt", "r")
    input = f.read()
    input = input[1:len(input) - 1]
    li = list(input.split(", "))
    for i in li:
        print(i)


def drawHDD(folder):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    f = open(dir_path + "\\output\\" + folder + "\\" + folder + ".txt", "r")
    input = f.read()
    input = input[1:len(input) - 1]
    readInput = input[1:input.find("<sep>")-2]
    writeOutput = input[input.find("<sep>")+7:len(input)-1]
    readInputList = list(readInput.split("], ["))
    writeInputList = list(writeOutput.split("], ["))

    read = []
    write = []
    for i in readInputList:
        read.append(int(i[:i.find(',')]))
    for i in writeInputList:
        write.append(int(i[:i.find(',')]))


def drawNET(folder):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    f = open(dir_path + "\\output\\" + folder + "\\" + folder + ".txt", "r")
    input = f.read()
    input = input[1:len(input) - 1]
    readInput = input[:input.find("]<sep>[")]
    writeOutput = input[input.find("]<sep>[") + 7:len(input)]

    read = list(readInput.split(", "))
    write = list(writeOutput.split(", "))
