from PyQt5 import QtCore, QtWidgets, Qt, QtGui
from PyQt5.QtCore import QPropertyAnimation, QAnimationGroup, QAbstractAnimation

from Code.Widgets.ComplexWidgets import CheckListWidget
from Code.Widgets.BuiltInWidgets import *
from Code.Widgets.AnimatedWidget import ProgressBar
from Code.GlobalFunctions import TimeDateToPercentageOfPassedTime
from Code.APIRequests.APIGetRequests import RGet_CheckListItems
from Code.Widgets.ComplexWidgets.TasksListWidget.ItemWidget import ItemWidget
from Code.PandasFunctions import ReplaceValuesByIndex
from Code.APIRequests.APIPostRequests import RPost_ForFoldableTask
from PyQt5.QtGui import QPainter

from icecream import ic
import copy
import traceback


# a foldable item widget (item for "TasksListWidget")
class FoldableItemWidget(ItemWidget):
    # setting up the new item widget
    def __init__(self, tasks_list_widget, row, df_index, types):
        super().__init__(tasks_list_widget, row["name"])

        self.ID = row["_id"]
        self.DFIndex = df_index

        self.Description = row["description"]
        self.Progress = row["progress"]
        self.Types = types

        self.DueDate = row["due_date"]
        self.DueTime = row["due_time"].split(':')
        self.AssignedDate = row["assigned_date"]
        self.AssignedTime = row["assigned_time"].split(':')

        self.IsFolded = True
        self.wasCheckListUpdatedByServer = False

        self.UnFoldSize = 325
        self.FoldSize = self.height()

        self.setProperty("FoldSize", self.height())

        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setStyleSheet("QFrame#TaskFrame {border: 2px solid gray; border-radius: 8px;}")

        StartX = self.TasksListWidget.ItemsPixWidth - 10 - 150
        calculated_progress = ProgressBar.CalculateProgress(self.Progress)
        self.ProgressBar = ProgressBar(self, calculated_progress, 'TaskItemProgressBar',
                                       GeometryRect=QtCore.QRect(StartX, 4, 150, 32))

    # changing the double click event - show cause the item to fold or unfold
    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.button() == QtCore.Qt.LeftButton:
            self.TasksListWidget.PresenterTaskEvent(self)

    # changing the mouse pressed event - show as selected
    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.button() == QtCore.Qt.LeftButton:
            self.TasksListWidget.SavePreviouslySelectedItem(self)

    # setting up the unfold animation
    def UnFold(self, get_private_or_public):
        self.GetPrivateOrPublic = get_private_or_public
        # self.TaskIndex = TaskIndex

        self.CheckListDict = RGet_CheckListItems(self.GetPrivateOrPublic(), self.ID, self.TasksListWidget.UserID)

        self.CheckList = copy.deepcopy(self.CheckListDict)  # self.CheckListDict['items']
        self.CheckList.pop("_id")

        self.CheckListTitle = CreateLabel(self, 10, 'CheckList:', 'CheckListTitle',
                                          WordWrap=True, GeometryRect=QtCore.QRect(10, 40, 100, 30))

        self.CheckListTitle.setFont(GetFont(10, 'Aharoni'))

        self.CheckListFrame = CreateFrame(self, 'CheckListFrame',
                                          Shape=QtWidgets.QFrame.StyledPanel, Shadow=QtWidgets.QFrame.Plain,
                                          LineWidth=2, MidLineWidth=0, GeometryRect=QtCore.QRect(10, 65, 300, 0))
        self.CheckListFrame.setStyleSheet("QFrame#CheckListFrame {border: 2px solid gray; border-radius: 16px;}")
        self.CheckListFrame.raise_()
        self.CheckListFrame.show()

        self.CheckListWidget = CheckListWidget()
        self.CheckListWidget.SetUp(self, QtCore.QRect(10, 65, 300, 0))
        self.CheckListWidget.setStyleSheet("QFrame#CheckListWidget {border: 2px solid gray; border-radius: 16px;}")
        for item_id, item_values in self.CheckList.items():
            text, state = item_values[0], item_values[1]
            self.CheckListWidget.AddItem(item_id, state, text, self.ProgressAnimationAttribute)

        # update the progress bar
        self.ProgressAnimationAttribute()

        painter = QtGui.QPainter(self.CheckListWidget)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # color = self.property("color")
        painter.setPen(Qt.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(125, 106, 224, 100), Qt.Qt.SolidPattern))
        painter.drawRoundedRect(QtCore.QRect(10, 65, 300, 0), 16, 16)
        # self.CheckListWidget.hide()

        self.DescriptionTitle = CreateLabel(self, 10, 'Description:', 'DescriptionTitle',
                                            WordWrap=True, GeometryRect=QtCore.QRect(320, 40, 100, 30))

        self.DescriptionTitle.setFont(GetFont(10, 'Aharoni'))

        self.DescriptionText = CreateLabel(self, 12, self.Description, 'DescriptionText',
                                           WordWrap=True, GeometryRect=QtCore.QRect(320, 65, 240, 150),
                                           FrameShape=QtWidgets.QFrame.Box)
        self.DescriptionText.setAlignment(QtCore.Qt.AlignTop)
        self.DescriptionText.setStyleSheet("QFrame#DescriptionText {border: 2px solid gray; border-radius: 16px;}")

        # setting the key as the id of the item because the same task may have two or more items
        # so the task id cannot be used
        self.TasksListWidget.UnFoldedTasks[id(self)] = self
        self.TasksListWidget.UnFoldedItemID = id(self)

        self.IsFolded = False

        self.UnFoldAnimation = QPropertyAnimation(self, b"FoldSize")
        self.UnFoldAnimation.setEndValue(self.UnFoldSize)
        self.UnFoldAnimation.setDuration(500)
        self.UnFoldAnimation.valueChanged.connect(self.AnimationValueChangeEvent)
        self.UnFoldAnimation.finished.connect(self.UnFoldAnimationFinished)
        self.UnFoldAnimation.start()

    # on unfold animation finish
    def UnFoldAnimationFinished(self):
        self.setFixedHeight(self.property("FoldSize"))

    # during the item unfolding animation - updating the total pixcel length of all the items together
    #                                       and updating the hight of the widget inside the item
    def AnimationValueChangeEvent(self):  # when the size hint change the frame jumps left as if there is no scroll
        delta = self.property("FoldSize") - self.height()

        self.setFixedHeight(self.property("FoldSize"))

        for_unfold_animation = 70 <= self.height() and self.CheckListWidget.height() < 250
        for_fold_animation = self.height() <= 318 and self.CheckListWidget.height() > 0

        if for_unfold_animation or for_fold_animation:
            height = self.CheckListWidget.height() + delta
            if height > 250:
                height = 250

            self.CheckListWidget.setFixedHeight(height)
            self.CheckListFrame.setFixedHeight(height)

        self.TasksListWidget.ItemsPixLength.value += delta

        if self.height() > 235 and not hasattr(self, 'PassedTimeProgressBar'):
            self.SetUpPassedTimeProgressBar()

    # modifing the progressBar animation widget to fit the needs of a date based progress bar - setup
    def SetUpPassedTimeProgressBar(self):
        PercentageOfPassedTime = TimeDateToPercentageOfPassedTime(self.AssignedDate, self.AssignedTime,
                                                                  self.DueDate, self.DueTime)
        self.PassedTimeProgressBar = ProgressBar(self, PercentageOfPassedTime, 'PassedTimeProgressBar',
                                                 GeometryRect=QtCore.QRect(365, 240, 150, 32))
        self.PassedTimeProgressBar.show()
        self.PassedTimeProgressBar.Animation.finished.connect(self.PassedTimeProgressBarAnimationFinished)

        title = 'Due to: ' + self.DueDate + '  ' + ":".join(self.DueTime)
        self.TimeTitle = CreateLabel(self, 12, title, 'TimeTitle',
                                     GeometryRect=QtCore.QRect(320, 270, 240, 30))
        self.TimeTitle.setAlignment(QtCore.Qt.AlignCenter)

    # modifing the progressBar animation widget to fit the needs of a date based progress bar - animation finished event
    def PassedTimeProgressBarAnimationFinished(self):
        if self.PassedTimeProgressBar.value() >= 100:
            self.PassedTimeProgressBar.setFormat('Expiered')
            self.PassedTimeProgressBar.setStyleSheet("QProgressBar{border-radius: 5px; border-color: black;}"
                                                     "QProgressBar::chunk {border-radius :5px} "
                                                     "QProgressBar::chunk {background-color: red;}")

    # setting up the fold animation for the item
    def Fold(self):
        # self.setMinimumSize(QtCore.QSize(self.width(), self.FoldSize))

        self.FoldAnimation = QPropertyAnimation(self, b"FoldSize")
        self.FoldAnimation.setEndValue(self.FoldSize)
        self.FoldAnimation.setDuration(500)  # recommended 500
        self.FoldAnimation.valueChanged.connect(self.AnimationValueChangeEvent)
        self.FoldAnimation.start()
        self.FoldAnimation.finished.connect(self.FoldAnimationFinished)

    # removing all unused values on fold animation finish
    def FoldAnimationFinished(self):
        self.DeleteAllAttributes()

        self.setFixedHeight(self.FoldSize)

        self.IsFolded = True

        tasks_df = self.TasksListWidget.GetTasksDF()
        task_dict = tasks_df.iloc[self.DFIndex].to_dict()

        del self.TasksListWidget.UnFoldedTasks[id(self)]

        RPost_ForFoldableTask(self.TasksListWidget.GetPrivateOrPublic(), True,
                              task_dict, self.CheckListDict, self.TasksListWidget.UserID)
        # RPost_AfterFoldTask(self.TasksListWidget.GetPrivateOrPublic(), task_dict, self.CheckListDict,
        # self.TasksListWidget.UserID)

    # the function is called mostly from the "CheckListItemWidget"
    # (called from the unfolding function once to check that the progress is updated and fit to the got checklist)
    # when checking a box to one of the item the task total progress is changing - activating the change animation
    def ProgressAnimationAttribute(self):
        if hasattr(self, 'ProgressBarAnimation'):
            if self.ProgressBar.value() > 100:
                self.ProgressBar.AnimationFinishedEvent(self.ProgressBar.value() / 100)

        AmountOfCheckedItems = self.CheckListWidget.GetAmountOfCheckedItems()
        AmountOfItems = self.Progress[1]

        # check if the progress was realy changed
        if self.Progress != [AmountOfCheckedItems, AmountOfItems]:
            self.updateProgressBar([AmountOfCheckedItems, AmountOfItems])
            # update the progress value in the local TasksDF (DatatFrame)
            self.updateTasksDFProgress()
            # update the progress value and the progress bar in all the other item widgets
            self.updateItemsWidgetsProgress()

            if hasattr(self, "CheckList"):
                # update the checklist list object
                self.CheckList = self.CheckListWidget.GetItemsDict()
                # updating the Checklist dict object (which includs the ID)
                self.CheckListDict.update(self.CheckList)

                if not self.wasCheckListUpdatedByServer:

                    tasks_df = self.TasksListWidget.GetTasksDF()
                    task_dict = tasks_df.iloc[self.DFIndex].to_dict()

                    RPost_ForFoldableTask(self.TasksListWidget.GetPrivateOrPublic(), False,
                                          task_dict, self.CheckListDict, self.TasksListWidget.UserID)

                    # RPost_UpdateCheckList(self.TasksListWidget.GetPrivateOrPublic(),
                    # self.TasksListWidget.UserID, self.CheckListDict)
                else:
                    self.wasCheckListUpdatedByServer = False

    # on deletion on the item or on task folding - makes sure that all animation have been deleted properly
    def DeleteAllAnimations(self):
        if hasattr(self, 'ProgressBarAnimation'):
            self.ProgressBar.Animation.stop()
            del self.ProgressBarAnimation
            self.ProgressBar.AnimationFinishedEvent(self.Progress)

        self.FoldAnimationFinished()

    # on deletion on the item or on task folding - makes sure that all attributes have been deleted properly
    def DeleteAllAttributes(self):
        if hasattr(self, 'FoldAnimation'):
            self.FoldAnimation.stop()

        if hasattr(self, 'UnFoldAnimation'):
            self.UnFoldAnimation.stop()

        if hasattr(self, 'DescriptionText'):
            self.DescriptionTitle.deleteLater()
            del self.DescriptionTitle
            self.DescriptionText.deleteLater()
            del self.DescriptionText

        if hasattr(self, 'CheckListWidget'):
            self.CheckListTitle.deleteLater()
            del self.CheckListTitle
            self.CheckListWidget.RemoveAllItems()
            self.CheckListWidget.deleteLater()
            del self.CheckListWidget

        if hasattr(self, 'PassedTimeProgressBarAnimation'):
            self.PassedTimeProgressBarAnimation.stop()
            self.PassedTimeProgressBar.deleteLater()
            del self.PassedTimeProgressBar
            self.TimeTitle.deleteLater()
            self.TimeTitle.show()
            del self.TimeTitle

    # updates the local TasksDF (DataFrame)
    def updateTasksDFProgress(self):
        AmountOfCheckedItems = self.CheckListWidget.GetAmountOfCheckedItems()
        AmountOfItems = self.Progress[1]
        progress = [AmountOfCheckedItems, AmountOfItems]

        self.TasksListWidget.UpdateTasksDF(ReplaceValuesByIndex(self.TasksListWidget.GetTasksDF(), self.DFIndex,
                                                                "progress", progress))

    # when checking an item checklist item - makes sure that all progressbars of the same item are updated
    # a task can be represented more the one time
    def updateItemsWidgetsProgress(self):
        type_item_widgets_dict, schedule_item_widgets_dict = self.TasksListWidget.GetWidgetsDict()

        task_items = [schedule_item_widgets_dict[self.ID], *type_item_widgets_dict[self.ID].values()]

        for task_item in task_items:
            task_item.updateProgressBar(self.Progress)

    # updated the item check list - only called for unfolded items
    # when updating the status the progress would be updated athumaticle from the statuse change event
    def updateCheckListItem(self, item_id: str, item_value: [str, int]):
        if hasattr(self, "CheckListWidget"):
            item_index = self.CheckListWidget.ItemsOccupiedIds.index(item_id)
            item = self.CheckListWidget.ItemsArrangementList[item_index]
            item.updateText(item_value[0])

            if item.GetStatus() != item_value[1]:
                self.wasCheckListUpdatedByServer = True
                item.updateStatus(item_value[1])
            else:
                # update the checklist list object
                self.CheckList = self.CheckListWidget.GetItemsDict()
                # updating the Checklist dict object (which includs the ID)
                self.CheckListDict.update(self.CheckList)

    # updated the object Progress value and the ProgressBar object based on the TasksDF
    # def updateItemFoldedProgressBar(self, new_value: list[int, int]):
    def updateProgressBar(self, new_value: list[int, int]):
        if new_value != self.Progress:  # and self.IsFolded:
            calculated_progress = self.ProgressBar.CalculateProgress(new_value)
            self.ProgressBar.ProgressAnimation(calculated_progress)
            self.Progress = new_value

    # updated the object Name value based on the TasksDF
    def updateName(self, new_name: str):
        if new_name != self.Name:
            self.Label.setText(new_name)
            self.Name = new_name

    # updating the task description - when got an update from the server
    def updateDescription(self, new_description: str):
        if new_description != self.Description:
            self.Description = new_description

            if hasattr(self, "DescriptionText"):
                self.DescriptionText.setText(self.Description)

    # update the item types - only for items from the date soreted list
    # if the item is in the type sorted list a new item sould be inserted in the right place
    # (almost all the needed function exsist just need to connect to type change)
    def updateTypes(self, new_types: list[str]):
        if isinstance(new_types, list) and new_types != self.Types:
            self.Types = new_types

    # updating the task due or assigned dates - when got an update from the server
    def updateDate(self, dueORassigned: str, new_date: str):
        if new_date != getattr(self, f"{dueORassigned}Date"):
            setattr(self, f"{dueORassigned}Date", new_date)
            self.updateTimeWidgets(dueORassigned)

    # updating the task due or assigned time - when got an update from the server
    def updateTime(self, dueORassigned: str, new_time: str):
        if new_time != getattr(self, f"{dueORassigned}Time"):
            setattr(self, f"{dueORassigned}Time", new_time.split(':'))
            self.updateTimeWidgets(dueORassigned)

    # after any change in the time of date update the time passed progressbar
    # after change in the due time or date update the text of the widget
    def updateTimeWidgets(self, dueORassigned: str):
        if hasattr(self, "TimeTitle"):
            if dueORassigned == "Due":
                title = 'Due to: ' + self.DueDate + '  ' + ":".join(self.DueTime)
                self.TimeTitle.setText(title)

            PercentageOfPassedTime = TimeDateToPercentageOfPassedTime(self.AssignedDate, self.AssignedTime,
                                                                      self.DueDate, self.DueTime)
            self.PassedTimeProgressBar.ProgressAnimation(PercentageOfPassedTime)

    # setting up the insert or remove animation of a task to a shown task widget list
    def InsertOrRemoveTask(self, insert_or_remove: str, insert_index=0):
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setStyleSheet("QFrame#TaskFrame {border: 0px solid gray; border-radius: 8px;}")

        # setting valuse based on "insert_or_remove" command
        if insert_or_remove == "Insert":
            start_x_pos = self.TasksListWidget.ItemsPixWidth
            task_animation_end_value = 0
            task_frame_height = self.height()
            self.TasksListWidget.ItemsPixLength.value -= task_frame_height
            space_animation_end_value = task_frame_height
            self.setFixedHeight(0)
            self.setProperty("FoldSize", 0)
            self.Insert(insert_index)

        else:
            start_x_pos = 0
            task_animation_end_value = -self.TasksListWidget.ItemsPixWidth
            space_animation_end_value = 0
            task_frame_height = self.height()

        print(self.TasksListWidget.ItemsPixLength.value)

        # setting up the animation and all the relevent widget
        self.AnimationTaskFrame = CreateFrame(self, 'RemoveTaskFrame', Shape=QtWidgets.QFrame.Box,
                                              Shadow=QtWidgets.QFrame.Raised, LineWidth=2, MidLineWidth=0,
                                              FixedSize=QtCore.QSize(self.TasksListWidget.ItemsPixWidth,
                                                                     task_frame_height),
                                              GeometryRect=QtCore.QRect(start_x_pos, 0,
                                                                        self.TasksListWidget.ItemsPixWidth,
                                                                        task_frame_height))

        self.AnimationTaskFrame.setStyleSheet("QFrame#RemoveTaskFrame {border: 2px solid gray; border-radius: 8px;}")

        self.AnimationTaskFrame.setProperty("Position", start_x_pos)
        self.AnimationTaskFrame.show()

        self.Label.setParent(self.AnimationTaskFrame)
        self.Label.show()
        self.ProgressBar.setParent(self.AnimationTaskFrame)
        self.ProgressBar.show()

        self.TaskAnimation = QPropertyAnimation(self.AnimationTaskFrame, b"Position")
        self.TaskAnimation.setEndValue(task_animation_end_value)
        self.TaskAnimation.setDuration(300)
        self.TaskAnimation.valueChanged.connect(self.TaskAnimationValueChangeEvent)

        self.AnimationSeparator = True

        self.SpaceAnimation = QPropertyAnimation(self, b"FoldSize")
        self.SpaceAnimation.setEndValue(space_animation_end_value)
        self.SpaceAnimation.setDuration(200)
        self.SpaceAnimation.valueChanged.connect(self.SpaceAnimationValueChangeEvent)

        # starting from the right animation based on the "insert_or_remove" command
        if insert_or_remove == "Insert":
            self.SpaceAnimation.start()
            self.TaskAnimation.finished.connect(self.InsertAnimationFinishedEvent)
        else:
            self.TaskAnimation.start()
            self.SpaceAnimation.finished.connect(self.RemoveAnimationFinishedEvent)

    # on every change in the task "Position" property
    def TaskAnimationValueChangeEvent(self):
        x_pos = self.AnimationTaskFrame.property("Position")

        self.AnimationTaskFrame.setGeometry(x_pos, self.AnimationTaskFrame.y(),
                                            self.AnimationTaskFrame.width(), self.AnimationTaskFrame.height())

        # if the task is halfway out start the space removal animation
        if x_pos <= -self.TasksListWidget.ItemsPixWidth / 2.0 and self.AnimationSeparator:
            self.SpaceAnimation.start()
            self.AnimationSeparator = False

    # on every change in the task "FoldSize" property
    def SpaceAnimationValueChangeEvent(self):
        delta = self.property("FoldSize") - self.height()

        self.setFixedHeight(self.property("FoldSize"))

        if self in self.TasksListWidget.ItemsArrangementList:
            self.TasksListWidget.ItemsPixLength.value += delta

        # delta is bigger then 0 only if a task is being inserted
        # if the space is halfway open start the task insert animatiom
        if delta > 0 and self.height() >= self.SpaceAnimation.endValue() / 2.0 and self.AnimationSeparator:
            self.TaskAnimation.start()
            self.AnimationSeparator = False

    # when the command "insert_or_remove" is "Remove"
    # the space animation goes second - on finish of the space animation the hole remove animation is finished
    # the function is called when the Remove animation is finished
    def RemoveAnimationFinishedEvent(self):
        if self in self.TasksListWidget.ItemsArrangementList:
            self.TasksListWidget.ItemsArrangementList.remove(self)

        # after the hole task size was removed, remove the buffer between tasks items
        buffer = 2
        self.TasksListWidget.ItemsPixLength.value -= buffer

        # remove all the animation related and unused attrs
        self.DestroyIORTaskAnimation()

    # when the command "insert_or_remove" is "Insert"
    # the task animation goes second - on finish of the task animation the hole insert animation is finished
    # the function is called when the Insert animation is finished
    def InsertAnimationFinishedEvent(self):
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setStyleSheet("QFrame#TaskFrame {border: 2px solid gray; border-radius: 8px;}")

        # after the hole task size was added, add the buffer between tasks items
        buffer = 2
        self.TasksListWidget.ItemsPixLength.value += buffer

        self.Label.setParent(self)
        self.Label.show()
        self.ProgressBar.setParent(self)
        self.ProgressBar.show()

        self.show()

        # remove all the animation related and unused attrs
        self.DestroyIORTaskAnimation()

    # IOR - Insert Or Remove
    # Remove all the animation related and unused attrs
    def DestroyIORTaskAnimation(self):
        self.AnimationTaskFrame.hide()
        self.AnimationTaskFrame.deleteLater()
        delattr(self, "AnimationTaskFrame")
        self.SpaceAnimation.deleteLater()
        delattr(self, "SpaceAnimation")
        self.TaskAnimation.deleteLater()
        delattr(self, "TaskAnimation")
        delattr(self, "AnimationSeparator")
