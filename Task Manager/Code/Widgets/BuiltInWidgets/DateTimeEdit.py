from PyQt5 import QtWidgets, QtCore
#from Code.Widgets.DataTime.CalendarWidget import CalendarWidget

# Creates a DateTimeEdit widget
class CreateDateTimeEdit(QtWidgets.QDateTimeEdit):
    def __init__(self, Window, GeometryRect, DueToDate, DueToTime, Name, DisplayFormat):
        super().__init__(Window)

        self.setGeometry(GeometryRect)
        self.setFrame(True)
        self.setProperty('showGroupSeparator', False)
        self.setDate(QtCore.QDate(int(DueToDate[:4]), int(DueToDate[5:7]), int(DueToDate[8:])))
        self.setTime(QtCore.QTime(int(DueToTime[0:2]), int(DueToTime[3:5])))
        self.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(9999, 12, 31), QtCore.QTime(23, 59, 59)))
        self.setCalendarPopup(True)
        #cal = CalendarWidget(None)
        #self.setCalendarWidget(cal)
        self.setObjectName(Name)
        self.setDisplayFormat(DisplayFormat)
        #self.setCalendarPopup(False)
        #self.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        #self.mousePressEvent = self.OpenCalander
        #self.setMouseTracking(True)
        #self.mouseMoveEvent = self.OpenCalander

    #def OpenCalander(self, e):
        #CalendarWidget(None)

