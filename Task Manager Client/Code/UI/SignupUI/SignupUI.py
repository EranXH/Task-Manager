import re

from Code.APIRequests.APIPostRequests import RPost_Signup
from Code.UI.SignupUI.SetupUI import SetupUI


# the UI for Sign-up
class UserSignupUI(SetupUI):
    def __init__(self, UserLogin):
        self.BootUI(UserLogin)

    def BootUI(self, UserLogin):
        # activating the setup
        super().__init__(UserLogin)

        # calling the event loop
        self.SignupEvent()

    def SignupEvent(self):
        if self.raiseErrorWindow():
            self.UserLoginUI.BootUI(self.UserLogin)
            # if all of the information went into the server whitout any problems need to reBootUI of the LoginUI
            pass

    def raiseErrorWindow(self):
        email = self.EmailInput.text()
        user_name = self.UserNameInput.text()
        password = self.PasswordInput.text()
        second_password = self.SecondPasswordInput.text()

        # rais an error when some values are empty
        if not email or not user_name or not password or not second_password:
            response = {"response": "please fill up all the required information"}
            self.FailedSignup(response)
            return False

        if password != second_password:
            response = {"response": "passwords do not match"}
            self.FailedSignup(response)
            return False

        # check if an email adress is a valid one
        # pass the regular expression
        # and the string into the fullmatch() method
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, email):
            response = {"response": "this email address is not valid"}
            self.FailedSignup(response)
            return False

        # send the information to the serer
        response = RPost_Signup(email, user_name, password)
        if response["response"]:
            self.FailedSignup(response)
            return False

        else:
            return True

    def FailedSignup(self, response):
        self.UserLogin.resize(500, 300)
        self.CancelSignup.move(160, 260)

        self.ErrorMsg.setText(response['response'])