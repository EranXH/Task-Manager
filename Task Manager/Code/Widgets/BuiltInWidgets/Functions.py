from PyQt5 import QtCore, QtGui, QtWidgets


# Sets a given Widget font
def GetFont(FontSize, Font='Nirmala UI Semilight'):
    font = QtGui.QFont()
    font.setFamily(Font)
    font.setPointSize(FontSize)
    # Object.setFont(font)
    return font


# Sets a widget palette
def SetUpPalette(Color, ColorPart, Object):
    palette = QtGui.QPalette()
    brush = QtGui.QBrush(Color)
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, ColorPart, brush)
    Object.setPalette(palette)
    return Object


# Adjust the app window
def AdjustMainWindow(MainWindow, Name, Title, Size, Animated, DocumentMode, TabShape) -> QtWidgets.QMainWindow:
    MainWindow.setObjectName(Name)
    MainWindow.setWindowTitle(Title)
    MainWindow.resize(Size[0], Size[1])
    MainWindow.setAnimated(Animated)
    MainWindow.setDocumentMode(DocumentMode)
    MainWindow.setTabShape(TabShape)  # QtWidgets.QTabWidget.Rounded)

    # CenterMainWindow
    MainWindowRect = MainWindow.frameGeometry()
    CenterPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
    MainWindowRect.moveCenter(CenterPoint)
    MainWindow.move(MainWindowRect.topLeft())

    return MainWindow
