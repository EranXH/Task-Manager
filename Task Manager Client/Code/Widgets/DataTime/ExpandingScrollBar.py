from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QPropertyAnimation, QParallelAnimationGroup


# customizing a QScrollBar widget to make it expand when mouse hover over it
class ExpandingScrollBar(QtWidgets.QScrollBar):
    def __init__(self, Window=None):
        super().__init__(Window)

        self.setStyleSheet("QScrollBar {width:10px;}")

        self.setProperty("animation_width", 10)
        self.animation_end_value = 10

    # set scrollBar width
    def OnAnimationChange(self):
        width = str(self.property("animation_width"))
        self.setStyleSheet("QScrollBar {width:"+width+"px;}")

    # activate the animations
    def Animation(self):
        self.scrollBar_animation = QPropertyAnimation(self, b"animation_width")
        self.scrollBar_animation.setEndValue(self.animation_end_value)
        self.scrollBar_animation.setDuration(350)
        self.scrollBar_animation.valueChanged.connect(self.OnAnimationChange)
        self.scrollBar_animation.start()

    # on mouse hovers leaves the widget
    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.animation_end_value = 10
        self.Animation()

    # on mouse hovers enters the widget
    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.animation_end_value = 25
        self.Animation()
