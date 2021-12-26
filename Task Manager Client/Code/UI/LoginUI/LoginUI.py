import hashlib
import threading
from functools import partial
from PyQt5 import QtWidgets

from Code.UI.MainUI.MainUI import MainUI
from Code.APIRequests.APIGetRequests import *
import Code.UI.LoginUI.Functions as Func
from Code.UI.LoginUI.SetupUI import SetupUI
from Code.UI.LoginUI.UserDetailsHolder import UserDetailsHolder
from Code.UI.SignupUI.SignupUI import UserSignupUI

from icecream import ic

# the login UI
class UserLoginUI(SetupUI):
    # crate the UI + define key values
    def __init__(self, UserLogin):
        self.BootUI(UserLogin)

    def BootUI(self, UserLogin):
        # calling the event loop
        super().__init__(UserLogin)
        self.Events()
        #self.LoginButtonClickEvent()

    # The event loop
    def Events(self):
        # on clicking the Log-in button
        self.LoginSignup.accepted.connect(self.LoginButtonClickEvent)

        # on clicking the Sign-up button
        self.LoginSignup.rejected.connect(self.SignupButtonEvent)

        # on clicking the return button in the password input
        self.PasswordInput.returnPressed.connect(self.LoginButtonClickEvent)

    # the event loop for the sign-up window
    def SignupButtonEvent(self):
        self.UserSignupUI = UserSignupUI(self)
        self.UserSignupUI.CancelSignup.accepted.connect(self.UserSignupUI.SignupEvent)
        self.UserSignupUI.CancelSignup.rejected.connect(partial(self.BootUI, self.UserLogin))

    # the login event
    def LoginButtonClickEvent(self):
        # gets the user_name from the input widget
        # user_name = 'Gadi'
        user_name = self.UserNameInput.text()
        # hash the user_name - not yet implemented
        user_name_bytes = str.encode(user_name)
        user_name_hash = hashlib.sha224(user_name_bytes).hexdigest()

        # gets the password from the input widget
        # password = 'Gadi123'
        password = self.PasswordInput.text()
        # hash the password - not yet implemented
        password_bytes = str.encode(password)
        password_hash = hashlib.sha224(password_bytes).hexdigest()

        # check for missing information in the inputs
        # self.UserID = GetPasswordAuthentication(user_name_hash, password_hash)
        #user_info = RGet_Login(user_name_hash, password_hash)
        if user_name and password:
            # send a requests for user info from the server
            user_info = RGet_Login(user_name, password)
        elif not user_name:
            user_info = {'Error': 'Please enter your User Name'}
        else:
            user_info = {'Error': 'Please enter your Password'}
        ic(user_info)

        # active if the response approves
        if len(user_info.keys()) != 1:
            UserDetailsHolder.UpdateDetails(user_name, password)

            TasksDFs, TreeDFs, UserID = Func.ArrangeDFValues(user_info)
            PAPUserOptions = Func.ArrangeOptionsValues(user_info, user_name)

            MainUI(self.UserLogin, TasksDFs, TreeDFs, PAPUserOptions, user_name, UserID)

        else:
            self.FailedLogin(user_info)

    # pop an error message if the login failed from any reason
    def FailedLogin(self, user_info):
        self.UserLogin.resize(300, 225)
        self.LoginSignup.move(60, 185)

        self.ErrorMsg.setText(user_info['Error'])

# bytes([3])
# str.encode(str(g))
# print(hashlib.sha224(b'Gadi123').hexdigest())
# print(hashlib.sha224(b'Eran123').hexdigest())
# print(hashlib.sha224(b'Dana123').hexdigest())
# print(hashlib.sha224(b'Nir123').hexdigest())
# print(hashlib.sha224(b'Tami123').hexdigest())
