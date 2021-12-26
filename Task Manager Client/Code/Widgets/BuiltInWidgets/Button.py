from PyQt5 import QtWidgets, QtCore, QtGui
from .Functions import GetFont


# Creates a Button widget
class CreateButton(QtWidgets.QPushButton):
    def __init__(self, Window, Text, FontSize, Name,
                 SetFlat=True, GeometryRect=None, Layout=None, MaxSize=None, Icon=None):
        super().__init__(Window)

        self.setText(Text)
        self.setFont(GetFont(FontSize))
        self.setObjectName(Name)
        self.setFlat(SetFlat)

        if GeometryRect is not None:
            self.setGeometry(GeometryRect)
        if Layout is not None:
            Layout.addWidget(self)
        if MaxSize is not None:
            self.setMaximumSize(QtCore.QSize(MaxSize[0], MaxSize[1]))
        if Icon is not None:
            self.setIcon(QtGui.QIcon(Icon))
