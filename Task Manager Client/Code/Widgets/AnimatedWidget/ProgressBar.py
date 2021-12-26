from functools import partial
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QPropertyAnimation
from Code.Widgets.BuiltInWidgets.Functions import GetFont
from Code.GlobalFunctions import ParsesToInteger, ISInteger


# Creates a modified progressBar widget
class ProgressBar(QtWidgets.QProgressBar):
    # calculate the progress in float presentage
    @staticmethod
    def CalculateProgress(ProgressList):
        total_checklist_checked_items = ProgressList[0]
        total_checklist_items = ProgressList[1]

        if total_checklist_items != 0:
            return round(float(total_checklist_checked_items / total_checklist_items) * 100, 2)
        else:
            return 0.0

    # setting progressBar on creation
    def __init__(self, Window, Value, Name,
                 GeometryRect=False,  MaxSizeX=16777215):
        super().__init__(Window)

        self.setMaximumSize(QtCore.QSize(150, MaxSizeX))
        self.setFont(GetFont(12))
        self.setProperty("value", 0)
        self.setFormat('%p%')
        self.setOrientation(QtCore.Qt.Horizontal)
        # ProgressBar.setInvertedAppearance(False)
        self.setObjectName(Name)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet("QProgressBar{border-radius: 5px; border-color: black;} "
                           "QProgressBar::chunk {border-radius :5px} "
                           "QProgressBar::chunk {background-color: rgb(0, 128, 0);}")

        if GeometryRect:
            self.setGeometry(GeometryRect)

        self.ProgressAnimation(ParsesToInteger(Value))

    # the animation function - between the exsisting value and the new given one
    def ProgressAnimation(self, NewValue):
        self.setFormat('%p%')
        self.setMaximum(100 * 100)

        self.Animation = QPropertyAnimation(self, b"value")
        self.Animation.setStartValue(self.value() * 100)
        self.Animation.setEndValue(NewValue * 100)
        self.Animation.setDuration(500)
        self.Animation.start()
        self.Animation.valueChanged.connect(self.AnimationValueChangedEvent)
        self.Animation.finished.connect(partial(self.AnimationFinishedEvent, NewValue))

    # try to set the format to float base - may be int base before
    def AnimationValueChangedEvent(self):
        try:
            self.setFormat("%.02f %%" % float(self.value() / 100.0))
        except RuntimeError:
            pass

    # on progress animation finish:
    #           set the max to 100 (sended end progress may try to pass that)
    #           check if the float number is equal to the int number - if true represent the int format
    def AnimationFinishedEvent(self, NewValue):
        self.setMaximum(100)
        self.setProperty("value", NewValue)

        if ISInteger(ParsesToInteger(NewValue)):
            self.setFormat('%p%')
        else:
            self.setFormat("%.02f %%" % ParsesToInteger(NewValue))
