from PyQt5 import QtWidgets


# Creates a RadioButton widget
class CreateRadioButton(QtWidgets.QRadioButton):
    def __init__(self, Window, Layout, Name, Text, AutoExclusive):
        super().__init__(Window)
        self.setText(Text)
        self.setObjectName(Name)
        self.setAutoExclusive(AutoExclusive)
        Layout.addWidget(self)
