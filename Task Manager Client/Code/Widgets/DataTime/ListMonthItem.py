from PyQt5 import QtWidgets, QtCore, Qt
import calendar

from Code.Widgets.BuiltInWidgets import *
from Code.Widgets.DataTime.MonthItemTable import MonthItemTable


# the customizely created QListWidgetItem which incluse a mounth name title and the days date cells
class ListMonthItem(QtWidgets.QListWidgetItem):
    def __init__(self, list_widget, year_month):
        super().__init__(list_widget)

        self.NumberOfWeeks = calendar.month(year_month[0], year_month[1]).count('\n') - 2
        self.CellSize = int((list_widget.width()-5) / 7)

        self.Frame = CreateFrame(None, 'CalendarListItemFrame',
                                 MinimumSize=QtCore.QSize(2 + self.CellSize * 7, 25 + self.NumberOfWeeks * self.CellSize),
                                 MaximumSize=QtCore.QSize(2 + self.CellSize * 7, 25 + self.NumberOfWeeks * self.CellSize))
        #if len(list_widget.TablesList) != 0:
        self.Frame.setStyleSheet("QFrame#CalendarListItemFrame {border-top: 2px solid blue;}")

        # adding the table for showing the days date numbers
        self.Table = MonthItemTable(self, year_month)


        label_text = f"{calendar.month_name[year_month[1]]} {year_month[0]}"
        self.MonthTitle = CreateLabel(self.Frame, 10, label_text, 'NameLabel')
                                      #GeometryRect=QtCore.QRect(20, 80, 100, 40))

        self.setSizeHint(self.Frame.size())
        list_widget.setItemWidget(self, self.Frame)
        self.setFlags(Qt.Qt.NoItemFlags)



