from PyQt5 import Qt
from Code.Widgets.BuiltInWidgets import *
import datetime


# create a widget that inclueds clickable widgets which function as shorcuts keys
class ShortCutButtons(CreateLayoutWidget):
    def __init__(self, layout=None):
        # adding the raw of the short cuts buttons
        CreateLayoutWidget.__init__(self, None, 'ShortCutsLayoutWidget', layout=layout)
        layout = CreateHorizontalLayout(self, 0, "ShortCutsLayout")
        self.setLayout(layout)

        self.ButtonsObjectsList = []
        for text in ['Today', 'Tomorrow', 'Next Week', 'Next Weekend']:
            label = CreateLabel(None, 8, text, f'{text} label', Layout=self.layout())
            label.setAlignment(Qt.Qt.AlignCenter)
            label.setStyleSheet(
                        "QFrame {border-radius: 10px; border: 2px solid; padding-right: 5px; padding-left: 5px;}")
            #label.clicked.connect(print(text))
            self.ButtonsObjectsList.append(label)

        self.GetTomorrowDate()
        self.GetNextWeekDate()
        self.GetNextWeekEndDate()

    def GetTomorrowDate(self):
        date = datetime.date.today() + datetime.timedelta(1)
        date_tuple = date.timetuple()[:3]
        print(date_tuple)
        #return date_tuple

    def GetNextWeekDate(self):
        date = datetime.date.today() + datetime.timedelta(7)
        date_tuple = date.timetuple()[:3]
        print(date_tuple)
        # return date_tuple

    def GetNextWeekEndDate(self):
        # going throu the week to find the neext time there is a friday
        for d in range(8):
            date = datetime.date.today() + datetime.timedelta(d)
            print(date.strftime("%w"))
            if date.strftime("%w") == "5":
                print(date.timetuple()[:3])



