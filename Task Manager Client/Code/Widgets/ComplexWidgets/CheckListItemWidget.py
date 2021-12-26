from Code.Widgets.BuiltInWidgets import *
from PyQt5 import QtWidgets, Qt, QtCore
from Code.GlobalFunctions import ObjectHoldingTheValue


# item widget object of the check-list-widget
class CheckListItemWidget(object):
    def __init__(self, CheckListUI, ID: str, State: int, Text: str, HasStateChangeEvent):
        self.CheckListUI = CheckListUI
        self.ID = ID

        self.Frame = CreateFrame(None, 'CheckListItemFrame',
                                 Shape=QtWidgets.QFrame.NoFrame, Shadow=QtWidgets.QFrame.Raised,
                                 LineWidth=2, MidLineWidth=0,
                                 MinimumSize=QtCore.QSize(self.CheckListUI.ItemsPixWidth, 40),
                                 MaximumSize=QtCore.QSize(self.CheckListUI.ItemsPixWidth, 40))

        # Create a CheckBox widget within the Frame
        self.CheckBox = CreateCheckBox(self.Frame, "CheckListItemCheckBox", State, QtCore.QRect(0, 10, 20, 20),
                                       QtCore.QSize(20, 16777215), HasStateChangeEvent)

        self.Label = CreateLabel(self.Frame, 12, Text, 'CheckListItemLabel',
                                 GeometryRect=QtCore.QRect(22, 1, self.CheckListUI.ItemsPixWidth - 30, 38))

        # create an object with a value that on change activate a given function
        # the object represent the number of lines in the item
        self.NumberOfLine = ObjectHoldingTheValue()
        self.NumberOfLine.value = 0
        self.NumberOfLine.register_callback(self.ChangeItemHight)

        self.CheckListUI.ItemsArrangementList.append(self)
        self.CheckListUI.ItemsOccupiedIds.append(self.ID)

        # TODO: change here from ""
        self.Item = QtWidgets.QListWidgetItem("")
        self.Item.setSizeHint(self.Frame.size())

        self.CheckListUI.addItem(self.Item)
        self.CheckListUI.setItemWidget(self.Item, self.Frame)
        self.CheckListUI.scrollToItem(self.Item)

        # add the item higth and the buffer between items to the hight pixcle count of the check-list widget
        self.CheckListUI.ItemsPixLength.value += (40 + 2)

        if Text != '':
            self.ChangeEnterPos()

    # set an item as an editable item
    def SetUpTextEditable(self):
        self.Label.mouseDoubleClickEvent = self.LabelEvent

        self.TextEdit = CreateTextEdit(self.Frame, QtCore.QRect(22, 1, self.CheckListUI.ItemsPixWidth - 30, 38), 12,
                                       'CheckListItemTextEdit',  VScrollBar=QtCore.Qt.ScrollBarAlwaysOff,
                                       HScrollBar=QtCore.Qt.ScrollBarAlwaysOff)
        self.TextEditAllowedEvent = True

        self.TextEdit.keyPressEvent = self.TextEditEvent

        QtWidgets.QApplication.instance().focusChanged.connect(self.TextEditOutOfFocusEvent)

        self.TextEdit.setFocus()

    # the Label event - duble clicking the item lable should activate the option to edit it
    def LabelEvent(self, e):
        self.TextEdit.show()
        self.TextEditAllowedEvent = True
        self.TextEdit.setFocus()

    # the TextEdit event - on keypress update both the text-edit widget and the label widget
    # allow a user to exit the edit mode by pressing the "enter" key
    def TextEditEvent(self, KeyPress):
        new_text = self.TextEdit.toPlainText()
        something_changed = False

        if KeyPress.key() != QtCore.Qt.Key_Return and KeyPress.key() != QtCore.Qt.Key_Backspace:
            new_text = new_text + KeyPress.text()
            new_text, something_changed = self.AddEnter(new_text)

        elif KeyPress.key() == QtCore.Qt.Key_Backspace:
            new_text = new_text[:-1]
            if new_text != '':
                new_text, something_changed = self.RemoveEnter(new_text)

        elif KeyPress.key() == QtCore.Qt.Key_Return:
            self.TextEdit.hide()
            self.TextEditAllowedEvent = False

        if self.TextEditAllowedEvent:
            self.TextEdit.setPlainText('')
            self.TextEdit.insertPlainText(new_text)
            self.Label.setText(new_text)
            self.ChangeNumberOfLinesValue()
            self.CheckListUI.scrollToItem(self.Item)

    # Changes the number of lines value
    def ChangeNumberOfLinesValue(self):
        if hasattr(self, 'TextEdit'):
            text_size = int(self.TextEdit.document().size().height())
            self.NumberOfLine.value = int((text_size - 36) / 28)
        else:
            self.NumberOfLine.value = self.Label.text().count('\n')

    # Hide and disable TextEdit when it has a value and when it is out of focus
    def TextEditOutOfFocusEvent(self):
        if QtWidgets.QApplication.instance().focusWidget() != self.TextEdit:
            try:
                if len(self.TextEdit.toPlainText()) > 0:
                    self.TextEdit.hide()
                    self.TextEditAllowedEvent = False
            except RuntimeError:
                pass

    # Adding an "enter" to a given text depending on a given width
    def AddEnter(self, new_text):
        flipped_text = new_text[::-1]
        # allowed_length = self.TextEdit.width() - 10
        allowed_length = self.CheckListUI.ItemsPixWidth - 40

        if '\n' in new_text:
            after_return_pos = flipped_text.index('\n')
            after_return_pos = len(new_text) - after_return_pos
            after_return_text = new_text[after_return_pos:]
            befor_return_text = new_text[:after_return_pos]
        else:
            after_return_text = new_text
            befor_return_text = ''

        font = Qt.QFont('Nirmala UI Semilight', 12)
        font_metrics = Qt.QFontMetrics(font)
        text_width = font_metrics.width(after_return_text)
        something_changed = False

        if text_width > allowed_length:
            if ' ' in after_return_text:
                after_return_flipped = after_return_text[::-1]
                after_space_pos = after_return_flipped.index(' ')
                after_space_pos = len(after_return_text) - after_space_pos
                new_text = befor_return_text + after_return_text[:after_space_pos] + '\n' + after_return_text[after_space_pos:]
            else:
                return_pos = len(new_text) - 1
                new_text = new_text[:return_pos] + '\n' + new_text[return_pos:]

            something_changed = True

        return new_text, something_changed

    # Removing an "enter" to a given text depending on a given width
    def RemoveEnter(self, new_text):
        something_changed = False
        flipped_text = new_text[::-1]
        allowed_length = self.TextEdit.width() - 10

        PreviousHeight = self.GetHeight()

        if '\n' == new_text[-1]:
            new_text = new_text[:-1]
            something_changed = True

        elif '\n' in flipped_text:
            after_return_pos = flipped_text.index('\n')
            after_return_pos = len(new_text) - after_return_pos
            after_return_text = new_text[after_return_pos:]

            befor_return_text = new_text[:after_return_pos-1]
            between_returns_flipped = befor_return_text[::-1]

            if '\n' in befor_return_text:
                between_returns_pos = between_returns_flipped.index('\n')
                between_returns_pos = len(befor_return_text) - between_returns_pos
                between_returns_text = befor_return_text[between_returns_pos:]
            else:
                between_returns_text = befor_return_text

            between_and_after = between_returns_text + after_return_text

            font = Qt.QFont('Nirmala UI Semilight', 12)
            font_metrics = Qt.QFontMetrics(font)
            text_width = font_metrics.width(between_and_after)

            if text_width <= allowed_length:
                new_text = befor_return_text + after_return_text
                something_changed = True

        self.CheckListUI.ItemsPixLength.value += (self.GetHeight() - PreviousHeight)

        return new_text, something_changed

    # Changes the item pixel height depending on the number of lines it holds
    def ChangeItemHight(self, old_value, new_value):
        if old_value != new_value:
            PreviousHeight = self.GetHeight()

            standard_height = 38 + 28 * self.NumberOfLine.value
            self.Frame.setMinimumSize(QtCore.QSize(self.Frame.width(), standard_height + 2))
            self.Frame.setMaximumSize(QtCore.QSize(self.Frame.width(), standard_height + 2))

            self.Label.setGeometry(QtCore.QRect(22, 1, self.Label.width(), standard_height))
            # self.Label.setWordWrap(True)

            if hasattr(self, 'TextEdit'):
                self.TextEdit.setGeometry(QtCore.QRect(22, 1, self.TextEdit.width(), standard_height))

            standard_height = 14 * self.NumberOfLine.value
            self.CheckBox.setGeometry(QtCore.QRect(0, 10 + standard_height, 20, 20))

            self.Item.setSizeHint(self.Frame.size())

            self.CheckListUI.ItemsPixLength.value += (self.GetHeight() - PreviousHeight)

    # Changes the item pixel width depending on the new given one
    def ChangeItemWidth(self):
        self.Frame.setMinimumSize(QtCore.QSize(self.CheckListUI.ItemsPixWidth, self.Frame.height()))
        self.Frame.setMaximumSize(QtCore.QSize(self.CheckListUI.ItemsPixWidth, self.Frame.height()))

        NewTextWidgetsWidth = self.CheckListUI.ItemsPixWidth - 30

        self.Label.setGeometry(QtCore.QRect(22, 1, NewTextWidgetsWidth, self.Label.height()))

        if hasattr(self, 'TextEdit'):
            self.TextEdit.setGeometry(QtCore.QRect(22, 1, NewTextWidgetsWidth, self.TextEdit.height()))

        self.Item.setSizeHint(self.Frame.size())

        self.ChangeEnterPos()

    # Changes the "enter" position
    def ChangeEnterPos(self):
        item_text = self.Label.text()
        item_new_text = ''
        for letter in item_text:
            if letter != '\n':
                item_new_text = item_new_text + letter
                item_new_text, useless_value = self.AddEnter(item_new_text)

        if hasattr(self, 'TextEdit'):
            self.TextEdit.setPlainText('')
            self.TextEdit.insertPlainText(item_new_text)

        self.Label.setText(item_new_text)

        self.ChangeNumberOfLinesValue()

    # Return the pixel height of the item
    def GetHeight(self):
        return self.Frame.frameRect().height()

    # Return the Text of the item
    def GetText(self):
        # return self.TextEdit.toPlainText()
        return self.Label.text()

    # Insert an updated text to the item
    def updateText(self, new_text: str):
        if self.Label.text() != new_text:
            self.Label.setText(new_text)

            if hasattr(self, 'TextEdit'):
                self.TextEdit.setPlainText('')
                self.TextEdit.insertPlainText(new_text)

    # Return the status of the item
    def GetStatus(self):
        return self.CheckBox.checkState()

    # Insert an updated status to the item
    def updateStatus(self, new_status: int):
        if self.CheckBox.checkState() != new_status:
            self.CheckBox.setChecked(bool(new_status))

    # Return the index of the item
    def GetIndex(self):
        return self.CheckListUI.row(self.Item)

    # Hide the item
    def Hide(self):
        self.Frame.hide()

    # Remove the item
    def Remove(self):
        self.CheckListUI.ItemsPixLength.value -= (self.GetHeight() + 2)
        self.CheckListUI.takeItem(self.GetIndex())
        self.Frame.deleteLater()
        self.Label.deleteLater()
        self.CheckBox.deleteLater()
        if hasattr(self, 'TextEdit'):
            self.TextEdit.deleteLater()

        del self



