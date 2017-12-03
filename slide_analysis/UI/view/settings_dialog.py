from PyQt5.QtWidgets import QDialog

from slide_analysis.UI.controller.constants import *
from slide_analysis.UI.view.ui_settings_dialog import Ui_SettingsDialog


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, controller):
        super(QDialog, self).__init__()
        self.setupUi(self)
        self.controller = controller
        self.init_buttons()
        self.similar_images_count_slider.valueChanged.connect(self.slider_position_changed)
        self.choose_descriptors_combo_box.activated.connect(self.descriptor_changed)
        self.choose_similarities_combo_box.currentIndexChanged.connect(self.similarity_changed)
        self.set_current_settings()
        self.current_settings = {}
        self.init_slider()
        self.init_combo_boxes()

    def init_combo_boxes(self):
        self.choose_descriptors_combo_box.addItems(
            map(lambda x: x.__name__, self.controller.get_descriptors()))
        self.choose_similarities_combo_box.addItems(
            map(lambda x: x.__name__, self.controller.get_similarities()))

    def init_slider(self):
        self.similar_images_count_slider.setValue(self.current_slider_value)

    def set_current_settings(self):
        self.current_slider_value = self.controller.get_chosen_n()
        self.current_descriptor_idx = self.controller.get_chosen_descriptor_idx()
        self.current_similarity_idx = self.controller.get_chosen_similarity_idx()

    def slider_position_changed(self):
        self.current_slider_value = self.similar_images_count_slider.value()
        self.current_settings[CHOSEN_N] = self.current_slider_value
        self.similar_images_count_label.setText(self.current_slider_value.__str__())

    def descriptor_changed(self):
        self.current_descriptor_idx = self.choose_descriptors_combo_box.currentIndex()
        self.current_settings[CHOSEN_DESCRIPTOR_IDX] = self.current_descriptor_idx

    def similarity_changed(self):
        self.current_similarity_idx = self.choose_similarities_combo_box.currentIndex()
        self.current_settings[CHOSEN_SIMILARITY_IDX] = self.current_similarity_idx

    def show_dialog(self):
        self.show()

    def accept(self):
        self.controller.settings_changed(self.current_settings)
        self.close()

    def decline(self):
        self.current_settings = None
        self.set_current_settings()
        self.close()

    def init_buttons(self):
        self.settings_conformation_buttons.accepted.connect(self.accept)
        self.settings_conformation_buttons.rejected.connect(self.decline)
