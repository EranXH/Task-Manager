from pandas import DataFrame
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from PyQt5 import QtCore, QtGui, QtWidgets

from Code.Widgets.BuiltInWidgets import *
#from Code.Widgets.ComplexWidgets.TasksListWidget.ItemWidget import TaskListItemWidget

from icecream import ic


'''
Using the "TaskDF" creating an items dict which includs the "task_id" as a key after that there are two options:
    if used for Type - create a new dict as the value,
                       in the dict the key is the type name and the value 
                       is a "TasksListWidget" "FoldableItem" item obejct
    if used for Date - creating a dict where the value is a "TasksListWidget" "FoldableItem" item obejct 
'''


def CreateItemWidgetsDict(TasksListWidget, TasksDF: DataFrame, includes_type: bool) -> dict:
    items = {}

    for index, row in TasksDF.iterrows():
        if includes_type:
            tasks_by_type = {}
            for _type in row["types"]:
                tasks_by_type[_type] = TasksListWidget.CreateFoldableItem(row, index, _type)
            items[row["_id"]] = tasks_by_type

        else:
            items[row["_id"]] = TasksListWidget.CreateFoldableItem(row, index, row["types"])

    return items


# Create a Type Dictionary
def CreateTypeDictionary(TasksDF: DataFrame, TypeItemWidgetsDict: dict[int, dict[str, object]]):
    # SortedDataFrame = TasksDF.sort_values(by=['Type', 'Due To Date', 'Due To Time'])
    TypeList = TasksDF['types'].tolist()
    IDsList = TasksDF['_id'].tolist()

    TypeDictionary: dict[str, list] = {}
    for place, Types in enumerate(TypeList):
        for _type in Types:
            if _type in TypeDictionary:
                TypeDictionary[_type].append(TypeItemWidgetsDict[IDsList[place]][_type])
            else:
                TypeDictionary[_type] = [TypeItemWidgetsDict[IDsList[place]][_type]]

    return TypeDictionary


# return an updated TypeTabButtonsNames list, clear TypeTabList and insert to it all the types names
def UpdateTypeTabList(TypeTabList, TypeDictionary):
    TypeTabList.clear()
    TypeTabButtonsNames = [*TypeDictionary]
    TypeTabButtonsNames.insert(0, 'Everything')
    for place in range(0, len(TypeTabButtonsNames)):
        TypeTabList.insertItem(place, TypeTabButtonsNames[place])
    return TypeTabButtonsNames


# Create a Date Dictionary
def CreatDateDictionary(TasksDF: DataFrame, ScheduleItemWidgetsDict: dict[int, object]):
    SortedDataFrame = TasksDF.sort_values(by=['due_date', 'due_time'], ascending=[False, True])

    DateList = SortedDataFrame['due_date'].tolist()
    TimeList = SortedDataFrame['due_time'].tolist()
    IDsList = SortedDataFrame['_id'].tolist()

    DateDictionary = {}
    for place, date in enumerate(DateList):
        if date in DateDictionary:
            DateDictionary[date].append(ScheduleItemWidgetsDict[IDsList[place]])
        else:
            DateDictionary[date] = [ScheduleItemWidgetsDict[IDsList[place]]]

    return DateDictionary


# Slice the unnecessary parts of the dictionary
def SliceDateDictionary(DateDictionary, Days, Months):
    NewDateDictionary = {}
    CurrentDate = datetime.today()
    HowLong = CurrentDate + relativedelta(days=Days, months=Months) - CurrentDate
    DatesList = [CurrentDate + timedelta(days=d) for d in range(HowLong.days)]
    DatesList = [d.strftime('%Y/%m/%d') for d in DatesList]

    for key_date in DateDictionary:
        if Days == 0 and Months == 0:
            if key_date < CurrentDate.strftime('%Y/%m/%d'):
                NewDateDictionary[key_date] = DateDictionary[key_date]

        if key_date == CurrentDate.strftime('%Y/%m/%d'):
            DummyDateDictionary = []
            for task_item in DateDictionary[key_date]:
                CurrentTime = datetime.now().strftime('%H:%M').split(':')
                CurrentTimeFloat = int(CurrentTime[0]) + float('0.' + CurrentTime[1])

                TimeFloat = int(task_item.DueTime[0]) + float('0.' + task_item.DueTime[1])
                if TimeFloat - CurrentTimeFloat >= 0 and (Days != 0 or Months != 0):
                    DummyDateDictionary.append(task_item)
                if TimeFloat - CurrentTimeFloat < 0 and Days == 0 and Months == 0:
                    DummyDateDictionary.append(task_item)
            if DummyDateDictionary:
                NewDateDictionary[key_date] = DummyDateDictionary

        elif key_date in DatesList and (Days != 0 or Months != 0):
            NewDateDictionary[key_date] = DateDictionary[key_date]

    return NewDateDictionary

# set up the "ScheduleTabListDictionary" and the "DateDictionary"
# used in the date selection tab for fast switches between the selected options
def SetUpDateDictionaries(TasksDF: DataFrame, ScheduleItemWidgetsDict: dict[int, object]):
    # check if TaskDF is not empty -> empty when user dosnt have any tasks
    if not TasksDF.empty:
        # create a dictionary wich is sort by date
        DateDictionary = CreatDateDictionary(TasksDF, ScheduleItemWidgetsDict)
    else:
        DateDictionary = {}

    MyDayDictionary = SliceDateDictionary(DateDictionary, 1, 0)
    MyWeekDictionary = SliceDateDictionary(DateDictionary, 7, 0)
    MyMonthDictionary = SliceDateDictionary(DateDictionary, 0, 1)
    ExpiredDictionary = SliceDateDictionary(DateDictionary, 0, 0)

    ScheduleTabListDictionary = {'Everything': DateDictionary, 'My Day': MyDayDictionary,
                                 'My Week': MyWeekDictionary, 'My Month': MyMonthDictionary,
                                 'Expired': ExpiredDictionary}

    return DateDictionary, ScheduleTabListDictionary


# a function for updateing the "ScheduleTabList" after a new item have been added or an item has been deleted
def UpdateScheduleTabList(ScheduleTabList, ScheduleTabListDictionary):
    ScheduleTabList.clear()

    for place in range(0, len([*ScheduleTabListDictionary])):
        item_name = [*ScheduleTabListDictionary][place]
        ScheduleTabList.insertItem(place, item_name)


# create a TabsList widget
def CreateTabsList(MainTab, TabName):
    Tab = CreateLayoutWidget(None, f"{TabName}Tab")
    MainTab.addTab(Tab, TabName)

    TabList = CreateList(Tab, 12, f"{TabName}TabList",
                         GeometryRect=QtCore.QRect(1, 0, 273, 366),
                         AcceptDrops=False, DropIndicatorShown=False, DragEnabled=False, VScrollMode=False,
                         DragDropMode=False, FrameShape=QtWidgets.QFrame.NoFrame)

    TabList = SetUpPalette(QtGui.QColor(225, 225, 225), QtGui.QPalette.Base, TabList)

    return Tab, TabList
