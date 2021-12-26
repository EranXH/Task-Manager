from PyQt5 import QtWidgets
from .Functions import GetFont


# Create a Label widget within the Frame
class CreateLabel(QtWidgets.QLabel):
    def __init__(self, Window, FontSize, Text, Name,
                 WordWrap=False, GeometryRect=None, FrameShape=None, MaximumSize=None, Layout=None, Show=True):
        super().__init__(Window)

        self.setText(Text)
        self.setFont(GetFont(FontSize))
        self.setObjectName(Name)
        self.setMouseTracking(True)
        self.setWordWrap(WordWrap)

        if GeometryRect is not None:
            self.setGeometry(GeometryRect)
        if FrameShape is not None:
            self.setFrameShape(FrameShape)
        if MaximumSize is not None:
            self.setMaximumSize(MaximumSize)
        if Layout is not None:
            Layout.addWidget(self)
        if Show:
            self.show()
