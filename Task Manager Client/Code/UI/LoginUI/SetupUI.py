from PyQt5 import QtCore, QtWidgets

from Code.Widgets.BuiltInWidgets import *


# the setup of the log-in ui
class SetupUI:
    def __init__(self, UserLogin):
        self.UserLogin = AdjustMainWindow(UserLogin, 'UserLogin', 'Log In Window', (300, 180), True, False,
                                          QtWidgets.QTabWidget.Rounded)

        self.UserLoginWidgets = CreateLayoutWidget(self.UserLogin, 'UserLoginWidgets')

        self.AppNameLabel = CreateLabel(self.UserLoginWidgets, 12, 'Task Manager App Name', 'AppNameLabel',
                                        GeometryRect=QtCore.QRect(0, 0, 301, 51))
        self.AppNameLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.GridLayoutWidget = CreateLayoutWidget(self.UserLoginWidgets, 'GridLayoutWidget',
                                                   GeometryRect=QtCore.QRect(10, 50, 280, 90))

        self.GridLayout = QtWidgets.QGridLayout(self.GridLayoutWidget)
        self.GridLayout.setContentsMargins(0, 0, 0, 0)
        #self.GridLayout.setHorizontalSpacing(10)
        self.GridLayout.setVerticalSpacing(0)
        self.GridLayout.setObjectName("GridLayout")

        self.PasswordLabel = CreateLabel(self.GridLayoutWidget, 12, 'Password', 'PasswordLabel')
        self.GridLayout.addWidget(self.PasswordLabel, 1, 0, 1, 1)

        self.UserNameLabel = CreateLabel(self.GridLayoutWidget, 12, 'User Name', 'UserNameLabel')
        self.GridLayout.addWidget(self.UserNameLabel, 0, 0, 1, 1)

        self.UserNameInput = CreateLineEdit(self.GridLayoutWidget, 'UserNameInput', '', 12)
        self.GridLayout.addWidget(self.UserNameInput, 0, 1, 1, 1)

        self.PasswordInput = CreateLineEdit(self.GridLayoutWidget, 'PasswordInput', '', 12, MaxLength=14)
        self.PasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.GridLayout.addWidget(self.PasswordInput, 1, 1, 1, 1)

        # creating a ready to go popup error message
        self.ErrorMsg = CreateLabel(self.UserLoginWidgets, 12, '', 'ErrorMsgLabel',
                                    GeometryRect=QtCore.QRect(0, 130, 301, 51))
        self.ErrorMsg.setAlignment(QtCore.Qt.AlignCenter)

        self.LoginSignup = CreateDialogButtonBox(self.UserLoginWidgets, QtCore.Qt.RightToLeft, "LoginSignup",
                                                 'Sign up', 'Log in', geometry_rect=QtCore.QRect(60, 140, 180, 30))
        self.UserLogin.setCentralWidget(self.UserLoginWidgets)

        self.UserLogin.show()
