import sys

from slide_analysis.UI.controller import Controller

if __name__ == '__main__':
    controller = Controller(sys.argv)
    sys.exit(controller.run())
