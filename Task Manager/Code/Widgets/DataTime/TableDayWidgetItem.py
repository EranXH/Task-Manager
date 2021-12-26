from PyQt5 import QtWidgets, Qt, QtCore, QtGui
from Code.Widgets.BuiltInWidgets import *
import copy


# the item widget for the month tabel - represent the day of the month
class TableDayWidgetItem(QtWidgets.QWidget):
    clickedValue = QtCore.pyqtSignal(int)

    def __init__(self, cell_size, date, week_index, day_index, *args, **kwargs):
        super().__init__(None)
        self.Date = date
        self.WeekIndex = week_index
        self.DayIndex = day_index
        self.CellSize = cell_size

        self.setObjectName("DayWidgetItem")
        self.setFixedSize(self.CellSize, self.CellSize)

        self.Label = CreateLabel(self, 10, str(self.Date[2]), "DayWidgetLabel", Show=False)
        self.Label.setFixedSize(self.CellSize, self.CellSize)
        self.Label.setAlignment(Qt.Qt.AlignCenter)

        self.CornersColor = QtGui.QColor(255, 255, 255, 255)
        self.BackgroungColor = QtGui.QColor(255, 255, 255, 255)

        #(125, 106, 224, 100) -> select color, today date when not in select range
        #(125, 106, 224, 150) -> today date when in select range
        #(125, 106, 224, 255) -> start and due colors
        #(255, 255, 255, 255) -> non selected cell color

        self.Corners = [True, True, True, True]     # [top-left, top-right, bottom-right, bottom-left]

    # rewrite the "paintEvent" to fit the widget needs
    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # color = self.property("color")
        painter.setPen(Qt.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(self.CornersColor, Qt.Qt.SolidPattern))

        left = 0
        top = 0
        radius = 12

        rect = QtCore.QRectF(left, top, self.CellSize, self.CellSize)
        path = QtGui.QPainterPath()
        path.setFillRule(Qt.Qt.WindingFill)

        squareSize = self.CellSize / 2

        # create the ability to be round in spacific corners

        # top left
        if self.Corners[0]:
            path.addRoundedRect(QtCore.QRectF(left, top, squareSize, squareSize), radius, radius)
            path.addRect(left, top, squareSize, squareSize)

        # top right
        if self.Corners[1]:
            path.addRoundedRect(QtCore.QRectF(left + squareSize, top, squareSize, squareSize), radius, radius)
            path.addRect(left + squareSize, top, squareSize, squareSize)

        # bottom left
        if self.Corners[2]:
            path.addRoundedRect(QtCore.QRectF(left, top + squareSize, squareSize, squareSize), radius, radius)
            path.addRect(left, top + squareSize, squareSize, squareSize)

        # bottom right
        if self.Corners[3]:
            path.addRoundedRect(QtCore.QRectF(left + squareSize, top + squareSize, squareSize, squareSize), radius,
                                radius)
            path.addRect(left + squareSize, top + squareSize, squareSize, squareSize)

        if True in self.Corners:
            painter.drawPath(path.simplified())

            painter.setBrush(QtGui.QBrush(Qt.Qt.white, Qt.Qt.SolidPattern))

            rect = QtCore.QRectF(left, top, self.CellSize, self.CellSize)
            painter.drawRoundedRect(rect, radius, radius)

        painter.setBrush(QtGui.QBrush(self.BackgroungColor, Qt.Qt.SolidPattern))

        rect = QtCore.QRectF(left, top, self.CellSize, self.CellSize)
        painter.drawRoundedRect(rect, radius, radius)
