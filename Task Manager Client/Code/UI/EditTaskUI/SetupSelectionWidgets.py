from ...Widgets.ComplexWidgets import SelectionWidget
from ...Widgets.ComplexWidgets import SelectionAddButtonWidget
from .AssociateTab import AssociateTab
from .TypeTab import TypeTab

# creating a Tab with a scroll area that conatins selectable widgets
class NTSelectionWidgets(object):
    def __init__(self, SelectionTab, SelectionTabsFrameRect, SelectionTabsScrollRect, SelectionTabsSCWRect,
                 SelectionTabsLabelRect, PAPUserOptions, TasksDFs, TreeDFs, IDToRouteDicts, TaskID,
                 InchargeSelectedOptions=None, AssignSelectedOptions=None):
        self.SelectionTab = SelectionTab

        self.SelectionTabsFrameRect = SelectionTabsFrameRect
        self.SelectionTabsScrollRect = SelectionTabsScrollRect
        self.SelectionTabsSCWRect = SelectionTabsSCWRect     # SCWRect stands for Scroll Contents Widget Rect
        self.SelectionTabsLabelRect = SelectionTabsLabelRect

        (PublicUserOptions, PrivateUserOptions) = PAPUserOptions
        (PublicTasksDF, PrivateTasksDF) = TasksDFs
        (PublicTreeDF, PrivateTreeDF) = TreeDFs
        (PrivateIDToRouteDict, PublicIDToRouteDict) = IDToRouteDicts

        self.InchargeSelectedOptions = InchargeSelectedOptions
        self.AssignSelectedOptions = AssignSelectedOptions

        self.PrivateAssociateTab = AssociateTab(PrivateTreeDF, PrivateTasksDF, 'Private', SelectionTabsFrameRect,
                                                SelectionTabsLabelRect, SelectionTab, SelectionTabsScrollRect,
                                                PrivateIDToRouteDict, TaskID)
        self.PublicAssociateTab = AssociateTab(PublicTreeDF, PublicTasksDF, 'Public', SelectionTabsFrameRect,
                                               SelectionTabsLabelRect, SelectionTab, SelectionTabsScrollRect,
                                               PublicIDToRouteDict, TaskID)
        self.SelectionTab.removeTab(self.SelectionTab.indexOf(self.PublicAssociateTab.Tab))

        self.PrivateTypeTab = TypeTab(PrivateUserOptions, 'Private',
                                      SelectionTabsFrameRect, SelectionTabsScrollRect, SelectionTabsSCWRect,
                                      SelectionTabsLabelRect, SelectionTab)
        self.PublicTypeTab = TypeTab(PublicUserOptions, 'Public',
                                      SelectionTabsFrameRect, SelectionTabsScrollRect, SelectionTabsSCWRect,
                                      SelectionTabsLabelRect, SelectionTab)
        self.SelectionTab.removeTab(self.SelectionTab.indexOf(self.PublicTypeTab.Widget.Tab))

        self.ForbiddenNames = self.PrivateAssociateTab.ForbiddenNames
        self.TreeEditableItems = self.PrivateAssociateTab.TreeWidget.EditableItems

        self.CreateIAWidgets(PublicUserOptions)

    # TODO: need to connect the names of the buttons to the real IDs
    #  so they will also be able to see the there incharge or there assigned task
    # IA stands for Incharge and Assign
    def CreateIAWidgets(self, PublicUserOptions):
        # Creating the Incharge tab
        self.InchargeWidget = SelectionWidget('Incharge', self.SelectionTabsFrameRect,  self.SelectionTabsScrollRect,
                                              self.SelectionTabsSCWRect, self.SelectionTabsLabelRect,
                                              'Select whom is incharge of your new task', self.SelectionTab)
        self.InchargeOptionsList = PublicUserOptions["incharge"]
        self.InchargeWidget.AddOptionsButtons(self.InchargeOptionsList)
        self.SelectionTab.removeTab(self.SelectionTab.indexOf(self.InchargeWidget.Tab))

        # Creating the Assign tab
        self.AssignWidget = SelectionWidget('Assign', self.SelectionTabsFrameRect,  self.SelectionTabsScrollRect,
                                            self.SelectionTabsSCWRect, self.SelectionTabsLabelRect,
                                            'Select to whom you want to assign your new task', self.SelectionTab)
        self.AssignOptionsList = PublicUserOptions["assign"]
        self.AssignWidget.AddOptionsButtons(self.AssignOptionsList)
        self.SelectionTab.removeTab(self.SelectionTab.indexOf(self.AssignWidget.Tab))

    # changing the selection tab to fit whether the task is private or public
    def SelectionWidgetsEvent(self, PrivateTaskToggle):
        # saves the current tab index in oreder to stay on it at the end of the event
        CurrentTabIndex = self.SelectionTab.currentIndex()
        # saves the current progress bar value
        progress_bar_value = self.TreeEditableItems[0].ProgressBar.value()

        if PrivateTaskToggle.isChecked():   # when Private
            # removing Public related Tabs
            self.SelectionTab.removeTab(self.SelectionTab.indexOf(self.PublicAssociateTab.Tab))
            self.SelectionTab.removeTab(self.SelectionTab.indexOf(self.PublicTypeTab.Widget.Tab))

            self.SelectionTab.removeTab(self.SelectionTab.indexOf(self.InchargeWidget.Tab))
            self.SelectionTab.removeTab(self.SelectionTab.indexOf(self.AssignWidget.Tab))

            # adding the relevent tabs - Private
            self.SelectionTab.addTab(self.PrivateAssociateTab.Tab, self.PrivateAssociateTab.TabName)
            self.SelectionTab.addTab(self.PrivateTypeTab.Widget.Tab, self.PrivateTypeTab.Widget.TabName)

            self.ForbiddenNames = self.PrivateAssociateTab.ForbiddenNames

            self.TreeEditableItems = self.PrivateAssociateTab.TreeWidget.EditableItems

        else:   # when Public
            # removing Private related Tabs
            self.SelectionTab.removeTab(self.SelectionTab.indexOf(self.PrivateAssociateTab.Tab))
            self.SelectionTab.removeTab(self.SelectionTab.indexOf(self.PrivateTypeTab.Widget.Tab))

            # adding the relevent tabs - Public
            self.SelectionTab.addTab(self.PublicAssociateTab.Tab, self.PublicAssociateTab.TabName)
            self.SelectionTab.addTab(self.PublicTypeTab.Widget.Tab, self.PublicTypeTab.Widget.TabName)
            self.SelectionTab.addTab(self.InchargeWidget.Tab, self.InchargeWidget.TabName)
            self.SelectionTab.addTab(self.AssignWidget.Tab, self.AssignWidget.TabName)

            self.ForbiddenNames = self.PublicAssociateTab.ForbiddenNames

            self.TreeEditableItems = self.PublicAssociateTab.TreeWidget.EditableItems

        # sets the new progress bar value to be the same as the old one
        for item in self.TreeEditableItems:
            item.ProgressBar.AnimationFinishedEvent(progress_bar_value)
        # sets the current tab index to the saved one in order to stay at the same tab as it was befor the event
        self.SelectionTab.setCurrentIndex(CurrentTabIndex)

        # Get_PoP_DFValues(self.UIClass, self.UIClass.PrivateOrPublic)
