from PyQt5 import QtWidgets
from .Functions import GetFont


# Creates a TextEdit widget
class CreateTextEdit(QtWidgets.QTextEdit):
    def __init__(self, Window, GeometryRect, FontSize, Name,
                 VScrollBar=None, HScrollBar=None, Show=True):
        super().__init__(Window)

        self.setGeometry(GeometryRect)
        self.setFont(GetFont(FontSize))
        self.setObjectName(Name)
        self.setMouseTracking(True)
        self.setTabletTracking(True)

        if VScrollBar is not None:
            self.setVerticalScrollBarPolicy(VScrollBar)
        if HScrollBar is not None:
            self.setHorizontalScrollBarPolicy(HScrollBar)
        if Show:
            self.show()
