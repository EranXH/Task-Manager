from PyQt5 import QtWidgets


# Create a CheckBox widget
class CreateCheckBox(QtWidgets.QCheckBox):
    def __init__(self, Window, Name, State, GeometryRect, MinimumSize,
                 HasStateChangeEvent=None):
        super().__init__(Window)

        self.setObjectName(Name)
        self.setChecked(State)
        self.setGeometry(GeometryRect)
        self.setMaximumSize(MinimumSize)

        if HasStateChangeEvent is not None:
            self.stateChanged.connect(HasStateChangeEvent)
