import sys
import traceback
from datetime import datetime


# create a crash report when a crash acore - if exsist add to the function logger
def CrashReporter(*exc_info):
    CrashReport = "".join(traceback.format_exception(*exc_info))
    CrashTime = datetime.now().strftime("#Date-%d.%m.%Y #Time-%H.%M.%S")
    CrashReport = f'\nCrash Report:\n{CrashReport}\nStart Time: {PROGRAM_BEGINNING_DATE_TIME}\nCrash Time: {CrashTime}'

    with open(f"CrashLog/Crash Report {PROGRAM_BEGINNING_DATE_TIME}.txt", "a") as file_object:
        file_object.write(CrashReport)

    sys.__excepthook__(*exc_info)
    sys.exit()
