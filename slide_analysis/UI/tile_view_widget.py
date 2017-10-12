from PyQt5 import QtCore

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class TilePreviewPopup(QLabel):
    def __init__(self, tile):
        super().__init__()
        self.tile_label = QLabel(self)
        pixmap = QPixmap.fromImage(tile)
        self.tile_label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        position = self.cursor().pos()
        self.move(position)
        self.setWindowFlags(Qt.Popup | Qt.WindowStaysOnTopHint
                            | Qt.FramelessWindowHint
                            | Qt.X11BypassWindowManagerHint)

    # def leaveEvent(self, event):
    #     """ When the mouse leave this widget, destroy it. """
    #     self.destroy()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.close()
            event.accept()
        else:
            super().keyPressEvent(event)
