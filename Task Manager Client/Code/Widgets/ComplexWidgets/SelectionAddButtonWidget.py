from PyQt5 import QtCore, QtWidgets
from Code.Widgets.BuiltInWidgets import *


# the object add button widget for the selection tabs
class SelectionAddButtonWidget(object):
    def __init__(self, Window, Layout, ButtonName, LineEditName, OptionsList, FunctionOnNewValEvent):
        self.Window = Window
        self.Layout = Layout

        self.Button = CreateButton(self.Window, '➕', 9, ButtonName, SetFlat=False, Layout=self.Layout)
        self.LineEdit = CreateLineEdit(self.Window, LineEditName, '', 12, MaxLength=15, Hide=True, Layout=self.Layout)

        self.OptionsList = OptionsList
        self.FunctionOnNewValEvent = FunctionOnNewValEvent

        self.Button.clicked.connect(self.ButtonEvent)
        self.LineEdit.keyReleaseEvent = self.LineEditEvent

    # hide AddButton object and show AddLineEdit object executable for Type Share and Assign
    def ButtonEvent(self):
        self.Button.hide()
        self.LineEdit.show()

    # on text editing finish -
    def ButtonFinishEvent(self):
        self.LineEdit.hide()
        self.Button.show()

    # Add item according to the LineEdit
    def LineEditEvent(self, KeyPress):
        if QtWidgets.QApplication.focusWidget().objectName() == self.LineEdit.objectName():
            # for an empty text finish
            if len(self.LineEdit.text()) == 0 and KeyPress.key() == QtCore.Qt.Key_Backspace:
                self.ButtonFinishEvent()

            if len(self.LineEdit.text()) > 0 and KeyPress.key() == QtCore.Qt.Key_Return:
                if self.LineEdit.text() not in self.OptionsList:
                    self.OptionsList.insert(0, self.LineEdit.text())
                    self.LineEdit.setText('')
                    self.ButtonFinishEvent()
                    self.FunctionOnNewValEvent(self.OptionsList)
