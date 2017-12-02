from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

from slide_analysis.UI.view.image_display import ImageDisplay
from slide_analysis.UI.view.image_helper import ImageHelper
from slide_analysis.UI.view.settings_dialog import SettingsDialog
from slide_analysis.UI.view.ui_mainWindow import Ui_MainWindow
from slide_analysis.constants.tile import BASE_TILE_WIDTH, BASE_TILE_HEIGHT


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, controller, model):
        super(MainWindow, self).__init__()
        self.showMaximized()
        self.model = model
        self.controller = controller
        self.image_helper = None

        self.setupUi(self)
        self.fullslide_viewer = ImageDisplay(self)
        self.fullslideImageLayout.addWidget(self.fullslide_viewer)

        self.imageVerticalLayout = QGridLayout(self.topImagesScrollAreaWidgetContents)
        self.topImagesScrollArea.setWidgetResizable(True)
        self.topImagesScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.topImagesScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.image_popup_widget = None
        self.settings_dialog = None
        self.show()

        self.create_actions()
        self.create_menus()

    def show_top_n(self, tiles):
        for i in reversed(range(self.imageVerticalLayout.count())):
            self.imageVerticalLayout.itemAt(i).widget().setParent(None)

        row = col = 0
        for tile in tiles:
            label = QLabel()
            pixmap = QPixmap.fromImage(tile)
            pixmap = pixmap.scaled(BASE_TILE_WIDTH, BASE_TILE_HEIGHT, Qt.KeepAspectRatioByExpanding)
            label.setPixmap(pixmap)
            self.imageVerticalLayout.addWidget(label, row, col)
            col += 1
            if col % 2 == 0:
                row += 1
                col = 0

    def is_image_opened(self):
        return self.image_helper is not None

    def is_image_popup_shown(self):
        return self.image_popup_widget is not None

    def open(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        print("filepath:", filepath)
        if filepath:
            self.image_helper = ImageHelper(filepath)
            self.fullslide_viewer.set_image(self.image_helper)
            self.controller.set_desc_path(filepath)

    def get_pixmap(self, q_image):
        return QPixmap.fromImage(q_image)

    #
    # def normal_size(self):
    #     self.fullslide_viewer.adjustSize()

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
        self.exit_act.setShortcut("Ctrl+Q")
        self.exit_act.triggered.connect(self.close)

        #
        # self.normal_size_act = QAction("&Normal Size", self)
        # # , shortcut="Ctrl+S",
        # # enabled=False, triggered=self.normalSize)
        # self.normal_size_act.setShortcut("Ctrl+S")
        # # self.normal_size_act.setEnabled(False)
        # self.normal_size_act.triggered.connect(self.normal_size)

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

        self.calculate_descriptor_act = QAction("Calculate")
        self.calculate_descriptor_act.triggered.connect(self.controller.calculate_descriptors)

        self.settings_act = QAction("Settings")
        self.settings_act.triggered.connect(self.show_settings)

    def show_settings(self):
        if self.settings_dialog is None:
            self.settings_dialog = SettingsDialog(self.controller)
        self.settings_dialog.show()

    # noinspection PyAttributeOutsideInit
    def create_menus(self):
        self.file_menu = QMenu("&File", self)
        self.file_menu.addAction(self.open_act)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_act)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.settings_act)

        self.descriptor_menu = QMenu("&Descriptors", self)

        self.descriptor_menu.addAction(self.calculate_descriptor_act)

        self.help_menu = QMenu("&Help", self)
        self.help_menu.addAction(self.about_act)
        self.help_menu.addAction(self.about_qt_act)

        self.menuBar().addMenu(self.file_menu)
        self.menuBar().addMenu(self.descriptor_menu)
        self.menuBar().addMenu(self.help_menu)
