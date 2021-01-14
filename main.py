from Gui import *


def main():
    """
    Create a Gui object and calls the run method inside of it
    """
    gui = Gui()
    gui.run()


if __name__ == '__main__':
    """
    Set the maximum recursion limit
    Call the main method of the program
    """
    sys.setrecursionlimit(10 ** 6)
    main()
