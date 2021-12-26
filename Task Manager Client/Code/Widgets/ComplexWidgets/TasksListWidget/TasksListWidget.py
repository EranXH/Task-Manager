from __future__ import annotations

from PyQt5 import QtCore

from Code.Widgets.BuiltInWidgets import *
#from Code.ComplexWidgets.ProgressBarWidget import CreateProgressBar, CalculateProgress
from Code.Widgets.ComplexWidgets.TasksListWidget.ItemWidget import ItemWidget
from Code.Widgets.ComplexWidgets.TasksListWidget.FoldableItemWidget import FoldableItemWidget
from Code.GlobalFunctions import ObjectHoldingTheValue
from Code.PandasFunctions import DeleteRowsByValueAndColumnName, AppendRowByDict

from icecream import ic
import inspect
import traceback
import copy
from pandas import DataFrame
import numpy as np

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Code.UI.MainUI.MainUI import MainUI


# the Task List Widget
class TasksListWidget(CreateScroll):
    # set - up
    def __init__(self, Window, GeometryRect, UserID, functions_dict, MainUI: MainUI):   # ItemsPixWidth=586, ItemsPixLength=0): QtCore.QRect(277, 0, 592, 510)
        super().__init__(Window, GeometryRect, 12, 'TasksListWidget')
        self.setStyleSheet('QScrollArea {background: rgb(255, 255, 255);}')

        self.MainUI = MainUI

        # would be replaced by calling the "self.MainUI.FunctionName"
        # function taken from the main_ui for easier reachability
        self.GetPrivateOrPublic = functions_dict["GetPrivateOrPublic"]
        self.GetTasksDF = functions_dict["GetTasksDF"]
        self.UpdateTasksDF = functions_dict["UpdateTasksDF"]
        self.GetWidgetsDict = functions_dict["GetWidgetsDict"]
        self.UpdateAfterTaskRemoved = functions_dict["UpdateAfterTaskRemoved"]
        self.UpdateAfterTaskInsert = functions_dict["UpdateAfterTaskInsert"]

        self.UserID = UserID

        self.UnFoldedTasks = {}
        self.UnFoldedItemID = None

        self.PreviouslySelectedItem: FoldableItemWidget = None
        self.SelectedItem: FoldableItemWidget = None

        self.Widget = CreateLayoutWidget(self, "Scroll")
        self.Widget.setStyleSheet('QWidget#Scroll {background: rgb(255, 255, 255);}')

        self.WidgetLayout = CreateVerticalLayout(self.Widget, 0, "ScrollAreaLayout")

        #self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.Widget)

        self.ItemsArrangementList: list[ItemWidget, FoldableItemWidget] = []
        self.Titles: list = []
        self.ItemsPixWidth = self.width() - 6

        # setting objects which on change activate a given function
        # the object is the hight pixcle count of all the items in the list
        self.ItemsPixLength = ObjectHoldingTheValue()
        self.ItemsPixLength.value = 0
        self.ItemsPixLength.register_callback(self.ItemsPixLengthEvent)

    # the given callback function for the "ItemsPixLength" change
    # the function changes the list-widget width
    def ItemsPixLengthEvent(self, old_value, new_value):
        Change = False
        ListWidgetPixLength = self.height() - 4
        if old_value < ListWidgetPixLength <= new_value:
            Change = True
            self.ItemsPixWidth -= 20
        if old_value >= ListWidgetPixLength > new_value:
            Change = True
            self.ItemsPixWidth += 20
        if Change:
            for item in self.ItemsArrangementList:
                item.ChangeItemWidth()

        # getting the name of the function that activated this function
        # when changing tabs while a task is folding (or unfolding) the Widget Height size would change
        # and the spaces between tasks in the changed tab would be changed too
        _, _, function_name, _ = traceback.extract_stack()[-4]
        if function_name != "AnimationValueChangeEvent" or len(self.UnFoldedTasks):
            self.Widget.setFixedHeight(self.ItemsPixLength.value)

    # creating a new foldable item - for a task item
    def CreateFoldableItem(self, row, df_index, types):
        return FoldableItemWidget(self, row, df_index, types)

    # creating a new item - for a title item
    def CreateItem(self, name):
        return ItemWidget(self, name)

    # Add a row to the Main List widget
    def AddItems(self, Dictionary):
        for title_key in Dictionary:
            self.CreateItem(title_key).Add()
            self.Titles.append(title_key)
            for task_item in Dictionary[title_key]:
                task_item.Add()

    # removimg all items from the shown list of items
    # the tasks items would be still saved in the dictionaries in the mainui
    def RemoveAllItems(self):
        for item in self.ItemsArrangementList:
            item.Remove()
            if hasattr(item, "ID"):
                del item

        self.ItemsArrangementList = []
        self.ItemsPixLength.value = 0

    # setting selected item and saving the up-to-date previously selected item
    def SavePreviouslySelectedItem(self, TasksListItemWidget):
        if TasksListItemWidget.ID:  # self.Tab.currentIndex() <= 1 and
            if self.SelectedItem != TasksListItemWidget:
                self.PreviouslySelectedItem = self.SelectedItem
                self.SelectedItem = TasksListItemWidget

                TasksListItemWidget.setStyleSheet("QFrame#TaskFrame {border: 2px solid blue; border-radius: 8px;}")

                if self.PreviouslySelectedItem is not None:
                    self.PreviouslySelectedItem.setStyleSheet("QFrame#TaskFrame "
                                                              "{border: 2px solid gray; border-radius: 8px;}")

    # makes sure that at most only one task foldable item can be unfolded at a given point in time
    def PresenterTaskEvent(self, TasksListItemWidget):
        if TasksListItemWidget.ID:  # self.Tab.currentIndex() <= 1 and
            if not TasksListItemWidget.IsFolded:
                self.UnFoldedTasks[self.UnFoldedItemID].Fold()
                self.UnFoldedItemID = None

            else:
                if self.UnFoldedItemID is not None:
                    self.UnFoldedTasks[self.UnFoldedItemID].Fold()
                    self.UnFoldedItemID = None

                TasksListItemWidget.UnFold(self.GetPrivateOrPublic)

    # remove all the task presentors (all unfoloded tasks with animated widgets)
    # makes sure that no unused atters are exsist and cause errors
    def RemoveAllTaskPresentors(self):
        while self.UnFoldedTasks.values():
            task_item = list(self.UnFoldedTasks.values())[0]
            task_item.DeleteAllAnimations()

        self.UnFoldedTasks = {}
        self.UnFoldedItemID = None

        self.PreviouslySelectedItem = None

        if self.SelectedItem is not None:
            self.SelectedItem.setStyleSheet("QFrame#TaskFrame "
                                                      "{border: 2px solid gray; border-radius: 8px;}")

        self.SelectedItem = None

    # when a new task_row is pushed from the server and need to be inserted -
    #                                                                     this task sort and check where and what to do
    def InsertByTaskRow(self, task_row):
        # add the new row to the dataframe
        self.MainUI.TasksDF = AppendRowByDict(self.MainUI.TasksDF, task_row)

        task_id = task_row["_id"]
        task_index = self.MainUI.TasksDF.shape[0]
        task_type = task_row["types"]

        # check what is the selected sort title, and wether it is in the type or schedule sort (or tree sort)
        if self.MainUI.Tab.currentIndex() == 0:     # schedule sort
            try:
                Selected = self.MainUI.ScheduleTabList.selectedItems()[0].text()
            except IndexError:
                Selected = "Everything"
        elif self.MainUI.Tab.currentIndex() == 1:   # type sort
            try:
                Selected = self.MainUI.TypeTabList.selectedItems()[0].text()
            except IndexError:
                Selected = "Everything"
        else:
            Selected = ""

        # creating the items for the type and schedule sort and inserting them to the right place in the dicts
        new_items = set()

        # type
        tasks_by_type = {}
        for _type in task_row["types"]:
            new_item = self.CreateFoldableItem(task_row, task_index, _type)
            tasks_by_type[_type] = new_item
            new_items.add(new_item)

        self.MainUI.TypeItemWidgetsDict[task_id] = tasks_by_type
        self.MainUI.UpdateTypeObjects()

        # schedule
        new_item = self.CreateFoldableItem(task_row, task_index, task_row["types"])
        new_items.add(new_item)
        self.MainUI.ScheduleItemWidgetsDict[task_id] = new_item

        self.MainUI.UpdateScheduleObjects()

        # this if block determin if an insert animation should take place
        # check if the item should be represented in the selected sort title
        if Selected:
            visible_task_items = set()
            if self.MainUI.Tab.currentIndex() == 0:
                selected_dictionary = self.MainUI.GetSelectedDictionary(False, Selected,
                                                                        self.MainUI.ScheduleTabListDictionary)
            else:
                selected_dictionary = self.MainUI.GetSelectedDictionary(True, Selected, self.MainUI.TypeDictionary)

            for task_items_list in selected_dictionary.values():
                visible_task_items.update(task_items_list)

            # determin the position of the task item and need and the position of the title (if nessesery)
            titles = list(selected_dictionary.keys())
            for new_item in new_items.intersection(visible_task_items):
                for row_index, row in enumerate(selected_dictionary.values()):
                    for item_index, item in enumerate(row):
                        if new_item is item:
                            title = titles[row_index]
                            # if the title don't exsist add bot the title and the task item
                            if title not in self.Titles:
                                self.CreateItem(title).Insert(row_index + item_index)
                                self.Titles.append(title)
                                new_item.InsertOrRemoveTask("Insert", row_index + item_index + 1)
                            # if the title exsist add only the task item
                            else:
                                new_item.InsertOrRemoveTask("Insert", row_index + item_index)

    # when a task_row is pushed from the server as a deleted one and need to be removed from the user -
    # this function check where and what to do with the deleted task item
    def RemoveByTaskID(self, task_id):
        self.UpdateTasksDF(DeleteRowsByValueAndColumnName(self.GetTasksDF(), task_id, "_id"))

        # create a list of the task items based on the task_id
        type_item_widgets_dict, schedule_item_widgets_dict = self.GetWidgetsDict()
        task_items = [schedule_item_widgets_dict[task_id], *type_item_widgets_dict[task_id].values()]

        # run on all the task items list
        for task_item in task_items:
            task_item.InsertOrRemoveTask("Remove")

            # checkes if the above and below items are title items - remove the title item above
            task_preceding_item = self.getPrecedingItem(task_item)
            task_next_item = self.getNexItem(task_item)
            if task_preceding_item is not None and type(task_preceding_item) == ItemWidget and \
                    type(task_next_item) != FoldableItemWidget:
                task_preceding_item.Remove()
                self.ItemsArrangementList.remove(task_preceding_item)

            del task_item

        self.PreviouslySelectedItem = None
        self.SelectedItem = None

        self.UpdateAfterTaskRemoved(task_id)

    # clearing the list widget
    def Clear(self):
        self.RemoveAllTaskPresentors()
        self.RemoveAllItems()
        self.Widget.setFixedHeight(0)

    # get the Preceding item to a given item
    def getPrecedingItem(self, item):
        try:
            item_index = self.ItemsArrangementList.index(item)
            if item_index-1 >= 0:
                return self.ItemsArrangementList[item_index-1]
            else:
                return None
        except ValueError:
            return None

    # get the Next item to a given item
    def getNexItem(self, item):
        try:
            item_index = self.ItemsArrangementList.index(item)
            if item_index + 1 < len(self.ItemsArrangementList):
                return self.ItemsArrangementList[item_index + 1]
            else:
                return None
        except ValueError:
            return None
