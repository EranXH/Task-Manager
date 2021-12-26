from PyQt5 import QtWidgets, QtCore, QtGui
from Code.Widgets.BuiltInWidgets import *
from Code.Widgets.AnimatedWidget.PlusXButton import PlusXButton


# A frame representing of the Start and End Date widget
class DateFrame(CreateFrame):
    def __init__(self, paren_widget, text, calendar_list_widget):
        CreateFrame.__init__(self, None, "DateFrame", Shape=QtWidgets.QFrame.Box, LineWidth=2,
                             layout=paren_widget,
                             MinimumSize=QtCore.QSize(80, 40))
        # MaximumSize=QtCore.QSize(270, 40))
        self.setStyleSheet("QFrame#DateFrame {border-radius: 12px; border: 2px solid; padding-right: 5px;}")

        self._layout = CreateHorizontalLayout(self, 0, "TimeFrameLayout")

        self.CalendarListWidget = calendar_list_widget

        # self.PlusButton = CreateButton(None, "", 0, "PlusButton", Layout=self._layout, MaxSize=(25, 25),
        # the Icon link is not modular !!!!!
        # Icon="C:/My Program/Python Work/Task Manager/Files/PNG/AddTimeButton.png")
        # self.PlusButton.setEnabled(False)

        null_objetc = CreateLayoutWidget(None, 'null_objetc')
        null_objetc.setFixedSize(QtCore.QSize(5, 5))
        self._layout.addWidget(null_objetc)

        self.label = CreateLabel(None, 10, text, "DateLabel", Layout=self._layout)
        self.DateFrameName = text[:-5]

        self.plus_x_button = PlusXButton(None, size=25)  # , connected_func=self.ButtonClick)
        self.plus_x_button.mousePressEvent = self.PlusXButtonEvent
        self._layout.addWidget(self.plus_x_button)

        self.label.mousePressEvent = self.ChangeFocusOnClickEvent
        self.mousePressEvent = self.ChangeFocusOnClickEvent

    # the event handler for pressing the PlusX button
    def PlusXButtonEvent(self, e):
        self.ChangeFocusOnClickEvent(None)

        if not self.plus_x_button.state:
            self.label.setText(f"{self.DateFrameName} Date")
            DatetimeObject = self.CalendarListWidget.GetDatetimeObjectValue(self.DateFrameName)

            if self.CalendarListWidget.deSelectCellsInfo is not None:
                if DatetimeObject == self.CalendarListWidget.deSelectCellsInfo[1]:
                    keep_start, keep_due = False, True
                else:
                    keep_start, keep_due = True, False

                self.CalendarListWidget.deSelectCells(self.CalendarListWidget.deSelectCellsInfo[0],
                                                       self.CalendarListWidget.deSelectCellsInfo[1],
                                                       self.CalendarListWidget.deSelectCellsInfo[2],
                                                       keep_start=keep_start, keep_due=keep_due)

            else:
                self.CalendarListWidget.SetStartAndDueCells(DatetimeObject, QtGui.QColor(255, 255, 255, 255))

            self.plus_x_button.ActiveAnimation()
            self.CalendarListWidget.SetDatetimeObjectValue(self.DateFrameName, None)

    # change the focus ("selection mode")
    def ChangeFocusOnClickEvent(self, e):
        self.CalendarListWidget.DaysSelectionMode.value = self.DateFrameName
