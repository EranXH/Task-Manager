import warnings
import sys
from PyQt5 import QtWidgets
from Code.UI.LoginUI.LoginUI import UserLoginUI
from Code.Debugging import FunctionLogging
from Code.Debugging import CrashLogging
from Code.Debugging.CrashLogging import CrashReporter
from Code.Widgets.BuiltInWidgets.PopupMsg import CreatePopupMsg
from datetime import datetime
from functools import partial

warnings.filterwarnings('ignore')
warnings.simplefilter(action='ignore', category=FutureWarning)

PROGRAM_BEGINNING_DATE_TIME = datetime.now().strftime("#Date-%d.%m.%Y #Time-%H.%M.%S")
FunctionLogging.PROGRAM_BEGINNING_DATE_TIME = PROGRAM_BEGINNING_DATE_TIME
CrashLogging.PROGRAM_BEGINNING_DATE_TIME = PROGRAM_BEGINNING_DATE_TIME

# open (create) the crash log file
with open(f"CrashLog/Crash Report {PROGRAM_BEGINNING_DATE_TIME}.txt", "a") as file_object:
    file_object.write('Function LOG:\n')

if __name__ == '__main__':
    # rewrite the function to the crash-reporter function
    sys.excepthook = CrashReporter

    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QMainWindow()

    _ = UserLoginUI(Window)

    sys.exit(app.exec_())

