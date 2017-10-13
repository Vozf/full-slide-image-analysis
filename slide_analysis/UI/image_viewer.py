# from PyQt5.QtCore import QDir, Qt
# from PyQt5.QtGui import QPalette, QPixmap
# from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLabel,
#                              QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy)
#
from PyQt5 import QtCore

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QPalette, QPixmap
from PyQt5.QtWidgets import *

from slide_analysis.UI.image_helper import ImageHelper
from slide_analysis.UI.tile_view_widget import TilePreviewPopup
from slide_analysis.UI.ui_mainWindow import Ui_MainWindow
from slide_analysis.UI.constants import SIMILAR_TILE_SIZE


class ImageViewer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()
        self.image_helper = None
        self.setupUi(self)
        self.imageVerticalLayout = QBoxLayout(QBoxLayout.Down)
        self.topImagesScrollAreaWidgetContents.setLayout(self.imageVerticalLayout)
        self.topImagesScrollArea.setWidgetResizable(True)
        self.image_popup_widget = None
        self.show()

        self.scale_factor = 0.0

        self.imageLabel.setBackgroundRole(QPalette.Base)
        # self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.imageLabel.setScaledContents(True)

        self.create_actions()
        self.create_menus()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
            if event.buttons() == QtCore.Qt.NoButton and self.is_image_popup_shown():
                self.image_popup_widget.close()
        return QMainWindow.eventFilter(self, source, event)

    def resizeEvent(self, event):
        if not self.is_image_opened():
            return
        self.imageLabel.setPixmap(self.get_scaled_pixmap(self.image_helper.get_q_image()))

    def mousePressEvent(self, q_mouse_event):
        if not self.is_image_opened():
            return
        tile = self.image_helper.get_tile_from_coordinates(
                self.image_helper.get_tile_coodinates(q_mouse_event.pos(), self.scrollArea.geometry()))
        self.image_popup_widget = TilePreviewPopup(tile)
        self.image_popup_widget.show()
        self.show_top_n([tile])

    def mouseReleaseEvent(self, q_mouse_event):
        if not self.is_image_popup_shown():
            return
        self.image_popup_widget.close()
        q_mouse_event.accept()

    def show_top_n(self, tiles):
        for i in reversed(range(self.imageVerticalLayout.count())):
            self.imageVerticalLayout.removeItem(self.imageVerticalLayout.itemAt(i))

        for tile in tiles:
            label = QLabel()
            pixmap = QPixmap.fromImage(tile)
            pixmap = pixmap.scaled(SIMILAR_TILE_SIZE[0], SIMILAR_TILE_SIZE[1], Qt.KeepAspectRatio)
            label.setPixmap(pixmap)
            self.imageVerticalLayout.addWidget(label)

    def is_image_opened(self):
        return self.image_helper is not None

    def is_image_popup_shown(self):
        return self.image_popup_widget is not None

    def open(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        if file_name:
            self.image_helper = ImageHelper(file_name)
            self.imageLabel.setPixmap(self.get_scaled_pixmap(self.image_helper.get_q_image()))

    def get_scaled_pixmap(self, q_image):
        pixmap = QPixmap.fromImage(q_image)
        print('Scroll area size: ', self.scrollArea.size())
        return pixmap.scaled(self.scrollArea.width() - 20, self.scrollArea.height() - 20, Qt.IgnoreAspectRatio)

    def zoom_in(self):
        if not self.is_image_opened():
            return
        self.imageLabel.setPixmap(self.get_scaled_pixmap(self.image_helper.zoom_in()))

    def zoom_out(self):
        if not self.is_image_opened():
            return
        self.imageLabel.setPixmap(self.get_scaled_pixmap(self.image_helper.zoom_out()))

    def move_right(self):
        if not self.is_image_opened():
            return
        self.image_helper.move_right()
        # print(self.imageLabel.size())
        self.imageLabel.setPixmap(self.get_scaled_pixmap(self.image_helper.get_q_image()))

    def move_left(self):
        if not self.is_image_opened():
            return
        self.image_helper.move_left()
        # print(self.imageLabel.size())
        self.imageLabel.setPixmap(self.get_scaled_pixmap(self.image_helper.get_q_image()))

    def move_up(self):
        if not self.is_image_opened():
            return
        self.image_helper.move_up()
        # print(self.imageLabel.size())
        self.imageLabel.setPixmap(self.get_scaled_pixmap(self.image_helper.get_q_image()))

    def move_down(self):
        if not self.is_image_opened():
            return
        self.image_helper.move_down()
        # print(self.imageLabel.size())
        self.imageLabel.setPixmap(self.get_scaled_pixmap(self.image_helper.get_q_image()))

    def normal_size(self):
        self.imageLabel.adjustSize()

    # def fit_to_window(self):
    #     fitToWindow = self.fit_to_window_act.isChecked()
    #     self.scrollArea.setWidgetResizable(fitToWindow)
    #     if not fitToWindow:
    #         self.normal_size()
    #
    #     self.update_actions()

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

    # noinspection PyAttributeOutsideInit
    def create_actions(self):
        self.open_act = QAction("&Open...", self)
        self.open_act.setShortcut("Ctrl+O")
        self.open_act.triggered.connect(self.open)

        self.exit_act = QAction("E&xit", self)
        # , shortcut="Ctrl+Q",
        # triggered=self.close)
        self.exit_act.setShortcut("Ctrl+Q")
        self.exit_act.triggered.connect(self.close)

        self.zoom_in_act = QAction("Zoom &In", self)
        # , shortcut="Ctrl++",
        # enabled=False, triggered=self.zoomIn)
        # self.zoom_in_act.setEnabled(False)
        self.zoom_in_act.setShortcut("Ctrl++")
        self.zoom_in_act.triggered.connect(self.zoom_in)

        self.zoom_out_act = QAction("Zoom &Out", self)
        # , shortcut="Ctrl+-",
        # enabled=False, triggered=self.zoomOut)
        # self.zoom_out_act.setEnabled(False)
        self.zoom_out_act.setShortcut("Ctrl+-")
        self.zoom_out_act.triggered.connect(self.zoom_out)

        self.normal_size_act = QAction("&Normal Size", self)
        # , shortcut="Ctrl+S",
        # enabled=False, triggered=self.normalSize)
        self.normal_size_act.setShortcut("Ctrl+S")
        # self.normal_size_act.setEnabled(False)
        self.normal_size_act.triggered.connect(self.normal_size)

        # self.fit_to_window_act = QAction("&Fit to Window", self)
        # # , enabled=False,
        # # checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)
        # self.fit_to_window_act.setShortcut("Ctrl+F")
        # self.fit_to_window_act.setCheckable(True)
        # self.fit_to_window_act.setEnabled(False)
        # self.fit_to_window_act.triggered.connect(self.fit_to_window)

        self.about_act = QAction("&About", self)
        # , triggered=self.about)
        self.about_act.triggered.connect(self.about)

        self.about_qt_act = QAction("About &Qt", self)
        # , triggered=QApplication.instance().aboutQt)
        self.about_qt_act.triggered.connect(QApplication.instance().aboutQt)

        self.move_right_act = QAction("&Move right", self)
        self.move_right_act.setShortcut("Right")
        self.move_right_act.triggered.connect(self.move_right)

        self.move_left_act = QAction("&Move left", self)
        self.move_left_act.setShortcut("Left")
        self.move_left_act.triggered.connect(self.move_left)

        self.move_up_act = QAction("&Move up", self)
        self.move_up_act.setShortcut("Up")
        self.move_up_act.triggered.connect(self.move_up)

        self.move_down_act = QAction("&Move down", self)
        self.move_down_act.setShortcut("Down")
        self.move_down_act.triggered.connect(self.move_down)

    # noinspection PyAttributeOutsideInit
    def create_menus(self):
        self.file_menu = QMenu("&File", self)
        self.file_menu.addAction(self.open_act)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_act)

        self.view_menu = QMenu("&View", self)
        self.view_menu.addAction(self.zoom_in_act)
        self.view_menu.addAction(self.zoom_out_act)
        self.view_menu.addAction(self.normal_size_act)
        self.view_menu.addSeparator()
        # self.view_menu.addAction(self.fit_to_window_act)

        self.navigation_menu = QMenu("&Navigation", self)
        self.navigation_menu.addAction(self.move_right_act)
        self.navigation_menu.addAction(self.move_left_act)
        self.navigation_menu.addAction(self.move_down_act)
        self.navigation_menu.addAction(self.move_up_act)

        self.help_menu = QMenu("&Help", self)
        self.help_menu.addAction(self.about_act)
        self.help_menu.addAction(self.about_qt_act)

        self.menuBar().addMenu(self.file_menu)
        self.menuBar().addMenu(self.view_menu)
        self.menuBar().addMenu(self.navigation_menu)
        self.menuBar().addMenu(self.help_menu)

    # def update_actions(self):
    #     self.zoom_in_act.setEnabled(not self.fit_to_window_act.isChecked())
    #     self.zoom_out_act.setEnabled(not self.fit_to_window_act.isChecked())
    #     self.normal_size_act.setEnabled(not self.fit_to_window_act.isChecked())

    # def scale_image(self, factor):
    #     self.scale_factor *= factor
    #     self.imageLabel.resize(self.scale_factor * self.imageLabel.pixmap().size())
    #
    #     self.adjust_scroll_bar(self.scrollArea.horizontalScrollBar(), factor)
    #     self.adjust_scroll_bar(self.scrollArea.verticalScrollBar(), factor)
    #
    #     self.zoom_in_act.setEnabled(self.scale_factor < 3.0)
    #     self.zoom_out_act.setEnabled(self.scale_factor > 0.333)

    @staticmethod
    def run(argv):
        app = QApplication(argv)
        image_viewer = ImageViewer()
        app.installEventFilter(image_viewer)
        image_viewer.show()
        return app.exec_()

    @staticmethod
    def adjust_scroll_bar(scroll_bar, factor):
        scroll_bar.setValue(int(factor * scroll_bar.value()
                                + ((factor - 1) * scroll_bar.pageStep() / 2)))
