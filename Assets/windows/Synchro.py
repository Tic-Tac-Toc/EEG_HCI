from PySide2.QtWidgets import QMainWindow, QAction, QFileDialog
from PySide2.QtGui import QIcon

import scipy.io as sp

from Assets.windows.widgets.SynchroWidget import SynchroWidget

#PSC Window
class SynchroWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Synchronisation entre les électrodes")
        self.setIcon()

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        
        # Open QAction
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.OpenFile)

        self.file_menu.addAction(exit_action)
        self.file_menu.addAction(open_action)

        self.setGeometry(0,0,800,950) #Keep the head in circle
        
        self.mat = None

        self.widget = SynchroWidget() #Set SynchroWidget as central widget
        self.setCentralWidget(self.widget)
        self.widget.sliderwidgetupto.slider.valueChanged.connect( self.valueUpChanged ) # Link slider to select a range of value
        self.widget.sliderwidgetdownto.slider.valueChanged.connect( self.valueDownChanged ) # Link slider to select a range of value
        self.widget.sliderwidgetupto.slider.setValue(1)
        self.widget.sliderwidgetdownto.slider.setValue(100)
        self.show()    

    def setIcon(self):
        appIcon = QIcon("Assets/pics/logo.jpg")
        self.setWindowIcon(appIcon)

    #Allow user to load a file from disk to display PSC connection
    def OpenFile(self):
        path_to_file, _ = QFileDialog.getOpenFileName(self, self.tr("Load matrix"), self.tr("Datas/"), self.tr("Matrix (*.mat)"))
        self.mat = sp.loadmat(path_to_file)
        self.widget.SetLabelFile(path_to_file.split('/')[-1])
        if ('PSC' in self.mat.keys()):
            self.widget.widget.LoadConnection(self.mat['PSC'], self.sliderDownValue, self.sliderUpValue)
        else:
            self.widget.widget.LoadConnection(self.mat['data'], self.sliderDownValue, self.sliderUpValue)

    #Functions to update the range value of connection displayed et update the window
    def valueUpChanged( self, value ):
        self.widget.sliderwidgetupto.labelvalue.setText( ">" + str( value / 100.0 ) )
        self.sliderUpValue = value / 100.0
        if (self.mat is not None):
            if ('PSC' in self.mat.keys()):
                self.widget.widget.LoadConnection(self.mat['PSC'], self.sliderDownValue, self.sliderUpValue)
            else:
                self.widget.widget.LoadConnection(self.mat['data'], self.sliderDownValue, self.sliderUpValue)
    def valueDownChanged( self, value ):
        self.widget.sliderwidgetdownto.labelvalue.setText( "<" + str( value / 100.0 ) )
        self.sliderDownValue = value / 100.0
        if (self.mat is not None):
            if ('PSC' in self.mat.keys()):
                self.widget.widget.LoadConnection(self.mat['PSC'], self.sliderDownValue, self.sliderUpValue)
            else:
                self.widget.widget.LoadConnection(self.mat['data'], self.sliderDownValue, self.sliderUpValue)