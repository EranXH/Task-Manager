from ...Widgets.ComplexWidgets import SelectionWidget
from ...Widgets.ComplexWidgets import SelectionAddButtonWidget

# Type tab object allows creating tabs for both private and public options
class TypeTab(object):
    def __init__(self, UserOptions, PrivateOrPublic,
                 SelectionTabsFrameRect, SelectionTabsScrollRect, SelectionTabsSCWRect,     # SCWRect stands for Scroll Contents Widget Rect
                 SelectionTabsLabelRect, SelectionTab):
        self.OptionsList = UserOptions["types"]
        self.PrivateOrPublic = PrivateOrPublic

        self.Widget = SelectionWidget(f"{self.PrivateOrPublic}Types", SelectionTabsFrameRect,
                                      SelectionTabsScrollRect,
                                      SelectionTabsSCWRect,
                                      SelectionTabsLabelRect, 'Select the type of your new task',
                                      SelectionTab, TabName="Type", UndeclaredWidgetsNum=1)

        self.AddButtonWidget = SelectionAddButtonWidget(self.Widget.ScrollContentsWidget,
                                                        self.Widget.ScrollContentsLayout,
                                                        f"{self.PrivateOrPublic}TypeAddButton",
                                                        f"{self.PrivateOrPublic}TypeAddLineEdit", self.OptionsList,
                                                        self.Widget.AddOptionsButtons)

        self.Widget.AddOptionsButtons(self.OptionsList)
