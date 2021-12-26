from PyQt5 import QtWidgets
from .Functions import GetFont


# Creates a List of Widgets widget
class CreateList(QtWidgets.QListWidget):
    def __init__(self, Window, FontSize, Name,
                 GeometryRect=None, AcceptDrops=True, DropIndicatorShown=True, DragEnabled=True,
                 LayoutDirection=None, HScrollBar=None, VScrollBar=None, VScrollMode=True, DragDropMode=True, FrameShape=None):
        super().__init__(Window)

        self.setFont(GetFont(FontSize))
        self.setObjectName(Name)
        self.setSpacing(1)

        if GeometryRect is not None:
            self.setGeometry(GeometryRect)
        if LayoutDirection is not None:
            self.setLayoutDirection(LayoutDirection)
        if HScrollBar is not None:
            self.setHorizontalScrollBarPolicy(HScrollBar)
        if VScrollBar is not None:
            self.setVerticalScrollBarPolicy(VScrollBar)
        if VScrollMode:
            self.setVerticalScrollMode(self.ScrollPerPixel)
        if DragDropMode:
            self.setDragDropMode(self.InternalMove)
        if FrameShape is not None:
            self.setFrameShape(FrameShape)

        self.setAcceptDrops(AcceptDrops)
        self.setDropIndicatorShown(DropIndicatorShown)
        self.setDragEnabled(DragEnabled)
