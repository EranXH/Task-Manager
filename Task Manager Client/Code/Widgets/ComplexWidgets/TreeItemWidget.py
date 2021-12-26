from Code.Widgets.AnimatedWidget.ProgressBar import ProgressBar
from PyQt5 import QtCore, QtWidgets, QtGui
from icecream import ic


# the tree-widget item widget object
class TreeItemWidget(QtWidgets.QTreeWidgetItem):
    # setup
    def __init__(self, TreeWidgetUI, IsFirst, ParentItem, ID, Name, Progress, locationRoute):
        super().__init__()
        self.ID = ID
        self.Name = Name
        self.setText(0, self.Name)

        if TreeWidgetUI.IsUserCheckable:
            self.setCheckState(0, QtCore.Qt.Unchecked)

        if IsFirst:
            ParentItem.addTopLevelItem(self)
        else:
            ParentItem.addChild(self)

        self.Progress = ProgressBar.CalculateProgress(Progress)
        self.ProgressBar = ProgressBar(None, self.Progress, 'TreeItemProgressBar',
                                       MaxSizeX=30)

        TreeWidgetUI.setItemWidget(self, 1, self.ProgressBar)

        self.locationRoute = locationRoute
        self.completeRoute = f"{locationRoute}/{ID}"
        self.Index = len(TreeWidgetUI.Items)

    # changes between the item select and deselect modes
    def SelectAndDeselectItem(self, opacity):
        self.setForeground(0, QtGui.QBrush(QtGui.QColor(0, 0, 0, 256 * opacity)))

        # creating the unselected effect
        style_sheet = "QProgressBar{border-radius: 5px; border-color: black;} " \
                      "QProgressBar::chunk {border-radius :5px} QProgressBar::chunk {background - color: rgba(0, 128, 0, 0.5);}"
        self.ProgressBar.setStyleSheet("QProgressBar{border-radius: 5px; border-color: black;} "
                                       "QProgressBar::chunk {border-radius :5px} QProgressBar::chunk {"
                                       "background-color: rgba(0, 128, 0, "f"{255 * opacity}"");}")

        palette = self.ProgressBar.palette()
        palette.setColor(QtGui.QPalette.Text, QtGui.QColor(0, 0, 0, 255 * opacity))
        self.ProgressBar.setPalette(palette)
