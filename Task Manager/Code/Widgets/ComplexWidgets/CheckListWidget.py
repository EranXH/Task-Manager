from PyQt5 import QtCore
from Code.GlobalFunctions import ObjectHoldingTheValue
from Code.Widgets.BuiltInWidgets import CreateList
from .CheckListItemWidget import CheckListItemWidget


# the check list widget object
class CheckListWidget(CreateList):
    def __init__(self):
        pass

    def SetUp(self, Window, GeometryRect):
        CreateList.__init__(self, Window, 12, 'CheckListWidget', GeometryRect=GeometryRect,
                            LayoutDirection=QtCore.Qt.RightToLeft, HScrollBar=QtCore.Qt.ScrollBarAlwaysOff)
        self.show()

        # variables
        self.ItemsOccupiedIds = []

        self.ItemsArrangementList: list[CheckListItemWidget] = []
        self.ItemsPixWidth = GeometryRect.width() - 5

        self.ItemsPixLength = ObjectHoldingTheValue()
        self.ItemsPixLength.value = 0
        self.ItemsPixLength.register_callback(self.ItemsPixLengthEvent)

        self.PreviousSelectedRow = 0

        # events
        self.model().rowsMoved.connect(self.UpdateItemsArrangementList)
        self.model().rowsAboutToBeMoved.connect(self.ChangePreviousRowValue)

    # Change ItemPreviousRow value
    def ChangePreviousRowValue(self, e):
        self.PreviousSelectedRow = self.currentRow()

    # Update ItemsArrangementList
    def UpdateItemsArrangementList(self, e):
        previous_row = self.PreviousSelectedRow
        current_row = self.currentRow()
        if previous_row != current_row:
            item = self.ItemsArrangementList[previous_row]
            self.ItemsArrangementList.pop(previous_row)
            self.ItemsArrangementList.insert(current_row, item)

    # Change items width depending on items pix length
    def ItemsPixLengthEvent(self, old_value, new_value):
        Change = False
        ListWidgetPixLength = self.height() - 2
        if old_value < ListWidgetPixLength <= new_value:
            Change = True
            self.ItemsPixWidth -= 20
        if old_value >= ListWidgetPixLength > new_value:
            Change = True
            self.ItemsPixWidth += 20
        if Change:
            for item in self.ItemsArrangementList:
                item.ChangeItemWidth()
                try:
                    if item.TextEditAllowedEvent:
                        self.scrollToItem(item.Item)
                except AttributeError:
                    pass

    # check if there is an unused id or a new one should be used
    def GetAvailableID(self):
        # the first set - represent all the exsisting ids including the new one
        # the second set - represent all the used ids
        available_id = set(range(1, len(self.ItemsOccupiedIds) + 2)) - set(map(int, self.ItemsOccupiedIds))
        # take the first id
        return str(available_id.pop())

    # Add Check List Item
    def AddItem(self, ID, State, Text, HasStateChangeEvent):
        Add = True
        item_scroll_pos = 0

        for item in self.ItemsArrangementList:
            if len(item.GetText()) == 0:
                Add = False
                item.LabelEvent(None)
                self.scrollToItem(item.Item)
                break

            item_scroll_pos = item_scroll_pos + item.GetHeight()

        if Add:
            self.NewItem = CheckListItemWidget(self, ID, State, Text, HasStateChangeEvent)
            if Text == '':
                self.NewItem.SetUpTextEditable()

    # Remove Check List Item
    def RemoveItem(self):
        if len(self.ItemsArrangementList) == 1:
            self.ItemsArrangementList[0].LabelEvent(None)

        else:
            if self.currentRow() != -1:
                item_idx = self.currentRow()

            else:
                item_idx = len(self.ItemsArrangementList) - 1

            item = self.ItemsArrangementList[item_idx]
            self.ItemsOccupiedIds.remove(item.ID)
            item.Remove()
            del item
            self.ItemsArrangementList.pop(item_idx)

    # remove all the items from the check-list and cleaning up all the relvent variables
    def RemoveAllItems(self):
        for item in self.ItemsArrangementList:
            item.Remove()
        self.ItemsArrangementList = []

    # get a dict which represent all the check-list items
    def GetItemsDict(self) -> dict[str: list[str, int]]:
        return {item.ID: [item.GetText(), item.GetStatus()] for item in self.ItemsArrangementList
                                                                if item.GetText()}

    # get a number which represent the amount of checked items in the ckeck-list-widget
    def GetAmountOfCheckedItems(self) -> int:
        return len([item for item in self.ItemsArrangementList if item.GetStatus() == 2])
