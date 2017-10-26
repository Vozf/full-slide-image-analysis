from PyQt5.QtWidgets import QApplication

from slide_analysis.UI.view import ImageViewer
from slide_analysis.UI.model import Model
from slide_analysis.UI.controller.constants import *
from slide_analysis.utils.functions import get_tile_from_coordinates


class Controller:
    def __init__(self, argv):
        self.app = QApplication(argv)
        self.model = Model()
        self.image_viewer = ImageViewer(self, self.model)
        self.app.installEventFilter(self.image_viewer)
        self.chosen_descriptor_idx = 1
        self.descriptor_params = (3, 2, 3)
        self.chosen_similarity_idx = 0
        self.similarity_params = None
        self.chosen_n = 10

    def run(self):
        self.image_viewer.show()
        return self.app.exec_()

    def calculate_descriptors_idx(self, idx):
        def calculate_descriptor():
            filename = self.image_viewer.image_helper.filename
            self.model.calculate_descriptors(idx, None, filename, DESCRIPTOR_DIRECTORY_PATH)

        return calculate_descriptor

    def get_descriptors(self):
        return self.model.descriptors

    def get_similarities(self):
        return self.model.similarities

    def find_similar(self):
        coordinates = self.image_viewer.user_selected_coordinates
        dimensions = self.image_viewer.user_selected_dimensions
        desc_path = DESCRIPTOR_DIRECTORY_PATH + "/CMU-1-Small-Region/HistogramDescriptor/(3, 2, 3).bin"
        imagepath = self.image_viewer.image_helper.filename

        tile = get_tile_from_coordinates(imagepath, *coordinates, *dimensions)
        top_n = self.model.find_similar(desc_path, tile, self.chosen_n,
                                        self.chosen_similarity_idx, self.similarity_params)
        qts = list(map(lambda tup: self.image_viewer.image_helper.get_qt_from_coordinates((tup[1].x, tup[1].y)), top_n))

        self.image_viewer.show_top_n(qts)


