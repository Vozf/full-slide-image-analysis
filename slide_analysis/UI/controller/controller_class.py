import glob
import os

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication

from slide_analysis.UI.controller.constants import *
from slide_analysis.UI.model import Model
from slide_analysis.UI.view import ImageViewer
from slide_analysis.constants.tile import BASE_TILE_WIDTH, BASE_TILE_HEIGHT
from slide_analysis.utils.functions import get_tile_from_coordinates


class Controller:
    def __init__(self, argv):
        self.app = QApplication(argv)
        self.model = Model()
        self.image_viewer = ImageViewer(self, self.model)

        self.app.installEventFilter(self.image_viewer)
        self.settings = QSettings("grad", "slide_analysis")
        self.chosen_descriptor_idx = self.settings.value(CHOSEN_DESCRIPTOR_IDX, 1)
        self.descriptor_params = self.settings.value(DESCRIPTOR_PARAMS, (3, 2, 3))
        self.chosen_similarity_idx = self.settings.value(CHOSEN_SIMILARITY, 0)
        self.similarity_params = self.settings.value(SIMILARITY_PARAMS, None)
        self.last_descriptor_database = None
        self.selected_dimensions = (BASE_TILE_WIDTH, BASE_TILE_HEIGHT)

    def get_chosen_n(self):
        return self.settings.value(CHOSEN_N, CHOSEN_N_DEFAULT_VALUE, type=int)

    def get_chosen_descriptor_idx(self):
        return self.settings.value(CHOSEN_DESCRIPTOR_IDX, CHOSEN_DESCRIPTOR_IDX_DEFAULT_VALUE,
                                   type=int)

    def get_chosen_descriptor_name(self):
        return self.get_descriptors()[self.get_chosen_descriptor_idx()].__name__

    # def get_fullslide_image_descriptor_directory_path(self):
    #     filename = self.image_viewer.image_helper.filename
    #     return filename[0:filename.find('.')].replace('/', ' ')

    def run(self):
        self.image_viewer.show()
        return self.app.exec_()

    def settings_changed(self, settings_new_state):
        for k, v in settings_new_state.items():
            self.settings.setValue(k, v)

    def get_imagepath(self):
        return self.image_viewer.image_helper.get_filepath()

    def calculate_descriptors(self):
        imagepath = self.get_imagepath()
        descriptor_base = self.model.calculate_descriptors(self.chosen_descriptor_idx,
                                                           self.descriptor_params,
                                                           imagepath, DESCRIPTOR_DIRECTORY_PATH)
        self.last_descriptor_database = descriptor_base

    def get_descriptors(self):
        return self.model.descriptors

    def get_similarities(self):
        return self.model.similarities

    def find_similar(self, coordinates):
        dimensions = self.selected_dimensions
        imagepath = self.get_imagepath()
        # todo remove when database select is added
        self.last_descriptor_database = self._select_last_modified_file_in_folder()
        desc_path = self.last_descriptor_database
        tile = get_tile_from_coordinates(imagepath, *coordinates, *dimensions)
        top_n = self.model.find_similar(desc_path, tile, self.get_chosen_n(),
                                        self.chosen_similarity_idx, self.similarity_params)
        qts = list(map(lambda tup: self.image_viewer.image_helper.get_qt_from_coordinates(
            tup), top_n))
        self.image_viewer.show_top_n(qts)

    @staticmethod
    def _select_last_modified_file_in_folder():
        files_path = os.path.join(DESCRIPTOR_DIRECTORY_PATH, '*')
        files = sorted(
            glob.iglob(files_path), key=os.path.getctime, reverse=True)
        return files[0]
