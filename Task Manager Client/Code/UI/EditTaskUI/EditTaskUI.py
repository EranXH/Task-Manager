import time

from PyQt5 import QtCore
from functools import partial
from .SetupUI import SetupUI
from Code.Widgets.AnimatedWidget import ProgressBar
from Code.UI.InheritableObjects.DeleteAllWidgets import DeleteAllWidgets

from icecream import ic


# the window ui for editing or creating a task
class EditTaskUI(SetupUI, DeleteAllWidgets):
    # the SetUp for the NewTaskUI
    # called only on the first time the object is created - saves the users_id
    def __init__(self, UserID):
        self.UserID = UserID

    # boots the window complete ui
    def BootUI(self, EditTask, TreeDFs, TasksDFs, PAPUserOptions, PrivateOrPublic, TaskID):
        DeleteAllWidgets.__init__(self, 'EditTask')
        SetupUI.__init__(self, EditTask, TreeDFs, TasksDFs, PAPUserOptions, PrivateOrPublic, TaskID)
        self.CheckListWidget.AddItem(self.CheckListWidget.GetAvailableID(), 0, '', self.CL_PAA_TEI)

    # used for both private and public so no need for it to be an instence method
    @classmethod
    def GetTaskForbiddenRoutes(cls, IDToRouteDict, TaskID):
        try:
            return IDToRouteDict[TaskID]
        except KeyError:
            return []

    # Call all the background running events
    def Events(self):
        self.ScheduledToggle.clicked.connect(self.ScheduledEvent)

        self.PrivateTaskToggle.clicked.connect(self.PrivateTaskEvent)

        self.MinusButton.clicked.connect(self.MinusButtonEvent)  # self.CheckListWidget.RemoveItem)
        self.PlusButton.clicked.connect(self.PlusButtonEvent)   # partial(self.CheckListWidget.AddItem, 0, '', self.CL_PAA_TEI))

        # operate for every key press but does not work when the clear button is pressed
        self.NameInput.keyPressEvent = self.NameInputKeyPressEvent
        # allways active and only helps when the clear button is pressed
        self.NameInput.textChanged.connect(self.NameInputTextChangedEvent)

        # activate the private associate Tab
        PrivateForbiddenRoutes = self.GetTaskForbiddenRoutes(self.PrivateIDToRouteDict, self.TaskID)
        self.PrivateAssociateTab.TreeWidget.itemClicked.connect(partial(self.PrivateAssociateTab.TreeItemClickedEvent,
                                                                        PrivateForbiddenRoutes, self))

        # activate the public associate Tab
        PublicForbiddenRoutes = self.GetTaskForbiddenRoutes(self.PublicIDToRouteDict, self.TaskID)
        self.PublicAssociateTab.TreeWidget.itemClicked.connect(partial(self.PublicAssociateTab.TreeItemClickedEvent,
                                                                       PublicForbiddenRoutes, self))

    # a function the check if for every text change of the task text name input is empty
    # if it is empty - enter the "New Task" text
    def NameInputTextChangedEvent(self, text):
        if text == "":
            self.NameInput.setText(text)
            for item in self.TreeEditableItems:
                item.setText(0, "New Task")

    # the task name input text event - when a key is pressed the function is called
    # TODO: missing many shortcuts - should implement an event.acept like expression in the start
    def NameInputKeyPressEvent(self, KeyPress):
        text = self.NameInput.text()

        if KeyPress.key() != QtCore.Qt.Key_Backspace:
            new_text = text + KeyPress.text()

            if len(new_text) != self.NameInput.maxLength() and new_text != "New Task" and \
                    (self.PublicForbiddenNamesCheck(new_text) or self.PrivateForbiddenNamesCheck(new_text)):
                self.NameInput.setText(new_text)
            else:
                new_text = text

        else:
            new_text = text[:-1]
            self.NameInput.setText(new_text)

        if new_text == "":
            new_text = "New Task"

        for item in self.TreeEditableItems:
            item.setText(0, new_text)
            item.Name = new_text

    # Called From Code.CheckListItemPresenter
    # CL stands for CheckList
    # PAA stands for Progress Animation Attribute
    # TEI stands for Tree Editable Item
    # a function that is connected to the change in selected items in the newly created CeckList
    # when a change happen the proggress bar of the TreeEditableItem is animated to the right amount
    def CL_PAA_TEI(self):
        # if hasattr(self, 'ProgressBarAnimation'):
        if self.TreeEditableItems[0].ProgressBar.value() > 100:
            for item in self.TreeEditableItems:
                item.ProgressBar.AnimationFinishedEvent(item.ProgressBar.value()/100)

        AmountOfCheckedItems = self.CheckListWidget.GetAmountOfCheckedItems()
        AmountOfItems = len(self.CheckListWidget.ItemsArrangementList)
        CalculatedProgress = ProgressBar.CalculateProgress([AmountOfCheckedItems, AmountOfItems])
        for item in self.TreeEditableItems:
            item.ProgressBar.ProgressAnimation(CalculatedProgress)

    # on clicking the minus button is the check-list tab
    def MinusButtonEvent(self):
        self.CheckListWidget.RemoveItem()
        self.CL_PAA_TEI()

    # on clicking the plus button is the check-list tab
    def PlusButtonEvent(self):
        self.CheckListWidget.AddItem(self.CheckListWidget.GetAvailableID(), 0, '', self.CL_PAA_TEI)
        self.CL_PAA_TEI()

    # on clicking the private or public tuggle
    # Yet to be completly implemented
    def PrivateTaskEvent(self):
        if self.PrivateTaskToggle.isChecked():
            # define values
            self.PrivateTaskLabel.setText('Private Task')
            self.PrivateOrPublic = "Private"

        else:
            # define values
            self.PrivateTaskLabel.setText('Public Task')
            self.PrivateOrPublic = "Public"

        self.SelectionWidgetsEvent(self.PrivateTaskToggle)

        current_name = self.NameInput.text()
        if current_name:
            for item in self.TreeEditableItems:
                item.setText(0, current_name)
        else:
            for item in self.TreeEditableItems:
                item.setText(0, 'New Task')

        # update all the DFs and Optinal List values acording to the PrivateOrPublic value
        # Get_PoP_DFValues(self, self.PrivateOrPublic)
        # Get_IAT_OptionsValues(self, self.PrivateOrPublic)

    # Disabling the option to select date and time
    def ScheduledEvent(self):
        if self.ScheduledToggle.isChecked():
            self.ScheduledOffLine.hide()
            self.ScheduledInput.show()
        else:
            self.ScheduledOffLine.show()
            self.ScheduledInput.hide()
