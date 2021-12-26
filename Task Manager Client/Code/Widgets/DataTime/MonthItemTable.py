from PyQt5 import QtCore, Qt, QtGui
from Code.Widgets.BuiltInWidgets import *
from Code.Widgets.DataTime.TableDayWidgetItem import TableDayWidgetItem
from functools import partial
import calendar
import datetime


# A modified widget which holds a table fill with items (numbers which represent dates in the month)
class MonthItemTable(CreateLayoutWidget):
    def __init__(self, parent_widget, year_month):
        self.parent_widget = parent_widget
        self.NumberOfWeeks, self.CellSize, self.YearMonth = parent_widget.NumberOfWeeks, parent_widget.CellSize, year_month

        geometry_rect = QtCore.QRect(0, 25, 2 + self.CellSize * 7, self.NumberOfWeeks * self.CellSize)

        CreateLayoutWidget.__init__(self, self.parent_widget.Frame, "TableLayoutWidget")

        self.setGeometry(geometry_rect)

        self._layout = CreateGridLayout(self, 0, "TableLayout")

        num_days = calendar.monthrange(self.YearMonth[0], self.YearMonth[1])[1]
        week_index = 0
        self.day_to_week_day_indexs = {}

        # get to the calendar_list_object from ListMonthItem
        calendar_list_object = self.parent_widget.listWidget()

        # add all the day widgets (the item widgets which represnt the number of the day in the week)
        for day_number in range(1, num_days+1):     # adding 1 because the range ends at one value befor the end value
            # changing the week order from starting in monday to starting in sunday
            day_index = datetime.date(year=self.YearMonth[0], month=self.YearMonth[1], day=day_number).weekday()+1
            if day_index == 7:
                day_index = 0

            date = (self.YearMonth[0], self.YearMonth[1], day_number)
            day_widget = TableDayWidgetItem(self.CellSize, date, week_index, day_index)

            # connect the mousePressEvent of the day_widget to the function in calendar_list_object
            # and sending the widget object
            day_widget.mousePressEvent = partial(calendar_list_object.CellPressedEvent, day_widget)
            self._layout.addWidget(day_widget, week_index, day_index)

            self.day_to_week_day_indexs[day_number] = (day_index, week_index)

            if day_index == 6:
                week_index += 1

    # set up the color overlay of selected dates
    def CreateCurvedWidget(self, start_day, end_day, start_day_index, start_week_index, end_day_index, end_week_index):
        if start_day_index != 0 and end_day - start_day >= 7:
            if start_day != 1:
                day_widget = self._layout.itemAtPosition(start_week_index, start_day_index - 1).widget()

            else:
                day_widget = TableDayWidgetItem(self.CellSize, '   ', 100, 100)
                self._layout.addWidget(day_widget, start_week_index, start_day_index - 1)

            day_widget.Corners = [False, False, False, True]
            day_widget.CornersColor = QtGui.QColor(125, 106, 224, 50)
            day_widget.update()

        if end_day_index != 6 and end_day - start_day >= 7:
            if end_day != len(self.day_to_week_day_indexs):
                day_widget = self._layout.itemAtPosition(end_week_index, end_day_index + 1).widget()

            else:
                day_widget = TableDayWidgetItem(self.CellSize, '   ', 100, 100)
                self._layout.addWidget(day_widget, end_week_index, end_day_index + 1)

            day_widget.Corners = [True, False, False, False]
            day_widget.CornersColor = QtGui.QColor(125, 106, 224, 50)
            day_widget.update()

    # remove the color overlay of a given range
    def RemoveCurveWidget(self, start_day_index, start_week_index, end_day_index, end_week_index):
        widgets = []
        for (week_index, day_index) in [(start_week_index, start_day_index - 1), (end_week_index, end_day_index + 1)]:
            try:
                widgets.append(self._layout.itemAtPosition(week_index, day_index).widget())
            except AttributeError:
                pass

        for day_widget in widgets:
            if day_widget.WeekIndex == 100:
                self._layout.removeWidget(day_widget)
                day_widget.deleteLater()
            else:
                day_widget.CornersColor = Qt.Qt.white
                day_widget.update()

    # TODO: create remove create romove - the remove does not work
    # the selection function of each table - with a given range color all the items in the range
    def SelectCells(self, start_day=1, end_day=8):
        if end_day > len(self.day_to_week_day_indexs):
            end_day = len(self.day_to_week_day_indexs)

        (start_day_index, start_week_index) = self.day_to_week_day_indexs[start_day]
        (end_day_index, end_week_index) = self.day_to_week_day_indexs[end_day]

        self.CreateCurvedWidget(start_day, end_day, start_day_index, start_week_index, end_day_index, end_week_index)
        #self.RemoveCurveWidget(start_day_index, start_week_index, end_day_index, end_week_index)
        #self.CreateCurvedWidget(start_day, end_day, start_day_index, start_week_index, end_day_index, end_week_index)

        for day in range(start_day, end_day+1):
            (day_index, week_index) = self.day_to_week_day_indexs[day]
            day_widget = self._layout.itemAtPosition(week_index, day_index).widget()
            Corners = [True, True, True, True]     # [top-left, top-right, bottom-right, bottom-left]

            # top-left
            if (day == start_day) or (day_index == 0 and start_day_index > 0 and week_index == start_week_index + 1):
                Corners[0] = False

            # top-right
            if (day_index == 6 and week_index == start_week_index) or (day == end_day and end_day - start_day < 7):
                Corners[1] = False

            # bottom-left
            if (day == start_day and end_day - start_day < 7) or (day_index == 0 and week_index == end_week_index):
                Corners[2] = False

            # bottom-right
            if (day == end_day) or (day_index == 6 and end_day - 7 < day):
                Corners[3] = False

            day_widget.Corners = Corners
            day_widget.CornersColor = QtGui.QColor(125, 106, 224, 50)
            day_widget.BackgroungColor = QtGui.QColor(125, 106, 224, 50)

            day_widget.update()

    # the deselection function of each table - with a given range clear the items in the range
    def deSelectCells(self, start_day=1, end_day=8):
        if end_day > len(self.day_to_week_day_indexs):
            end_day = len(self.day_to_week_day_indexs)

        (start_day_index, start_week_index) = self.day_to_week_day_indexs[start_day]
        (end_day_index, end_week_index) = self.day_to_week_day_indexs[end_day]

        self.RemoveCurveWidget(start_day_index, start_week_index, end_day_index, end_week_index)

        for day in range(start_day, end_day+1):
            (day_index, week_index) = self.day_to_week_day_indexs[day]
            day_widget = self._layout.itemAtPosition(week_index, day_index).widget()

            day_widget.CornersColor = QtGui.QColor(255, 255, 255, 255)
            day_widget.BackgroungColor = QtGui.QColor(255, 255, 255, 255)

            day_widget.update()
