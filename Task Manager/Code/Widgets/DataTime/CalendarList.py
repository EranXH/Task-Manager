from Code.GlobalFunctions import ObjectHoldingTheValue
from Code.Widgets.BuiltInWidgets import *
from Code.Widgets.DataTime.ListMonthItem import ListMonthItem
from Code.Widgets.DataTime.DateFrame import DateFrame
from Code.Widgets.DataTime.ExpandingScrollBar import ExpandingScrollBar

from PyQt5 import QtWidgets, QtCore, QtGui
import pandas as pd
from datetime import datetime, timedelta

# the calander dates list widget
class CalendarList(CreateList):
    def __init__(self, calendar_widget):
        self.CalendarWidget = calendar_widget

        self.StartDateWidget = DateFrame(self.CalendarWidget.DatesLayout, "Start Date", self)
        self.DueDateWidget = DateFrame(self.CalendarWidget.DatesLayout, "Due Date", self)

        # setup the list widget
        CreateList.__init__(self, None, 12, "List",
                            AcceptDrops=False, DropIndicatorShown=False, DragEnabled=False,
                            HScrollBar=QtCore.Qt.ScrollBarAlwaysOff,
                            DragDropMode=False, FrameShape=QtWidgets.QFrame.NoFrame)

        self.setFixedSize(self.CalendarWidget.width(), 350)
        self.setVerticalScrollBar(ExpandingScrollBar())
        self.setStyleSheet('QListWidget::item {background: rgb(255, 255, 255);}')
        self.verticalScrollBar().setSingleStep(15)      # setting the pixel diffrece on each scroll step

        self.CalendarWidget.layout().addWidget(self)

        self.StartDatetimeObject = None
        self.DueDatetimeObject = None

        self.DaysSelectionMode = ObjectHoldingTheValue()
        self.DaysSelectionMode.value = None
        self.DaysSelectionMode.register_callback(self.SetDateFramesColor)
        self.DaysSelectionMode.value = "Start"

        self.TodayDatetimeObject = datetime.today()
        self.TodayTuple = self.TodayDatetimeObject.timetuple()[0:3]

        start = datetime(self.TodayTuple[0], self.TodayTuple[1], 1)
        end = datetime(self.TodayTuple[0]+1, self.TodayTuple[1], 1)

        self.datetimeObjectList = pd.date_range(start, end, freq='MS').tolist()

        self.DateList = [date.timetuple()[0:2] for date in self.datetimeObjectList]

        self.Month = {"01": "January", "02": "February", "03": "March", "04": "April",
                      "05": "May", "06": "June", "07": "July", "08": "August",
                      "09": "September", "10": "October", "11": "November", "12": "December"}

        self.TablesList = {}
        last_entered_month = None

        # create month tables based ao a given range
        for year_month in self.DateList:
            Table = ListMonthItem(self, year_month)
            self.TablesList[year_month] = Table

        # mark the current day date
        table = self.TablesList[self.TodayTuple[0:2]].Table
        (day_index, week_index) = table.day_to_week_day_indexs[self.TodayTuple[2]]
        self.TodayDayWidget = table._layout.itemAtPosition(week_index, day_index).widget()
        self.TodayDayWidget.BackgroungColor = QtGui.QColor(125, 106, 224, 150)
        self.TodayDayWidget.update()

        self.deSelectCellsInfo = None

    # a function that should actiate when the mouse is above a table item
    def Under(self, e):
        pass

    # set the DateFrame widget item (a table item widget) style-sheet - set the start and end color gui
    def SetDateFramesColor(self, old_value, new_value):
        if new_value == "Start":
            self.StartDateWidget.setStyleSheet(
                "QFrame#DateFrame {border-radius: 12px; border: 2px solid blue; padding-right: 5px;}")
            self.DueDateWidget.setStyleSheet(
                "QFrame#DateFrame {border-radius: 12px; border: 2px solid black; padding-right: 5px;}")
        elif new_value == "Due":
            self.StartDateWidget.setStyleSheet(
                "QFrame#DateFrame {border-radius: 12px; border: 2px solid black; padding-right: 5px;}")
            self.DueDateWidget.setStyleSheet(
                "QFrame#DateFrame {border-radius: 12px; border: 2px solid blue; padding-right: 5px;}")

    # returns the "asked" (by entering the "datetime_object_name" -> "Start" or "Due") Date widget values
    def GetDatetimeObjectValue(self, datetime_object_name):
        if datetime_object_name == "Start":
            return self.StartDatetimeObject
        elif datetime_object_name == "Due":
            return self.DueDatetimeObject

    # set "Start" or "Due" object attrs
    def SetDatetimeObjectValue(self, datetime_object_name, value):
        if datetime_object_name == "Start":
            self.StartDatetimeObject = value
        elif datetime_object_name == "Due":
            self.DueDatetimeObject = value

    # the function for handling a press on a cell (date widget in the month table)
    def CellPressedEvent(self, widget, e):
        date = widget.Date
        date_datetime_object = datetime(date[0], date[1], date[2])

        # if a chosen date is after the already chosen Due date, it whould change the selection type to be Due
        if self.DueDatetimeObject is not None and date_datetime_object > self.DueDatetimeObject:
            self.DaysSelectionMode.value = 'Due'
        # if a chosen date is befor the already chosen Start date, it whould change the selection type to be Start
        if self.StartDatetimeObject is not None and date_datetime_object < self.StartDatetimeObject:
            self.DaysSelectionMode.value = 'Start'

        # if cell was selected and the current selection mode is "Due"
        if self.DaysSelectionMode.value == 'Due':
            if self.DueDatetimeObject is not None:
                self.SetStartAndDueCells(self.DueDatetimeObject, QtGui.QColor(255, 255, 255, 255))
            else:
                self.DueDateWidget.plus_x_button.ActiveAnimation()

            self.DueDatetimeObject = date_datetime_object
            self.DueDateWidget.label.setText(f"{date[2]} {date_datetime_object.strftime('%b')}")
            self.SetStartAndDueCells(self.DueDatetimeObject, QtGui.QColor(125, 106, 224, 255))

            if self.deSelectCellsInfo is not None:
                self.deSelectCells(self.deSelectCellsInfo[0], self.deSelectCellsInfo[1], self.deSelectCellsInfo[2])
            if self.StartDatetimeObject is not None:
                # add the year number to the date label when the start and the due year are different
                if self.StartDatetimeObject.year != date_datetime_object.year:
                    self.DueDateWidget.label.setText(
                        f"{self.DueDatetimeObject.day} {self.DueDatetimeObject.strftime('%b')} {self.DueDatetimeObject.year}")
                    self.StartDateWidget.label.setText(
                        f"{self.StartDatetimeObject.day} {self.StartDatetimeObject.strftime('%b')} {self.StartDatetimeObject.year}")

                # makes sure that if the years are the same no year number is being shon
                else:
                    self.StartDateWidget.label.setText(
                                            f"{self.StartDatetimeObject.day} {self.StartDatetimeObject.strftime('%b')}")

                self.CalendarWidget.GetValues()
                print('did print worked2?')
                print(self.StartDatetimeObject.timetuple()[0:3])
                self.SelectCells()

            # Only if StartDatetimeObject is None then the next thime a date is being selected it would be the start date
            else:
                self.DaysSelectionMode.value = 'Start'

        # if cell was selected and the current selection mode is "Start"
        elif self.DaysSelectionMode.value == 'Start':
            if self.StartDatetimeObject is not None:
                self.SetStartAndDueCells(self.StartDatetimeObject, QtGui.QColor(255, 255, 255, 255))
            else:
                self.StartDateWidget.plus_x_button.ActiveAnimation()

            self.StartDatetimeObject = date_datetime_object
            self.StartDateWidget.label.setText(f"{date[2]} {date_datetime_object.strftime('%b')}")
            self.SetStartAndDueCells(self.StartDatetimeObject, QtGui.QColor(125, 106, 224, 255))

            if self.deSelectCellsInfo is not None:
                self.deSelectCells(self.deSelectCellsInfo[0], self.deSelectCellsInfo[1], self.deSelectCellsInfo[2])
            if self.DueDatetimeObject is not None:
                # add the year number to the date label when the start and the due year are different
                if self.DueDatetimeObject.year != date_datetime_object.year:
                    self.DueDateWidget.label.setText(
                        f"{self.DueDatetimeObject.day} {self.DueDatetimeObject.strftime('%b')} {self.DueDatetimeObject.year}")
                    self.StartDateWidget.label.setText(
                        f"{self.StartDatetimeObject.day} {self.StartDatetimeObject.strftime('%b')} {self.StartDatetimeObject.year}")
                # makes sure that if the years are the same no year number is being shon
                else:
                    self.DueDateWidget.label.setText(
                                                f"{self.DueDatetimeObject.day} {self.DueDatetimeObject.strftime('%b')}")
                self.SelectCells()

            self.DaysSelectionMode.value = 'Due'

    # returns a list of tuples that are like this - ((), ()) - the start date and the due date tuples inside a tuple
    @staticmethod
    def GetMonthRange(start_date: datetime, due_date: datetime):
        last_month = start_date.month
        month_start_date = start_date.timetuple()[0:3]
        StartAndDueList = []
        for n in range(int((due_date - start_date).days)):
            date = start_date + timedelta(n)
            if date.month != last_month:
                # arranging values befor appending to list
                last_day_of_month = date - timedelta(1)
                month_due_date = last_day_of_month.timetuple()[:3]
                StartAndDueList.append((month_start_date, month_due_date))

                # updating valuse for next month
                last_month = date.month
                month_start_date = date.timetuple()[0:3]

        if due_date.day == 1 and start_date.timetuple()[0:3] != due_date.timetuple()[:3]:
            StartAndDueList.append((month_start_date, date.timetuple()[:3]))
            StartAndDueList.append((due_date.timetuple()[:3], due_date.timetuple()[:3]))
        else:
            StartAndDueList.append((month_start_date, due_date.timetuple()[:3]))

        return StartAndDueList

    # Color a cell given a datetime_object and a color - used for the Start and Due cells
    def SetStartAndDueCells(self, datetime_object: datetime, q_color):
        date = datetime_object.timetuple()[:3]
        table = self.TablesList[date[0:2]].Table
        (day_index, week_index) = table.day_to_week_day_indexs[date[2]]
        day_widget = table._layout.itemAtPosition(week_index, day_index).widget()
        day_widget.BackgroungColor = q_color
        day_widget.update()

        self.CalendarWidget.GetValues()
        print('did print worked2?')
        print(self.StartDatetimeObject.timetuple()[0:3])

    # a function that handles a newly aproved (from "CellPressedEvent") selected cell
    # mark the cells based of the spasification shown in the "TableDayWidgetItem" file at the __init__ function end
    def SelectCells(self):
        StartAndDueList = self.GetMonthRange(self.StartDatetimeObject, self.DueDatetimeObject)
        self.deSelectCellsInfo = (StartAndDueList, self.StartDatetimeObject, self.DueDatetimeObject)

        for (month_start_date, month_due_date) in StartAndDueList:
            month_table = self.TablesList[month_start_date[0:2]].Table
            month_table.SelectCells(start_day=month_start_date[2], end_day=month_due_date[2])

        if self.StartDatetimeObject < self.TodayDatetimeObject < self.DueDatetimeObject:
            self.TodayDayWidget.BackgroungColor = QtGui.QColor(125, 106, 224, 160)
            self.TodayDayWidget.update()

        self.SetStartAndDueCells(self.StartDatetimeObject, QtGui.QColor(125, 106, 224, 255))
        self.SetStartAndDueCells(self.DueDatetimeObject, QtGui.QColor(125, 106, 224, 255))

    # deselect celles based on a range
    def deSelectCells(self, start_and_due_list, start_date, due_date, keep_start=False, keep_due=False):
        for (month_start_date, month_due_date) in start_and_due_list:
            month_table = self.TablesList[month_start_date[0:2]].Table
            month_table.deSelectCells(start_day=month_start_date[2], end_day=month_due_date[2])

        if start_date < self.TodayDatetimeObject < due_date:
            self.TodayDayWidget.BackgroungColor = QtGui.QColor(125, 106, 224, 125)
            self.TodayDayWidget.update()

        if keep_start:
            self.SetStartAndDueCells(start_date, QtGui.QColor(125, 106, 224, 255))
        if keep_due:
            self.SetStartAndDueCells(due_date, QtGui.QColor(125, 106, 224, 255))

        self.deSelectCellsInfo = None
