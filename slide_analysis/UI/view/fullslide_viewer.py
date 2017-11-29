import time
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QFrame, QGraphicsPixmapItem

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
        self.setViewportUpdateMode(self.SmartViewportUpdate)
        self.controller = parent.controller
        self.image_popup_widget = None
        self.current_mouse_press_coordinates = None

    def mousePressEvent(self, q_mouse_event):
        if self.image_helper is not None:
            self.current_mouse_press_coordinates = q_mouse_event.pos()
            print(self.current_mouse_press_coordinates)
        QGraphicsView.mousePressEvent(self, q_mouse_event)

    def mouseReleaseEvent(self, q_mouse_event):
        if self.image_helper is not None:
            if self.current_mouse_press_coordinates == q_mouse_event.pos():
                user_selected_coordinates = self.image_helper \
                    .get_tile_coordinates(self.mapToScene(q_mouse_event.pos()))

                image_qt = self.image_helper.get_qt_from_coordinates(user_selected_coordinates)
                self.image_popup_widget = TilePreviewPopup(image_qt, self.controller, user_selected_coordinates)
                self.image_popup_widget.show()
            else:
                image_rect = self.mapToScene(self.viewport().rect()).boundingRect()
                self.image_helper.set_current_image_rect(image_rect)
                self.image_helper.update_image_rect()
                pixmap = QPixmap.fromImage(self.image_helper.update_q_image())
                self._photo.setPixmap(pixmap)
                self.update_image()
        QGraphicsView.mouseReleaseEvent(self, q_mouse_event)



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
        if self.is_image_popup_shown():
            print('popup is alive')
            self.image_popup_widget.destroy()
            self.image_popup_widget = None
        QGraphicsView.mouseMoveEvent(self, q_mouse_event)

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

    def update_image(self):
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
                    millis1 = round(time.time() * 1000)
                    self.image_helper.move_to_next_image_level()
                    millis2 = round(time.time() * 1000)
                    print('move to next image level ' + str(millis2 - millis1))

                    pixmap = QPixmap.fromImage(self.image_helper.get_current_image())
                    millis1 = round(time.time() * 1000)
                    self._photo.setPixmap(pixmap)
                    millis2 = round(time.time() * 1000)
                    print('set new pixmap ' + str(millis2 - millis1))
                    millis1 = round(time.time() * 1000)
                    self.update_image()
                    millis2 = round(time.time() * 1000)
                    print('update image ' + str(millis2 - millis1))
                    # self.scene().update()
                elif factor < 1 and (image_rect.width() / viewrect[0] > 2 or image_rect.height() / viewrect[1] > 2):
                    self.image_helper.set_current_image_rect(image_rect)
                    self.image_helper.move_to_prev_image_level()
                    pixmap = QPixmap.fromImage(self.image_helper.get_q_image())

                    self._photo.setPixmap(pixmap)
                    self.update_image()
                else:
                    self.scale(factor, factor)
            elif self._zoom == 0:
                self.image_helper.set_current_image_rect(image_rect)
                self.fitInView()
            else:
                self._zoom = 0
