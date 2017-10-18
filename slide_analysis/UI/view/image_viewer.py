# from PyQt5.QtCore import QDir, Qt
# from PyQt5.QtGui import QPalette, QPixmap
# from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLabel,
#                              QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy)
#
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QPalette, QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QAction, QApplication, QMenu
from slide_analysis.UI.view import ImageHelper

from slide_analysis.UI.view.ui_mainWindow import Ui_MainWindow


class ImageViewer(QMainWindow, Ui_MainWindow):
    def __init__(self, controller, model):
        super(ImageViewer, self).__init__()
        self.model = model
        self.controller = controller

        self.setupUi(self)
        self.show()

        self.scale_factor = 0.0

        # self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        # self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.imageLabel.setScaledContents(True)

        # self.scrollArea = QScrollArea()
        # self.scrollArea.setBackgroundRole(QPalette.Dark)
        # self.scrollArea.setWidget(self.imageLabel)
        # self.setCentralWidget(self.scrollArea)

        self.create_actions()
        self.create_menus()

        self.setWindowTitle("Image Viewer")
        # self.resize(500, 400)

    def open(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        print(filename)
        if filename:
            # image = openslide.OpenSlide(fileName).read_region((0, 0), 1, (1000, 1000))
            # openslideImage = openslide.OpenSlide(fileName)

            self.image_helper = ImageHelper(filename)

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

            # self.scrollArea.setWidgetResizable(True)

            # pixmap = QPixmap.fromImage(self.image_helper.get_q_image())
            # scaledPixmap = pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio)
            self.imageLabel.setPixmap(self.get_scaled_pixmap(self.image_helper.get_q_image()))

            # self.imageLabel.adjustSize()
            # self.fit_to_window_act.setEnabled(True)
            # self.update_actions()

            # if not self.fit_to_window_act.isChecked():
            #     self.imageLabel.adjustSize()

    def get_scaled_pixmap(self, qImage):
        pixmap = QPixmap.fromImage(qImage)
        return pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio)

    def zoom_in(self):
        # self.scaleImage(1.2)
        self.imageLabel.setPixmap(self.get_scaled_pixmap(self.image_helper.zoom_in()))

    def zoom_out(self):
        # self.scaleImage(0.8)
        self.imageLabel.setPixmap(self.get_scaled_pixmap(self.image_helper.zoom_out()))

    def move_right(self):
        self.image_helper.move_right()
        print(self.imageLabel.size())
        self.imageLabel.setPixmap(self.get_scaled_pixmap(self.image_helper.get_q_image()))

    def move_left(self):
        self.image_helper.move_left()
        print(self.imageLabel.size())
        self.imageLabel.setPixmap(self.get_scaled_pixmap(self.image_helper.get_q_image()))

    def move_up(self):
        self.image_helper.move_up()
        print(self.imageLabel.size())
        self.imageLabel.setPixmap(self.get_scaled_pixmap(self.image_helper.get_q_image()))

    def move_down(self):
        self.image_helper.move_down()
        print(self.imageLabel.size())
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

        descriptors = self.controller.get_descriptors()

        descriptors_action = list(map(lambda x: QAction(x.get_name()), descriptors))

        for i in range(len(descriptors_action)):
            descriptors_action[i].triggered.connect(self.controller.calculate_descriptors_idx(i))

        self.descriptors = descriptors_action

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

        self.descriptor_menu = QMenu("&Descriptors", self)
        for desc in self.descriptors:
            self.descriptor_menu.addAction(desc)

        self.help_menu = QMenu("&Help", self)
        self.help_menu.addAction(self.about_act)
        self.help_menu.addAction(self.about_qt_act)

        self.menuBar().addMenu(self.file_menu)
        self.menuBar().addMenu(self.view_menu)
        self.menuBar().addMenu(self.descriptor_menu)
        self.menuBar().addMenu(self.navigation_menu)
        self.menuBar().addMenu(self.help_menu)
        self.menuBar().addMenu(self.descriptor_menu)

    # def update_actions(self):
    #     self.zoom_in_act.setEnabled(not self.fit_to_window_act.isChecked())
    #     self.zoom_out_act.setEnabled(not self.fit_to_window_act.isChecked())
    #     self.normal_size_act.setEnabled(not self.fit_to_window_act.isChecked())

    def scale_image(self, factor):
        self.scale_factor *= factor
        self.imageLabel.resize(self.scale_factor * self.imageLabel.pixmap().size())

        self.adjust_scroll_bar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjust_scroll_bar(self.scrollArea.verticalScrollBar(), factor)

        self.zoom_in_act.setEnabled(self.scale_factor < 3.0)
        self.zoom_out_act.setEnabled(self.scale_factor > 0.333)

    @staticmethod
    def adjust_scroll_bar(scroll_bar, factor):
        scroll_bar.setValue(int(factor * scroll_bar.value()
                                + ((factor - 1) * scroll_bar.pageStep() / 2)))
