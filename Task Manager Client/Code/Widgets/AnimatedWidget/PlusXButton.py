from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import math
from PyQt5.QtCore import QPropertyAnimation, QParallelAnimationGroup
from Code.Widgets.BuiltInWidgets import *


class Line(QtWidgets.QWidget):
    clickedValue = QtCore.pyqtSignal(int)

    # on creating the widget adding the needed propeties and fixing the size
    def __init__(self, angle, line_type, size, parent_widget, *args, **kwargs):
        super().__init__(parent_widget)

        self.given_size = size
        self.line_type = line_type

        self.setProperty("color", QtGui.QColor(125, 106, 224))
        self.setProperty("angle", angle)

        self.setFixedSize(parent_widget.frameSize())

    # bulit in "paintEvent" is called automatically on every change
    # changed the function to fit the line paint needs
    def paintEvent(self, e):
        painter = QtGui.QPainter(self)

        # because the animation changes a property and not the attribute, takes the updated value
        color = self.property("color")
        brush = QtGui.QBrush(color)
        pen = QtGui.QPen(brush, 3, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        keep_round_cup_buffer = pen.width()
        half_line_size = int(self.given_size / 2 - keep_round_cup_buffer)
        # because the animation changes a property and not the attribute, takes the updated value
        angle = self.property("angle")

        if self.line_type:
            buffer_x = int(half_line_size * math.sin(math.radians(angle)))
            buffer_y = int(half_line_size * math.cos(math.radians(angle)))
        else:
            buffer_y = int(-(half_line_size * math.sin(math.radians(angle))))
            buffer_x = int(half_line_size * math.cos(math.radians(angle)))

        center_dot_xy = keep_round_cup_buffer + half_line_size
        start_point = QtCore.QPoint(center_dot_xy - buffer_x, center_dot_xy + buffer_y)
        end_point = QtCore.QPoint(center_dot_xy + buffer_x, center_dot_xy - buffer_y)

        line_obj = QtCore.QLine(start_point, end_point)

        painter.drawLine(line_obj)


# the callable widget object for an X to + animation
class PlusXButton(QtWidgets.QWidget):
    def __init__(self, parent_widget, size=30, connected_func=None):
        super().__init__(None)

        self.ConnectedFunc = connected_func
        self.state = True

        self.setFixedSize(size, size)
        self._layout = CreateHorizontalLayout(self, 0, 'PlusXButtonLayout')
        self._layout_widget = CreateLayoutWidget(None, "PlusXButtonLayoutWidget")
        self._layout.addWidget(self._layout_widget)

        self.vertical_line = Line(0, 1, size, self._layout_widget)
        self.horizontal_line = Line(0, 0, size, self._layout_widget)

    # the animation between X and +
    def ActiveAnimation(self):
        if not self.state:
            angle_end_value = 0
            color_end_value = QtGui.QColor(125, 106, 224)
            self.state = True
        else:
            angle_end_value = 45
            color_end_value = QtGui.QColor(128, 130, 149)
            self.state = False

        # for each line changing the angle and changing the color
        self.vertical_line_angle_animation = QPropertyAnimation(self.vertical_line, b"angle")
        self.vertical_line_angle_animation.setEndValue(angle_end_value)
        self.vertical_line_angle_animation.setDuration(500)
        self.vertical_line_angle_animation.valueChanged.connect(self.vertical_line.update)

        self.vertical_line_color_animation = QPropertyAnimation(self.vertical_line, b"color")
        self.vertical_line_color_animation.setEndValue(color_end_value)
        self.vertical_line_color_animation.setDuration(500)
        self.vertical_line_color_animation.valueChanged.connect(self.vertical_line.update)

        self.horizontal_line_angle_animation = QPropertyAnimation(self.horizontal_line, b"angle")
        self.horizontal_line_angle_animation.setEndValue(angle_end_value)
        self.horizontal_line_angle_animation.setDuration(500)
        self.horizontal_line_angle_animation.valueChanged.connect(self.horizontal_line.update)

        self.horizontal_line_color_animation = QPropertyAnimation(self.horizontal_line, b"color")
        self.horizontal_line_color_animation.setEndValue(color_end_value)
        self.horizontal_line_color_animation.setDuration(500)
        self.horizontal_line_color_animation.valueChanged.connect(self.horizontal_line.update)

        # adding all the animations to on parallel animation
        self.animations = QParallelAnimationGroup()
        self.animations.addAnimation(self.vertical_line_angle_animation)
        self.animations.addAnimation(self.vertical_line_color_animation)
        self.animations.addAnimation(self.horizontal_line_angle_animation)
        self.animations.addAnimation(self.horizontal_line_color_animation)

        self.animations.start()

        #self.animations.finished.connect(self.ConnectedFunc)

    #def mousePressEvent(self, e):
        #self.ActiveAnimation()
