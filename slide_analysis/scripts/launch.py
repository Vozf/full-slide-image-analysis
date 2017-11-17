import sys
import cProfile

from slide_analysis.UI.controller import Controller

if __name__ == '__main__':
    def run():
        controller = Controller(sys.argv)
        sys.exit(controller.run())
    cProfile.run('run()', sort=1)
