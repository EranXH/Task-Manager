from datetime import datetime, date, time
from Code.Debugging.FunctionLogging import LoggingTime


# Create an object that holds a value usefull when a value change event is needed
class ObjectHoldingTheValue:
    def __init__(self, initial_value=0):
        self._value = initial_value
        self._callbacks = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        old_value = self._value
        self._value = new_value
        self._notify_observers(old_value, new_value)

    def _notify_observers(self, old_value, new_value):
        for callback in self._callbacks:
            callback(old_value, new_value)

    def register_callback(self, callback):
        self._callbacks.append(callback)


# change the type of the values in a list to string
def StringTheListValues(List):
    StringList = []
    for value in List:
        if isinstance(value, str):
            StringList.append(repr(value))

    return StringList


# change the type of the values in a list to string
def IntTheListValues(List):
    return list(map(int, List))


# get a list the represent the differnce between two lists
def GetListDifference(List1, List2):
    SetDifference = set(List1) - set(List2)
    return list(SetDifference)


# checks if a float number is a hole number and can be represented as an int
def ParsesToInteger(Value):
    Value = float(str(Value))
    if Value == int(Value):
        return int(Value)
    else:
        return Value


def ISInteger(Value):
    return isinstance(Value, int)


def FromDateTimeToMinutes(DateTime):
    TimeInMinutes = DateTime.seconds / 60
    DateInDays = DateTime.days * 24 * 60
    return DateInDays + TimeInMinutes


def TimeDateToPercentageOfPassedTime(AssignedDate, AssignedTime, DueToDate, DueToTime):
    AssignedDate = date(int(AssignedDate[:4]), int(AssignedDate[5:7]), int(AssignedDate[8:]))
    AssignedTime = time(int(AssignedTime[0]), int(AssignedTime[1]))
    Assigned = datetime.combine(AssignedDate, AssignedTime)

    DueToDate = date(int(DueToDate[:4]), int(DueToDate[5:7]), int(DueToDate[8:]))
    DueToTime = time(int(DueToTime[0]), int(DueToTime[1]))
    DueTo = datetime.combine(DueToDate, DueToTime)

    AssignedUntilDueTo = DueTo - Assigned
    AssignedUntilDueTo = FromDateTimeToMinutes(AssignedUntilDueTo)

    Now = datetime.now()

    AssignedUntilNow = Now - Assigned
    AssignedUntilNow = FromDateTimeToMinutes(AssignedUntilNow)

    if int(AssignedUntilDueTo) != 0:
        PercentageOfPassedTime = round(AssignedUntilNow / AssignedUntilDueTo * 100, 2)
    else:
        PercentageOfPassedTime = 100.0

    if PercentageOfPassedTime > 100.0:
        PercentageOfPassedTime = 100.00

    return PercentageOfPassedTime


def GetAllSerialNumbersFromRoutes(RoutesList):
    return list(set([character for route in RoutesList for character in route if character != '/']))


# returns a list of common elements of two lists
def common_elemnts(set1: set, set2: set) -> set:
    return set1.intersection(set2)
