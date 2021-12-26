from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, Qt, QtCore, QtGui
from Code.Widgets.BuiltInWidgets import *
from Code.Widgets.DataTime.CalendarList import CalendarList
from Code.Widgets.DataTime.TimeFrame import TimeFrame
from Code.Widgets.DataTime.ShortCutButtons import ShortCutButtons
import sys

import pandas as pd
from datetime import datetime

#app = QApplication(sys.argv)


# the costum created Calendar widget
# the widget is Widget based - working on changing it to QCalendarWidget based
class CalendarWidget(QtWidgets.QCalendarWidget):    # CreateLayoutWidget
    def __init__(self, parent_widget, top=200, left=500):
        #CreateLayoutWidget.__init__(self, parent_widget, "CalendarWidget")
        super().__init__(None)
        width = 292
        height = 500
        #self.setStyleSheet("QWidget{background-color: white ;border: 0px;}")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(left, top, width, height)
        self.setFixedSize(width, height)
        self.show()

        # print(self.findChild(QtWidgets.QTableView))
        #self.findChild(QtWidgets.QVBoxLayout).deleteLater()
        #for widget in self.children():
            #print(widget)
            #widget.deleteLater()

        #self.setMinimumDate(Qt.QDate(2021, 11, 30))
        #self.setMaximumDate(Qt.QDate(2021, 11, 30))
        #self.setSelectionMode(Qt.QCalendarWidget.NoSelection)
        #self.updateCells = None
        #self.updateCell = None
        #self.setHorizontalHeaderFormat(Qt.QCalendarWidget.NoHorizontalHeader)
        #self.setVerticalHeaderFormat(Qt.QCalendarWidget.NoVerticalHeader)
        #self.setNavigationBarVisible(False)

        print("time1", self.children())
        #layout = CreateVerticalLayout(self, 3, "CentralLayout")
        #layout.setAlignment(QtCore.Qt.AlignHCenter)
        #self.setLayout(layout)

        # adding the raw of the Date Widgets
        self.DatesLayoutWidget = CreateLayoutWidget(None, 'DatesLayoutWidget')
        self.DatesLayout = CreateHorizontalLayout(self.DatesLayoutWidget, 5, "DatesLayout")
        self.layout().addWidget(self.DatesLayoutWidget)

        self.ShortCutButtons = ShortCutButtons(self.layout())

        # adding the raw of the days names
        self.DaysNamesLayoutWidget = CreateLayoutWidget(None, 'DaysNamesLayoutWidget')
        self.DaysNamesLayout = CreateHorizontalLayout(self.DaysNamesLayoutWidget, 0, "DaysNamesLayout")
        DaysLabelsObjectsList = []
        for text in ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']:
            label = CreateLabel(None, 9, text, f'{text} label', Layout=self.DaysNamesLayout)
            label.setAlignment(Qt.Qt.AlignCenter)
            DaysLabelsObjectsList.append(label)
        # adding an empty QWidget in the end - that way all the days names are alined
        null_objetc = CreateLayoutWidget(None, 'null_objetc')
        null_objetc.setFixedSize(QtCore.QSize(10, 10))
        self.DaysNamesLayout.addWidget(null_objetc)
        self.layout().addWidget(self.DaysNamesLayoutWidget)

        # adding the raw of the Calendar List Widget
        self.CalendarListWidget = CalendarList(self)

        # adding the raw of the Time Frame Widget
        #self.TimeFrameLayoutWidget = CreateLayoutWidget(None, 'TimeFrameLayoutWidget')
        #self.TimeFrameLayout = CreateHorizontalLayout(self.TimeFrameLayoutWidget, 0, "TimeFrameLayout")
        #self.TimeFrameLayoutWidget.setFixedSize(self.layout().sizeHint().width(), 50)    # (282, 50)
        #width = self.layout().sizeHint().width()
        self.TimeFrameWidget = TimeFrame(self)
        #self.layout().addWidget(self.TimeFrameLayoutWidget)

        # creating a Cancel or Done widgets
        self.CancelOrDoneLayoutWidget = CreateLayoutWidget(None, 'CancelOrDoneLayoutWidget')
        self.CancelOrDoneLayout = CreateHorizontalLayout(self.CancelOrDoneLayoutWidget, 0, "CancelOrDoneLayout")
        self.CancelOrDoneWidget = CreateDialogButtonBox(None, QtCore.Qt.RightToLeft, "CancelOrDone", 'Cancel', 'Done',
                                                        layout=self.CancelOrDoneLayout)
        self.layout().addWidget(self.CancelOrDoneLayoutWidget)

        print("time2", self.children())

    def GetValues(self):
        print("GetValuess", self.CalendarListWidget.StartDatetimeObject)


#CalendarWidget(None)

# Start the event loop.
#app.exec()
