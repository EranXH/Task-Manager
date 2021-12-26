from PyQt5 import QtWidgets, QtCore
from .Functions import GetFont


# Creates a scroll area object
class CreateScroll(QtWidgets.QScrollArea):
    def __init__(self, Window, GeometryRect, FontSize, Name,
                 Shape=None, Shadow=None, HorizontalScrollBar=None, VerticalScrollBar=None,
                 LayoutDirection=QtCore.Qt.RightToLeft):
        super().__init__(Window)

        self.setGeometry(GeometryRect)
        self.setFont(GetFont(FontSize))

        if Shape is not None:
            self.setFrameShape(Shape)
        if Shadow is not None:
            self.setFrameShadow(Shadow)
        if HorizontalScrollBar is not None:
            self.setHorizontalScrollBarPolicy(HorizontalScrollBar)
        if VerticalScrollBar is not None:
            self.setVerticalScrollBarPolicy(VerticalScrollBar)

        self.setLayoutDirection(LayoutDirection)
        self.setWidgetResizable(True)
        self.setObjectName(Name)
