from PyQt5 import QtWidgets, QtCore


# Create a Horizontal Layout widget
class CreateHorizontalLayout(QtWidgets.QHBoxLayout):
    def __init__(self, Window, Spacing, Name):
        super().__init__(Window)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(Spacing)
        self.setObjectName(Name)


# Create a Vertical Layout widget
class CreateVerticalLayout(QtWidgets.QVBoxLayout):
    def __init__(self, Window, Spacing, Name):
        super().__init__(Window)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(Spacing)
        self.setObjectName(Name)


# Create a Grid Layout widget
class CreateGridLayout(QtWidgets.QGridLayout):
    def __init__(self, layout_widget, spacing, name):
        super().__init__(layout_widget)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(spacing)
        self.setObjectName(name)


# Create a simple widget for Layout use
class CreateLayoutWidget(QtWidgets.QWidget):
    def __init__(self, Window, Name, GeometryRect=None, layout=None):
        super().__init__(Window)
        self.setObjectName(Name)

        if GeometryRect is not None:
            self.setGeometry(GeometryRect)
            self.setAcceptDrops(False)
            self.setLayoutDirection(QtCore.Qt.LeftToRight)

        if layout is not None:
            layout.addWidget(self)
