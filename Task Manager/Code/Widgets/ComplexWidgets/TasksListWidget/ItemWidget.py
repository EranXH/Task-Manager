from PyQt5 import QtWidgets, QtCore, QtGui

from Code.Widgets.BuiltInWidgets import *
from Code.Widgets.AnimatedWidget import *

from icecream import ic
import time


# A non foldable item widget for the "tasklistwidget" - used for title and as a perent class for the foldable item
class ItemWidget(CreateFrame):
    # set-up
    def __init__(self, tasks_list_widget, name):

        self.TasksListWidget = tasks_list_widget

        self.Name = name

        super().__init__(None, 'TaskFrame',
                         Shadow=QtWidgets.QFrame.Raised, LineWidth=2, MidLineWidth=0,
                         FixedSize=QtCore.QSize(self.TasksListWidget.ItemsPixWidth, 40))

        self.setStyleSheet('QFrame {background: rgb(255, 255, 255);}')
        self.hide()

        Width = self.TasksListWidget.ItemsPixWidth - 10 - 150 - 15 - 10
        self.Label = CreateLabel(self, 12, self.Name, 'TaskLabel',
                                 GeometryRect=QtCore.QRect(10, 0, Width, 38))

    # Changes the items pixel width depending on the new given one
    def ChangeItemWidth(self):
        self.setFixedSize(QtCore.QSize(self.TasksListWidget.ItemsPixWidth, self.height()))

        Width = self.TasksListWidget.ItemsPixWidth - 10 - 150 - 15 - 10
        self.Label.setGeometry(QtCore.QRect(10, 1, Width, self.Label.height()))

        if hasattr(self, "ID"):
            StartX = self.TasksListWidget.ItemsPixWidth - 10 - 150
            self.ProgressBar.setGeometry(QtCore.QRect(StartX, 5, 150, 32))

    # Remove the item
    def Remove(self):
        self.TasksListWidget.WidgetLayout.removeWidget(self)
        self.hide()

        if self.TasksListWidget.ItemsPixLength.value >= self.height() + 2:
            self.TasksListWidget.ItemsPixLength.value -= self.height() + 2
        else:
            self.TasksListWidget.ItemsPixLength.value = 0

    # Add the item
    def Add(self):
        self.TasksListWidget.WidgetLayout.addWidget(self)

        self.show()

        self.TasksListWidget.ItemsArrangementList.append(self)

        self.TasksListWidget.ItemsPixLength.value += self.height() + 2

    # insert item in the widget list in a given index
    def Insert(self, index):
        self.TasksListWidget.WidgetLayout.insertWidget(index, self)

        self.show()

        self.TasksListWidget.ItemsArrangementList.insert(index, self)

        self.TasksListWidget.ItemsPixLength.value += self.height() + 2

