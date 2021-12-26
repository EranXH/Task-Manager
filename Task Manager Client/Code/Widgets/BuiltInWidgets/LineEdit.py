from PyQt5 import QtWidgets
from .Functions import GetFont


# Creates a LineEdit widget
class CreateLineEdit(QtWidgets.QLineEdit):
    def __init__(self, Window, Name, Text, FontSize,
                 MaxLength=None, Hide=False, GeometryRect=None, Layout=None):
        super().__init__(Window)

        self.setText(Text)
        self.setObjectName(Name)
        self.setFont(GetFont(FontSize))

        if MaxLength is not None:
            self.setMaxLength(MaxLength)
        if Hide:
            self.hide()
        if GeometryRect is not None:
            self.setGeometry(GeometryRect)
        if Layout is not None:
            Layout.addWidget(self)
