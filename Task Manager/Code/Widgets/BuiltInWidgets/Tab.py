from PyQt5 import QtWidgets
from .Functions import GetFont


# Creates a Tab widget
class CreateTab(QtWidgets.QTabWidget):
    def __init__(self, Window, Name, Shape, Movable, GeometryRect=None, FontSize=12):
        super().__init__(Window)

        self.setUsesScrollButtons(False)
        self.setFont(GetFont(FontSize))
        self.setTabShape(Shape)
        self.setDocumentMode(True)
        self.setMovable(Movable)
        self.setObjectName(Name)

        if GeometryRect is not None:
            self.setGeometry(GeometryRect)
