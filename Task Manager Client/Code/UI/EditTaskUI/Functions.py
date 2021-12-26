from PyQt5 import QtCore, QtWidgets, QtGui


# TODO: edit both the GetFont function and the CreateLable class
#  so they can create the title lable for the new task
# Setup the NewTaskTitle object
def SetupTitle(Window):
    EditTaskTitle = QtWidgets.QLabel(Window)
    EditTaskTitle.setGeometry(QtCore.QRect(230, 0, 260, 60))
    font = QtGui.QFont()
    font.setFamily('Nirmala UI Semilight')
    font.setPointSize(22)
    font.setBold(True)
    font.setUnderline(True)
    font.setWeight(75)
    EditTaskTitle.setFont(font)
    EditTaskTitle.setText('New Task')
    EditTaskTitle.setLayoutDirection(QtCore.Qt.LeftToRight)
    EditTaskTitle.setAlignment(QtCore.Qt.AlignCenter)
    EditTaskTitle.setWordWrap(False)
    EditTaskTitle.setObjectName('EditTaskTitle')
    return EditTaskTitle
