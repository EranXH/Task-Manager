from PyQt5 import QtCore, QtWidgets, Qt, QtGui
from Code.Widgets.BuiltInWidgets import *


# set up the UI for Sign-up
class SetupUI:
    def __init__(self, UserLoginUI):
        self.UserLoginUI = UserLoginUI

        self.UserLogin = AdjustMainWindow(self.UserLogin, 'UserSignup', 'Sign Up Window', (500, 270), True, False,
                                           QtWidgets.QTabWidget.Rounded)

        # updating GridLayout size
        self.GridLayoutWidget.setGeometry(QtCore.QRect(10, 50, 480, 180))

        # remap the postions of the widget to enable the email widget to be first
        self.GridLayout.addWidget(self.UserNameLabel, 1, 0, 1, 1)
        self.GridLayout.addWidget(self.UserNameInput, 1, 1, 1, 1)
        self.GridLayout.addWidget(self.PasswordLabel, 2, 0, 1, 1)
        self.GridLayout.addWidget(self.PasswordInput, 2, 1, 1, 1)

        # clearing UserName and PassWord:
        self.PasswordInput.setText("")
        self.UserNameInput.setText("")

        self.EmailLabel = CreateLabel(self.GridLayoutWidget, 12, 'Email', 'EmailLabel')
        self.GridLayout.addWidget(self.EmailLabel, 0, 0, 1, 1)

        self.EmailInput = CreateLineEdit(self.GridLayoutWidget, 'EmailInput', '', 12) #, MaxLength=14)
        self.GridLayout.addWidget(self.EmailInput, 0, 1, 1, 1)

        self.SecondPasswordLabel = CreateLabel(self.GridLayoutWidget, 12, 'Renter Your Password', 'SecondPasswordLabel')
        self.GridLayout.addWidget(self.SecondPasswordLabel, 3, 0, 1, 1)

        self.SecondPasswordInput = CreateLineEdit(self.GridLayoutWidget, 'SecondPasswordInput', '', 12, MaxLength=14)
        self.SecondPasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.GridLayout.addWidget(self.SecondPasswordInput, 3, 1, 1, 1)

        self.LoginSignup.hide()
        self.CancelSignup = CreateDialogButtonBox(self.UserLoginWidgets, QtCore.Qt.RightToLeft, "CancelSignup",
                                                  'Cancel', 'Sign up', geometry_rect=QtCore.QRect(160, 230, 180, 30))
        self.CancelSignup.show()

        self.ErrorMsg.setGeometry(QtCore.QRect(0, 210, 500, 51))

    # gets all the varubels of UserLoginUI as part of the object varibles (self.)
    def __getattr__(self, attr):
        return getattr(self.UserLoginUI, attr)