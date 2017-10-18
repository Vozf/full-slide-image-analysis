from PyQt5.QtWidgets import QApplication

from slide_analysis.UI.view import ImageViewer
from slide_analysis.UI.model import Model
from slide_analysis.UI.controller.constants import *

class Controller:
    def __init__(self, argv):
        self.app = QApplication(argv)
        self.model = Model()
        self.image_viewer = ImageViewer(self, self.model)

    def run(self):
        self.image_viewer.show()
        return self.app.exec_()

    def calculate_descriptors_idx(self, idx):
        def calculate_descriptor():
            filename = self.image_viewer.image_helper.filename
            self.model.calculate_descriptors(idx, filename, DESCRIPTOR_DIRECTORY_PATH)

        return calculate_descriptor

    def get_descriptors(self):
        return self.model.descriptors
