import sys
import numpy as np
import time
import threading
import queue
import copy
from PyQt5 import QtCore, QtWidgets
from functools import partial

from Code.UI.MainUI.Functions import CreateTypeDictionary, SetUpDateDictionaries
from Code.APIRequests.APIGetRequests import RGet_CheckListItems, RGet_AvailableID
from Code.APIRequests.APIDeleteRequests import RDelete_Task
from Code.UI.MainUI.SetupUI import SetupUI
from Code.UI.EditTaskUI.EditTaskUI import EditTaskUI
from Code.UI.MainUI.SaveEvent import SaveEvent
from Code.UI.InheritableObjects.DeleteAllWidgets import DeleteAllWidgets
from Code.PandasFunctions import GetDataFrameFromIndexes, GetIdxListFromValuesList, UpdateRowByDict,\
                                    DeleteRowsByValueAndColumnName
from Code.Widgets.BuiltInWidgets import *
from Code.APIRequests.TreadingAPIGetRequests import Tread_RGet_UserInfoChanged
from Code.GlobalFunctions import ObjectHoldingTheValue
from Code.APIRequests.APIPostRequests import RPost_Logout

from icecream import ic


# TODO: need to add the functionality to the taggle betwen private and public tasks


# crate the main UI
class MainUI(SetupUI, DeleteAllWidgets):
    # Sets up MainUI
    def __init__(self, Main: QtWidgets.QMainWindow, TasksDFs, TreeDFs, PAPUserOptions, UserName, UserID):
        self.UserName = UserName
        self.UserID = UserID
        Main.closeEvent = self.WindowCloseEvent

        self.PrivateOrPublic = 'Public'
        self.BootUI(TasksDFs, TreeDFs, PAPUserOptions, self.PrivateOrPublic, Main)

    # tries to get the user logged off after the user closed the window
    def WindowCloseEvent(self, event):
        PopupMsg = CreatePopupMsg("Exit Message", "Are you sure you want to quit?", button_number=2,
                                  button_1=QtWidgets.QMessageBox.No,
                                  button_2=QtWidgets.QMessageBox.Yes)

        if PopupMsg.response == QtWidgets.QMessageBox.Yes:
            RPost_Logout(self.UserID)
            event.accept()

        else:
            event.ignore()

    # boot the ui of the main page and define the values
    def BootUI(self, TasksDFs, TreeDFs, PAPUserOptions, PrivateOrPublic, Main):
        DeleteAllWidgets.__init__(self, 'Main')
        SetupUI.__init__(self, TasksDFs, TreeDFs, PAPUserOptions, PrivateOrPublic, Main, self.UserID)

        self.SetUpUpdatePusherThread()

        self.Events()

    # later would be implemented differently
    # setting up the update thread and the timer that gets updates from the tread
    def SetUpUpdatePusherThread(self):
        # setting up a thread that requests updates from the server on a loop
        self.UpdatePusherThread = threading.Thread(name="UpdatePusherThread",
                                                   target=Tread_RGet_UserInfoChanged,
                                                   args=[self.PrivateOrPublic, self.UserID, self.UpdatesPusher])
        self.UpdatePusherThread.daemon = True
        self.UpdatePusherThread.start()

        self.TasksValuesChanged = []
        self.RemovedTasks = []
        self.AddedTasks = []

        self.CheckListValuesChanged = []

        # the time which waits for the tread updates on the main thread
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.UpdatesExcepter)
        self.timer.start(1000)

    # the UpdatePusherThread updated the object values base on what it got from the server
    # this allows the timer function (which runs on main thred) to get this info
    def UpdatesPusher(self, api_json):
        if api_json["tasks_values_changed"]:
            self.TasksValuesChanged: list = api_json["tasks_values_changed"]
        if api_json["removed_tasks"]:
            self.RemovedTasks: list = api_json["removed_tasks"]
        if api_json["added_tasks"]:
            self.AddedTasks: list = api_json["added_tasks"]

        if api_json["check_list_values_changed"]:
            self.CheckListValuesChanged: list = api_json["check_list_values_changed"]

    # Except the update info from the UpdatePusherThread and run the right functions
    # this function is called from "timer" object
    def UpdatesExcepter(self):
        if self.TasksValuesChanged:
            self.Updater_TasksValuesChanged()
            self.TasksValuesChanged = []

        if self.RemovedTasks:
            task_id: int
            for task_id in self.RemovedTasks:
                self.TasksListWidget.RemoveByTaskID(task_id)
            self.RemovedTasks = []

        if self.AddedTasks:
            task_row: dict
            for task_row in self.AddedTasks:
                self.TasksListWidget.InsertByTaskRow(task_row)
            self.AddedTasks = []

        if self.CheckListValuesChanged:
            self.Updater_CheckListValuesChanged()
            self.CheckListValuesChanged = []

    # update the "TasksListWidget" items and the local DataFrames base on the information sent from the server
    def Updater_TasksValuesChanged(self):
        change_dict: dict
        for change_dict in self.TasksValuesChanged:
            task_id = change_dict["_id"]
            del change_dict["_id"]

            row_index = GetIdxListFromValuesList(self.TasksDF, [task_id], "_id")[0]
            self.TasksDF = UpdateRowByDict(self.TasksDF, change_dict, row_index)

            task_items = [self.ScheduleItemWidgetsDict[task_id], *self.TypeItemWidgetsDict[task_id].values()]

            for change_key, change_value in change_dict.items():
                for task_item in task_items:
                    if change_key == "progress" and task_item.IsFolded:
                        task_item.updateProgressBar(change_value)

                    elif change_key == "name":
                        task_item.updateName(change_value)

                    elif change_key == "types":
                        task_item.updateTypes(change_value)

                    elif change_key == "description":
                        task_item.updateDescription(change_value)

                    elif change_key == "due_date":
                        task_item.updateDate("Due", change_value)
                    elif change_key == "due_time":
                        task_item.updateTime("Due", change_value)

                    elif change_key == "assigned_date":
                        task_item.updateDate("Due", change_value)
                    elif change_key == "assigned_time":
                        task_item.updateTime("Assigned", change_value)

    # if an exsisting check-list-item (by it`s id) had a value changed (text or checkbox state)
    # active this function to update the same in the client gui and data
    def Updater_CheckListValuesChanged(self):
        change_dict: dict
        for change_dict in self.CheckListValuesChanged:
            task_id = change_dict["_id"]
            del change_dict["_id"]

            task_items = [self.ScheduleItemWidgetsDict[task_id], *self.TypeItemWidgetsDict[task_id].values()]

            for change_key, change_value in change_dict.items():
                for task_item in task_items:
                    task_item.updateCheckListItem(change_key, change_value)

    # Call all the background running events
    def Events(self):
        self.TaskSearchLineEdit.mousePressEvent = self.TaskStartSearchEvent
        self.TaskSearchLineEdit.keyReleaseEvent = self.TaskEndSearchEvent

        self.NewTaskButton.clicked.connect(partial(self.CreateEvent, None))

        self.EditTaskButton.clicked.connect(self.EditEvent)

        self.DeleteTaskButton.clicked.connect(self.DeleteEvent)

        self.Tab.currentChanged.connect(self.ChangeTabEvent)

        # self.TypeTabList.itemSelectionChanged.connect(partial(self.TSTabListEvent, True, self.TypeTabList,
        #                                                       self.TypeDictionary))
        self.TypeTabList.itemSelectionChanged.connect(partial(self.ArrangeTSTabListEvent, True))

        # self.ScheduleTabList.itemSelectionChanged.connect(partial(self.TSTabListEvent, False, self.ScheduleTabList,
        # self.ScheduleTabListDictionary))
        self.ScheduleTabList.itemSelectionChanged.connect(partial(self.ArrangeTSTabListEvent, False))

        self.RelationTabList.itemSelectionChanged.connect(partial(self.TreeWidget.DisplaySelectedLeavesEvent, self,
                                                                  self.RelationTabList, self.TreeDF, self.TasksDF))

        self.TreeWidget.selectionModel().selectionChanged.connect(self.TreeItemSelectEvent)

        self.CompletedButton.clicked.connect(self.f)

        # self.EditButton.clicked.connect()

        # connect to FocusChangedEvent when the object focus is changed
        # QtWidgets.QApplication.instance().focusChanged.connect(self.FocusChangedEvent)

    # def FocusChangedEvent(self):
    # print(self.Main.focusWidget())

    # called by clicking th complete button - should show all the complete task
    # not yet implemented
    def f(self):
        pass
        # self.CompletedButton.isChecked()

    # New Task event
    def CreateEvent(self, task_id):
        # when it is the first time the button is clicked and the varible is new
        if not hasattr(self, "EditTaskUI"):
            self.EditTaskUI = EditTaskUI(self.UserID)

        self.EditTaskUI.BootUI(self.Main, self.TreeDFs, self.TasksDFs, self.PAPUserOptions,
                               self.PrivateOrPublic, task_id)

        self.Main.show()

        self.EditTaskUI.Events()

        # on clicking the save button - save the task and reboot MainUI
        self.EditTaskUI.CancelSaveInput.accepted.connect(partial(SaveEvent, self, self.EditTaskUI))

        # on clicking the cancel button reboot MainUI
        self.EditTaskUI.CancelSaveInput.rejected.connect(partial(self.BootUI, self.TasksDFs, self.TreeDFs,
                                                                 self.PAPUserOptions, self.PrivateOrPublic, self.Main))

    # when clicking the Edit Button this function would be activated - add the task info to the editing window
    def EditEvent(self):
        if self.TasksListWidget.SelectedItem is not None:
            task_item = self.TasksListWidget.SelectedItem
            task_index = self.TasksListWidget.SelectedItem.DFIndex

            task_df = GetDataFrameFromIndexes(self.TasksDF, [task_index])

            check_list_dict = RGet_CheckListItems(self.PrivateOrPublic, task_item.ID, self.UserID)
            check_list = copy.deepcopy(check_list_dict)  # self.CheckListDict['items']
            check_list.pop("_id")

            self.CreateEvent(task_item.ID)
            self.EditTaskUI.EnterValuesForEdit(task_df, check_list, self.EditTaskUI.CL_PAA_TEI)

        else:
            CreatePopupMsg("Error!", "Please select an item to edit")

    # deletes a selected task when the Delete Button is pressed
    # not yet implemented in the tree-widget
    def DeleteEvent(self):
        if self.TasksListWidget.SelectedItem is not None:

            task_item = self.TasksListWidget.SelectedItem
            task_id = task_item.ID
            task_name = task_item.Name

            PopupMsg = CreatePopupMsg("Delete Task Message", f"Are you sure you want to delete the {task_name} task?",
                                      button_number=2,
                                      button_1=QtWidgets.QMessageBox.No, button_2=QtWidgets.QMessageBox.Yes)

            if PopupMsg.response == QtWidgets.QMessageBox.Yes:
                response = RDelete_Task(self.PrivateOrPublic, task_name, task_id, self.UserID)
                if not response.get("response"):
                    self.TasksListWidget.RemoveByTaskID(task_id)

                else:
                    CreatePopupMsg("Error!", response.get("response"))

        else:
            CreatePopupMsg("Error!", "Please select an item to delete")

    # Change the Selected Item index depending on the selected Tree Item
    def TreeItemSelectEvent(self):
        pass
        # self.TreeWidget.selectedIndexes()
        # for ix in self.TasksTree.selectedIndexes():
        # text = ix.data(QtCore.Qt.DisplayRole)  # or ix.data()
        # for item_key in self.TasksTreeItems:
        # item_obj = self.TasksTreeItems[item_key][0]
        # item_idx = self.TasksTreeItems[item_key][1]
        # if item_obj.isSelected():
        # self.SelectedItem = item_idx

    # on tab selected item change - when the selected option in the date or type is change
    # call the "TSTabListEvent" with the right values fitted to the tab the change occurred in
    def ArrangeTSTabListEvent(self, IsType):
        self.TasksListWidget.Clear()

        if IsType:
            self.TSTabListEvent(IsType, self.TypeTabList, self.TypeDictionary)
        else:
            self.TSTabListEvent(IsType, self.ScheduleTabList, self.ScheduleTabListDictionary)

    # Get the dict (key- task_id; value- foldable_item_widget) by the selected option name, and if the tab is type
    @staticmethod
    def GetSelectedDictionary(IsType: bool, Selected: str, Dictionary: dict):
        if IsType:
            if Selected != 'Everything':
                return {Selected: Dictionary[Selected]}
            else:
                return Dictionary
        else:
            return Dictionary[Selected]

    # Show the list corresponding to the selected extension
    def TSTabListEvent(self, IsType, TabList, Dictionary):
        Selected = TabList.selectedItems()[0].text()
        s = self.GetSelectedDictionary(IsType, Selected, Dictionary)
        f = [list(k) for k in s.values()]
        _2D_visible_items_array = np.array(list(self.TypeItemWidgetsDict.values()))

        ic(_2D_visible_items_array)
        self.TasksListWidget.AddItems(self.GetSelectedDictionary(IsType, Selected, Dictionary))

    # Change between Tabs
    def ChangeTabEvent(self):
        self.TasksListWidget.raise_()
        self.TasksListWidget.Clear()

        if self.Tab.currentIndex() == 0:
            self.TasksListWidget.AddItems(self.DateDictionary)

        if self.Tab.currentIndex() == 1:
            self.TasksListWidget.AddItems(self.TypeDictionary)

        if self.Tab.currentIndex() == 2:
            self.TreeWidget.raise_()

    # Start Task Search event
    def TaskStartSearchEvent(self, event):
        self.TaskSearchLineEdit.setText('')

    # End Task Search event
    def TaskEndSearchEvent(self, event):
        self.TaskSearchLineEdit.setText('Search Task:')
