#from Code.UI.MainUI.MainUI import MainUI
from Code.UI.EditTaskUI.EditTaskUI import EditTaskUI

from datetime import date, datetime
from Code.APIRequests.APIGetRequests import RGet_AvailableID, RGet_Login
from Code.APIRequests.APIPostRequests import RPost_AfterEditingTask
from Code.GlobalFunctions import common_elemnts
import Code.UI.LoginUI.Functions as Func
from Code.UI.LoginUI.UserDetailsHolder import UserDetailsHolder
from Code.Widgets.BuiltInWidgets import *
from Code.PandasFunctions import GetDataFrameFromIndexes
import requests

from icecream import ic

class SaveEvent:
    def __init__(self, MainUIInstance, EditTaskUIInstance):
        self.MainUI = MainUIInstance
        self.EditTaskUI = EditTaskUIInstance

        # setting values in a short name based on the value of "PrivateOrPublic"
        self.ArrangeValues()
        self.CheckWhatsLeft()

        # check if all the inputs have been entered correctly
        if not self.WhatsLeft:
            # arranging the inputed values in a way which makes creating a new_row_dict easier
            CheckList, HasCheckList, CheckListAmountOfCheckedItems, CheckListAmountOfItems, \
            DueToDate, DueToTime, AssignedDate, AssignedTime = self.OrganizeValuesBeforNewRow()

            # creating a new_row_dict (a new task wich is represented in a dict -
            #                           which would be represented as a row in the DataFrame)
            new_task_dict = self.ArrangeTaskData(HasCheckList, CheckListAmountOfCheckedItems, CheckListAmountOfItems,
                                                 DueToDate, DueToTime, AssignedDate, AssignedTime)

            TasksDF = self.EditTaskUI.TasksDF.append(new_task_dict, ignore_index=True)

            if self.PrivateOrPublic == 'Private':
                PublicTasksDF, PublicTreeDF = self.PublicTasksDF, self.PublicTreeDF
                PrivateTasksDF, PrivateTreeDF = TasksDF, self.TreeDF
            else:
                PublicTasksDF, PublicTreeDF = TasksDF, self.TreeDF
                PrivateTasksDF, PrivateTreeDF = self.PrivateTasksDF, self.PrivateTreeDF

            # Organize and tries to send to the server
            if self.OrganizeAndSendToServer(new_task_dict, CheckList):
                # using the saved user loging info getting the updated user info
                user_info = RGet_Login(UserDetailsHolder.user_name_hash, UserDetailsHolder.password_hash)
                # if the "user_info" is returned corectly the len of it should be 4
                if len(user_info) == 4:
                    # arrange values before restarting the main window
                    TasksDFs, TreeDFs, UserID = Func.ArrangeDFValues(user_info)
                    PAPUserOptions = Func.ArrangeOptionsValues(user_info, self.MainUI.UserName)

                    # rebooting the main UI window
                    self.MainUI.BootUI(TasksDFs, TreeDFs, PAPUserOptions, self.PrivateOrPublic,
                                       self.EditTask)
                # when the "user_info" is not returned corectly pop up a message window with the error
                else:
                    CreatePopupMsg("Error!", user_info["Error!"])
        # if it falied popup a fitted error message
        else:
            self.CreateErrorMessage()

    # setting that the instens of this class would have all the atterbutes from the "MainUI" and "EditTaskUI" instenses
    def __getattr__(self, attr):
        # doing try exceps and not just returning getattr(self.EditTaskUI, attr) or getattr(self.MainUI, attr)
        # because pandas datafrase and series cannot be interpret as a bool
        try:
            return getattr(self.MainUI, attr)
        except AttributeError:
            return getattr(self.EditTaskUI, attr)

    # setting values in a short name based on the value of "PrivateOrPublic"
    def ArrangeValues(self):
        if self.PrivateOrPublic == "Private":
            self.TypeWidget = self.NewTaskUI.PrivateTypeTab.Widget
            self.RoutesList = self.PrivateAssociateTab.RoutesList
            self.OccupiedNamesByRoute = self.PrivateAssociateTab.OccupiedNamesByRoute
            self.TreeDF = self.PrivateAssociateTab.TreeDF
        else:
            self.TypeWidget = self.PublicTypeTab.Widget
            self.RoutesList = self.PublicAssociateTab.RoutesList
            self.OccupiedNamesByRoute = self.PublicAssociateTab.OccupiedNamesByRoute
            self.TreeDF = self.PublicAssociateTab.TreeDF

    # Arrange the new row dictionary
    def ArrangeTaskData(self, HasCheckList, CheckListAmountOfCheckedItems, CheckListAmountOfItems, DueToDate, DueToTime,
                        AssignedDate, AssignedTime):

        new_task_dict = {'name': self.NameInput.text(),
                         'types': self.TypeWidget.GetSelectedNames(),
                         'has_checklist': HasCheckList,
                         'progress': [CheckListAmountOfCheckedItems, CheckListAmountOfItems],
                         'has_schedule': self.ScheduledToggle.isChecked(),
                         'assigned_date': AssignedDate,
                         'assigned_time': AssignedTime,
                         'due_date': DueToDate,
                         'due_time': DueToTime,
                         'description': self.DescriptionInput.toPlainText(),
                         '_id': self.TaskID}

        if self.PrivateOrPublic == "Public":
            new_task_dict['incharge_users'] = self.InchargeWidget.GetSelectedNames()
            new_task_dict['assigned_users'] = self.AssignWidget.GetSelectedNames()
        else:
            new_task_dict['incharge_users'] = [self.UserName]
            new_task_dict['assigned_users'] = [self.UserName]

        return new_task_dict

    # Check what values are empty
    def CheckWhatsLeft(self):
        WhatIsMissing = {'Name': 'Name', "Associate": "Associate", 'Description': 'Description', 'Type': 'Type',
                         'Incharge': 'Incharge', 'Assign': 'Assign'}

        if self.NameInput.text():
            WhatIsMissing['Name'] = "Nothing Is Missing"

        if self.RoutesList:
            WhatIsMissing["Associate"] = "Nothing Is Missing"

        if len(self.DescriptionInput.toPlainText()) > 0:
            WhatIsMissing["Description"] = "Nothing Is Missing"

        if self.TypeWidget.GetSelectedNames():
            WhatIsMissing["Type"] = "Nothing Is Missing"

        if self.PrivateOrPublic == "Public":
            if self.InchargeWidget.GetSelectedNames():
                WhatIsMissing["Incharge"] = "Nothing Is Missing"

            if self.AssignWidget.GetSelectedNames():
                WhatIsMissing["Assign"] = "Nothing Is Missing"
        else:
            WhatIsMissing["Incharge"] = "Nothing Is Missing"
            WhatIsMissing["Assign"] = "Nothing Is Missing"

        self.WhatsLeft = [value for value in WhatIsMissing.values()
                                    if value != "Nothing Is Missing"]

    # arranging the inputed values in a way which makes creating a new_row_dict easier
    def OrganizeValuesBeforNewRow(self):
        if self.ScheduledToggle.isChecked():
            DueToDateInput = self.ScheduledInput.text()[:10]
            DueToDate = f"{DueToDateInput[6:]}/{DueToDateInput[3:5]}/{DueToDateInput[:2]}"
            DueToTime = self.ScheduledInput.text()[18:]
        else:
            DueToDate = ""
            DueToTime = ""

        AssignedDate = date.today().strftime('%Y/%m/%d')
        AssignedTime = datetime.now().strftime('%H:%M')

        CheckList = self.CheckListWidget.GetItemsDict()

        CheckListAmountOfCheckedItems = self.CheckListWidget.GetAmountOfCheckedItems()
        CheckListAmountOfItems = len(self.CheckListWidget.ItemsArrangementList)
        HasCheckList = True
        if CheckListAmountOfItems == 0:
            HasCheckList = False

        # TODO: need to think about how to update the tasks progress inside the tree widget
        # if HasCheckList:
            # TasksDF = UpdateAssociatedTaskProgressVal(self.URLList, self.TasksDF,
                                                      # CheckListAmountOfCheckedItems, CheckListAmountOfItems)

        return CheckList, HasCheckList, CheckListAmountOfCheckedItems, CheckListAmountOfItems,\
               DueToDate, DueToTime, AssignedDate, AssignedTime

    # organizing the dict which is sent to the server api
    def OrganizeAndSendToServer(self, new_task_dict, check_list_items: dict):
        IsEditingTask = False if self.TaskID == 999 else True
        self.TaskID = RGet_AvailableID(self.PrivateOrPublic) if self.TaskID == 999 else self.TaskID

        new_task_dict["_id"] = self.TaskID

        new_task_name = new_task_dict["name"]

        # --- Relation Lists --- #

        # if the task is new then it won't find anything befor editing
        if IsEditingTask:
            task_befor_editing = self.EditTaskUI.TasksDF[self.EditTaskUI.TasksDF["_id"] == self.TaskID]
            related_users_ids_befor_editing = {*task_befor_editing["assigned_users"].tolist()[0],
                                               *task_befor_editing["incharge_users"].tolist()[0]}

            related_users_ids_after_editing = {*self.InchargeWidget.GetSelectedNames(),
                                               *self.AssignWidget.GetSelectedNames()}

            removed_from_relation = list(related_users_ids_befor_editing - related_users_ids_after_editing)
            add_to_relation = list(related_users_ids_after_editing - related_users_ids_befor_editing)

            branches_routes_befor_edit = set(self.PublicIDToRouteDict[self.TaskID])

        else:
            removed_from_relation = []
            add_to_relation = list({*self.InchargeWidget.GetSelectedNames(), *self.AssignWidget.GetSelectedNames()})

            branches_routes_befor_edit = set()

        # the Tasks in self.OccupiedNamesByRoute are not fitted for the complete route, they are fitted for the location route
        # the location route is good for chacking for changes in all of the locations of the task after edit
        # but bad for asking what the is the id of the branch which is the complete route
        # that's means that both the id of the branch and the tasks are for the location route as an id

        # --- Branches to Delete --- #

        branches_routes_after_edit = set(self.OccupiedNamesByRoute.keys())

        # chack what elements don`t exsist now that exsist befor editing - deleting them
        if IsEditingTask:
            location_routes_to_delete: set = branches_routes_befor_edit - branches_routes_after_edit
        else:
            location_routes_to_delete = set()

        branches_to_delete = []

        if location_routes_to_delete != set():
            branches_to_delete = [{"_id": route, self.NameInput.text(): self.TaskID}
                                        for route in location_routes_to_delete]

        # --- Branches to Add --- #

        # chack what elements exsist now that didn`t exsist befor editing - adding them

        if IsEditingTask:
            location_routes_to_add: set = branches_routes_after_edit - branches_routes_befor_edit
        else:
            location_routes_to_add: set = branches_routes_after_edit

        branches_to_add = []

        if location_routes_to_add != set():
            branches_to_add = [{"_id": route, self.NameInput.text(): self.TaskID, "users": []}
                                    for route in location_routes_to_add]

        # --- Check List Items --- #
        check_list_items.update({"_id": self.TaskID, "user_id": self.UserID})

        # --- Arrange the Complete Body Dict --- #

        body_dict = {"task": new_task_dict, "user_id": self.UserID,
                     "branches to delete": branches_to_delete, "branches to add": branches_to_add,
                     "relation to delete": removed_from_relation, "relation to add": add_to_relation,
                     "check list items": check_list_items}

        ic(body_dict)
        # tries to send the updated info to the server
        try:
            RPost_AfterEditingTask(self.PrivateOrPublic, body_dict)
            return True
        # if it falied popup a fitted error message
        except requests.ConnectionError:
            CreatePopupMsg("Error!", "Failed To Connect To the Server")
            return False

    # used for creating the popup message for missing input information
    def CreateErrorMessage(self):
        if not isinstance(self.WhatsLeft[0], list):
            text = "Please fill up the missing information:\n" + ", ".join(self.WhatsLeft)
        else:
            text = 'This name of this task already exists in the groups you associated it with:\n' + ', '.join(
                self.WhatsLeft[0])

        CreatePopupMsg("Error!", text)
