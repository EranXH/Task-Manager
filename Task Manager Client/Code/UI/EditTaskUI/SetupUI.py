from Code.Widgets.BuiltInWidgets import *
from Code.Widgets.ComplexWidgets import CheckListWidget
from Code.UI.EditTaskUI.SetupSelectionWidgets import NTSelectionWidgets
from Code.UI.InheritableObjects import OrganizeDFValues
import Code.UI.EditTaskUI.Functions as Func
from Code.Widgets.AnimatedWidget.Toggle import Toggle

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from PyQt5 import QtCore, QtWidgets
from pandas import DataFrame
from icecream import ic


class SetupUI(NTSelectionWidgets, OrganizeDFValues):
    def __init__(self, Task, TreeDFs, TasksDFs, PAPUserOptions, PrivateOrPublic, TaskID):
        OrganizeDFValues.Organize(self, TasksDFs, TreeDFs, PrivateOrPublic)

        # set a known task id if a task id was not given
        self.TaskID = TaskID if TaskID is not None else 999

        # readjust the window to fit the task edit window format
        self.EditTask = AdjustMainWindow(Task, 'EditTask', 'Edit Task', (806, 563), True, False,
                                         QtWidgets.QTabWidget.Rounded)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.EditTask.sizePolicy().hasHeightForWidth())

        self.EditTask.setSizePolicy(sizePolicy)
        self.EditTask.setFont(GetFont(14))

        # creating a new central widget
        self.EditTaskWidgets = CreateLayoutWidget(None, 'EditTaskWidgets')

        self.EditTaskTitle = Func.SetupTitle(self.EditTaskWidgets)

        self.NameLabel = CreateLabel(self.EditTaskWidgets, 14, 'Name:', 'NameLabel',
                                     GeometryRect=QtCore.QRect(20, 80, 100, 40))

        self.NameInput = CreateLineEdit(self.EditTaskWidgets, 'NameInput', '', 12,
                                        MaxLength=13, GeometryRect=QtCore.QRect(130, 80, 200, 40))
        self.NameInput.setClearButtonEnabled(True)

        # setup schedule input
        self.ScheduledLabel = CreateLabel(self.EditTaskWidgets, 14, 'Scheduled:', 'ScheduledLabel',
                                          GeometryRect=QtCore.QRect(20, 186, 120, 40))
        self.ScheduledToggle = Toggle(window=self.EditTask, start_pos=True, toggle_pos=(155, 176), toggle_size=(80, 65))
        DueToTime = datetime.now().strftime('%H:%M')
        DueToDate = (date.today() + relativedelta(days=1)).strftime('%Y/%m/%d')
        self.ScheduledInput = CreateDateTimeEdit(self.EditTaskWidgets, QtCore.QRect(20, 244, 240, 40), DueToDate,
                                                 DueToTime, "ScheduledInput", "dd/MM/yyyy        HH:mm")
        self.ScheduledOffLine = CreateLineEdit(self.EditTaskWidgets, 'ScheduledOffLine', 'Scheduled Is Turned Off', 13,
                                               Hide=True, GeometryRect=QtCore.QRect(20, 244, 240, 40))
        self.ScheduledOffLine.setAlignment(QtCore.Qt.AlignCenter)

        # setup private or public toggle
        self.PrivateTaskLabel = CreateLabel(self.EditTaskWidgets, 14, f'{PrivateOrPublic} Task', 'PrivateTaskLabel',
                                            GeometryRect=QtCore.QRect(20, 134, 120, 40))
        self.PrivateTaskToggle = Toggle(window=self.EditTask, start_pos=PrivateOrPublic == "Private",
                                        toggle_pos=(155, 124), toggle_size=(80, 65))

        # adding the NameInput widget after the PrivateTaskToggle, so it will be above it
        self.EditTask.layout().addWidget(self.NameInput)

        # creating all the selection tabs - assign and incharge users, type selection and association tree widget
        SelectionTab = CreateTab(self.EditTaskWidgets, 'SelectionTab', QtWidgets.QTabWidget.Triangular, True,
                                 GeometryRect=QtCore.QRect(20, 303, 366, 240))  # 340 # 26

        IDToRouteDicts = (self.PrivateIDToRouteDict, self.PublicIDToRouteDict)
        SelectionTabsFrameRect = QtCore.QRect(-2, -2, 368, 210)
        SelectionTabsScrollRect = QtCore.QRect(12, 50, 346, 150)
        SelectionTabsSCWRect = QtCore.QRect(0, 0, 326, 170)     # SCWRect stands for Scroll Contents Widget Rect
        SelectionTabsLabelRect = QtCore.QRect(12, 7, 346, 40)
        NTSelectionWidgets.__init__(self, SelectionTab, SelectionTabsFrameRect, SelectionTabsScrollRect,
                                    SelectionTabsSCWRect, SelectionTabsLabelRect, PAPUserOptions,
                                    TasksDFs, TreeDFs, IDToRouteDicts, self.TaskID)

        self.PublicForbiddenNamesCheck = lambda new_name: self.PrivateOrPublic == "Public" and \
                                                          new_name not in self.PublicAssociateTab.ForbiddenNames
        self.PrivateForbiddenNamesCheck = lambda new_name: self.PrivateOrPublic == "Private" and \
                                                           new_name not in self.PublicAssociateTab.ForbiddenNames

        # shifts to the correct position acording to the toggle
        self.SelectionWidgetsEvent(self.PrivateTaskToggle)
        # self.SelectionWidgets = NTSelectionWidgets(SelectionTab, SelectionTabsFrameRect, SelectionTabsScrollRect,
        # SelectionTabsScrollContentsRect, SelectionTabsLabelRect,
        # PAPUserOptions, TasksDFs, TreeDFs, self)

        self.TextTab = CreateTab(self.EditTaskWidgets, 'TextTab', QtWidgets.QTabWidget.Triangular, True,
                                 GeometryRect=QtCore.QRect(416, 80, 370, 320))

        # Create the CheckList tab
        self.CheckListTab = CreateLayoutWidget(None, 'CheckListTab')
        self.CheckListFrame = CreateFrame(self.CheckListTab, 'CheckListFrame',
                                          Shape=QtWidgets.QFrame.Box, Shadow=QtWidgets.QFrame.Raised,
                                          LineWidth=2, MidLineWidth=0, GeometryRect=QtCore.QRect(-2, -2, 370, 290))
        self.CheckListLabel = CreateLabel(self.CheckListFrame, 10, 'Creat a cheacklist for your new task',
                                          'CheckListLabel', WordWrap=True, GeometryRect=QtCore.QRect(10, 0, 290, 40))

        layout_widget = CreateLayoutWidget(self.CheckListFrame, 'LayoutWidget',
                                           GeometryRect=QtCore.QRect(306, 7, 61, 31))
        self.CheckListPMLayout = CreateHorizontalLayout(layout_widget, 2, "CheckListPMLayout")

        self.MinusButton = CreateButton(None, "", 0, "MinusButton",
                                        Layout=self.CheckListPMLayout, MaxSize=(24, 24),
                                        Icon="Files/PNG/MinusButton.png")
        self.PlusButton = CreateButton(None, "", 0, "PlusButton",
                                       Layout=self.CheckListPMLayout, MaxSize=(24, 24),
                                       Icon="Files/PNG/PlusButton.png")

        self.CheckListWidget = CheckListWidget()
        self.CheckListWidget.SetUp(self.CheckListFrame, QtCore.QRect(10, 40, 350, 240))

        self.TextTab.addTab(self.CheckListTab, "CheckList")

        # Create the Description tab
        self.DescriptionTab = CreateLayoutWidget(None, 'DescriptionTab')
        self.DescriptionFrame = CreateFrame(self.DescriptionTab, 'DescriptionFrame',
                                            Shape=QtWidgets.QFrame.Box, Shadow=QtWidgets.QFrame.Raised,
                                            LineWidth=2, MidLineWidth=0,GeometryRect=QtCore.QRect(-2, -2, 370, 290))
        self.DescriptionLabel = CreateLabel(self.DescriptionFrame, 10, 'Describe your new task', 'DescriptionLabel',
                                            WordWrap=True, GeometryRect=QtCore.QRect(10, 0, 290, 40))
        self.DescriptionInput = CreateTextEdit(self.DescriptionFrame, QtCore.QRect(10, 40, 350, 240),
                                               12, 'DescriptionInput')
        self.TextTab.addTab(self.DescriptionTab, "Description")

        self.CancelSaveInput = CreateDialogButtonBox(self.EditTaskWidgets, QtCore.Qt.LeftToRight, "CancelSaveInput",
                                                     'Cancel', 'Save', geometry_rect=QtCore.QRect(416, 445, 370, 60))

        self.EditTask.setCentralWidget(self.EditTaskWidgets)

    # the function would be call when a task was chosen to be edited - enters the edited task values
    def EnterValuesForEdit(self, task_df, check_list, func_for_check_list_item):
        # arranging the check-list-items
        self.CheckListWidget.RemoveAllItems()
        for item_id, item_values in check_list.items():
            text, state = item_values[0], item_values[1]
            self.CheckListWidget.AddItem(item_id, state, text, func_for_check_list_item)
        func_for_check_list_item()      # recalculate the progress value base on the new checklist items

        # arranging the task: name, description and changing the title to "Edit Task"
        task_name = task_df["name"][0]
        self.NameInput.setText(task_name)
        self.DescriptionInput.setText(task_df["description"][0])
        self.EditTaskTitle.setText('Edit Task')

        # fill the selection widget to fit the edited task
        self.InchargeWidget.SelectByName(task_df["incharge_users"][0])
        self.AssignWidget.SelectByName(task_df["assigned_users"][0])

        if self.PrivateOrPublic == "Public":
            self.PublicTypeTab.Widget.SelectByName(task_df["types"][0])
        else:
            self.PrivateTypeTab.Widget.SelectByName(task_df["type"][0])

        # if a task has no schedule - fit the widget
        # yet to be implemented
        if task_df["has_schedule"][0]:
            # TODO: change the time to fit what is writen in the task
            pass
