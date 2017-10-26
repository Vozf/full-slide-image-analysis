from PyQt5.QtWidgets import QDialog

from slide_analysis.UI.view.ui_settings_dialog import Ui_SettingsDialog


class SettingsDialog(QDialog, Ui_SettingsDialog):

    def __init__(self):
        super(QDialog, self).__init__()
        self.setupUi(self)
        self.init_buttons()
        self.similar_images_count_slider.valueChanged.connect(self.slider_position_changed)
        self.current_slider_value = 0
        self.current_descriptor = None
        self.current_metrics = None

    def slider_position_changed(self):
        self.current_slider_value = self.similar_images_count_slider.value()
        self.similar_images_count_label.setText(self.current_slider_value.__str__())

    def show_dialog(self):
        self.show()

    def accept(self):
        self.close()

    def decline(self):
        self.close()

    def init_buttons(self):
        self.settings_conformation_buttons.accepted.connect(self.accept)
        self.settings_conformation_buttons.rejected.connect(self.decline)
