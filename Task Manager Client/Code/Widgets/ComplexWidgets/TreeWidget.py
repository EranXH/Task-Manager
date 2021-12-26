from PyQt5 import QtWidgets
from Code.Widgets.BuiltInWidgets.Functions import GetFont
from Code.PandasFunctions import GetIdxListFromValuesList, GetDataFrameFromIndexes, ReplaceValuesByIndex
from Code.Widgets.ComplexWidgets.TreeItemWidget import TreeItemWidget


# the tree-widget object
class TreeWidget(QtWidgets.QTreeWidget):
    # setup
    def __init__(self, Window, GeometryRect, ColumnCount, ColumnList, FontSize, IsUserCheckable):
        super().__init__(Window)
        self.setGeometry(GeometryRect)
        self.setColumnCount(ColumnCount)
        self.setHeaderLabels(ColumnList)
        self.setUniformRowHeights(False)
        header = self.header()
        # header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.setFont(GetFont(FontSize))
        self.setStyleSheet("QTreeWidget::item {margin: 2px 0;}")

        self.IsUserCheckable = IsUserCheckable
        self.Items = {}
        self.EditableItems = []

    # Arange the Tree Dictionary and the Items object from the CreatTreeItem function
    def AddItems(self, TreeDF, TasksDF, editable_items_routes_list):
        self.TreeDF = TreeDF
        self.editable_items_routes_list = editable_items_routes_list

        for row_index in range(self.TreeDF.shape[0]):
            tree_row_values = self.TreeDF.iloc[row_index]

            locationRoute = tree_row_values['URL']
            IDs_list = tree_row_values['IDs']

            if not TasksDF.empty:
                task_index_list = GetIdxListFromValuesList(TasksDF, IDs_list, '_id')
            else:
                task_index_list = []

            self.AddItems_InnerLoop(task_index_list, IDs_list, locationRoute, TasksDF)

        self.show()

    # for clearty - moved the inner loop of adding an item to a sepeeret function
    def AddItems_InnerLoop(self, task_index_list, IDs_list, locationRoute, TasksDF):
        # for each route - run a for loop on all the tasks
        for (task_index, task_ID) in zip(task_index_list, IDs_list):
            task_index = int(task_index)

            task_row_value = TasksDF.iloc[task_index]

            name = task_row_value['name']
            progress = task_row_value['progress']

            if locationRoute == 'root/':
                parent = self
                is_first = True

            else:
                if locationRoute in self.Items:
                    parent = self.Items[locationRoute]
                    is_first = False

                else:
                    parent = self
                    is_first = True

            completeRoute = f"{locationRoute}/{task_ID}"

            # creating a task item and fitting it to its complete route in the items dict
            Item = TreeItemWidget(self, is_first, parent, task_ID, name, progress, locationRoute)
            self.Items[completeRoute] = Item

            # adds all items that there id is the same id as the editable task id - checked base on item route
            # when treewidget is used not for the EditTaskUI enter editable_items_routes_list as an empty list ([])
            if completeRoute in self.editable_items_routes_list:
                self.EditableItems.append(Item)

    # remove all the items from the tree - widget
    def RemoveItems(self):
        root = self.invisibleRootItem()
        for key_route in [*self.Items]:
            tree_item = self.Items[key_route]
            (tree_item.parent() or root).removeChild(tree_item)

            # making sure that the attr is not being called for deletion when it has already been deleted
            if hasattr(tree_item, "ProgressBar"):
                tree_item.ProgressBar.deleteLater()     # delete the pyqt5 object
                delattr(tree_item, "ProgressBar")       # delete the attr from the tree_item object

            del tree_item

    # Show the selected Tree Leave
    def DisplaySelectedLeavesEvent(self, ParentClass, ListWidget, TreeDF, TasksDF):
        SelectedOption = ListWidget.selectedItems()[0].text()
        ParentClass.EditSelectedIndex = None

        if SelectedOption != 'Everything':
            selected_option_id = ParentClass.MainLeavesList[SelectedOption]

            tree_groups = TreeDF.groupby('URL')
            all_routes_names = list(tree_groups.groups)

            leave_route_wtn = "root"  # wtn stands for (W - without | T - Tasks | N - Name)
            leave_route = f"{leave_route_wtn}/{selected_option_id}/"
            relevent_routes = [route for route in all_routes_names
                                    if leave_route in route]

            relevent_routes.insert(0, leave_route[:-1])
            relevent_routes.insert(0, leave_route_wtn)

            relevent_indexs = GetIdxListFromValuesList(TreeDF, relevent_routes, 'URL')

            self.DisplayedTreeDF = GetDataFrameFromIndexes(TreeDF, relevent_indexs)
            self.DisplayedTreeDF = ReplaceValuesByIndex(self.DisplayedTreeDF, relevent_indexs[0],
                                                        'IDs', [selected_option_id])

        else:
            self.DisplayedTreeDF = TreeDF

        if not self.DisplayedTreeDF.equals(self.TreeDF):
            self.RemoveItems()
            self.AddItems(self.DisplayedTreeDF, TasksDF, [])

            ParentClass.TasksTreeItems = self.Items
