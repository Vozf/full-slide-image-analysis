from PyQt5.QtWidgets import QApplication, QMainWindow

from ui_mainWindow import Ui_MainWindow
from PySide.QtGui import *
from PySide.QtCore import *


class ImageViewer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    imageViewer = ImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())
