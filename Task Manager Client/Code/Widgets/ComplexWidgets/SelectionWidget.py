from PyQt5 import QtCore, QtWidgets
from Code.Widgets.BuiltInWidgets import *


# Creates a list of the radio buttons objects for the selections tabs (Type, Share, Assign)
def CreateRadioButtonsList(NamesList, CategoryName, VerticalLayout, FillUpList):
    RadioButtonsList = []
    for name in NamesList:
        radiobutton = CreateRadioButton(None, VerticalLayout, name + CategoryName, name, False)
        RadioButtonsList.append(radiobutton)

    if FillUpList:
        for _ in range(len(NamesList), FillUpList, 1):
            FillUpLabel = CreateLabel(None, 12, '', '', Layout=VerticalLayout)
            RadioButtonsList.append(FillUpLabel)

    return RadioButtonsList


# a selection widget object
# used in the "EditTaskUI" for the slection tabs
class SelectionWidget(object):
    def __init__(self, SelectionType, FrameRect, ScrollRect, ScrollContentsWidgetRect, LabelRect, LabelText, TabWidget,
                 TabName=None, UndeclaredWidgetsNum=0):
        self.SelectionType = SelectionType

        self.Tab = CreateLayoutWidget(None, f"{self.SelectionType}Tab")
        self.Frame = CreateFrame(self.Tab, f"{self.SelectionType}Frame",
                                 Shape=QtWidgets.QFrame.Box, Shadow=QtWidgets.QFrame.Raised,
                                 LineWidth=2, MidLineWidth=0, GeometryRect=FrameRect)

        self.Scroll = CreateScroll(self.Frame, ScrollRect, 12, f"{self.SelectionType}Scroll",
                                   HorizontalScrollBar=QtCore.Qt.ScrollBarAlwaysOff)
        self.ScrollContentsWidget = CreateLayoutWidget(None, f"{self.SelectionType}ScrollContentsWidget",
                                                       ScrollContentsWidgetRect)

        self.ScrollContentsLayout = QtWidgets.QVBoxLayout(self.ScrollContentsWidget)
        self.ScrollContentsLayout.setObjectName(f"{self.SelectionType}ScrollContentsLayout")

        self.OptionsButtonsList = []
        self.UndeclaredWidgetsNum = UndeclaredWidgetsNum

        self.Scroll.setWidget(self.ScrollContentsWidget)

        self.Label = CreateLabel(self.Frame, 10, LabelText, f"{self.SelectionType}Label",
                                 WordWrap=True, GeometryRect=LabelRect)

        if TabName is None:
            self.TabName = self.SelectionType
        else:
            self.TabName = TabName

        TabWidget.addTab(self.Tab, self.TabName)

    # function for adding a list of radio buttons widget to the selection widget
    def AddOptionsButtons(self, OptionsList):
        self.RemoveOptionsButtons()

        self.OptionsList = OptionsList
        self.OptionsButtonsList = CreateRadioButtonsList(OptionsList, self.SelectionType,
                                                         self.ScrollContentsLayout, True)

        # the total number of widgets inside the scroll area
        widget_count = len(self.OptionsButtonsList) + self.UndeclaredWidgetsNum

        # checks if the length of the list to determin if a scrollbar is needed
        if widget_count < 4:
            self.Scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.Scroll.verticalScrollBar().setDisabled(True)

        elif widget_count >= 4:
            self.Scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.Scroll.verticalScrollBar().setDisabled(False)

    # remove all exsisiting radio buttons in the selection widget
    def RemoveOptionsButtons(self):
        for button in self.OptionsButtonsList:
            button.deleteLater()

    # get the name of all the selected items
    def GetSelectedNames(self):
        return [name for index, name in enumerate(self.OptionsList)
                        if self.OptionsButtonsList[index].isChecked()]

    # select items in the selection widget by a list of names
    def SelectByName(self, NamesList):
        for name in NamesList:
            found_widget = self.ScrollContentsWidget.findChild(QtWidgets.QRadioButton, f"{name}{self.SelectionType}")
            if found_widget is not None:
                found_widget.setChecked(True)
