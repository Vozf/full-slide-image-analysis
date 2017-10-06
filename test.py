from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QPainter, QPalette, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLabel,
                             QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter

from ui_mainWindow import Ui_MainWindow
from PySide.QtGui import *
from PySide.QtCore import *
from image_helper import ImageHelper

# TODO Remove the unnecessary methods and fields
class ImageViewer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()
        self.setupUi(self)
        self.show()

        self.printer = QPrinter()
        self.scaleFactor = 0.0

        # self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        # self.scrollArea = QScrollArea()
        # self.scrollArea.setBackgroundRole(QPalette.Dark)
        # self.scrollArea.setWidget(self.imageLabel)
        # self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Image Viewer")
        # self.resize(500, 400)

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File",
                                                  QDir.currentPath())
        if fileName:
            # image = openslide.OpenSlide(fileName).read_region((0, 0), 1, (1000, 1000))
            # openslideImage = openslide.OpenSlide(fileName)

            self.imageHelper = ImageHelper(fileName)

            # print openslideImage.dimensions
            # print openslideImage.level_dimensions
            # print openslideImage.level_count
            # self.image = openslideImage.get_thumbnail((self.imageLabel.width(), self.imageLabel.height()))
            #
            # self.image = openslideImage.read_region((0, 0), openslideImage.level_count - 1,
            #                                         openslideImage.level_dimensions[openslideImage.level_count - 1])

            # image.convert("RGBA")
            # qim = ImageQt.ImageQt(self.image)

            # qim = self.imageHelper.get_QImage()

            # image = QImage(fileName)
            # if image.isNull():
            #     QMessageBox.information(self, "Image Viewer",
            #             "Cannot load %s." % fileName)
            #     return

            self.imageLabel.setPixmap(QPixmap.fromImage(self.imageHelper.get_QImage()))
            self.scaleFactor = 1.0

            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def zoomIn(self):
        # self.scaleImage(1.2)
        self.imageLabel.setPixmap(QPixmap.fromImage(self.imageHelper.zoom_in()))

    def zoomOut(self):
        # self.scaleImage(0.8)
        self.imageLabel.setPixmap(QPixmap.fromImage(self.imageHelper.zoom_out()))

    def move_right(self):
        self.imageHelper.move_right()
        print self.imageLabel.size()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.imageHelper.get_QImage()))

    def move_left(self):
        self.imageHelper.move_left()
        print self.imageLabel.size()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.imageHelper.get_QImage()))

    def move_up(self):
        self.imageHelper.move_up()
        print self.imageLabel.size()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.imageHelper.get_QImage()))

    def move_down(self):
        self.imageHelper.move_down()
        print self.imageLabel.size()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.imageHelper.get_QImage()))

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def about(self):
        QMessageBox.about(self, "About Image Viewer",
                          "<p>The <b>Image Viewer</b> example shows how to combine "
                          "QLabel and QScrollArea to display an image. QLabel is "
                          "typically used for displaying text, but it can also display "
                          "an image. QScrollArea provides a scrolling view around "
                          "another widget. If the child widget exceeds the size of the "
                          "frame, QScrollArea automatically provides scroll bars.</p>"
                          "<p>The example demonstrates how QLabel's ability to scale "
                          "its contents (QLabel.scaledContents), and QScrollArea's "
                          "ability to automatically resize its contents "
                          "(QScrollArea.widgetResizable), can be used to implement "
                          "zooming and scaling features.</p>"
                          "<p>In addition the example shows how to use QPainter to "
                          "print an image.</p>")

    def createActions(self):
        self.openAct = QAction("&Open...", self)
        self.openAct.setShortcut("Ctrl+O")
        self.openAct.triggered.connect(self.open)

        self.printAct = QAction("&Print...", self)
        # , shortcut="Ctrl+P",
        # enabled=False, triggered=self.print_)
        self.printAct.setEnabled(False)
        self.printAct.setShortcut("Ctrl+P")
        self.printAct.triggered.connect(self.print_)

        self.exitAct = QAction("E&xit", self)
        # , shortcut="Ctrl+Q",
        # triggered=self.close)
        self.exitAct.setShortcut("Ctrl+Q")
        self.exitAct.triggered.connect(self.close)

        self.zoomInAct = QAction("Zoom &In (25%)", self)
        # , shortcut="Ctrl++",
        # enabled=False, triggered=self.zoomIn)
        self.zoomInAct.setEnabled(False)
        self.zoomInAct.setShortcut("Ctrl++")
        self.zoomInAct.triggered.connect(self.zoomIn)

        self.zoomOutAct = QAction("Zoom &Out (25%)", self)
        # , shortcut="Ctrl+-",
        # enabled=False, triggered=self.zoomOut)
        self.zoomOutAct.setEnabled(False)
        self.zoomOutAct.setShortcut("Ctrl+-")
        self.zoomOutAct.triggered.connect(self.zoomOut)

        self.normalSizeAct = QAction("&Normal Size", self)
        # , shortcut="Ctrl+S",
        # enabled=False, triggered=self.normalSize)
        self.normalSizeAct.setShortcut("Ctrl+S")
        self.normalSizeAct.setEnabled(False)
        self.normalSizeAct.triggered.connect(self.normalSize)

        self.fitToWindowAct = QAction("&Fit to Window", self)
        # , enabled=False,
        # checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)
        self.fitToWindowAct.setShortcut("Ctrl+F")
        self.fitToWindowAct.setCheckable(True)
        self.fitToWindowAct.setEnabled(False)
        self.fitToWindowAct.triggered.connect(self.fitToWindow)

        self.aboutAct = QAction("&About", self)
        # , triggered=self.about)
        self.aboutAct.triggered.connect(self.about)

        self.aboutQtAct = QAction("About &Qt", self)
        # , triggered=QApplication.instance().aboutQt)
        self.aboutQtAct.triggered.connect(QApplication.instance().aboutQt)

        self.moveRightAct = QAction("&Move right", self)
        self.moveRightAct.setShortcut("Right")
        self.moveRightAct.triggered.connect(self.move_right)

        self.moveLeftAct = QAction("&Move left", self)
        self.moveLeftAct.setShortcut("Left")
        self.moveLeftAct.triggered.connect(self.move_left)

        self.moveUpAct = QAction("&Move up", self)
        self.moveUpAct.setShortcut("Up")
        self.moveUpAct.triggered.connect(self.move_up)

        self.moveDownAct = QAction("&Move down", self)
        self.moveDownAct.setShortcut("Down")
        self.moveDownAct.triggered.connect(self.move_down)

    def createMenus(self):

        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.navigationMenu = QMenu("&Navigation", self)
        self.navigationMenu.addAction(self.moveRightAct)
        self.navigationMenu.addAction(self.moveLeftAct)
        self.navigationMenu.addAction(self.moveDownAct)
        self.navigationMenu.addAction(self.moveUpAct)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.navigationMenu)
        self.menuBar().addMenu(self.helpMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    imageViewer = ImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())
