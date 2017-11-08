from PyQt5 import QtCore

from PyQt5.QtCore import Qt, QRectF, QEvent, QTimer, QRect
from PyQt5.QtGui import QPixmap, QResizeEvent, QMouseEvent, QCursor, QTransform
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QFrame, QGraphicsPixmapItem

from slide_analysis.UI.view import ImageHelper
from slide_analysis.UI.view.tile_view_widget import TilePreviewPopup


class FullslideViewer(QGraphicsView):
    def __init__(self, parent):
        super(FullslideViewer, self).__init__(parent)
        self._zoom = 0
        self.image_helper = None
        self._scene = QGraphicsScene(self)
        self._photo = QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        self.controller = parent.controller
        self.image_popup_widget = None

    def mousePressEvent(self, q_mouse_event):
        if not self.is_image_opened():
                return
        user_selected_coordinates = self.image_helper\
            .get_tile_coordinates(self.mapToScene(q_mouse_event.pos()))

        image_qt = self.image_helper.get_qt_from_coordinates(user_selected_coordinates)
        self.image_popup_widget = TilePreviewPopup(image_qt, self.controller, user_selected_coordinates)
        self.image_popup_widget.show()

    # def mouseReleaseEvent(self, q_mouse_event):
    #     if not self.is_image_popup_shown():
    #         return
    #     self.image_popup_widget.destroy()
    #     q_mouse_event.accept()



    # def resizeEvent(self, event: QResizeEvent):
    #     self.fitInView()
    #
    # def get_scene(self):
    #     return self._scene

    # def keyPressEvent(self, event):
    #     if event.key() == QtCore.Qt.Key_Space:
    #         if self.is_image_popup_shown():
    #             if self.controller.last_descriptor_database is None:
    #                 # todo add popup
    #                 print("there should be popup to select descriptor database")
    #             self.controller.find_similar(self.image_popup_widget.coordinates)
    #             self.image_popup_widget.destroy()
    #             event.accept()
    #     else:
    #         super().keyPressEvent(event)

    def mouseMoveEvent(self, q_mouse_event):
        if not self.is_image_popup_shown():
            return
        self.image_popup_widget.destroy()
        q_mouse_event.accept()
    #     width, height = self.width(), self.height()
    #     event_x, event_y = event.x(), event.y()
    #
    #     if event_y < 0 or event_y > height or \
    #                     event_x < 0 or event_x > width:
    #         # Mouse cursor has left the widget. Wrap the mouse.
    #         global_pos = self.mapToGlobal(event.pos())
    #         if event_y < 0 or event_y > height:
    #             # Cursor left on the y axis. Move cursor to the
    #             # opposite side.
    #             global_pos.setY(global_pos.y() +
    #                             (height if event_y < 0 else -height))
    #         else:
    #             # Cursor left on the x axis. Move cursor to the
    #             # opposite side.
    #             global_pos.setX(global_pos.x() +
    #                             (width if event_x < 0 else -width))
    #
    #         # For the scroll hand dragging to work with mouse wrapping
    #         # we have to emulate a mouse release, move the cursor and
    #         # then emulate a mouse press. Not doing this causes the
    #         # scroll hand drag to stop after the cursor has moved.
    #         r_event = QMouseEvent(QEvent.MouseButtonRelease,
    #                               self.mapFromGlobal(QCursor.pos()),
    #                               Qt.LeftButton,
    #                               Qt.NoButton,
    #                               Qt.NoModifier)
    #         self.mouseReleaseEvent(r_event)
    #         QCursor.setPos(global_pos)
    #         p_event = QMouseEvent(QEvent.MouseButtonPress,
    #                               self.mapFromGlobal(QCursor.pos()),
    #                               Qt.LeftButton,
    #                               Qt.LeftButton,
    #                               Qt.NoModifier)
    #         QTimer.singleShot(0, lambda: self.mousePressEvent(p_event))
    #     else:
    #         QGraphicsView.mouseMoveEvent(self, event)

    def fitInView(self, **kwargs):
        rect = QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            # unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
            # self.scale(1 / unity.width(), 1 / unity.height())
            viewrect = self.viewport().rect()
            scenerect = self.transform().mapRect(rect)
            factor = min(viewrect.width() / scenerect.width(),
                         viewrect.height() / scenerect.height())
            # if factor <= 0.8:
            #     self.move_to_next_image_level()
            self.scale(factor, factor)
            self.centerOn(rect.center())

    # def move_to_next_image_level(self):
    #     pixmap = QPixmap.fromImage(self.image_helper.zoom_in())
    #     if pixmap and not pixmap.isNull():
    #         self.setDragMode(QGraphicsView.ScrollHandDrag)
    #         # self._photo =  QGraphicsPixmapItem()
    #         self._photo.setPixmap(pixmap)
    #         # self._scene.addItem(self._photo)
    #         # self._scene.addPixmap(pixmap)
    #         self.fitInView()
    #     else:
    #         self.setDragMode(QGraphicsView.NoDrag)
    #         self._photo.setPixmap(QPixmap())
    def is_image_popup_shown(self):
        return self.image_popup_widget is not None

    def is_image_opened(self):
        return self.image_helper is not None

    def set_image(self, image_helper):
        self._zoom = 0
        # self._scene.clear()
        self.image_helper = image_helper
        viewrect = [self.viewport().rect().width(), self.viewport().rect().height()]
        pixmap = QPixmap.fromImage(self.image_helper.update_q_image(viewrect))
        if pixmap and not pixmap.isNull():
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
            self.fitInView()
        else:
            self.setDragMode(QGraphicsView.NoDrag)
            self._photo.setPixmap(QPixmap())

    def zoomFactor(self):
        return self._zoom

    def update_image_after_changing_level(self):
        self.fitInView()
        factor = self.image_helper.get_scale_factor()
        self.scale(factor, factor)
        rect_tuple = self.image_helper.get_current_displayed_image_rect()
        self.ensureVisible(rect_tuple[0], rect_tuple[1], rect_tuple[2], rect_tuple[3], 0, 0)

    def wheelEvent(self, event):
        if not self._photo.pixmap().isNull():
            viewrect = [self.viewport().rect().width(), self.viewport().rect().height()]
            image_rect = self.mapToScene(self.viewport().rect()).boundingRect()
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                # print(image_rect)

                if factor > 1 and (image_rect.width() / viewrect[0] < 0.5 or image_rect.height() / viewrect[1] < 0.5):
                    # print(image_rect)
                    self.image_helper.set_current_image_rect(image_rect)
                    self.image_helper.move_to_next_image_level()
                    pixmap = QPixmap.fromImage(self.image_helper.get_current_image())

                    self._photo.setPixmap(pixmap)
                    self.update_image_after_changing_level()
                    # self.scene().update()
                elif factor < 1 and (image_rect.width() / viewrect[0] > 2 or image_rect.height() / viewrect[1] > 2):
                    self.image_helper.set_current_image_rect(image_rect)
                    self.image_helper.move_to_prev_image_level()
                    pixmap = QPixmap.fromImage(self.image_helper.get_q_image())

                    self._photo.setPixmap(pixmap)
                    self.update_image_after_changing_level()
                else:
                    self.scale(factor, factor)
            elif self._zoom == 0:
                self.image_helper.set_current_image_rect(image_rect)
                self.fitInView()
            else:
                self._zoom = 0
