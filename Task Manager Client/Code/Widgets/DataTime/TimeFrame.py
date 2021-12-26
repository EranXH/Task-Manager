from Code.Widgets.BuiltInWidgets import *
from PyQt5 import QtWidgets, QtCore
from Code.Widgets.AnimatedWidget.PlusXButton import PlusXButton
from Code.Widgets.DataTime.TimeSelectionWidget import TimeSelectionWidget


# the lowes frame in the layout of the calendar-widget
# a frame which represent the selected time - press to add time
class TimeFrame(CreateFrame):
    def __init__(self, parent_widget):
        width = parent_widget.width()
        CreateFrame.__init__(self, None, "TimeFrame", Shape=QtWidgets.QFrame.Box, LineWidth=2,
                             layout=parent_widget.layout(),
                             MinimumSize=QtCore.QSize(width, 40),
                             MaximumSize=QtCore.QSize(width, 40))
                             #MinimumSize=QtCore.QSize(width - 10, 40),
                             #MaximumSize=QtCore.QSize(width - 10, 40))
        self.setStyleSheet("QFrame#TimeFrame {border-radius: 12px; border: 2px solid; padding-right: 5px;}")
        parent_widget.layout().addWidget(self)

        self._layout = CreateHorizontalLayout(self, 0, "TimeFrameLayout")

        # the Icon link is not modular !!!!!
        self.PlusButton = CreateButton(None, "", 0, "PlusButton", Layout=self._layout, MaxSize=(25, 25),
                                       Icon="C:/My Program/Python Work/Task Manager/Files/PNG/AddTimeButton.png")
        self.PlusButton.setEnabled(False)

        self.label = CreateLabel(None, 10, "Set Time", "TimeLabel", Layout=self._layout)
        self.plus_x_button = PlusXButton(None, size=25, connected_func=self.Try)
        self._layout.addWidget(self.plus_x_button)

        #self.PlusButton.clicked.connect(self.Try)
        self.plus_x_button.mousePressEvent = self.Try
        self.label.mousePressEvent = self.Try
        self.mousePressEvent = self.Try



    def Try(self, e=None):
        self.label12 = TimeSelectionWidget() #CreateLabel(None, 15, "Set Time", "TimeLabel")
        self.label12.show()

        print('may')
        #l = CreateFrame(None, "TimeSelectionWidgetFrame",
                        #MinimumSize=QtCore.QSize(300, 200), MaximumSize=QtCore.QSize(300, 200))
        #l.show()
        #l.setStyleSheet("QFrame {border-radius: 12px; border: 2px solid; padding-right: 5px;}")