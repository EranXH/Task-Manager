from PyQt5 import QtCore, QtWidgets, QtGui

from Code.UI.InheritableObjects import OrganizeDFValues
from Code.Widgets.ComplexWidgets import TreeWidget, TasksListWidget
from Code.PandasFunctions import GetIdxListFromValuesList, GetDataFrameFromIndexes
from Code.UI.MainUI.Functions import *


# boot the ui of the main page and define the values
class SetupUI(OrganizeDFValues):
    def __init__(self, TasksDFs, TreeDFs, PAPUserOptions, PrivateOrPublic, Main, UserID):
        OrganizeDFValues.Organize(self, TasksDFs, TreeDFs, PrivateOrPublic)
        self.PAPUserOptions = PAPUserOptions

        self.Main = AdjustMainWindow(Main, "MainWindow", "Main Window", (1100, 510), True, False,
                                     QtWidgets.QTabWidget.Rounded)

        self.MainWidget = CreateLayoutWidget(self.Main, "MainWidget")

        self.Background = CreateLabel(self.MainWidget, 12, '', 'Background',
                                      GeometryRect=QtCore.QRect(0, 0, 1100, 510), Show=False)

        self.Background = SetUpPalette(QtGui.QColor(225, 225, 225), QtGui.QPalette.Base, self.Background)

        # --- Tree Widget --- #

        self.TreeWidget = TreeWidget(self.MainWidget, QtCore.QRect(277, 0, 592, 510), 2, ['name', 'progress'], 12,
                                     False)

        self.TreeWidget.AddItems(self.TreeDF, self.TasksDF, [])

        self.TreeDF = self.TreeWidget.TreeDF
        self.TasksTreeItems = self.TreeWidget.Items

        try:
            IDsList = list(self.TreeDF.groupby('URL').get_group('root')['IDs'][0])
            IndexList = GetIdxListFromValuesList(self.TasksDF, IDsList, '_id')
            self.MainLeavesList = GetDataFrameFromIndexes(self.TasksDF, IndexList)['name'].to_list()
        except KeyError:
            IDsList = []
            self.MainLeavesList = []

        self.MainLeavesList.insert(0, 'Everything')
        IDsList.insert(0, 'root')
        self.MainLeavesList = dict(zip(self.MainLeavesList, IDsList))

        # --- List Widget --- #

        # self.CheckListWidget.setStyleSheet("QListWidget:item:hover {background-color:transparent;}")
        functions_dict = {"GetPrivateOrPublic": self.GetPrivateOrPublic,
                          "GetTasksDF": self.GetTasksDF, "UpdateTasksDF": self.UpdateTasksDF,
                          "GetWidgetsDict": self.GetWidgetsDict, "UpdateAfterTaskRemoved": self.UpdateAfterTaskRemoved,
                          "UpdateAfterTaskInsert": self.UpdateAfterTaskInsert}

        # when giving here self it will include the "MainUI" too
        self.TasksListWidget = TasksListWidget(self.MainWidget, QtCore.QRect(277, 0, 592, 510), UserID, functions_dict,
                                               self)

        if not self.TasksDF.empty:
            self.TypeItemWidgetsDict = CreateItemWidgetsDict(self.TasksListWidget, self.TasksDF, True)
            self.ScheduleItemWidgetsDict = CreateItemWidgetsDict(self.TasksListWidget, self.TasksDF, False)
        else:
            self.TypeItemWidgetsDict, self.ScheduleItemWidgetsDict = {}, {}

            # --- Left Layout --- #

        self.LeftVerticalLayoutWidget = CreateLayoutWidget(self.MainWidget, 'LeftVerticalLayoutWidget',
                                                           GeometryRect=QtCore.QRect(-1, 0, 272, 510))
        self.LeftVerticalLayout = CreateVerticalLayout(self.LeftVerticalLayoutWidget, 0, 'LeftVerticalLayout')

        # --- Task Search + Completer --- #

        # TODO: the completer isnt finished, it is not connected to any meaningful function
        self.TaskSearchLineEdit = CreateLineEdit(self.LeftVerticalLayoutWidget, 'TaskSearchLineEdit', 'Search Task:', 12,
                                                 MaxLength=13, Layout=self.LeftVerticalLayout)
        self.TaskSearchLineEdit = SetUpPalette(QtGui.QColor(225, 225, 225), QtGui.QPalette.Base,
                                               self.TaskSearchLineEdit)
        # check if TaskDF is not empty -> empty when user dosnt have any tasks
        if not self.TasksDF.empty:
            Completer = QtWidgets.QCompleter(self.TasksDF['name'].tolist())
        else:
            Completer = QtWidgets.QCompleter([])
        Completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.TaskSearchLineEdit.setCompleter(Completer)

        # --- Tabs --- #

        self.Tab = CreateTab(self.LeftVerticalLayoutWidget, 'Tab', QtWidgets.QTabWidget.Rounded, False)

        # --- Schedule Tab --- #

        self.ScheduleTab, self.ScheduleTabList = CreateTabsList(self.Tab, 'Schedule')

        self.UpdateScheduleObjects()

        # --- Type Tab --- #

        self.TypeTab, self.TypeTabList = CreateTabsList(self.Tab, 'Type')
        # self.TypeDictionary = CreateTypeDictionary(self.TasksDF)#self.TasksDF)

        self.UpdateTypeObjects()


        # --- Add Items to List Widget --- #
        self.TasksListWidget.AddItems(self.DateDictionary)

        # --- Relation Tab --- #

        self.RelationTab, self.RelationTabList = CreateTabsList(self.Tab, 'Relation')

        for place, leave in enumerate(self.MainLeavesList.keys()):
            self.RelationTabList.insertItem(place, leave)

        self.LeftVerticalLayout.addWidget(self.Tab)

        # --- Completed Button --- #

        self.CompletedButton = CreateButton(self.LeftVerticalLayoutWidget, 'Completed', 12, 'CompletedButton',
                                            Layout=self.LeftVerticalLayout)

        # --- Right Side --- #

        self.RightVerticalLayoutWidget = CreateLayoutWidget(self.MainWidget, 'RightVerticalLayoutWidget',
                                                            GeometryRect=QtCore.QRect(874, -3, 226, 120))
        self.RightVerticalLayout = CreateVerticalLayout(self.RightVerticalLayoutWidget, 0, 'RightVerticalLayout')

        self.EditTaskButton = CreateButton(None, 'Edit Task', 12, 'EditTaskButton',
                                           Layout=self.RightVerticalLayout)

        self.NewTaskButton = CreateButton(None, 'New Task', 12, 'NewTaskButton',
                                          Layout=self.RightVerticalLayout)

        self.DeleteTaskButton = CreateButton(None, 'Delete Task', 12, 'DeleteTaskButton',
                                             Layout=self.RightVerticalLayout)

        self.LeftLine = CreateFrame(self.MainWidget, 'LeftLine',
                                    Shape=QtWidgets.QFrame.VLine, Shadow=QtWidgets.QFrame.Sunken,
                                    LineWidth=0, MidLineWidth=5,
                                    GeometryRect=QtCore.QRect(266, 0, 16, 510))
        self.RightLine = CreateFrame(self.MainWidget, 'RightLine',
                                     Shape=QtWidgets.QFrame.VLine, Shadow=QtWidgets.QFrame.Sunken,
                                     LineWidth=0, MidLineWidth=5,
                                     GeometryRect=QtCore.QRect(863, 0, 16, 510))

        self.Main.setCentralWidget(self.MainWidget)

        self.Main.show()

    # all the functions below are using in the "TasksListWidget", "FoldableItemWidget"
    # they are used to gaining exsses to the MainUI instese attrbutes
    # a better way started to be implemented but the function are still in use
    # the function are self-explanatory, and do exactly as they are named

    def UpdateAfterTaskRemoved(self, task_id):
        del self.ScheduleItemWidgetsDict[task_id]
        self.UpdateScheduleObjects()

        del self.TypeItemWidgetsDict[task_id]
        self.UpdateTypeObjects()

    def UpdateAfterTaskInsert(self, ScheduleItemWidgetsDict, TypeItemWidgetsDict):
        self.ScheduleItemWidgetsDict = ScheduleItemWidgetsDict
        self.UpdateScheduleObjects()
        self.TypeItemWidgetsDict = TypeItemWidgetsDict
        self.UpdateTypeObjects()

    def UpdateScheduleObjects(self):
        self.DateDictionary, self.ScheduleTabListDictionary = SetUpDateDictionaries(self.TasksDF,
                                                                                    self.ScheduleItemWidgetsDict)

        UpdateScheduleTabList(self.ScheduleTabList, self.ScheduleTabListDictionary)

    def UpdateTypeObjects(self):
        # check if TaskDF is not empty -> empty when user dosnt have any tasks
        if not self.TasksDF.empty:
            self.TypeDictionary = CreateTypeDictionary(self.TasksDF, self.TypeItemWidgetsDict)
        else:
            self.TypeDictionary = {}

        self.TypeTabButtonsNames = UpdateTypeTabList(self.TypeTabList, self.TypeDictionary)

    def GetWidgetsDict(self):
        return self.TypeItemWidgetsDict, self.ScheduleItemWidgetsDict

    # used in FoldableItemWidget to get the updated value
    def GetPrivateOrPublic(self):
        return self.PrivateOrPublic

    def GetTasksDF(self) -> DataFrame:
        return self.TasksDF

    def UpdateTasksDF(self, TasksDF: DataFrame):
        self.TasksDF = TasksDF

