from PyQt5 import QtWidgets


# Creates a Frame widget
class CreateFrame(QtWidgets.QFrame):
    def __init__(self, Window, Name,
                 Shape=QtWidgets.QFrame.NoFrame, Shadow=QtWidgets.QFrame.Plain, LineWidth=0, MidLineWidth=0,
                 MinimumSize=None, MaximumSize=None, FixedSize=None,
                 GeometryRect=None, layout=None):
        super().__init__(Window)

        self.setFrameShape(Shape)
        self.setFrameShadow(Shadow)
        self.setLineWidth(LineWidth)
        self.setMidLineWidth(MidLineWidth)
        self.setObjectName(Name)

        if MaximumSize is not None:
            self.setMaximumSize(MaximumSize)
        if MinimumSize is not None:
            self.setMinimumSize(MinimumSize)
        if FixedSize is not None:
            self.setFixedSize(FixedSize)
        if GeometryRect is not None:
            self.setGeometry(GeometryRect)
        if layout is not None:
            layout.addWidget(self)
