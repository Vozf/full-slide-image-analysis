from PyQt5 import QtCore

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class TilePreviewPopup(QLabel):
    def __init__(self, tile, controller, coordinates):
        super().__init__()
        self.controller = controller
        self.coordinates = coordinates
        pixmap = QPixmap.fromImage(tile)
        self.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        position = self.cursor().pos()
        self.setMouseTracking(True)
        self.move(position)
        self.setWindowFlags(Qt.WindowStaysOnTopHint
                            | Qt.FramelessWindowHint)

    # def leaveEvent(self, event):
    #     """ When the mouse leave this widget, destroy it. """
    #     self.destroy()

    def mouseMoveEvent(self, event):
        self.destroy()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            if self.controller.descriptor_database is None:
                # todo add popup
                print("there should be popup to select descriptor database")
            self.controller.find_similar(self.coordinates)
            self.destroy()
            event.accept()
        else:
            super().keyPressEvent(event)
