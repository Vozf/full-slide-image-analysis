from PyQt5.QtWidgets import QDialog

from slide_analysis.UI.controller.constants import *
from slide_analysis.UI.view.ui_settings_dialog import Ui_SettingsDialog


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, controller):
        super(QDialog, self).__init__()
        self.setupUi(self)
        self.controller = controller
        self.init_buttons()
        self.similar_images_count_slider.valueChanged.connect(self.image_count_slider_position_changed)
        self.similar_images_columns_count_slider.valueChanged.connect(self.columns_count_slider_position_changed)
        self.init_combo_boxes()
        self.init_settings_value()

    def init_combo_boxes(self):
        self.choose_descriptors_combo_box.addItems(
            map(lambda x: x.__name__, self.controller.get_descriptors()))
        self.choose_similarities_combo_box.addItems(
            map(lambda x: x.__name__, self.controller.get_similarities()))

    def init_settings_value(self):
        self.similar_images_count_slider.setValue(self.controller.get_chosen_n())
        self.similar_images_columns_count_slider.setValue(self.controller.get_columns_count())
        self.choose_descriptors_combo_box.setCurrentIndex(self.controller
                                                          .get_chosen_descriptor_idx())
        self.choose_similarities_combo_box.setCurrentIndex(self.controller
                                                           .get_chosen_similarity_idx())

    def image_count_slider_position_changed(self):
        self.similar_images_count_label.setText(str(self.similar_images_count_slider.value()))

    def columns_count_slider_position_changed(self):
        self.similar_images_columns_count_text_label.setText(str(self.similar_images_columns_count_slider.value()))

    def show_dialog(self):
        self.show()

    def accept(self):
        settings = {
            CHOSEN_N: self.similar_images_count_slider.value(),
            CHOSEN_COLUMNS_COUNT: self.similar_images_columns_count_slider.value(),
            CHOSEN_DESCRIPTOR_IDX: self.choose_descriptors_combo_box.currentIndex(),
            CHOSEN_SIMILARITY_IDX: self.choose_similarities_combo_box.currentIndex(),
        }
        self.controller.settings_changed(settings)
        self.close()

    def decline(self):
        self.close()

    def init_buttons(self):
        self.settings_conformation_buttons.accepted.connect(self.accept)
        self.settings_conformation_buttons.rejected.connect(self.decline)
