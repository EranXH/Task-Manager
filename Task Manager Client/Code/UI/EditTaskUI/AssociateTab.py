from PyQt5 import QtWidgets, QtCore
from ...Widgets.ComplexWidgets import TreeWidget, TreeItemWidget
from ...Widgets.BuiltInWidgets import *
from ...APIRequests.APIGetRequests import RGet_TreeBranches
import requests

from icecream import ic


# Associate Tab object allows to create tabs for both private and public options
# Used in the Task Editing window for both private and public Tree association tabs (private is yet to be implemeneted)
class AssociateTab(object):
    def __init__(self, TreeDF, TasksDF, PrivateOrPublic, SelectionTabsFrameRect, SelectionTabsLabelRect,
                 SelectionTab, SelectionTabsScrollRect, IDToRouteDict, TaskID):
        self.TreeDF, self.TasksDF = TreeDF.copy(), TasksDF.copy()

        self.TaskID = TaskID

        # when creating a route for a task in order to insert it to the tree it combins the route and the ID
        # if the route in '' (empty) the the combination would be just 'root'
        if PrivateOrPublic == 'Public':
            self.TreeDF.loc[-1] = ['', ["root"]]  # adding a row
            self.TreeDF.index += 1  # shifting index
            self.TreeDF = self.TreeDF.sort_index()  # sorting by index

        self.PrivateOrPublic = PrivateOrPublic

        self.TabName = 'Associate'

        # creating the main widgets
        self.Tab = CreateLayoutWidget(None, f"{self.PrivateOrPublic}AssociateTab")
        self.Frame = CreateFrame(self.Tab, f"{self.PrivateOrPublic}AssociateFrame",
                                 Shape=QtWidgets.QFrame.Box, Shadow=QtWidgets.QFrame.Raised,
                                 LineWidth=2, MidLineWidth=0, GeometryRect=SelectionTabsFrameRect)
        self.Label = CreateLabel(self.Frame, 10, 'Select tasks your new task should be associated with',
                                 f"{self.PrivateOrPublic}AssociateLabel", WordWrap=True,
                                 GeometryRect=SelectionTabsLabelRect)
        SelectionTab.addTab(self.Tab, self.TabName)

        self.TreeWidget = TreeWidget(self.Frame, SelectionTabsScrollRect, 2, ['name', 'progress'], 12, True)

        self.Setup(IDToRouteDict)

    def Setup(self, IDToRouteDict):
        # set a list that contains only the routes of the chosen task
        try:
            editable_items_routes_list = IDToRouteDict[self.TaskID]
        except KeyError:
            editable_items_routes_list = []

        # modify list - each route now includs the task id
        editable_items_routes_list = [f"{route_str}/{self.TaskID}" for route_str in editable_items_routes_list]

        # if the task is not in main root then add the option to select main root as a place for the task
        if f"root/{self.TaskID}" not in editable_items_routes_list:
            # TODO: make sure that both the location and the complete route are root
            TreeRootEditableItem = TreeItemWidget(self.TreeWidget, True, self.TreeWidget, "New Task",
                                                  "New Task", [0, 1], 'root')
            TreeRootEditableItem.SelectAndDeselectItem(0.5)

        self.ForbiddenNames = []
        self.OccupiedNamesByRoute = {}

        # adding all the items (task) in the user tree to the TreeWidget
        self.TreeWidget.AddItems(self.TreeDF, self.TasksDF, editable_items_routes_list)

        # aplaying the select effect on all the item that are placed where task already exsist
        self.RoutesList = []
        for editable_item in self.TreeWidget.EditableItems:
            editable_item: TreeItemWidget = editable_item

            editable_item.setCheckState(0, QtCore.Qt.Checked)
            editable_item.SelectAndDeselectItem(1)

            # adding all the editable items route to a list
            self.RoutesList.append(editable_item.locationRoute)

        if self.RoutesList:
            self.UpdateOccupiedNamesByRoute(self.RoutesList)
            self.UpdateForbiddenNames()

        # inserting the root editable task at the first pos
        if f"root/{self.TaskID}" not in editable_items_routes_list:
            if self.TreeWidget.EditableItems:
                name = self.TreeWidget.EditableItems[0].Name
                TreeRootEditableItem.setText(0, name)
            self.TreeWidget.EditableItems.insert(0, TreeRootEditableItem)

    # used after the occupied dict has been updated - to update the forbidden names for the task name input
    def UpdateForbiddenNames(self):
        self.ForbiddenNames = [name for key_dict in self.OccupiedNamesByRoute.values()
                                        for name in key_dict.keys()]
        self.ForbiddenNames = list(set(self.ForbiddenNames))

    # updates the occupied dict by a list of id`s of the associated branches
    def UpdateOccupiedNamesByRoute(self, routes_list: list):
        # just for the function, delete all duplications from the routes_list
        routes_list = list(set(routes_list))
        try:
            branches = RGet_TreeBranches(self.PrivateOrPublic, routes_list)
            if branches:
                for branche in branches:
                    branche: dict = branche
                    route = branche["_id"]
                    branche.pop("_id")
                    # removing the edited task from the routes - if the task is new an exception would be rasied
                    try:
                        id_index_values = list(branche.values()).index(self.TaskID)
                        branche.pop(list(branche.keys()).pop(id_index_values))
                    except ValueError:
                        pass

                    self.OccupiedNamesByRoute[route] = branche
            else:
                self.OccupiedNamesByRoute = self.OccupiedNamesByRoute | {route: {} for route in routes_list}
            return True     # "Updated"

        except requests.ConnectionError:
            CreatePopupMsg("Error!", "Failed To Connect To the Server")
            return False    # "Failed"

    # the function is activated on clicking an item in the tree widget
    # updated the "RoutesList", "OccupiedNamesByRoute", "ForbiddenNames" when the clicked item is authorized
    def TreeItemClickedEvent(self, forbidden_routes: list, EditTaskUI, item: TreeItemWidget, column):
        # check if the mouse pressed on the item name of the checkbox
        if column == 0:
            new_task_name = EditTaskUI.NameInput.text()
            # TODO: find out when local and when complete
            if item.Name == new_task_name or new_task_name == "":
                added_route = item.locationRoute
            else:
                added_route = item.completeRoute

            if item.completeRoute not in forbidden_routes:
                # when the item is selected
                if item.checkState(column):

                    if self.UpdateOccupiedNamesByRoute([added_route]):
                        self.UpdateForbiddenNames()
                        if new_task_name in self.ForbiddenNames:
                            item.setCheckState(0, QtCore.Qt.Unchecked)
                            del self.OccupiedNamesByRoute[added_route]

                        else:
                            # if the selected item is an editable item - updates the widget look to
                            #                                            fit the checkbox state
                            if item in self.TreeWidget.EditableItems:
                                item.SelectAndDeselectItem(1)
                            self.RoutesList.append(added_route)
                            self.UpdateForbiddenNames()

                    # if the item is unauthorized - because the task name already exsist as one of the leaves of the branche
                    else:
                        item.setCheckState(0, QtCore.Qt.Unchecked)
                        del self.OccupiedNamesByRoute[added_route]

                # when the item is deselected
                elif added_route in self.RoutesList:
                    route_list_item_index = self.RoutesList.index(added_route)
                    self.RoutesList.pop(route_list_item_index)

                    del self.OccupiedNamesByRoute[added_route]
                    self.UpdateForbiddenNames()

                    # if the unauthorized item is an editable item - updates the gui state
                    if item in self.TreeWidget.EditableItems:
                        item.SelectAndDeselectItem(0.5)

            # if the item is unauthorized - because the clecked branche is alredy in use
            else:
                item.setCheckState(0, QtCore.Qt.Unchecked)