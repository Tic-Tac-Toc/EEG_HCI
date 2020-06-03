from PySide2.QtWidgets import QMainWindow, QAction
from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import (QHBoxLayout, QVBoxLayout, QHeaderView, QSizePolicy, QTableView, QWidget, QLabel, QComboBox, QRadioButton, QPushButton)
from PySide2.QtCore import QDateTime, Qt
from PySide2.QtGui import QPainter
from PySide2.QtCharts import QtCharts

from Assets.windows.widgets.GraphFormWidget import GraphFormWidget
from Assets.windows.widgets.ToolsWidget import ToolsWidget

class OneGraphWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Visualisation graphique")      

        widget = GraphFormWidget()
        self.setCentralWidget(widget)

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

        # Modify Option QAction
        tools_action = QAction("Options", self)
        tools_action.setShortcut("Ctrl+T")
        tools_action.triggered.connect(self.showTool)

        self.file_menu.addAction(exit_action)
        self.file_menu.addAction(tools_action)

        # Window dimensions
        geometry = qApp.desktop().availableGeometry(self)
        self.showMaximized()  

    def showTool(self):
        self.toolwidget = ToolsWidget()
        self.toolwidget.show()
    