from PyQt5.QtWidgets import QDialog

from slide_analysis.UI.view.ui_settings_dialog import Ui_SettingsDialog


class SettingsDialog(QDialog, Ui_SettingsDialog):

    def __init__(self):
        super(QDialog, self).__init__()
        self.setupUi(self)
        self.init_buttons()

    def show_dialog(self):
        self.show()

    def accept(self):
        self.close()

    def decline(self):
        self.close()

    def init_buttons(self):
        self.settings_conformation_buttons.accepted.connect(self.accept)
        self.settings_conformation_buttons.rejected.connect(self.decline)