from PyQt5 import QtWidgets, QtCore
from Code.Widgets.BuiltInWidgets import *


# this widget would be activated from the "TimeFrame"
# this widget is used for selecting time
class TimeSelectionWidget(CreateFrame):
    def __init__(self):
        CreateFrame.__init__(self, None, "TimeSelectionWidgetFrame",
                             MinimumSize=QtCore.QSize(250, 150), MaximumSize=QtCore.QSize(250, 150))
        self.show()

        self._layout = CreateHorizontalLayout(self, 10, "Layout")

        self.HoursList = CreateList(None, 12, "HoursList",
                                    AcceptDrops=False, DropIndicatorShown=False, DragEnabled=False)
        self._layout.addWidget(self.HoursList)
        for hour in range(1, 13):
            self.HoursList.addItem(str(hour))

        self.MinutesList = CreateList(self, 12, "MinutesList",
                                      AcceptDrops=False, DropIndicatorShown=False, DragEnabled=False)
        self._layout.addWidget(self.MinutesList)
        for minute in range(60):
            if minute > 9:
                self.MinutesList.addItem(str(minute))
            else:
                self.MinutesList.addItem(f"0{minute}")

        self.AMPMList = CreateList(self, 12, "AMPMList",
                                   AcceptDrops=False, DropIndicatorShown=False, DragEnabled=False)
        self._layout.addWidget(self.AMPMList)
        self.AMPMList.addItem("AM")
        self.AMPMList.addItem("PM")

        self.AMPMList.itemClicked.connect(self.UnNamed)

    # starting to create a function for selection event
    def UnNamed(self, item):
        print(item.text())
        print(self.AMPMList.selectedItems()[0].text())
