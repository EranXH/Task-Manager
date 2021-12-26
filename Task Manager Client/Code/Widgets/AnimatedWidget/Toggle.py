from PyQt5.QtCore import (Qt, QSize, QPoint, QPointF, QRectF, QEasingCurve, QPropertyAnimation,
                          QSequentialAnimationGroup, pyqtSlot, pyqtProperty)
from PyQt5.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter
from PyQt5.QtWidgets import QCheckBox
from PyQt5 import QtCore


# a toggle widget object - based on QCheckBox widget
class Toggle(QCheckBox):

    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)

    # on creating a new widget - setting-up
    def __init__(self, window=None, bar_color=Qt.gray, checked_color="#00B0FF", handle_color=Qt.white,
                 pulse_unchecked_color="#44999999", pulse_checked_color="#4400B0EE", animation_duration=200,
                 start_pos=False, pulse_duration=350, pulse_start_value=10, pulse_end_value=20,
                 toggle_pos=(0, 0), toggle_size=(80, 60)):
        super().__init__(window)
        self.show()

        # Save our properties on the object via self, so we can access them later
        # in the paintEvent.
        self._bar_brush = QBrush(bar_color)
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())

        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color))

        self._pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))
        self._pulse_checked_animation = QBrush(QColor(pulse_checked_color))

        # Setup the rest of the widget.
        self.PosX = toggle_pos[0]
        self.PosY = toggle_pos[1]

        self.SizeX = toggle_size[0]
        self.SizeY = toggle_size[1]

        self.Length = self.PosX + self.SizeX
        self.Hight = self.PosY + self.SizeY

        self.setContentsMargins(self.PosX, self.PosY, self.Length, self.Hight)# self.PosX+self.SizeX, self.PosY+self.SizeY)

        self._handle_position = 0
        self._pulse_radius = 0

        # set up the animation attributes
        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(animation_duration)  # time in ms

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(pulse_duration)  # time in ms
        self.pulse_anim.setStartValue(pulse_start_value)
        self.pulse_anim.setEndValue(pulse_end_value)

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        self.animations_group.addAnimation(self.pulse_anim)

        self.setChecked(start_pos)
        self.setup_animation(start_pos)

        self.stateChanged.connect(self.setup_animation)

        self.setFixedSize(self.sizeHint())

        #if window is not None:
            #window.layout().addWidget(self)

    def sizeHint(self):
        return QSize(self.Length, self.Hight)

    # setting the built-in function to the currect hitbox
    def hitButton(self, pos: QPoint):
        if self.PosX <= pos.x() <= self.Length and \
                self.PosY + 10 <= pos.y() <= self.Hight - 12:
            return True
        else:
            return False

    # seting up a slot to connect to from "statusChange"
    @pyqtSlot(int)
    def setup_animation(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    # the built in ""paintEvent" - edited to fit the modified widget needs
    def paintEvent(self, e: QPaintEvent):
        contRect = QtCore.QRect(self.PosX, self.PosY, self.SizeX, self.SizeY)
        handleRadius = round(0.24 * contRect.height())
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(0, 0, contRect.width() - handleRadius, 0.40 * contRect.height())
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

        # the handle will move along this line
        trailLength = contRect.width() - 2 * handleRadius

        xPos = contRect.x() + handleRadius + trailLength * self._handle_position
        if self.pulse_anim.state() == QPropertyAnimation.Running:
            p.setBrush(self._pulse_checked_animation if self.isChecked()
                       else self._pulse_unchecked_animation)
            p.drawEllipse(QPointF(xPos, barRect.center().y()), self._pulse_radius, self._pulse_radius)

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)

        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(QPointF(xPos, barRect.center().y()), handleRadius, handleRadius)

        p.end()

    # creating a pyqt property for the animation
    @pyqtProperty(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        """change the property
        we need to trigger QWidget.update() method, either by:
            1- calling it here [ what we doing ].
            2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        self._handle_position = pos
        self.update()

    # creating a pyqt property for the animation
    @pyqtProperty(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        """change the property
        we need to trigger QWidget.update() method, either by:
            1- calling it here [ what we doing ].
            2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        self._pulse_radius = pos
        self.update()
