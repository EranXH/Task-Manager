from PyQt5 import QtWidgets
from .Functions import GetFont


# Creates a Table widget
class CreateTable(QtWidgets.QTableWidget):
    def __init__(self, Name,
                 font_size=1, show_grid=True, h_header_visible=True, v_header_visible=True,
                 geometry_rect=None, layout=None, perent_window=None,
                 h_scroll_bar=None, v_scroll_bar=None, h_cell_size=None, v_cell_size=None):
        super().__init__(perent_window)

        self.setObjectName(Name)
        self.setRowCount(self.NumberOfWeeks)
        self.setColumnCount(7)

        self.setShowGrid(show_grid)
        self.horizontalHeader().setVisible(h_header_visible)
        self.verticalHeader().setVisible(v_header_visible)

        self.setFont(GetFont(font_size))

        if geometry_rect is not None:
            self.setGeometry(geometry_rect)
        if layout is not None:
            layout.addWidget(self)
        if h_scroll_bar is not None:
            self.setHorizontalScrollBarPolicy(h_scroll_bar)
        if v_scroll_bar is not None:
            self.setVerticalScrollBarPolicy(v_scroll_bar)
        if h_cell_size is not None:
            self.horizontalHeader().setDefaultSectionSize(h_cell_size)
        if v_cell_size is not None:
            self.verticalHeader().setDefaultSectionSize(v_cell_size)
