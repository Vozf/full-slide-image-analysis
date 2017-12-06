from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication
import os
import glob

from slide_analysis.UI.controller.constants import *
from slide_analysis.UI.model import Model
from slide_analysis.UI.view import MainWindow
from slide_analysis.UI.view import ImageHelper
from slide_analysis.constants.tile import BASE_TILE_WIDTH, BASE_TILE_HEIGHT
from slide_analysis.descriptor_database_service import DescriptorDatabaseWriteService \
    as DDWS
from slide_analysis.utils.functions import get_tile_from_coordinates, get_tiles_coords_from_indexes


class Controller:
    def __init__(self, argv):
        self.app = QApplication(argv)
        self.model = Model()
        self.settings = QSettings("grad", "slide_analysis")
        self.image_viewer = MainWindow(self, self.model)

        self.app.installEventFilter(self.image_viewer)

        geometry = self.settings.value(GEOMETRY)
        if geometry is not None:
            self.image_viewer.restoreGeometry(geometry)
        window_state = self.settings.value(WINDOW_STATE)
        if window_state is not None:
            self.image_viewer.restoreState(window_state)

        last_image = self.settings.value(LAST_IMAGE)
        if last_image is not None:
            self.open_filepath(last_image)

        self.descriptor_database = None
        self.selected_dimensions = (BASE_TILE_WIDTH, BASE_TILE_HEIGHT)

    def get_similar_images_area_width(self):
        return DEFAULT_LEFT_RIGHT_MARGIN * 2 + BASE_TILE_WIDTH * self.get_columns_count() + \
                       DEFAULT_IN_BETWEEN_MARGIN * 2 * (self.get_columns_count() - 1)

    def get_chosen_n(self):
        return self.settings.value(CHOSEN_N, CHOSEN_N_DEFAULT_VALUE, type=int)

    def get_columns_count(self):
        return self.settings.value(CHOSEN_COLUMNS_COUNT, CHOSEN_COLUMNS_COUNT_DEFAULT_VALUE, type=int)

    def get_chosen_descriptor_idx(self):
        return self.settings.value(CHOSEN_DESCRIPTOR_IDX, CHOSEN_DESCRIPTOR_IDX_DEFAULT_VALUE,
                                   type=int)

    def get_descriptor_params(self):
        return self.settings.value(DESCRIPTOR_PARAMS, DESCRIPTOR_PARAMS_DEFAULT_VALUE,
                                   type=tuple)

    def get_chosen_similarity_idx(self):
        return self.settings.value(CHOSEN_SIMILARITY_IDX, CHOSEN_SIMILARITY_IDX_DEFAULT_VALUE,
                                   type=int)

    def get_similarity_params(self):
        return self.settings.value(SIMILARITY_PARAMS, SIMILARITY_PARAMS_DEFAULT_VALUE,
                                   type=float)

    def run(self):
        self.image_viewer.show()
        return self.app.exec_()

    def settings_changed(self, settings_new_state):
        for k, v in settings_new_state.items():
            self.settings.setValue(k, v)
        self.image_viewer.set_similar_images_area_width(self.get_similar_images_area_width())
        self.image_viewer.clear_top_images_area()

    def get_imagepath(self):
        return self.image_viewer.image_helper.get_filepath()

    def calculate_descriptors(self):
        imagepath = self.get_imagepath()
        descriptor_base = self.model.calculate_descriptors(self.get_chosen_descriptor_idx(),
                                                           self.get_descriptor_params(),
                                                           imagepath, DESCRIPTOR_DIRECTORY_PATH)
        self.descriptor_database = descriptor_base
        self.model.init_search_service(descriptor_base)

    def get_descriptors(self):
        return self.model.descriptors

    def get_similarities(self):
        return self.model.similarities

    def find_similar(self, coordinates):
        dimensions = self.selected_dimensions
        imagepath = self.get_imagepath()

        tile = get_tile_from_coordinates(imagepath, *coordinates, *dimensions)
        similarity_obj = self.model.find_similar(tile, self.get_chosen_n(),
                                        self.get_chosen_similarity_idx(),
                                        self.get_similarity_params())
        top_n = similarity_obj["top_n"]
        img_arr = similarity_obj["img_arr"]
        qts = list(map(lambda tup: self.image_viewer.image_helper.get_qt_from_coordinates(
            tup), top_n))
        self.similarity_map = self.image_viewer.image_helper.img_from_arr(img_arr)
        chosen_image = self.image_viewer.image_helper.get_qt_from_coordinates(coordinates)
        self.image_viewer.show_top_n(chosen_image, qts)

    def get_similarity_map(self):
        return self.similarity_map

    @staticmethod
    def _select_last_modified_file_in_folder():
        files_path = os.path.join(DESCRIPTOR_DIRECTORY_PATH, '*')
        files = sorted(
            glob.iglob(files_path), key=os.path.getctime, reverse=True)
        return files[0]

    def set_desc_path(self, image_path):
        descr_base_path = \
            DDWS.generate_name_of_basefile(DESCRIPTOR_DIRECTORY_PATH,
                                           image_path,
                                           self.get_descriptors()[
                                               self.get_chosen_descriptor_idx()],
                                           self.get_descriptor_params())
        if os.path.exists(descr_base_path):
            self.descriptor_database = descr_base_path
            self.model.init_search_service(descr_base_path)
        else:
            print('----- There is no calculated descriptors for chosen params -----')

    def close_event(self):
        self.settings.setValue(GEOMETRY, self.image_viewer.saveGeometry())
        self.settings.setValue(WINDOW_STATE, self.image_viewer.saveState())

    def open_filepath(self, filepath):
        if not filepath:
            return
        self.image_viewer.image_helper = ImageHelper(filepath)
        self.image_viewer.image_display.set_image(self.image_viewer.image_helper)
        self.set_desc_path(filepath)

        self.settings.setValue(LAST_IMAGE, filepath)
