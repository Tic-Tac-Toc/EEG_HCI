from PySide2.QtWidgets import (QHBoxLayout, QVBoxLayout, QWidget, QLabel, QPushButton)
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap

from Assets.windows.OneGraph import OneGraphWindow
from Assets.windows.Synchro import SynchroWindow
from Assets.windows.WindowsTools import DefineLayoutChildAlignment

#Main window
class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("EEG IHM - Télécom SudParis")   

        self.CreateLayout()
        
        self.resize(self.picture.width()+300, self.picture.height()+100)
        self.setFixedSize(self.picture.width()+300, self.picture.height()+200)

    def CreateLayout(self):
        layout = QVBoxLayout()

        self.picture = QPixmap("Assets/pics/applogo.png")
        label = QLabel(self)
        label.setPixmap(self.picture)

        FirstRowLayout = QHBoxLayout()
        FirstRowLayout.addWidget(label)
        DefineLayoutChildAlignment(FirstRowLayout, Qt.AlignHCenter)
        

        signalButton = QPushButton("Visualisation de signal") 
        signalButton.clicked.connect(self.signalButtonClick)
        signalButton.setFixedHeight(50)
        synchronisationButton = QPushButton("Visualisation de synchronisation")
        synchronisationButton.clicked.connect(self.PSCButtonClick)
        synchronisationButton.setFixedHeight(50)

        SecondRowLayout = QHBoxLayout()
        SecondRowLayout.setMargin(10)
        SecondRowLayout.setSpacing(10)
        SecondRowLayout.addWidget(signalButton)
        SecondRowLayout.addWidget(synchronisationButton)

        layout.addItem(FirstRowLayout)
        layout.addItem(SecondRowLayout)

        self.setLayout(layout) 
    
    #Open graph window
    def signalButtonClick(self):
        self.signalwindow = OneGraphWindow()
        self.signalwindow.show()

    #Open synchro visualisation window
    def PSCButtonClick(self):
        self.pscwindow = SynchroWindow()
        self.pscwindow.show()        