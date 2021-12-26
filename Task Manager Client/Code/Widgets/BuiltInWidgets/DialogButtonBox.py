from PyQt5 import QtWidgets


# Creates a DialogButtonBox widget
class CreateDialogButtonBox(QtWidgets.QDialogButtonBox):
    def __init__(self, Window, LayoutDirectiona, Name, cancel_text, save_text, layout=None, geometry_rect=None):
        super().__init__(Window)

        self.setLayoutDirection(LayoutDirectiona)
        self.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Save)
        self.setCenterButtons(True)
        self.setObjectName(Name)

        self.button(QtWidgets.QDialogButtonBox.Cancel).setText(cancel_text)
        self.button(QtWidgets.QDialogButtonBox.Save).setText(save_text)

        if layout is not None:
            layout.addWidget(self)
        if geometry_rect is not None:
            self.setGeometry(geometry_rect)
