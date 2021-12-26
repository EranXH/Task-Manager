from PyQt5 import QtWidgets


# Creates a MessageBox widget
class CreatePopupMsg(QtWidgets.QMessageBox):
    def __init__(self, window_title, text, button_number=0, button_1=QtWidgets.QMessageBox.Ok, button_1_func=None,
                 button_2=QtWidgets.QMessageBox.Yes, button_2_func=None,
                 icon=QtWidgets.QMessageBox.Warning):
        super().__init__()

        if button_number > 2:
            raise ValueError("Value should be between 0-2")

        if button_number >= 1:
            self.addButton(button_1)
        if button_number == 2:
            self.addButton(button_2)

        self.setWindowTitle(window_title)
        self.setText(text)
        self.setIcon(icon)
        self.response = self.exec_()

        if self.response == button_1 and button_1_func is not None:
            button_1_func()

        if self.response == button_2 and button_2_func is not None:
            button_2_func()